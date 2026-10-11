"""OASIS catalogue updater CLI (targets layer, catalogue subsystem).

Commands:
  list     list datasets / catalogues from the system config and local status
  update   download/refresh remote catalogues (If-Modified-Since aware)
  verify   verify tracked catalogues against manifest (sha256)

Config resolution: --config > $OASIS_CONFIG > ~/.config/oasis/config.yaml > ./catalogues.yaml
All runtime output is English (CODING_STANDARDS §2.2).
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .config import ConfigError, load_config, resolve_config_path
from .fetch import download, is_unchanged, now_iso
from .manifest import FileEntry, Manifest, load_manifest, save_manifest, sha256_of


def _load(args):
    path = resolve_config_path(args.config)
    try:
        cfg = load_config(path)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
    print(f"config: {cfg.config_path}")
    return cfg


def _catalogue_state(cfg, ds, c) -> str:
    if c.target_dir:
        m = load_manifest(cfg.store_root / c.target_dir)
        return "not-updated" if m is None else f"updated {m.generated_at}"
    if ds.kind in ("local_volume", "local_store"):
        base = ds.access_path() or cfg.store_root
        return "ok" if (base / c.path).exists() else "missing"
    return "-"


def cmd_list(args) -> int:
    cfg = _load(args)
    print(f"store_root: {cfg.store_root}")
    for ds in cfg.datasets:
        print(f"\n[{ds.kind}] {ds.id} — {ds.title}")
        print(f"  access: {ds.access_summary()}")
        for c in ds.catalogues:
            state = _catalogue_state(cfg, ds, c)
            tag = "updatable" if c.updatable else "read-only"
            print(f"  - {c.id:22s} [{state}] [{tag}] {c.title or c.path or c.url}")
            detail = []
            if c.format:
                detail.append(c.format)
            if c.size_hint:
                detail.append(c.size_hint)
            if c.path and ds.kind == "local_volume":
                detail.append(c.path)
            if detail:
                print(f"      {' | '.join(detail)}")
    return 0


def cmd_update(args) -> int:
    cfg = _load(args)
    picked = cfg.select_updatable(args.ids)
    if not picked:
        print("no matching updatable catalogues")
        return 1
    for ds, c in picked:
        target = cfg.store_root / c.target_dir
        target.mkdir(parents=True, exist_ok=True)
        prev = load_manifest(target)
        files = {f.path: f for f in (prev.files if prev else [])}
        file_name = c.url.rsplit("/", 1)[-1] or c.id
        dest = target / file_name
        old = files.get(file_name)

        print(f"== {ds.id} / {c.id}")
        if not args.force and dest.exists() and old and old.version and is_unchanged(c.url, old.version):
            print(f"   {file_name}: unchanged (server Last-Modified {old.version})")
            files[file_name] = FileEntry(
                id=c.id,
                path=file_name,
                bytes=old.bytes,
                sha256=old.sha256,
                version=old.version,
                epoch=old.epoch or old.version,
                provider=c.provider or ds.provider,
                licence=c.licence or ds.licence,
                source_url=c.url,
            )
        else:
            print(f"   fetching {file_name}")
            print(f"     from {c.url}")
            info = download(c.url, dest, force=args.force)
            sha = sha256_of(dest)
            snapshot = info.last_modified or info.fetched_at
            state = "unchanged" if (old and old.sha256 == sha) else "updated"
            if info.resumed_from:
                print(f"     resumed from {info.resumed_from} bytes")
            print(f"     saved {dest.stat().st_size} bytes, sha256={sha[:16]}..., {state}")
            files[file_name] = FileEntry(
                id=c.id,
                path=file_name,
                bytes=dest.stat().st_size,
                sha256=sha,
                version=snapshot,
                epoch=snapshot,
                provider=c.provider or ds.provider,
                licence=c.licence or ds.licence,
                source_url=c.url,
            )
        manifest = Manifest(generated_at=now_iso(), target_dir=c.target_dir,
                            files=sorted(files.values(), key=lambda f: f.path))
        path = save_manifest(target, manifest)
        print(f"   manifest: {path}")
    return 0


def cmd_verify(args) -> int:
    cfg = _load(args)
    picked = cfg.select_tracked(args.ids)
    if not picked:
        print("no matching tracked catalogues")
        return 1
    rc = 0
    seen: set[str] = set()
    for ds, c, tdir in picked:
        if tdir in seen:
            continue
        seen.add(tdir)
        target = cfg.store_root / tdir
        manifest = load_manifest(target)
        if manifest is None:
            print(f"[{tdir}] FAIL: manifest missing")
            rc = 1
            continue
        for fe in manifest.files:
            p = target / fe.path
            ok = p.exists() and p.stat().st_size == fe.bytes and sha256_of(p) == fe.sha256
            print(f"[{tdir}] {'OK  ' if ok else 'FAIL'} {fe.path} ({fe.bytes} bytes)")
            if not ok:
                rc = 1
    return rc


def main(argv=None) -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", default=None,
                        help="config file (default: ~/.config/oasis/config.yaml, "
                             "fallback ./catalogues.yaml)")

    parser = argparse.ArgumentParser(
        prog="oasis-catalog",
        description="OASIS catalogue updater (targets layer, catalogue subsystem)",
        parents=[common],
    )
    parser.add_argument("--version", action="version", version=f"oasis-catalog {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", parents=[common], help="list datasets/catalogues and local status")

    p_update = sub.add_parser("update", parents=[common],
                              help="download/refresh remote catalogues (dataset id or catalogue id)")
    p_update.add_argument("ids", nargs="*", help="dataset/catalogue ids (default: all updatable)")
    p_update.add_argument("--force", action="store_true", help="discard local copies and re-download")

    p_verify = sub.add_parser("verify", parents=[common],
                              help="verify tracked catalogues against manifest (sha256)")
    p_verify.add_argument("ids", nargs="*", help="dataset/catalogue ids (default: all tracked)")

    args = parser.parse_args(argv)
    handlers = {"list": cmd_list, "update": cmd_update, "verify": cmd_verify}
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
