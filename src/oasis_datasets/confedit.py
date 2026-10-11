"""Controlled writes for config-family files (DSM-003 §10.1).

Features: mtime guard (concurrency), atomic replace (temp + os.replace),
timestamped backups with retention (`.bak/<name>.<ts>`, keep last N).
"""

from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

BACKUP_DIRNAME = ".bak"
KEEP_BACKUPS = 10


def read_with_mtime(path: Path) -> tuple[str | None, float | None]:
    if not path.exists():
        return None, None
    return path.read_text(encoding="utf-8"), path.stat().st_mtime


def mtime_changed(path: Path, recorded: float | None) -> bool:
    """True when the on-disk file changed since `recorded` (None = no guard)."""
    if recorded is None:
        return False
    if not path.exists():
        return True
    return abs(path.stat().st_mtime - recorded) > 1e-6


def atomic_write(path: Path, text: str, keep: int = KEEP_BACKUPS) -> Path | None:
    """Back up the existing file (if any), then atomically replace with `text`.

    Returns the backup path (or None when there was nothing to back up).
    """
    backup: Path | None = None
    if path.exists():
        backup_dir = path.parent / BACKUP_DIRNAME
        backup_dir.mkdir(exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        backup = backup_dir / f"{path.name}.{stamp}"
        seq = 1
        while backup.exists():
            backup = backup_dir / f"{path.name}.{stamp}-{seq}"
            seq += 1
        shutil.copy2(path, backup)
        history = sorted(p for p in backup_dir.glob(f"{path.name}.*"))
        for old in history[:-keep]:
            old.unlink()

    tmp = path.parent / (path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)
    return backup
