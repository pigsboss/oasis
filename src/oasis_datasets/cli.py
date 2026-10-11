"""OASIS datasets manager CLI (targets layer).

Commands: list / verify / sync / probe / storages / inventory / propose / review / migrate-config.
Resolution: inventory.yaml first, legacy `config.datasets` fallback (DSM-002 §3.8).
Config resolution: --config > $OASIS_CONFIG > ~/.config/oasis/config.yaml > ./catalogues.yaml
All runtime output is English (CODING_STANDARDS §2.2).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from oasis_catalog.config import ConfigError, load_config, resolve_config_path

from . import __version__
from . import mirror as mirror_mod
from .checksums import discover
from .resolve import dest_for, load_inventory_for, local_refs
from .sync import ensure_remote_dir, load_storages, run_sync
from .verify import verify


def _load(args):
    path = resolve_config_path(args.config)
    try:
        cfg = load_config(path)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
    print(f"config: {cfg.config_path}")
    return cfg


def _local_root(ds, c) -> Path | None:
    base = ds.access_path()
    if base is None or ds.kind not in ("local_volume", "local_store"):
        return None
    return base / c.path


def _list_inventory(args, inv) -> int:
    print(f"source: {inv.path} ({len(inv.datasets)} datasets, {len(inv.proposals)} proposals)")
    for ds in inv.datasets:
        ds_id = str(ds.get("id", ""))
        channels = ds.get("channels") or []
        if args.ids and ds_id not in args.ids and not any(ch.get("id") in args.ids for ch in channels):
            continue
        status = ds.get("status", "active")
        print(f"\n[{status}] {ds_id} — {ds.get('title', '')}")
        pref = ", ".join(ds.get("storage_pref") or [])
        if pref:
            print(f"  storage_pref: {pref}")
        for ch in channels:
            cid = str(ch.get("id", "?"))
            if args.ids and ds_id not in args.ids and cid not in args.ids:
                continue
            proto = str(ch.get("protocol", "?"))
            if proto == "file" and ch.get("path"):
                root = Path(str(ch["path"])).expanduser()
                if not root.exists():
                    print(f"  - {cid:16s} [file ] MISSING {root}")
                    continue
                manifests = discover(root) if root.is_dir() else []
                names = ", ".join(m.name for m in manifests) if manifests else "-"
                print(f"  - {cid:16s} [file ] ok  {root}  manifests: {names}")
            else:
                target = ch.get("url") or ch.get("host") or ""
                print(f"  - {cid:16s} [{proto:5s}] {target} (not probed)")
    if inv.proposals:
        print(f"\n{len(inv.proposals)} proposal(s) pending — `review list` for details")
    return 0


def cmd_list(args) -> int:
    cfg = _load(args)
    inv = load_inventory_for(cfg.config_path)
    if inv.datasets:
        return _list_inventory(args, inv)
    for ds in cfg.datasets:
        if args.ids and ds.id not in args.ids and not any(c.id in args.ids for c in ds.catalogues):
            continue
        print(f"\n[{ds.kind}] {ds.id} — {ds.title}")
        print(f"  access: {ds.access_summary()}")
        for c in ds.catalogues:
            if args.ids and ds.id not in args.ids and c.id not in args.ids:
                continue
            root = _local_root(ds, c)
            if root is None:
                tag = "remote/updatable" if c.updatable else "-"
                print(f"  - {c.id:24s} [{tag}]")
                continue
            if not root.exists():
                print(f"  - {c.id:24s} [MISSING] {root}")
                continue
            manifests = discover(root)
            names = ", ".join(m.name for m in manifests) if manifests else "-"
            print(f"  - {c.id:24s} [ok] manifests: {names}")
            if c.size_hint:
                print(f"      size: {c.size_hint}")
    return 0


def cmd_verify(args) -> int:
    cfg = _load(args)
    inv = load_inventory_for(cfg.config_path)
    refs = local_refs(cfg, inv, args.ids)
    if not refs:
        print("no matching local catalogues")
        return 2
    rc = 0
    for ref in refs:
        if not ref.root.exists():
            print(f"== {ref.ds_id}/{ref.cid}: FAIL path missing {ref.root}")
            rc = 1
            continue
        mode = "full" if args.full else f"sample={args.sample}"
        print(f"== {ref.ds_id}/{ref.cid} ({mode}): {ref.root}")
        reports, failures = verify(ref.root, sample=args.sample, full=args.full)
        if not reports and failures == 2:
            print("   no checksum manifest found")
            rc = max(rc, 2)
            continue
        for report in reports:
            print(f"   manifest: {report.manifest.path.name}  entries={report.listed}  "
                  f"content={report.manifest.content}  missing={report.missing_listed}")
            for result in report.results:
                suffix = f"  ({result.detail})" if result.detail else ""
                print(f"     {result.status:7s} {result.name}{suffix}")
        if failures:
            rc = 1
    return rc


def cmd_sync(args) -> int:
    cfg = _load(args)
    if not (args.to or args.to_path):
        print("error: provide --to <storage-id> or --to-path DIR", file=sys.stderr)
        return 2
    storages = load_storages(cfg.config_path) if args.to else {}
    inv = load_inventory_for(cfg.config_path)
    refs = local_refs(cfg, inv, args.ids)
    if not refs:
        print("no matching local catalogues")
        return 2
    rc = 0
    for ref in refs:
        if not ref.root.exists():
            print(f"== {ref.ds_id}/{ref.cid}: FAIL source missing {ref.root}")
            rc = 1
            continue
        if args.to:
            storage = storages.get(args.to)
            if storage is None:
                print(f"== {ref.ds_id}/{ref.cid}: FAIL unknown storage '{args.to}'")
                rc = 1
                continue
            access = storage.get("access") or {}
            protocols = list(access.get("protocols") or
                             ([access["protocol"]] if access.get("protocol") else []))
            if any(p in ("ssh", "ssh+rsync") for p in protocols):
                host = str(access.get("host", ""))
                remote_base = str(access.get("path", ""))
                if not host or not remote_base or "<TODO" in host or "<TODO" in remote_base:
                    print(f"== {ref.ds_id}/{ref.cid}: FAIL storage '{args.to}' ssh target "
                          "not fully configured (host/path)")
                    rc = 1
                    continue
                remote_dir = f"{remote_base.rstrip('/')}/oasis-datasets/{ref.rel_path or ref.ds_id}"
                if args.apply:
                    mkdir_target = remote_dir if ref.root.is_dir() else str(Path(remote_dir).parent)
                    if ensure_remote_dir(host, mkdir_target, apply=True) != 0:
                        print(f"== {ref.ds_id}/{ref.cid}: FAIL remote mkdir {mkdir_target}")
                        rc = 1
                        continue
                dest = f"{host}:{remote_dir}"
            else:
                base = access.get("path")
                if not base:
                    print(f"== {ref.ds_id}/{ref.cid}: FAIL storage '{args.to}' has no file path")
                    rc = 1
                    continue
                base = Path(str(base)).expanduser()
                if not base.exists():
                    print(f"== {ref.ds_id}/{ref.cid}: FAIL storage '{args.to}' not mounted ({base})")
                    rc = 1
                    continue
                dest = dest_for(base, ref)
        else:
            dest = Path(args.to_path).expanduser() / (ref.rel_path or ref.ds_id)
        mode = "APPLY" if args.apply else "DRY-RUN"
        print(f"== {ref.ds_id}/{ref.cid} [{mode}] {ref.root} -> {dest}")
        rc |= run_sync(ref.root, dest, apply=args.apply)
    return rc


def cmd_mirror(args) -> int:
    """Remote (https) dataset -> local storage, with manifest (DSM-002 §3.2)."""
    cfg = _load(args)
    inv = load_inventory_for(cfg.config_path)
    storages = load_storages(cfg.config_path)
    if not args.to:
        print("error: provide --to <storage-id>", file=sys.stderr)
        return 2
    storage = storages.get(args.to)
    if storage is None:
        print(f"error: unknown storage '{args.to}'", file=sys.stderr)
        return 2
    base = (storage.get("access") or {}).get("path")
    if not base or "<TODO" in str(base):
        print(f"error: storage '{args.to}' has no configured file path", file=sys.stderr)
        return 2
    base_path = Path(str(base)).expanduser()
    if not base_path.exists():
        print(f"error: storage '{args.to}' not mounted ({base_path})", file=sys.stderr)
        return 2
    picked = [ds for ds in inv.datasets if ds.get("id") in args.ids]
    unknown = [i for i in args.ids if i not in {ds.get("id") for ds in inv.datasets}]
    if unknown:
        print(f"error: unknown dataset id(s): {', '.join(unknown)}", file=sys.stderr)
        return 2
    rc = 0
    for ds in picked:
        channels = [c for c in (ds.get("channels") or [])
                    if c.get("protocol") == "https" and c.get("url")]
        if args.channel:
            channels = [c for c in channels if c.get("id") == args.channel]
        if not channels:
            print(f"== {ds.get('id')}: no https channel, skipped")
            continue
        channel = channels[0]
        if not args.apply:
            try:
                p = mirror_mod.plan(ds, channel, storage)
            except Exception as exc:  # noqa: BLE001 - report probe failure
                print(f"== {ds.get('id')}: FAIL probe: {exc}")
                rc = 1
                continue
            print(f"== {ds.get('id')} [DRY-RUN] {p['url']}")
            print(f"   size: {p['size']} B  version: {p['version']}  ranges: {p['accept_ranges']}")
            print(f"   dest: {p['dest_file']}")
            continue

        def emit(etype, data, _id=ds.get("id")):
            if etype == "log":
                print("   " + str(data.get("text", "")))
            elif etype == "error":
                print("   ERROR " + str(data.get("message", "")), file=sys.stderr)

        code, result = mirror_mod.mirror_one(ds, channel, storage, emit, parallel=args.parallel)
        if code == 0 and result:
            mirror_mod.write_manifest(ds, [result], emit)
        rc |= code
    return rc


def _extract_config(argv: list[str]) -> tuple[str | None, list[str]]:
    """Pull every `--config VALUE` / `--config=VALUE` out of argv.

    Done pre-argparse because subparsers re-apply their own defaults and
    would clobber a --config given before the subcommand.
    """
    config: str | None = None
    rest: list[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--config":
            if i + 1 >= len(argv):
                print("error: --config requires a value", file=sys.stderr)
                raise SystemExit(2)
            config = argv[i + 1]
            i += 2
        elif arg.startswith("--config="):
            config = arg.split("=", 1)[1]
            i += 1
        else:
            rest.append(arg)
            i += 1
    return config, rest


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    config, argv = _extract_config(argv)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", default=argparse.SUPPRESS,
                        help="config file (default: ~/.config/oasis/config.yaml)")

    parser = argparse.ArgumentParser(
        prog="oasis-datasets",
        description="OASIS datasets manager (targets layer): list / verify / sync / probe / storages / inventory / propose / review / migrate-config",
        parents=[common],
    )
    parser.add_argument("--version", action="version", version=f"oasis-datasets {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", parents=[common], help="inventory datasets and checksum readiness")
    p_list.add_argument("ids", nargs="*", help="dataset/catalogue ids (default: all)")

    p_verify = sub.add_parser("verify", parents=[common], help="verify against official checksum manifests")
    p_verify.add_argument("ids", nargs="+", help="dataset/catalogue ids")
    p_verify.add_argument("--sample", type=int, default=8, help="files to sample (default: 8)")
    p_verify.add_argument("--full", action="store_true", help="verify every listed file (slow)")

    p_sync = sub.add_parser("sync", parents=[common], help="place/refresh a dataset on another storage")
    p_sync.add_argument("ids", nargs="+", help="dataset/catalogue ids")
    p_sync.add_argument("--to", default=None, help="target storage id (from storages:; file or ssh)")
    p_sync.add_argument("--to-path", default=None, help="ad-hoc destination root (mirrors catalogue path)")
    p_sync.add_argument("--apply", action="store_true", help="execute (default: dry-run)")

    p_mirror = sub.add_parser("mirror", parents=[common],
                              help="remote (https) dataset -> local storage, with manifest")
    p_mirror.add_argument("ids", nargs="+", help="dataset ids (must have an https channel)")
    p_mirror.add_argument("--to", required=True, help="target storage id (local file path)")
    p_mirror.add_argument("--channel", default=None, help="restrict to one channel id")
    p_mirror.add_argument("--parallel", type=int, default=8, help="range-download parallelism")
    p_mirror.add_argument("--apply", action="store_true", help="execute (default: dry-run plan)")

    from .inventory_cli import register as register_inventory_cli
    from .ops_cli import register as register_ops_cli
    handlers = {"list": cmd_list, "verify": cmd_verify, "sync": cmd_sync, "mirror": cmd_mirror}
    handlers.update(register_inventory_cli(sub, common))
    handlers.update(register_ops_cli(sub, common))

    args = parser.parse_args(argv)
    args.config = config
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
