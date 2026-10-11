"""Task runtime with a persisted event stream (DSM-003 §8).

Layout: ~/.local/state/oasis/tasks/<task_id>/{task.json, events.jsonl, out.log}
States: queued | running | done | failed | cancelled
Events: {seq, ts, task_id, type: state|progress|log|done|error, data}
"""

from __future__ import annotations

import json
import secrets
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

TASKS_ROOT = Path("~/.local/state/oasis/tasks")
TERMINAL = {"done", "failed", "cancelled"}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_task_id() -> str:
    return time.strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(2)


@dataclass
class Task:
    id: str
    kind: str
    params: dict
    state: str = "queued"
    created_at: str = ""
    started_at: str | None = None
    ended_at: str | None = None
    exit_code: int | None = None
    error: str | None = None
    detail: str = ""
    dir: Path | None = None
    cancel_flag: threading.Event = field(default_factory=threading.Event)

    def public(self) -> dict:
        return {k: getattr(self, k) for k in
                ("id", "kind", "params", "state", "created_at", "started_at",
                 "ended_at", "exit_code", "error", "detail")}


class TaskManager:
    """In-process workers; the on-disk event stream is the shared truth."""

    def __init__(self, root: Path | None = None):
        self.root = Path(root) if root else TASKS_ROOT.expanduser()
        self._tasks: dict[str, Task] = {}
        self._seq: dict[str, int] = {}
        self._lock = threading.Lock()
        self._cond = threading.Condition()

    # ── lifecycle ────────────────────────────────────────────────
    def start(self, kind: str, params: dict, worker: Callable[[Task, Callable], int]) -> Task:
        task = Task(id=new_task_id(), kind=kind, params=dict(params), created_at=now_iso())
        task.dir = self.root / task.id
        task.dir.mkdir(parents=True, exist_ok=True)
        self._write(task)
        with self._lock:
            self._tasks[task.id] = task
            self._seq[task.id] = 0
        threading.Thread(target=self._run, args=(task, worker), daemon=True).start()
        return task

    def _run(self, task: Task, worker: Callable[[Task, Callable], int]) -> None:
        task.state = "running"
        task.started_at = now_iso()
        self._write(task)
        self.emit(task, "state", {"state": "running"})
        try:
            rc = worker(task, lambda etype, data: self.emit(task, etype, data))
            task.exit_code = int(rc or 0)
            task.state = "done" if task.exit_code == 0 else "failed"
        except Exception as exc:  # noqa: BLE001 - surface any worker failure on the stream
            task.state = "failed"
            task.error = f"{type(exc).__name__}: {exc}"
            task.exit_code = 1
            self.emit(task, "error", {"message": task.error})
        task.ended_at = now_iso()
        self._write(task)
        self.emit(task, "state", {"state": task.state})

    def cancel(self, task_id: str) -> bool:
        task = self.get(task_id)
        if task is None or task.state in TERMINAL:
            return False
        task.cancel_flag.set()
        return True

    # ── events ───────────────────────────────────────────────────
    def emit(self, task: Task, etype: str, data: dict) -> dict:
        with self._cond:
            seq = self._seq.get(task.id, 0) + 1
            self._seq[task.id] = seq
            event = {"seq": seq, "ts": now_iso(), "task_id": task.id, "type": etype, "data": data}
            if task.dir:
                with open(task.dir / "events.jsonl", "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(event, ensure_ascii=False) + "\n")
                if etype == "log":
                    with open(task.dir / "out.log", "a", encoding="utf-8") as fh:
                        fh.write(str(data.get("text", "")) + "\n")
            self._cond.notify_all()
        return event

    def events(self, task_id: str, after: int = 0) -> list[dict]:
        task = self.get(task_id)
        path = (task.dir if task else self.root / task_id) / "events.jsonl"
        if not path.exists():
            return []
        out = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("seq", 0) > after:
                out.append(event)
        return out

    def wait_events(self, task_id: str, after: int, timeout: float = 15.0) -> list[dict]:
        with self._cond:
            if self._seq.get(task_id, 0) <= after:
                self._cond.wait(timeout=timeout)
        return self.events(task_id, after)

    # ── queries ──────────────────────────────────────────────────
    def get(self, task_id: str) -> Task | None:
        with self._lock:
            return self._tasks.get(task_id)

    def list_tasks(self, limit: int = 50) -> list[dict]:
        """Disk-first listing (CLI sees tasks from other processes) merged with memory."""
        seen: dict[str, dict] = {}
        if self.root.is_dir():
            for path in self.root.glob("*/task.json"):
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                seen[str(data.get("id", path.parent.name))] = data
        with self._lock:
            for task in self._tasks.values():
                seen[task.id] = task.public()
        ordered = sorted(seen.values(), key=lambda t: str(t.get("created_at", "")), reverse=True)
        return ordered[:limit]

    # ── persistence ──────────────────────────────────────────────
    def _write(self, task: Task) -> None:
        if not task.dir:
            return
        payload = task.public()
        tmp = task.dir / "task.json.tmp"
        tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(task.dir / "task.json")
