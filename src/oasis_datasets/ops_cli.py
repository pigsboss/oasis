"""CLI for channel probing, the local file-system view, and the web UI (M1/M2).

Commands: probe [ids...] [--channel id] [--timeout S] | storages [--json] | web [--port N] [--no-open]
          slice list | slice run <ids...> [--chunks M-N] [--apply]
All runtime output is English (CODING_STANDARDS §2.2).
"""

from __future__ import annotations

import json
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

    p_hdf5 = sub.add_parser("hdf5", parents=[common],
                            help="CSV.gz -> HDF5 rendition (optional format; canonical stays CSV.gz)")
    p_hdf5.add_argument("files", nargs="+", help="CSV.gz file(s)")
    p_hdf5.add_argument("--dest", default=None, help="output dir (default: alongside source)")
    p_hdf5.add_argument("--apply", action="store_true", help="execute (default: dry-run plan)")

    return {"probe": cmd_probe, "storages": cmd_storages, "web": cmd_web,
            "slice": cmd_slice, "tasks": cmd_tasks, "mpc": cmd_mpc, "hdf5": cmd_hdf5}
