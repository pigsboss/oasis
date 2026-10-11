"""Append-only review/audit log (review-log.jsonl).

Spec: DSM-003 §3 — one JSON object per line; fields ts/action/target/by/note.
The tool only appends; validation reports damage without rewriting.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

LOG_NAME = "review-log.jsonl"
ACTIONS = {"propose", "approve", "reject", "deprecate", "edit"}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_log(path: Path, action: str, target: str, by: str = "owner", note: str = "") -> dict:
    entry = {"ts": now_iso(), "action": action, "target": target, "by": by, "note": note}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def read_log(path: Path, tail: int | None = None) -> list[dict]:
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            entries.append({"_invalid": line})
    return entries[-tail:] if tail else entries


def validate_log(path: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    if not path.exists():
        return 0, []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        count += 1
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {i}: invalid JSON ({exc})")
            continue
        for key in ("ts", "action", "target", "by"):
            if key not in obj:
                errors.append(f"line {i}: missing field '{key}'")
        if obj.get("action") not in ACTIONS:
            errors.append(f"line {i}: invalid action '{obj.get('action')}'")
    return count, errors
