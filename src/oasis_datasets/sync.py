"""rsync-based placement/sync (dry-run by default; never deletes on the target)."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

import yaml


def ensure_remote_dir(host: str, path: str, apply: bool) -> int:
    """`ssh host mkdir -p path` for remote targets (no-op in dry-run)."""
    if not apply:
        return 0
    cmd = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", host,
           f"mkdir -p {shlex.quote(path)}"]
    print("   $ " + " ".join(cmd))
    return subprocess.run(cmd).returncode


def run_sync(src: Path, dest: Path | str, apply: bool = False) -> int:
    """Mirror `src` into `dest` via rsync. Dry-run unless apply=True.

    `dest` may be a local Path or a remote `host:path` string (ssh transport).
    Safety: no --delete (target extras are kept); source is opened read-only.
    File sources (e.g. a single .tar.gz payload) go path-to-path; directory
    sources use trailing-slash semantics (`src/` -> `dest/`).
    """
    remote = isinstance(dest, str)
    cmd = ["rsync", "-a", "--partial", "--human-readable", "--info=progress2"]
    if not apply:
        cmd.append("--dry-run")
    if src.is_file():
        cmd += [str(src), str(dest)]
        target = None if remote else Path(dest).parent
    else:
        cmd += [str(src) + "/", str(dest) + "/"]
        target = None if remote else Path(dest)
    print("   $ " + " ".join(cmd))
    if apply and target is not None:
        target.mkdir(parents=True, exist_ok=True)
    elif not apply and src.is_file() and target is not None and not target.exists():
        print(f"   [dry-run] would create {target}/ first; then copy {src.name}")
        return 0
    return subprocess.run(cmd).returncode


def load_storages(config_path: Path) -> dict[str, dict]:
    """Read the `storages:` section from the system config (id -> mapping)."""
    raw = yaml.safe_load(Path(config_path).read_text(encoding="utf-8")) or {}
    storages = {}
    for item in raw.get("storages") or []:
        sid = str(item.get("id", ""))
        if sid:
            storages[sid] = dict(item)
    return storages
