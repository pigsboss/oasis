"""CLI for channel probing, the local file-system view, and the web UI (M1/M2).

Commands: probe [ids...] [--channel id] [--timeout S] | storages [--json] | web [--port N] [--no-open]
          slice list | slice run <ids...> [--chunks M-N] [--apply]
All runtime output is English (CODING_STANDARDS §2.2).
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from oasis_catalog.config import resolve_config_path

from . import slice_export
from .inventory_cli import load_all
from .probe import probe_inventory
from .storage_view import (STATE_ABSENT, STATE_ATTACHED_UNMOUNTED, build_view,
                           render_text)
from .sync import load_storages


def cmd_probe(args) -> int:
    cfg_path, inv_path, log_path, cfg, inv = load_all(args)
    if not inv.datasets:
        print("inventory is empty (run migrate-config first)", file=sys.stderr)
        return 1
    known = {str(d.get("id")) for d in inv.datasets}
    unknown = [i for i in args.ids if i not in known]
    if unknown:
        print(f"unknown dataset id(s): {', '.join(unknown)}", file=sys.stderr)
        return 1
    rc = 0
    for ds_id, results in probe_inventory(inv.datasets, args.ids, channel_id=args.channel,
                                          timeout=args.timeout):
        print(f"== {ds_id}")
        if not results:
            print("   (no matching channel)")
            continue
        for res in results:
            head = f"   - {res.channel_id:12s} [{res.protocol:5s}] {res.state.upper():7s}"
            if res.latency_ms is not None:
                head += f" {res.latency_ms}ms"
            print(head)
            if res.version:
                print(f"       version: {res.version}")
            if res.detail:
                print(f"       {res.detail}")
            if res.state == "fail":
                rc = 1
    return rc


def cmd_storages(args) -> int:
    cfg_path, inv_path, log_path, cfg, inv = load_all(args)
    view = build_view(load_storages(cfg_path))
    if args.json:
        print(json.dumps(view, indent=2, ensure_ascii=False))
    else:
        print(render_text(view))
    for row in view["storages"]:
        if row["state"] in (STATE_ABSENT, STATE_ATTACHED_UNMOUNTED):
            return 1
    return 0


def _load_specs(slices_dir: Path, ids: list[str]) -> tuple[list[dict], list[str]]:
    specs: list[dict] = []
    errors: list[str] = []
    for path in sorted(slices_dir.glob("*.yaml")):
        if ids and path.stem not in ids:
            continue
        try:
            specs.append(slice_export.load_spec(path))
        except Exception as exc:  # noqa: BLE001 - report per-file
            errors.append(f"{path.name}: {exc}")
    found = {str(s.get("id")) for s in specs}
    for wanted in ids:
        if wanted not in found:
            errors.append(f"slice '{wanted}' not found in {slices_dir}")
    return specs, errors


def cmd_slice(args) -> int:
    cfg_path, inv_path, log_path, cfg, inv = load_all(args)
    slices_dir = cfg_path.parent / "slices"
    if args.slice_command == "list":
        specs, errors = _load_specs(slices_dir, [])
        if not specs and not errors:
            print(f"no slice specs in {slices_dir}")
            return 0
        for spec in specs:
            verrs, vwarns = slice_export.validate_spec(spec, {d.get("id") for d in inv.datasets},
                                                       set(load_storages(cfg_path)))
            status = "OK" if not verrs else f"{len(verrs)} error(s)"
            print(f"{spec.get('id'):20s} source={spec.get('source')}  {status}")
            for message in verrs + vwarns:
                print(f"    - {message}")
        for message in errors:
            print(f"ERROR {message}", file=sys.stderr)
        return 2 if errors else 0

    if args.slice_command != "run":
        return 2
    specs, errors = _load_specs(slices_dir, list(args.ids))
    if errors:
        for message in errors:
            print(f"ERROR {message}", file=sys.stderr)
        return 2
    if not specs:
        print("no matching slice specs")
        return 2
    inventory_ids = {d.get("id") for d in inv.datasets}
    storage_ids = set(load_storages(cfg_path))
    for spec in specs:
        verrs, _ = slice_export.validate_spec(spec, inventory_ids, storage_ids, spec.get("id"))
        if verrs:
            for message in verrs:
                print(f"ERROR {spec.get('id')}: {message}", file=sys.stderr)
            return 2
    source, err = slice_export.resolve_source(specs[0], inv)
    if source is None:
        print(f"ERROR {err}", file=sys.stderr)
        return 2
    for spec in specs[1:]:
        other, err2 = slice_export.resolve_source(spec, inv)
        if other is None or (other.dataset_id, other.root) != (source.dataset_id, source.root):
            print(f"ERROR spec '{spec['id']}' does not share source with the group", file=sys.stderr)
            return 2
    for spec in specs:
        problems = slice_export.check_columns(spec, source)
        if problems:
            for message in problems:
                print(f"ERROR {spec['id']}: {message}", file=sys.stderr)
            return 2
    storages = load_storages(cfg_path)
    chunk_list = slice_export.parse_chunks(args.chunks, len(source.chunks))
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"slice group [{mode}]: {', '.join(str(s.get('id')) for s in specs)}")
    print(f"  source : {source.dataset_id} [{source.channel_id}] {source.root}")
    print(f"  chunks : {len(chunk_list) if chunk_list else len(source.chunks)}/{len(source.chunks)}"
          + (f" (selection: {args.chunks})" if chunk_list else ""))
    for spec in specs:
        print(f"  output : {spec.get('id')} -> {slice_export.output_file(spec, storages)}")
    if not args.apply:
        print("  (dry-run: plan only; add --apply to export)")
        return 0

    from .tasks import TaskManager
    mgr = TaskManager()
    worker = (lambda task, emit: slice_export.run_slices(
        specs, inv, storages, task.dir, emit, chunks=chunk_list, chunk_text=args.chunks))
    task = mgr.start("slice", {"ids": [str(s.get("id")) for s in specs],
                               "chunks": args.chunks}, worker)
    print(f"  task   : {task.id} (dir {task.dir})")
    last = 0
    printed = set()
    while task.state not in ("done", "failed", "cancelled"):
        time.sleep(0.4)
        for event in mgr.events(task.id, last):
            last = event["seq"]
            _print_slice_event(event, printed)
    for event in mgr.events(task.id, last):
        _print_slice_event(event, printed)
    print(f"  result : {task.state} (exit {task.exit_code})")
    return 0 if task.state == "done" else 1


def _print_slice_event(event: dict, printed: set) -> None:
    etype, data = event["type"], event["data"]
    if etype == "log":
        print("   " + str(data.get("text", "")))
    elif etype == "error":
        print("   ERROR " + str(data.get("message", "")), file=sys.stderr)
    elif etype == "progress":
        key = data.get("done")
        if key not in printed:
            printed.add(key)
            extra = data.get("kept") or data.get("categories") or ""
            print(f"   progress: {data.get('done')}/{data.get('total', '?')} {extra}")


def cmd_kernels(args) -> int:
    from . import kernels as kn
    reg_path = Path(resolve_config_path(args.config)).parent / kn.REGISTRY_NAME
    reg = kn.load_registry(reg_path)
    if getattr(args, "proxy", None):
        os.environ["HTTP_PROXY"] = args.proxy
        os.environ["HTTPS_PROXY"] = args.proxy
    if args.kernels_command == "list":
        return kn.cmd_list(reg, as_json=args.json)
    if args.kernels_command == "verify":
        return kn.cmd_verify(reg, args.dirs, as_json=args.json)
    if args.kernels_command == "fetch":
        return kn.cmd_fetch(reg, args.ids, parallel=args.parallel, apply=args.apply)
    if args.kernels_command == "send":
        return kn.cmd_send(reg, args.ids, app=args.app, apply=args.apply)
    print("usage: kernels list|verify|fetch|send", file=sys.stderr)
    return 2


def cmd_consolidate(args) -> int:
    from . import consolidate as cs
    dataset_id = None
    if args.from_path:
        src = Path(args.from_path).expanduser()
    else:
        if not args.catalogue:
            print("error: give an inventory dataset id or --from PATH", file=sys.stderr)
            return 2
        cfg_path, inv_path, log_path, cfg, inv = load_all(args)
        ds = next((d for d in inv.datasets if d.get("id") == args.catalogue), None)
        if ds is None:
            print(f"error: dataset '{args.catalogue}' not in inventory", file=sys.stderr)
            return 2
        channels = [c for c in (ds.get("channels") or [])
                    if c.get("protocol") == "file" and c.get("path")]
        if not channels:
            print(f"error: dataset '{args.catalogue}' has no file channel", file=sys.stderr)
            return 2
        src = Path(str(channels[0]["path"])).expanduser()
        dataset_id = args.catalogue

    plan, err = cs.build_plan(source=src, dataset_path=None, app=Path(args.app),
                              profile_spec=args.profile, dataset_id=dataset_id,
                              region_spec=args.region, attributes=args.attributes,
                              limit=args.limit, name=args.name,
                              column_profile=args.column_profile,
                              layout=args.layout, order=args.order,
                              index=args.index, hdu=args.hdu,
                              jobs=args.jobs, schema=args.schema)
    if plan is None:
        print(f"error: {err}", file=sys.stderr)
        return 2
    total_bytes = sum(p.stat().st_size for p in plan.source_files)
    if not args.apply:
        print("consolidate [DRY-RUN]")
        print(f"  name   : {plan.name}  mode: {plan.mode}")
        print(f"  profile: {plan.profile.name} (delimiter={plan.profile.delimiter!r}, "
              f"header={plan.profile.header})")
        print(f"  source : {len(plan.source_files)} file(s), {total_bytes/1e6:.1f} MB")
        for p_ in plan.source_files[:5]:
            print(f"           {p_}")
        if len(plan.source_files) > 5:
            print(f"           ... (+{len(plan.source_files)-5} more)")
        print(f"  columns: {len(plan.columns)} total"
              + (f"; writing: {', '.join(plan.attributes)}" if plan.attributes else ""))
        print(f"  format : {plan.source_format}; layout={plan.layout}; order={plan.order}; "
              f"column-profile={plan.column_profile}; index={','.join(plan.index_columns)}; "
              f"jobs={plan.jobs}")
        if plan.warnings:
            for w in plan.warnings:
                print(f"  warning: {w}")
        if plan.region:
            print(f"  region : {plan.region}")
        if plan.limit:
            print(f"  limit  : {plan.limit} input rows (partial)")
        print(f"  dest   : {plan.dest_h5}")
        print("  (dry-run: plan only; add --apply to consolidate)")
        return 0

    from .tasks import TaskManager
    mgr = TaskManager()
    worker = (lambda task, emit: cs.run_consolidate(plan, emit))
    task = mgr.start("consolidate", {"name": plan.name, "mode": plan.mode,
                                     "app": str(plan.dest_dir.parent)}, worker)
    print(f"  task   : {task.id} (dir {task.dir})")
    last = 0
    printed: set = set()
    while task.state not in ("done", "failed", "cancelled"):
        time.sleep(0.4)
        for event in mgr.events(task.id, last):
            last = event["seq"]
            _print_slice_event(event, printed)
    for event in mgr.events(task.id, last):
        _print_slice_event(event, printed)
    print(f"  result : {task.state} (exit {task.exit_code})")
    return 0 if task.state == "done" else 1


def _parse_cone(text):
    parts = [float(x) for x in str(text).split(",")]
    if len(parts) != 3:
        raise ValueError("--cone needs RA,DEC,RADIUS_DEG")
    return tuple(parts)


def _parse_box(text):
    parts = [float(x) for x in str(text).split(",")]
    if len(parts) != 4:
        raise ValueError("--box needs RA1,RA2,DEC1,DEC2")
    return tuple(parts)


def cmd_consolidate_select(args) -> int:
    from .select import ConsolidatedCatalog
    ids = []
    if args.ids:
        ids.extend(int(x) for x in str(args.ids).split(",") if x.strip())
    if args.id:
        ids.extend(int(x) for x in args.id)
    cone = _parse_cone(args.cone) if args.cone else None
    box = _parse_box(args.box) if args.box else None
    cols = [c.strip() for c in args.columns.split(",")] if args.columns else None
    try:
        cat = ConsolidatedCatalog(args.source)
        sel = cat.select(ids=ids or None, cone=cone, box=box, where=args.where or "",
                         columns=cols, limit=args.limit)
    except (ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.count:
        print(sel.meta["rows"])
        return 0
    if not args.out:
        print("error: give --out or --count", file=sys.stderr)
        return 2
    out = Path(args.out).expanduser()
    fmt = args.format
    if fmt == "csv":
        sel.to_csv(out)
    elif fmt == "npy":
        sel.to_npy(out)
    elif fmt == "fits":
        try:
            sel.to_fits(out)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
    else:
        print(f"error: unsupported format '{fmt}'", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(sel.meta, indent=2, ensure_ascii=False))
    else:
        print(f"selected {sel.meta['rows']} row(s) -> {out}")
    return 0


def cmd_hpxmap(args) -> int:
    from .hpxmap import build_map, write_healpix_fits, write_npy_map
    out = Path(args.out).expanduser()
    fmt = args.format
    if fmt is None:
        fmt = "npy" if out.suffix.lower() == ".npy" else "fits"
    def progress(done, total):
        if args.progress:
            print(f"  {done}/{total} rows", file=sys.stderr)
    try:
        result = build_map(
            args.source, nside=args.nside, quantity=args.quantity,
            expr=args.expr, weight_expr=args.weight_expr,
            unit=args.unit, label=args.label, chunk_rows=args.chunk,
            limit=args.limit, progress=progress)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if fmt == "npy":
        path = write_npy_map(out, result)
    else:
        path = write_healpix_fits(out, result)
    if args.json:
        print(json.dumps(result.meta, indent=2, ensure_ascii=False))
    else:
        print(f"HEALPix nside={result.meta['nside']} npix={result.meta['npix']} "
              f"quantity={result.meta['quantity']} rows={result.meta['rows']} -> {path}")
    return 0


def cmd_spectral_cube(args) -> int:
    from .spectra import build_spectral_cube
    def progress(done, total):
        if args.progress:
            print(f"  {done}/{total} rows", file=sys.stderr)
    try:
        result = build_spectral_cube(
            args.source, args.out, nside=args.nside,
            chunk_rows=args.chunk, buffer_parents=args.buffer_parents,
            no_g_supp=args.no_g_supp, nir_supp=args.nir_supp,
            xp_supp=args.xp_supp, progress=progress)
    except (ValueError, OSError, FileExistsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"spectral cube nside={result.nside} shape=({result.npix},{result.nwave}) "
          f"rows={result.rows} model={result.model} quality=D -> {result.path}")
    return 0


def cmd_crossmatch(args) -> int:
    from .crossmatch import crossmatch_tables
    try:
        result = crossmatch_tables(
            args.left, args.right, args.out,
            radius_arcsec=args.radius_arcsec,
            left_node=args.left_table, right_node=args.right_table,
            left_ra=args.left_ra, left_dec=args.left_dec,
            right_ra=args.right_ra, right_dec=args.right_dec,
            left_id=args.left_id, right_id=args.right_id,
            chunk_rows=args.chunk, fmt=args.format)
    except (ValueError, OSError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"crossmatch radius={result.radius_arcsec} arcsec "
          f"left={result.left_rows} right={result.right_rows} "
          f"matches={result.matches} -> {result.path}")
    return 0


def _default_mpcorb() -> Path | None:
    for candidate in (Path.home() / "Datasets/catalogs/mpc/elements/MPCORB.DAT.gz",
                      Path.home() / "oasis-catalog-store/catalogs/mpc/elements/MPCORB.DAT.gz"):
        if candidate.exists():
            return candidate
    return None


def cmd_mpc(args) -> int:
    if args.mpc_command != "parse":
        print("usage: mpc parse [--raw PATH] [--dest DIR] [--limit N] [--apply]", file=sys.stderr)
        return 2
    from . import mpcorb
    raw = Path(args.raw).expanduser() if args.raw else _default_mpcorb()
    if raw is None or not raw.exists():
        print("error: MPCORB.DAT.gz not found (use --raw)", file=sys.stderr)
        return 2
    dest = Path(args.dest).expanduser() if args.dest else raw.parent
    if not args.apply:
        print("mpc parse [DRY-RUN]")
        print(f"  source : {raw} ({raw.stat().st_size / 1e6:.1f} MB)")
        print(f"  sha256 : {mpcorb.sha256_file(raw)[:16]}…")
        print(f"  dest   : {dest}/mpc_elements.csv.gz + mpc_elements.manifest.json")
        print(f"  columns: {', '.join(mpcorb.COLUMNS)}")
        print("  category v1: NEO q<1.3 | TNO a>30.1 | Centaur 5.5<a<30.1 | "
              "MBA 2.0<=a<=3.2 | other")
        print(f"  rows   : {mpcorb.count_rows(raw)}")
        if args.limit:
            print(f"  limit  : {args.limit} (partial run)")
        print("  (dry-run: plan only; add --apply to parse)")
        return 0

    from .tasks import TaskManager
    mgr = TaskManager()
    worker = (lambda task, emit: mpcorb.run_parse(raw, dest, task.dir, emit,
                                                  limit=args.limit))
    task = mgr.start("mpc_parse", {"raw": str(raw), "dest": str(dest),
                                   "limit": args.limit}, worker)
    print(f"  task   : {task.id} (dir {task.dir})")
    last = 0
    printed: set = set()
    while task.state not in ("done", "failed", "cancelled"):
        time.sleep(0.4)
        for event in mgr.events(task.id, last):
            last = event["seq"]
            _print_slice_event(event, printed)
    for event in mgr.events(task.id, last):
        _print_slice_event(event, printed)
    print(f"  result : {task.state} (exit {task.exit_code})")
    return 0 if task.state == "done" else 1


def cmd_hdf5(args) -> int:
    from . import hdf5_export
    files = [Path(f).expanduser() for f in args.files]
    missing = [f for f in files if not f.exists()]
    if missing:
        for f in missing:
            print(f"error: file not found: {f}", file=sys.stderr)
        return 2
    dest = Path(args.dest).expanduser() if args.dest else None

    def out_for(src: Path) -> Path:
        name = src.name[:-7] + ".h5" if src.name.endswith(".csv.gz") else src.name + ".h5"
        return (dest / name) if dest else src.with_name(name)

    if not args.apply:
        print("hdf5 rendition [DRY-RUN]")
        for src in files:
            header, types, rows, _ = hdf5_export.scan_file(src)
            print(f"  {src}")
            print(f"    -> {out_for(src)}  ({rows} rows)")
            print("    columns: " + ", ".join(f"{n}({t})" for n, t in zip(header, types)))
        print("  (dry-run: plan only; add --apply to convert)")
        return 0

    rc = 0
    for src in files:
        def emit(etype, data):
            if etype == "log":
                print("   " + str(data.get("text", "")))
            elif etype == "error":
                print("   ERROR " + str(data.get("message", "")), file=sys.stderr)

        out = out_for(src)
        result = hdf5_export.convert(src, out, emit)
        problems = hdf5_export.verify_readback(src, out)
        if problems:
            rc = 1
            for problem in problems[:5]:
                print(f"   MISMATCH {problem}", file=sys.stderr)
        else:
            print(f"   readback OK ({min(3, result['rows'])} row(s) compared)")
    return rc


def cmd_tasks(args) -> int:
    from .tasks import TaskManager
    mgr = TaskManager()
    if args.tasks_command == "list":
        tasks = mgr.list_tasks(limit=args.limit)
        if not tasks:
            print("no tasks")
            return 0
        for t in tasks:
            note = (t.get("detail") or t.get("error") or "")[:60]
            print(f"{t['id']}  {t['kind']:10s} {t['state']:8s} "
                  f"exit={t.get('exit_code') if t.get('exit_code') is not None else '-':4} "
                  f"{t.get('created_at','')}  {note}")
        return 0
    task_id = args.id
    task = mgr.get(task_id)
    print(json.dumps(task.public() if task else {"id": task_id,
                                                 "state": "unknown (not in this process)"},
                     indent=2, ensure_ascii=False))
    if args.tasks_command == "show":
        for event in mgr.events(task_id):
            data = json.dumps(event["data"], ensure_ascii=False)
            print(f"[{event['seq']:4}] {event['ts']} {event['type']:8s} {data[:160]}")
        return 0
    if args.tasks_command == "watch":
        last = 0
        while True:
            for event in mgr.events(task_id, last):
                last = event["seq"]
                data = json.dumps(event["data"], ensure_ascii=False)
                print(f"[{event['seq']:4}] {event['ts']} {event['type']:8s} {data[:160]}")
                if event["type"] == "state" and event["data"].get("state") in (
                        "done", "failed", "cancelled"):
                    return 0 if event["data"]["state"] == "done" else 1
            time.sleep(0.5)
    print("usage: tasks list | tasks show <id> | tasks watch <id>", file=sys.stderr)
    return 2


def cmd_web(args) -> int:
    cfg_path = Path(resolve_config_path(args.config))
    if not cfg_path.exists():
        print(f"error: config file not found: {cfg_path}", file=sys.stderr)
        return 1
    from .webapp import serve
    return serve(cfg_path, port=args.port, open_browser=not args.no_open)


def register(sub, common) -> dict:
    p_probe = sub.add_parser("probe", parents=[common],
                             help="channel connectivity + version determination (read-only)")
    p_probe.add_argument("ids", nargs="*", help="dataset ids (default: all)")
    p_probe.add_argument("--channel", default=None, help="restrict to one channel id")
    p_probe.add_argument("--timeout", type=float, default=10.0, help="network timeout seconds")

    p_st = sub.add_parser("storages", parents=[common],
                          help="file-system view of registered storages")
    p_st.add_argument("--json", action="store_true", help="JSON output")

    p_web = sub.add_parser("web", parents=[common],
                           help="local web UI on 127.0.0.1 (foreground)")
    p_web.add_argument("--port", type=int, default=8787, help="listen port (default 8787)")
    p_web.add_argument("--no-open", action="store_true", help="do not open a browser")

    p_slice = sub.add_parser("slice", parents=[common],
                             help="slice specs: list / run (dry-run default)")
    slice_sub = p_slice.add_subparsers(dest="slice_command", required=True)
    slice_sub.add_parser("list", parents=[common], help="list slice specs + validation status")
    p_run = slice_sub.add_parser("run", parents=[common],
                                 help="run a slice group (specs sharing a source scan once)")
    p_run.add_argument("ids", nargs="+", help="slice spec ids (files in ~/.config/oasis/slices/)")
    p_run.add_argument("--chunks", default=None, help="chunk selection, e.g. '0-99,200' (partial run)")
    p_run.add_argument("--apply", action="store_true", help="execute (default: dry-run plan)")

    p_tasks = sub.add_parser("tasks", parents=[common], help="task runtime: list / show / watch")
    tasks_sub = p_tasks.add_subparsers(dest="tasks_command", required=True)
    p_tl = tasks_sub.add_parser("list", parents=[common], help="recent tasks")
    p_tl.add_argument("--limit", type=int, default=20)
    tasks_sub.add_parser("show", parents=[common], help="task.json + events of a task").add_argument("id")
    tasks_sub.add_parser("watch", parents=[common],
                         help="follow a task's event stream until it finishes").add_argument("id")

    p_mpc = sub.add_parser("mpc", parents=[common], help="MPC catalogue tools: parse")
    mpc_sub = p_mpc.add_subparsers(dest="mpc_command", required=True)
    p_parse = mpc_sub.add_parser("parse", parents=[common],
                                 help="MPCORB.DAT.gz -> element table (CSV.gz) + manifest")
    p_parse.add_argument("--raw", default=None, help="raw MPCORB.DAT.gz (default: delivery/store)")
    p_parse.add_argument("--dest", default=None, help="output dir (default: raw's dir)")
    p_parse.add_argument("--limit", type=int, default=None, help="first N rows (test/partial)")
    p_parse.add_argument("--apply", action="store_true", help="execute (default: dry-run plan)")

    p_k = sub.add_parser("kernels", parents=[common],
                         help="SPICE kernel registry & supply (foundation assets)")
    k_sub = p_k.add_subparsers(dest="kernels_command", required=True)
    k_list = k_sub.add_parser("list", parents=[common], help="registry + store status")
    k_list.add_argument("--json", action="store_true")
    k_ver = k_sub.add_parser("verify", parents=[common],
                             help="checksum verification (store, or given dirs)")
    k_ver.add_argument("dirs", nargs="*")
    k_ver.add_argument("--json", action="store_true")
    k_fetch = k_sub.add_parser("fetch", parents=[common],
                               help="channel -> store (parallel ranges, resume, verify)")
    k_fetch.add_argument("ids", nargs="+", help="kernel ids (or 'all')")
    k_fetch.add_argument("--parallel", type=int, default=8)
    k_fetch.add_argument("--proxy", default=None, help="HTTP(S) proxy, e.g. http://127.0.0.1:7897")
    k_fetch.add_argument("--apply", action="store_true", help="execute (default: dry-run plan)")
    k_send = k_sub.add_parser("send", parents=[common],
                              help="store -> <app>/spice_kernels (verify + manifest)")
    k_send.add_argument("ids", nargs="+", help="kernel ids (or 'all')")
    k_send.add_argument("--app", required=True, help="application workspace directory")
    k_send.add_argument("--apply", action="store_true", help="execute (default: dry-run plan)")

    p_c = sub.add_parser("consolidate", parents=[common],
                         help="bring a catalogue into an app workspace (PyTables working set)")
    p_c.add_argument("catalogue", nargs="?", help="inventory dataset id (or use --from)")
    p_c.add_argument("--from", dest="from_path", default=None, help="source file or directory")
    p_c.add_argument("--app", required=True, help="application workspace directory")
    p_c.add_argument("--profile", default=None, help="builtin profile name or YAML file")
    p_c.add_argument("--region", default=None, help="cone:RA,DEC,RADIUS_DEG | box:RA1,RA2,DEC1,DEC2")
    p_c.add_argument("--attributes", default=None, help="comma-separated attribute subset")
    p_c.add_argument("--limit", type=int, default=None, help="max input rows (partial/test)")
    p_c.add_argument("--name", default=None, help="output basename override")
    p_c.add_argument("--column-profile", choices=["core", "full"], default=None,
                     help="column set (default: profile default, Gaia=core)")
    p_c.add_argument("--layout", choices=["spatial", "source_id", "csr"], default=None,
                     help="table layout (default: profile, Gaia=spatial)")
    p_c.add_argument("--order", type=int, default=None, help="HEALPix order for spatial layout")
    p_c.add_argument("--index", default=None,
                     help="comma-separated CSI columns (default: source_id,phot_g_mean_mag)")
    p_c.add_argument("--hdu", default=None, help="FITS HDU name/index (default: 0)")
    p_c.add_argument("--jobs", type=int, default=1,
                     help="parallel CSV reader processes (default: 1)")
    p_c.add_argument("--schema", default=None,
                     help="JSON column dtype schema; skips full type inference")
    p_c.add_argument("--apply", action="store_true", help="execute (default: dry-run plan)")

    p_s = sub.add_parser("consolidate-select", parents=[common],
                         help="select rows from a consolidated PyTables catalogue")
    p_s.add_argument("source", help="consolidated .h5")
    p_s.add_argument("--id", action="append", default=None, help="source_id (repeatable)")
    p_s.add_argument("--ids", default=None, help="comma-separated source_ids")
    p_s.add_argument("--cone", default=None, help="RA,DEC,RADIUS_DEG")
    p_s.add_argument("--box", default=None, help="RA1,RA2,DEC1,DEC2")
    p_s.add_argument("--where", default=None, help="PyTables condition, e.g. 'phot_g_mean_mag < 18'")
    p_s.add_argument("--columns", default=None, help="comma-separated output columns")
    p_s.add_argument("--limit", type=int, default=None)
    p_s.add_argument("--format", choices=["csv", "fits", "npy"], default="csv")
    p_s.add_argument("--out", default=None)
    p_s.add_argument("--count", action="store_true")
    p_s.add_argument("--json", action="store_true")

    p_h = sub.add_parser("hpxmap", parents=[common],
                         help="bincount a consolidated catalogue onto a HEALPix map")
    p_h.add_argument("source", help="consolidated .h5")
    p_h.add_argument("--nside", type=int, required=True,
                     help="target NESTED nside (power of two)")
    p_h.add_argument("--quantity", choices=["count", "sum", "mean", "weighted_mean"],
                     default="count")
    p_h.add_argument("--expr", default=None,
                     help="value expression, e.g. 'phot_g_mean_flux' or '10**(-0.4*phot_g_mean_mag)'")
    p_h.add_argument("--weight-expr", default=None, help="weight expression for weighted_mean")
    p_h.add_argument("--unit", default=None, help="physical unit written to FITS BUNIT/TUNIT1")
    p_h.add_argument("--label", default=None, help="human label for OBJECT")
    p_h.add_argument("--chunk", type=int, default=1_000_000, help="rows per chunk")
    p_h.add_argument("--limit", type=int, default=None)
    p_h.add_argument("--out", required=True)
    p_h.add_argument("--format", choices=["fits", "npy"], default=None)
    p_h.add_argument("--json", action="store_true")
    p_h.add_argument("--progress", action="store_true")
    p_h.set_defaults(func=cmd_hpxmap)

    p_cm = sub.add_parser("crossmatch", parents=[common],
                          help="spatial nearest-neighbour match between HDF5 tables")
    p_cm.add_argument("left")
    p_cm.add_argument("right")
    p_cm.add_argument("--out", required=True)
    p_cm.add_argument("--radius-arcsec", type=float, default=3.0)
    p_cm.add_argument("--left-table", default="/table")
    p_cm.add_argument("--right-table", default="/table")
    p_cm.add_argument("--left-ra", default="ra")
    p_cm.add_argument("--left-dec", default="dec")
    p_cm.add_argument("--right-ra", default="ra")
    p_cm.add_argument("--right-dec", default="dec")
    p_cm.add_argument("--left-id", default=None)
    p_cm.add_argument("--right-id", default=None)
    p_cm.add_argument("--chunk", type=int, default=200_000)
    p_cm.add_argument("--format", choices=["hdf5", "csv"], default="hdf5")
    p_cm.set_defaults(func=cmd_crossmatch)

    p_sc = sub.add_parser("spectral-cube", parents=[common],
                          help="build a per-pixel 343-point HEALPix spectral cube")
    p_sc.add_argument("source", help="consolidated spatial .h5")
    p_sc.add_argument("--nside", type=int, default=2048)
    p_sc.add_argument("--out", required=True)
    p_sc.add_argument("--chunk", type=int, default=1_000_000)
    p_sc.add_argument("--buffer-parents", type=int, default=4096)
    p_sc.add_argument("--no-g-supp", default=None,
                      help="no_g_supp.h5 with source_id/class_code/rp_mag")
    p_sc.add_argument("--nir-supp", default=None,
                      help="nir_supp.h5 with 2MASS/AllWISE matches")
    p_sc.add_argument("--xp-supp", default=None,
                      help="xp_supp.h5 with sampled XP per-pixel spectra")
    p_sc.add_argument("--progress", action="store_true")
    p_sc.set_defaults(func=cmd_spectral_cube)

    p_hdf5 = sub.add_parser("hdf5", parents=[common],
                            help="CSV.gz -> HDF5 rendition (optional format; canonical stays CSV.gz)")
    p_hdf5.add_argument("files", nargs="+", help="CSV.gz file(s)")
    p_hdf5.add_argument("--dest", default=None, help="output dir (default: alongside source)")
    p_hdf5.add_argument("--apply", action="store_true", help="execute (default: dry-run plan)")

    return {"probe": cmd_probe, "storages": cmd_storages, "web": cmd_web,
            "slice": cmd_slice, "tasks": cmd_tasks, "mpc": cmd_mpc, "hdf5": cmd_hdf5,
            "consolidate": cmd_consolidate, "consolidate-select": cmd_consolidate_select,
            "hpxmap": cmd_hpxmap, "crossmatch": cmd_crossmatch,
            "spectral-cube": cmd_spectral_cube, "kernels": cmd_kernels}
