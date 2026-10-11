"""Local web UI for the datasets manager (127.0.0.1 only).

Routes per DSM-003 §7; config editors per §10; every mutating action goes
preview → one-shot token → atomic write + backup + audit (DSM-003 §10.1).
Dependencies: stdlib + bundled htmx (static/); no external network assets.
"""

from __future__ import annotations

import difflib
import html
import json
import re
import secrets
import sys
import threading
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import yaml

from oasis_catalog.config import ConfigError, load_config, resolve_config_path

from . import inventory as inv_mod
from . import migrate as migrate_mod
from . import reviewlog
from .confedit import atomic_write, read_with_mtime
from .probe import probe_inventory
from . import slice_export
from .storage_view import build_view, render_text
from .sync import load_storages
from .tasks import Task, TaskManager
STATIC_DIR = Path(__file__).parent / "static"
TOKEN_TTL = 600  # seconds (DSM-003 §7.2)
esc = html.escape


def _human(nbytes: int) -> str:
    value = float(nbytes)
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if value < 1000 or unit == "PB":
            return f"{value:.1f} {unit}"
        value /= 1000
    return f"{value:.1f} PB"


@dataclass
class EditSession:
    token: str
    kind: str                      # write | task
    action: str
    summary: str = ""
    diff_html: str = ""
    created: float = field(default_factory=time.time)
    expires: float = 0.0
    # write sessions
    target: str = ""
    path: Path | None = None
    new_content: str = ""
    base_mtime: float | None = None
    log_entries: list[dict] = field(default_factory=list)
    # task sessions
    task_kind: str = ""
    task_params: dict = field(default_factory=dict)

    @property
    def expired(self) -> bool:
        return time.time() > self.expires


class WebApp:
    def __init__(self, config_path: Path, tasks_root: Path | None = None):
        self.config_path = Path(config_path)
        self.inv_path = self.config_path.parent / "inventory.yaml"
        self.log_path = self.config_path.parent / reviewlog.LOG_NAME
        self.slices_dir = self.config_path.parent / "slices"
        self.tasks = TaskManager(tasks_root)
        self.edits: dict[str, EditSession] = {}
        self._lock = threading.Lock()

    # ── state loaders ───────────────────────────────────────────
    def load_config(self):
        try:
            return load_config(self.config_path), None
        except ConfigError as exc:
            return None, str(exc)

    def inventory(self) -> inv_mod.Inventory:
        return inv_mod.load_inventory(self.inv_path)

    def storage_ids(self) -> set[str]:
        ids = set(load_storages(self.config_path))
        return ids or {"macbook_ssd", "raid5_archive", "zfs_nas"}

    def validate_inventory(self, inv) -> tuple[list[str], list[str]]:
        errors, warnings = inv_mod.validate_inventory(inv, self.storage_ids())
        _, log_errors = reviewlog.validate_log(self.log_path)
        return errors + log_errors, warnings

    # ── preview: builds an EditSession (the only way to a token) ─
    def preview(self, params: dict) -> tuple[dict | None, str]:
        """Dispatch a preview request; returns (plan, html_fragment|error_text)."""
        action = str(params.get("action") or "").strip()
        if action in ("review.approve", "review.reject"):
            return self.plan_review(action.split(".", 1)[1], str(params.get("id") or ""),
                                    str(params.get("note") or ""))
        if action == "edit.inventory":
            return self.plan_edit_inventory(params)
        if action == "edit.facilities":
            return self.plan_edit_facilities(params)
        if action == "edit.slice":
            return self.plan_edit_slice(str(params.get("slice_id") or ""),
                                        str(params.get("content") or ""))
        if action == "migrate":
            return self.plan_migrate()
        if action == "probe":
            raw = params.get("ids")
            if isinstance(raw, list):
                ids = [str(i) for i in raw]
            else:
                ids = [part for part in re.split(r"[,\s]+", str(raw or "")) if part]
            try:
                timeout = float(params.get("timeout") or 10.0)
            except (TypeError, ValueError):
                return None, "timeout must be a number"
            return self.plan_probe(ids, str(params.get("channel") or "") or None, timeout)
        if action == "slice":
            raw = params.get("ids")
            if isinstance(raw, list):
                ids = [str(i) for i in raw]
            else:
                ids = [part for part in re.split(r"[,\s]+", str(raw or "")) if part]
            return self.plan_slice_run(ids, str(params.get("chunks") or "") or None)
        return None, f"unknown action '{action}'"

    def plan_slice_run(self, ids: list[str], chunks_text: str | None) -> tuple[dict | None, str]:
        if not ids:
            return None, "no slice ids given"
        specs = []
        for sid in ids:
            path = self.slices_dir / f"{sid}.yaml"
            if not path.exists():
                return None, f"slice spec not found: {sid}"
            try:
                specs.append(slice_export.load_spec(path))
            except Exception as exc:  # noqa: BLE001 - report as preview error
                return None, f"{sid}: {exc}"
        inv = self.inventory()
        inventory_ids = {d.get("id") for d in inv.datasets}
        for spec in specs:
            errors, _ = slice_export.validate_spec(spec, inventory_ids, self.storage_ids(),
                                                   str(spec.get("id")))
            if errors:
                return None, f"{spec.get('id')}: " + "; ".join(errors)
        source, err = slice_export.resolve_source(specs[0], inv)
        if source is None:
            return None, err
        for spec in specs[1:]:
            other, err2 = slice_export.resolve_source(spec, inv)
            if other is None or (other.dataset_id, other.root) != (source.dataset_id, source.root):
                return None, f"spec '{spec.get('id')}' does not share source with the group"
        for spec in specs:
            problems = slice_export.check_columns(spec, source)
            if problems:
                return None, f"{spec.get('id')}: " + "; ".join(problems)
        try:
            chunk_list = slice_export.parse_chunks(chunks_text, len(source.chunks))
        except ValueError as exc:
            return None, str(exc)
        storages = load_storages(self.config_path)
        lines = [f"slice group: {', '.join(str(s.get('id')) for s in specs)}",
                 f"source: {source.dataset_id} [{source.channel_id}] {source.root}",
                 f"chunks: {len(chunk_list) if chunk_list else len(source.chunks)}/{len(source.chunks)}"
                 + (f" (selection: {chunks_text})" if chunk_list else ""),
                 "outputs:"]
        for spec in specs:
            lines.append(f"  {spec.get('id')} -> {slice_export.output_file(spec, storages)}")
        session = self.create_token(kind="task", action="slice", task_kind="slice_run",
                                    task_params={"ids": [str(s.get("id")) for s in specs],
                                                 "chunks": chunks_text or ""},
                                    summary=f"slice export: {', '.join(str(s.get('id')) for s in specs)}")
        fragment = (f"<p><b>Plan</b></p><pre>{esc(chr(10).join(lines))}</pre>"
                    "<p><button class='primary' hx-post='/api/actions/execute' "
                    f"hx-vals='{{\"token\": \"{session.token}\"}}' hx-target='#action-result'>"
                    "Confirm export…</button> <span class='muted small'>token expires in 10 min</span></p>")
        plan = {"token": session.token, "plan": "\n".join(lines)}
        return plan, fragment

    def create_token(self, **kwargs) -> EditSession:
        if kwargs.get("kind") == "write" and kwargs.get("path") is not None \
                and "base_mtime" not in kwargs:
            kwargs["base_mtime"] = read_with_mtime(Path(kwargs["path"]))[1]
        token = secrets.token_urlsafe(24)
        session = EditSession(token=token, expires=time.time() + TOKEN_TTL, **kwargs)
        with self._lock:
            self.edits[token] = session
            if len(self.edits) > 64:
                for key in [k for k, s in self.edits.items() if s.expired][:32]:
                    self.edits.pop(key, None)
        return session

    def get_token(self, token: str) -> EditSession | None:
        with self._lock:
            session = self.edits.pop(token, None)   # one-shot
        if session is None or session.expired:
            return None
        return session

    # ── execute ─────────────────────────────────────────────────
    def execute(self, session: EditSession) -> dict:
        if session.kind == "task":
            worker = _task_workers.get(session.task_kind)
            if worker is None:
                return {"ok": False, "detail": f"no worker for task kind '{session.task_kind}'"}
            task = self.tasks.start(session.task_kind, session.task_params,
                                    worker(self))
            return {"ok": True, "task_id": task.id, "detail": f"task {task.id} started"}
        if session.kind == "write":
            path = session.path
            if path is None:
                return {"ok": False, "detail": "write session without a path"}
            _, current_mtime = read_with_mtime(path)
            if _mtime_changed(path, current_mtime, session.base_mtime):
                return {"ok": False,
                        "detail": f"{path.name} changed on disk since preview; reload and retry"}
            backup = atomic_write(path, session.new_content)
            for entry in session.log_entries:
                reviewlog.append_log(self.log_path, entry.get("action", "edit"),
                                     entry.get("target", f"config:{session.target}"),
                                     note=entry.get("note", session.summary)[:200])
            if not session.log_entries:
                reviewlog.append_log(self.log_path, "edit", f"config:{session.target}",
                                     note=session.summary[:200])
            detail = f"wrote {path}"
            if backup:
                detail += f" (backup {backup.name})"
            return {"ok": True, "detail": detail}
        return {"ok": False, "detail": f"unknown session kind '{session.kind}'"}

    # ── action planners (preview) ───────────────────────────────
    def plan_review(self, op: str, entry_id: str, note: str) -> tuple[dict | None, str]:
        inv = self.inventory()
        before = inv_mod.dump_inventory(inv)
        try:
            if op == "approve":
                inv_mod.approve(inv, entry_id)
            elif op == "reject":
                inv_mod.reject(inv, entry_id)
            else:
                return None, f"unsupported review op '{op}'"
        except KeyError as exc:
            return None, str(exc)
        after = inv_mod.dump_inventory(inv)
        session = self.create_token(kind="write", action=f"review.{op}", target="inventory",
                                    path=self.inv_path, new_content=after,
                                    summary=f"{op} proposal '{entry_id}'",
                                    diff_html=_diff_html(before, after),
                                    log_entries=[{"action": op, "target": f"dataset:{entry_id}",
                                                  "note": note or ""}])
        return {"token": session.token, "plan": f"review {op}: {entry_id}",
                "diff": _diff_text(before, after), "diff_html": session.diff_html}, self._flash_ok(session)

    def plan_edit_inventory(self, form: dict) -> tuple[dict | None, str]:
        """Assemble a dataset (or proposal) from form fields, then diff."""
        inv = self.inventory()
        before_raw = inv_mod.dump_inventory(inv)
        try:
            entry = _dataset_from_form(form)
        except ValueError as exc:
            return None, str(exc)
        mode = form.get("mode", "edit")
        edit_id = (form.get("edit_id") or "").strip()
        errors, warnings = inv_mod.validate_entry(entry, "dataset", self.storage_ids(),
                                                  f"dataset '{entry.get('id')}'")
        if mode == "propose":
            if not (form.get("reason") or "").strip():
                errors.append("proposal: reason required")
            known = {d.get("id") for d in inv.datasets} | {p.get("id") for p in inv.proposals}
            if entry.get("id") in known:
                errors.append(f"proposal id '{entry.get('id')}' already exists (V-06)")
            if errors:
                return None, "; ".join(errors)
            entry["proposed_at"] = inv_mod.now_iso()
            entry["proposed_by"] = "owner"
            entry["reason"] = form.get("reason", "")
            inv.proposals.append(entry)
            summary = f"propose '{entry.get('id')}'"
        else:
            if not any(d.get("id") == edit_id for d in inv.datasets):
                return None, f"dataset '{edit_id}' not found"
            if entry.get("id") != edit_id:
                if any(d.get("id") == entry.get("id") for d in inv.datasets):
                    errors.append(f"dataset id '{entry.get('id')}' already exists (V-01)")
            if errors:
                return None, "; ".join(errors)
            for i, item in enumerate(inv.datasets):
                if item.get("id") == edit_id:
                    merged = dict(item)
                    merged.update(entry)
                    inv.datasets[i] = merged
                    break
            summary = f"edit dataset '{entry.get('id')}'"
        after_raw = inv_mod.dump_inventory(inv)
        session = self.create_token(kind="write", action="edit", target="inventory",
                                    path=self.inv_path, new_content=after_raw, summary=summary,
                                    diff_html=_diff_html(before_raw, after_raw))
        plan = {"token": session.token, "plan": summary,
                "diff": _diff_text(before_raw, after_raw), "diff_html": session.diff_html}
        if warnings:
            plan["warnings"] = warnings
        return plan, self._flash_ok(session)

    def plan_edit_facilities(self, form: dict) -> tuple[dict | None, str]:
        storages, nodes, errors = _facilities_from_form(form)
        known_nodes = {n["id"] for n in nodes}
        seen = set()
        for s in storages:
            if s["id"] in seen:
                errors.append(f"duplicate storage id '{s['id']}'")
            seen.add(s["id"])
            node = s.get("node")
            if node and node not in known_nodes:
                errors.append(f"storage '{s['id']}': unknown node '{node}'")
            access = s.get("access") or {}
            protos = access.get("protocols") or ([access["protocol"]] if access.get("protocol") else [])
            if not protos:
                errors.append(f"storage '{s['id']}': protocol required")
            if "file" in protos and not access.get("path") and s.get("class") != "portable":
                errors.append(f"storage '{s['id']}': file access requires path")
            if any(p in ("smb", "ssh", "ssh+rsync") for p in protos) and not access.get("host"):
                errors.append(f"storage '{s['id']}': {','.join(protos)} access requires host")
        if errors:
            return None, "; ".join(errors)
        old_text = read_with_mtime(self.config_path)[0] or ""
        try:
            new_text = _splice_sections(old_text,
                                        {"storages": _yaml_block("storages", storages),
                                         "nodes": _yaml_block("nodes", nodes)})
        except ValueError as exc:
            return None, str(exc)
        # paranoia: the spliced file must still load
        try:
            yaml.safe_load(new_text)
        except yaml.YAMLError as exc:
            return None, f"spliced YAML invalid: {exc}"
        session = self.create_token(kind="write", action="edit", target="facilities",
                                    path=self.config_path, new_content=new_text,
                                    summary=f"edit facilities ({len(storages)} storages, {len(nodes)} nodes)",
                                    diff_html=_diff_html(old_text, new_text))
        plan = {"token": session.token, "plan": session.summary,
                "diff": _diff_text(old_text, new_text), "diff_html": session.diff_html}
        return plan, self._flash_ok(session)

    def plan_edit_slice(self, slice_id: str, content: str) -> tuple[dict | None, str]:
        slice_id = slice_id.strip()
        if not inv_mod.ID_RE.match(slice_id):
            return None, "slice id must match [a-z0-9_]+"
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as exc:
            return None, f"YAML invalid: {exc}"
        errors = []
        if not isinstance(data, dict):
            errors.append("slice spec must be a mapping")
        else:
            if data.get("id") != slice_id:
                errors.append(f"spec id '{data.get('id')}' must equal file id '{slice_id}'")
            source = data.get("source")
            if source and source not in {d.get("id") for d in self.inventory().datasets}:
                errors.append(f"source '{source}' not in inventory")
            output = data.get("output") or {}
            storage = output.get("storage")
            if storage and storage not in self.storage_ids():
                errors.append(f"output.storage '{storage}' not registered")
        if errors:
            return None, "; ".join(errors)
        path = self.slices_dir / f"{slice_id}.yaml"
        before = read_with_mtime(path)[0] or ""
        session = self.create_token(kind="write", action="edit", target=f"slices/{slice_id}",
                                    path=path, new_content=content if content.endswith("\n") else content + "\n",
                                    summary=f"edit slice '{slice_id}'",
                                    diff_html=_diff_html(before, content))
        plan = {"token": session.token, "plan": session.summary,
                "diff": _diff_text(before, content), "diff_html": session.diff_html}
        return plan, self._flash_ok(session)

    def plan_migrate(self) -> tuple[dict | None, str]:
        cfg, err = self.load_config()
        if err:
            return None, err
        if not cfg.datasets:
            return None, "nothing to migrate (legacy config.datasets is empty)"
        if self.inv_path.exists():
            return None, f"inventory already exists: {self.inv_path}"
        payload, logs = migrate_mod.build_inventory(cfg, self.storage_ids())
        inv = inv_mod.Inventory(path=self.inv_path, version=payload["inventory_version"],
                                datasets=payload["datasets"], proposals=payload["proposals"])
        errors, _ = inv_mod.validate_inventory(inv, self.storage_ids())
        if errors:
            return None, "; ".join(errors)
        content = inv_mod.dump_inventory(inv)
        session = self.create_token(kind="write", action="migrate", target="inventory",
                                    path=self.inv_path, new_content=content,
                                    summary=f"migrate {len(inv.datasets)} datasets to inventory.yaml",
                                    log_entries=list(logs))
        plan = {"token": session.token, "plan": session.summary,
                "diff": _diff_text("", content), "diff_html": _diff_html("", content)}
        return plan, self._flash_ok(session)

    def plan_probe(self, ids: list[str], channel: str | None, timeout: float) -> tuple[dict | None, str]:
        inv = self.inventory()
        known = {d.get("id") for d in inv.datasets}
        unknown = [i for i in ids if i not in known]
        if unknown:
            return None, f"unknown dataset id(s): {', '.join(unknown)}"
        targets = ids or sorted(known)
        session = self.create_token(kind="task", action="probe", task_kind="probe",
                                    task_params={"ids": targets, "channel": channel, "timeout": timeout},
                                    summary=f"probe {len(targets)} dataset(s)" +
                                            (f" channel={channel}" if channel else ""))
        return {"token": session.token, "plan": session.summary}, self._flash_ok(session)

    def _flash_ok(self, session: EditSession) -> str:
        plan = f"<p><b>Plan:</b> {esc(session.summary)}</p>"
        if session.diff_html:
            plan += session.diff_html
        plan += ("<p><button class='primary' hx-post='/api/actions/execute' "
                 f"hx-vals='{{\"token\": \"{session.token}\"}}' hx-target='#action-result'>"
                 "Confirm</button> <span class='muted small'>token expires in 10 min</span></p>")
        return plan

# ── form / yaml helpers ─────────────────────────────────────────
def _flash(kind: str, text: str) -> str:
    return f"<div class='flash {kind}'>{esc(text)}</div>"


def _mtime_changed(path: Path, current: float | None, recorded: float | None) -> bool:
    if recorded is None:
        return current is not None
    if current is None:
        return True
    return abs(current - recorded) > 1e-6


def _diff_text(before: str, after: str) -> str:
    return "".join(difflib.unified_diff(before.splitlines(keepends=True),
                                        after.splitlines(keepends=True), "before", "after"))


def _diff_html(before: str, after: str, max_lines: int = 400) -> str:
    if before == after:
        return "<p class='muted'>no changes</p>"
    lines = list(difflib.unified_diff(before.splitlines(), after.splitlines(),
                                      "before", "after", lineterm=""))
    body = "\n".join(esc(line) for line in lines[:max_lines])
    if len(lines) > max_lines:
        body += "\n... (truncated)"
    return f"<pre>{body}</pre>"


def _yaml_block(key: str, items: list[dict]) -> str:
    return yaml.safe_dump({key: items}, allow_unicode=True, sort_keys=False)


def _splice_sections(text: str, sections: dict[str, str]) -> str:
    """Replace top-level `key:` blocks in YAML text; trailing comments are kept."""
    lines = text.splitlines(keepends=True)
    for key, block in sections.items():
        start = None
        for i, line in enumerate(lines):
            if re.match(rf"^{re.escape(key)}:\s*(#.*)?$", line):
                start = i
                break
        if start is None:
            raise ValueError(f"section '{key}:' not found in file")
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if re.match(r"^[A-Za-z_][\w-]*:", lines[j]):
                end = j
                break
        tail = end
        while tail > start + 1 and (lines[tail - 1].strip() == "" or lines[tail - 1].lstrip().startswith("#")):
            tail -= 1
        new_block = block.rstrip("\n") + "\n\n"
        lines[start:tail] = [new_block]
    return "".join(lines)


def _dataset_from_form(form: dict) -> dict:
    ds_id = str(form.get("ds_id") or "").strip()
    if not ds_id:
        raise ValueError("dataset id required")
    entry: dict = {
        "id": ds_id,
        "title": str(form.get("ds_title") or "").strip(),
        "publisher": str(form.get("ds_publisher") or "").strip(),
        "licence": {"name": str(form.get("lic_name") or "").strip(),
                    "url": str(form.get("lic_url") or "").strip()},
    }
    status = str(form.get("ds_status") or "").strip()
    if status:
        entry["status"] = status
    fmt: dict = {}
    for key, fname in (("type", "fmt_type"), ("files", "fmt_files"), ("size_hint", "fmt_size_hint")):
        val = str(form.get(fname) or "").strip()
        if val:
            if key == "files":
                try:
                    val = int(val)
                except ValueError as exc:
                    raise ValueError("fmt.files must be an integer") from exc
            fmt[key] = val
    if fmt:
        entry["fmt"] = fmt
    notes = str(form.get("ds_notes") or "").strip()
    if notes:
        entry["notes"] = notes
    entry["storage_pref"] = sorted(k[len("pref_"):] for k, v in form.items()
                                   if k.startswith("pref_") and v)
    channels_raw = str(form.get("channels_yaml") or "")
    try:
        channels = yaml.safe_load(channels_raw) if channels_raw.strip() else []
    except yaml.YAMLError as exc:
        raise ValueError(f"channels YAML invalid: {exc}") from exc
    if not isinstance(channels, list):
        raise ValueError("channels must be a YAML list")
    entry["channels"] = channels
    return entry


def _facilities_from_form(form: dict) -> tuple[list[dict], list[dict], list[str]]:
    errors: list[str] = []
    storages: list[dict] = []
    nodes: list[dict] = []

    def rows(prefix: str, count_key: str) -> int:
        raw = form.get(count_key)
        try:
            return max(0, min(64, int(str(raw or 0))))
        except ValueError:
            return 0

    for i in range(rows("s", "storage_rows")):
        sid = str(form.get(f"s_{i}_id") or "").strip()
        if not sid:
            continue
        if not re.match(r"^[a-z0-9_]+$", sid):
            errors.append(f"storage id '{sid}' must match [a-z0-9_]+")
        protocols = [p.strip() for p in str(form.get(f"s_{i}_protocols") or "").split(",") if p.strip()]
        access: dict = {}
        if len(protocols) == 1:
            access["protocol"] = protocols[0]
        elif protocols:
            access["protocols"] = protocols
        else:
            errors.append(f"storage '{sid}': protocol required")
        host = str(form.get(f"s_{i}_host") or "").strip()
        path = str(form.get(f"s_{i}_path") or "").strip()
        if host:
            access["host"] = host
        if path:
            access["path"] = path
        extra_raw = str(form.get(f"s_{i}_extra") or "").strip()
        if extra_raw:
            try:
                extra = json.loads(extra_raw)
                if isinstance(extra, dict):
                    access.update({k: v for k, v in extra.items() if k not in access})
            except json.JSONDecodeError:
                errors.append(f"storage '{sid}': bad extra payload")
        item: dict = {"id": sid}
        for key, fname in (("class", f"s_{i}_class"), ("node", f"s_{i}_node")):
            val = str(form.get(fname) or "").strip()
            if val:
                item[key] = val
        item["access"] = access
        for key, fname in (("io", f"s_{i}_io"), ("role", f"s_{i}_role"), ("notes", f"s_{i}_notes")):
            val = str(form.get(fname) or "").strip()
            if val:
                item[key] = val
        storages.append(item)

    for i in range(rows("n", "node_rows")):
        nid = str(form.get(f"n_{i}_id") or "").strip()
        if not nid:
            continue
        item = {"id": nid}
        for key, fname in (("title", f"n_{i}_title"), ("role", f"n_{i}_role")):
            val = str(form.get(fname) or "").strip()
            if val:
                item[key] = val
        protocol = str(form.get(f"n_{i}_protocol") or "").strip()
        alias = str(form.get(f"n_{i}_alias") or "").strip()
        access = {"protocol": protocol} if protocol else {}
        if alias:
            access["alias"] = alias
        item["access"] = access
        nodes.append(item)
    return storages, nodes, errors


# ── pages ───────────────────────────────────────────────────────
NAV = [("/", "overview"), ("/inventory", "inventory"), ("/storages", "storages"),
       ("/config/inventory", "edit inventory"), ("/config/facilities", "edit facilities"),
       ("/config/slices", "edit slices"), ("/tasks", "tasks"), ("/logs", "audit")]


def _shell(title: str, active: str, body: str, extra_js: str = "") -> str:
    nav = " ".join(f"<a href='{href}' class='{'active' if href == active else ''}'>{esc(label)}</a>"
                   for href, label in NAV)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>oasis-datasets · {esc(title)}</title>
<link rel="stylesheet" href="/static/app.css">
<script src="/static/htmx.min.js"></script>
</head><body>
<header><h1>oasis-datasets</h1><nav>{nav}</nav></header>
<main>
<div id="action-result"></div>
{body}
</main>
{extra_js}
</body></html>"""


def _storages_table(view: dict) -> str:
    rows = []
    for row in view["storages"]:
        cap = (f"free {_human(row['capacity']['free'])} / {_human(row['capacity']['total'])}"
               if row["capacity"] else "")
        where = row["mount"] or row["path"] or row["detail"]
        rows.append(f"<tr><td class='mono'>{esc(row['id'])}</td><td>{esc(row['state'])}</td>"
                    f"<td class='mono small'>{esc(where)}</td><td class='small'>{esc(cap)}</td></tr>")
    return ("<table><tr><th>id</th><th>state</th><th>path</th><th>capacity</th></tr>"
            + "".join(rows) + "</table>")


def render_overview(app: WebApp) -> str:
    cfg, cfg_err = app.load_config()
    inv = app.inventory()
    view = build_view(load_storages(app.config_path))
    parts = [f"<h2>Overview</h2>",
             f"<p class='small muted'>config: <span class='mono'>{esc(str(app.config_path))}</span>"
             + (f" — <span class='err'>{esc(cfg_err)}</span>" if cfg_err else " <span class='ok'>(ok)</span>")
             + "</p>"]
    if cfg and cfg.datasets and not inv.datasets:
        parts.append(_flash("warn",
                            f"legacy config.datasets present ({len(cfg.datasets)} datasets) and inventory.yaml "
                            "is empty.") +
                     "<form hx-post='/api/actions/preview' hx-target='#action-result'>"
                     "<input type='hidden' name='action' value='migrate'>"
                     "<button class='primary'>Preview migration</button></form>")
    elif cfg and cfg.datasets:
        parts.append(_flash("warn", f"legacy config.datasets still present ({len(cfg.datasets)} datasets); "
                                    "inventory.yaml is authoritative for list/verify/sync."))
    active = [d for d in inv.datasets if d.get("status", "active") == "active"]
    parts.append(f"<p>inventory: <b>{len(inv.datasets)}</b> datasets "
                 f"({len(active)} active), <b>{len(inv.proposals)}</b> proposals "
                 f"<a class='small' href='/inventory'>[open]</a></p>")
    parts.append("<h2>Storages</h2>" + _storages_table(view))
    log = reviewlog.read_log(app.log_path, tail=5)
    parts.append("<h2>Recent audit</h2>")
    if log:
        parts.append("<table><tr><th>ts</th><th>action</th><th>target</th><th>note</th></tr>" +
                     "".join(f"<tr><td class='mono small'>{esc(str(e.get('ts','')))}</td>"
                             f"<td>{esc(str(e.get('action','')))}</td>"
                             f"<td class='mono small'>{esc(str(e.get('target','')))}</td>"
                             f"<td class='small'>{esc(str(e.get('note','')))}</td></tr>" for e in log) +
                     "</table>")
    else:
        parts.append("<p class='muted'>no audit entries yet</p>")
    tasks = app.tasks.list_tasks(limit=5)
    parts.append("<h2>Recent tasks</h2>")
    if tasks:
        parts.append(_tasks_table(tasks))
    else:
        parts.append("<p class='muted'>no tasks yet</p>")
    return "\n".join(parts)


def _tasks_table(tasks: list[dict]) -> str:
    rows = []
    for t in tasks:
        badge = "ok" if t["state"] == "done" else ("err" if t["state"] == "failed" else "warn")
        rows.append(f"<tr><td class='mono'><a href='/tasks/{esc(t['id'])}'>{esc(t['id'])}</a></td>"
                    f"<td>{esc(t['kind'])}</td><td class='{badge}'>{esc(t['state'])}</td>"
                    f"<td class='mono small'>{esc(str(t.get('created_at','')))}</td>"
                    f"<td class='small'>{esc(str(t.get('detail') or t.get('error') or ''))}</td></tr>")
    return ("<table><tr><th>id</th><th>kind</th><th>state</th><th>created</th><th>detail</th></tr>"
            + "".join(rows) + "</table>")


def render_inventory(app: WebApp) -> str:
    inv = app.inventory()
    errors, warnings = app.validate_inventory(inv)
    parts = [f"<h2>Inventory</h2><p class='small muted mono'>{esc(str(app.inv_path))}</p>"]
    if errors:
        parts.append(_flash("err", "; ".join(errors)))
    for warning in warnings:
        parts.append(_flash("warn", warning))
    rows = []
    for ds in inv.datasets:
        channels = ds.get("channels") or []
        chan = "<br>".join(f"<span class='mono small'>{esc(str(ch.get('id')))} · "
                           f"{esc(str(ch.get('protocol')))}</span>"
                           f"<span class='muted small'> {esc(str(ch.get('path') or ch.get('url') or ch.get('host') or ''))}</span>"
                           for ch in channels)
        rows.append(f"<tr><td class='mono'>{esc(str(ds.get('id','')))}</td>"
                    f"<td>{esc(str(ds.get('title','')))}</td>"
                    f"<td class='small'>{esc(str(ds.get('publisher','')))}</td>"
                    f"<td>{esc(str(ds.get('status','active')))}</td>"
                    f"<td class='small'>{esc(', '.join(ds.get('storage_pref') or []))}</td>"
                    f"<td class='small'>{chan}</td>"
                    f"<td><a class='btn small' href='/config/inventory?edit={esc(str(ds.get('id','')))}'>edit</a></td></tr>")
    parts.append("<table><tr><th>id</th><th>title</th><th>publisher</th><th>status</th>"
                 "<th>storage_pref</th><th>channels</th><th></th></tr>" + "".join(rows) + "</table>")
    if inv.proposals:
        parts.append("<h2>Proposals (review inbox)</h2>")
        rows = []
        for p in inv.proposals:
            pid = esc(str(p.get("id", "")))
            rows.append(f"<tr><td class='mono'>{pid}</td><td>{esc(str(p.get('title','')))}</td>"
                        f"<td class='small'>{esc(str(p.get('reason','')))}</td><td>"
                        f"<form class='inline' hx-post='/api/actions/preview' hx-target='#action-result'>"
                        f"<input type='hidden' name='action' value='review.approve'>"
                        f"<input type='hidden' name='id' value='{pid}'>"
                        f"<input type='text' name='note' placeholder='note' style='width:140px'> "
                        f"<button class='primary'>approve…</button></form> "
                        f"<form class='inline' hx-post='/api/actions/preview' hx-target='#action-result'>"
                        f"<input type='hidden' name='action' value='review.reject'>"
                        f"<input type='hidden' name='id' value='{pid}'>"
                        f"<input type='text' name='note' placeholder='reason' style='width:140px'> "
                        f"<button class='danger'>reject…</button></form></td></tr>")
        parts.append("<table><tr><th>id</th><th>title</th><th>reason</th><th>review</th></tr>"
                     + "".join(rows) + "</table>")
    return "\n".join(parts)


def render_storages(app: WebApp) -> str:
    storages = load_storages(app.config_path)
    view = build_view(storages)
    parts = ["<h2>Storages & file system</h2>",
             f"<pre>{esc(render_text(view))}</pre>",
             _storages_table(view)]
    unregistered = view["volumes"]["unregistered_mounted"]
    if unregistered:
        parts.append("<h2>Unregistered volumes</h2><table>"
                     "<tr><th>volume</th><th>mount</th><th></th></tr>" +
                     "".join(f"<tr><td>{esc(v['name'])}</td><td class='mono small'>{esc(v['mount'])}</td>"
                             f"<td><a class='btn small' href='/config/facilities?register="
                             f"{urllib.parse.quote(str(v['mount']))}'>register as storage…</a></td></tr>"
                             for v in unregistered) + "</table>")
    return "\n".join(parts)


def render_logs(app: WebApp) -> str:
    entries = reviewlog.read_log(app.log_path)
    count, errors = reviewlog.validate_log(app.log_path)
    parts = [f"<h2>Audit log</h2><p class='small muted mono'>{esc(str(app.log_path))} "
             f"({count} entries, {len(errors)} error(s))</p>"]
    for error in errors:
        parts.append(_flash("err", error))
    rows = []
    for e in entries[-200:]:
        rows.append(f"<tr><td class='mono small'>{esc(str(e.get('ts','')))}</td>"
                    f"<td>{esc(str(e.get('action','')))}</td>"
                    f"<td class='mono small'>{esc(str(e.get('target','')))}</td>"
                    f"<td class='small'>{esc(str(e.get('by','')))}</td>"
                    f"<td class='small'>{esc(str(e.get('note','')))}</td></tr>")
    parts.append("<table><tr><th>ts</th><th>action</th><th>target</th><th>by</th><th>note</th></tr>"
                 + "".join(rows) + "</table>")
    return "\n".join(parts)


def render_tasks(app: WebApp) -> str:
    tasks = app.tasks.list_tasks()
    parts = ["<h2>Tasks</h2>"]
    parts.append(_tasks_table(tasks) if tasks else "<p class='muted'>no tasks yet</p>")
    parts.append("<h3>Start a probe task</h3>"
                 "<form hx-post='/api/actions/preview' hx-target='#action-result'>"
                 "<input type='hidden' name='action' value='probe'>"
                 "<label>dataset ids (comma/space separated; empty = all)</label>"
                 "<input type='text' name='ids' placeholder='gaia_gdr3_gaia_source, mpcorb'>"
                 "<label>channel id (optional)</label>"
                 "<input type='text' name='channel' placeholder='local'>"
                 "<p><button class='primary'>Preview probe…</button></p></form>")
    return "\n".join(parts)


def render_task(app: WebApp, task_id: str) -> str:
    task = app.tasks.get(task_id)
    params = task.public() if task else {"id": task_id, "state": "not in this process (see task.json)"}
    task_dir = (task.dir if task else app.tasks.root / task_id)
    parts = [f"<h2>Task <span class='mono'>{esc(task_id)}</span></h2>",
             f"<pre>{esc(json.dumps(params, indent=2, ensure_ascii=False))}</pre>",
             f"<p class='small muted mono'>dir: {esc(str(task_dir))}</p>",
             "<h3>events</h3><div id='events' class='mono small'></div>",
             f"""<script>
const src = new EventSource("/api/events/{esc(task_id)}");
const el = () => document.getElementById('events');
src.onmessage = e => {{
  const d = JSON.parse(e.data);
  el().textContent += `[${{d.seq}}] ${{d.ts}} ${{d.type}} ${{JSON.stringify(d.data)}}\\n`;
  if (d.type === 'state' && ['done','failed','cancelled'].includes(d.data.state)) src.close();
}};
</script>"""]
    return "\n".join(parts)

# ── config editors ──────────────────────────────────────────────
def _dataset_form(app: WebApp, ds: dict, edit_id: str | None) -> str:
    lic = ds.get("licence") or {}
    fmt = ds.get("fmt") or {}
    prefs = set(ds.get("storage_pref") or [])
    channel_text = yaml.safe_dump(ds.get("channels") or [], allow_unicode=True, sort_keys=False) \
        if ds.get("channels") else "- {id: primary, protocol: https, url: 'https://…', version_rule: {type: last_modified}}\n"
    checks = "".join(
        f"<label class='small'><input type='checkbox' name='pref_{esc(sid)}' "
        f"{'checked' if sid in prefs else ''}> {esc(sid)}</label>"
        for sid in sorted(app.storage_ids()))
    mode = "edit" if edit_id else "propose"
    reason_block = "" if edit_id else (
        "<label>reason (required for proposals)</label>"
        "<input type='text' name='reason' placeholder='why this dataset is needed'>")
    return f"""
<h2>{'Edit dataset' if edit_id else 'New dataset (proposal)'}</h2>
<form hx-post="/api/actions/preview" hx-target="#action-result">
<input type="hidden" name="action" value="edit.inventory">
<input type="hidden" name="mode" value="{mode}">
<input type="hidden" name="edit_id" value="{esc(edit_id or '')}">
<div class="grid">
  <div><label>id</label><input type="text" name="ds_id" value="{esc(str(ds.get('id','')))}"
       {'readonly' if edit_id else ''}></div>
  <div><label>title</label><input type="text" name="ds_title" value="{esc(str(ds.get('title','')))}"></div>
  <div><label>publisher</label><input type="text" name="ds_publisher" value="{esc(str(ds.get('publisher','')))}"></div>
  <div><label>status</label><select name="ds_status">
      <option value="active" {'selected' if ds.get('status','active')=='active' else ''}>active</option>
      <option value="deprecated" {'selected' if ds.get('status')=='deprecated' else ''}>deprecated</option>
  </select></div>
  <div><label>licence.name</label><input type="text" name="lic_name" value="{esc(str(lic.get('name','')))}"></div>
  <div><label>licence.url</label><input type="text" name="lic_url" value="{esc(str(lic.get('url','')))}"></div>
  <div><label>fmt.type</label><input type="text" name="fmt_type" value="{esc(str(fmt.get('type','')))}"></div>
  <div><label>fmt.files</label><input type="number" name="fmt_files" value="{esc(str(fmt.get('files','')))}"></div>
  <div><label>fmt.size_hint</label><input type="text" name="fmt_size_hint" value="{esc(str(fmt.get('size_hint','')))}"></div>
  <div><label>notes</label><input type="text" name="ds_notes" value="{esc(str(ds.get('notes','')))}"></div>
  <div class="full"><label>storage_pref</label>{checks}</div>
  <div class="full"><label>channels (YAML list; protocol fields: file.path / https.url / ssh.host+path)</label>
    <textarea class="yaml" name="channels_yaml">{esc(channel_text)}</textarea></div>
  <div class="full">{reason_block}</div>
</div>
<p><button class="primary">Preview {'changes' if edit_id else 'proposal'}…</button>
   <a class="btn" href="/config/inventory">cancel</a></p>
</form>"""


def render_config_inventory(app: WebApp, query: dict) -> str:
    inv = app.inventory()
    edit_id = (query.get("edit") or [None])[0]
    is_new = "new" in query
    parts = ["<h2>Inventory editor</h2>",
             "<p class='small muted'>Changes go through preview → confirm; writes are atomic with backup + audit.</p>"]
    rows = []
    for ds in inv.datasets:
        rows.append(f"<tr><td class='mono'>{esc(str(ds.get('id','')))}</td>"
                    f"<td>{esc(str(ds.get('title','')))}</td>"
                    f"<td><a class='btn small' href='/config/inventory?edit={esc(str(ds.get('id','')))}'>edit</a></td></tr>")
    parts.append("<table><tr><th>id</th><th>title</th><th></th></tr>" + "".join(rows) + "</table>")
    parts.append("<p><a class='btn' href='/config/inventory?new=1'>+ new dataset (proposal)</a> "
                 "<a class='btn' href='/inventory'>review inbox →</a></p>")
    if edit_id:
        ds = next((d for d in inv.datasets if d.get("id") == edit_id), None)
        if ds is None:
            parts.append(_flash("err", f"dataset '{edit_id}' not found"))
        else:
            parts.append(_dataset_form(app, ds, edit_id))
    elif is_new:
        parts.append(_dataset_form(app, {}, None))
    return "\n".join(parts)


def render_config_facilities(app: WebApp, query: dict) -> str:
    raw_text = read_with_mtime(app.config_path)[0] or ""
    try:
        raw = yaml.safe_load(raw_text) or {}
    except yaml.YAMLError as exc:
        return _flash("err", f"config.yaml invalid: {exc}")
    storages = list(raw.get("storages") or [])
    nodes = list(raw.get("nodes") or [])
    node_ids = [str(n.get("id", "")) for n in nodes]

    prefill = (query.get("register") or [None])[0]
    template: dict | None = None
    if prefill:
        name = Path(prefill).name.lower().replace(" ", "_").replace("-", "_")
        name = re.sub(r"[^a-z0-9_]", "", name) or "new_storage"
        template = {"id": name, "class": "archive",
                    "access": {"protocol": "file", "path": prefill}}

    def storage_row(i: int, s: dict) -> str:
        access = s.get("access") or {}
        protocols = ",".join(access.get("protocols") or ([access["protocol"]] if access.get("protocol") else []))
        extra = {k: v for k, v in access.items()
                 if k not in ("protocol", "protocols", "host", "path")}
        classes = ("hot", "scratch", "archive", "shared", "portable")
        class_opts = "".join(f"<option value='{c}' {'selected' if s.get('class')==c else ''}>{c}</option>"
                             for c in classes)
        node_opts = "<option value=''></option>" + "".join(
            f"<option value='{esc(n)}' {'selected' if s.get('node')==n else ''}>{esc(n)}</option>"
            for n in node_ids)
        return f"""<tr>
<td><input type="text" name="s_{i}_id" value="{esc(str(s.get('id','')))}" style="width:120px"></td>
<td><select name="s_{i}_class">{class_opts}</select></td>
<td><select name="s_{i}_node">{node_opts}</select></td>
<td><input type="text" name="s_{i}_protocols" value="{esc(protocols)}" style="width:110px"></td>
<td><input type="text" name="s_{i}_host" value="{esc(str(access.get('host','')))}" style="width:110px"></td>
<td><input type="text" name="s_{i}_path" value="{esc(str(access.get('path','')))}"></td>
<td><input type="text" name="s_{i}_io" value="{esc(str(s.get('io','')))}"></td>
<td><input type="text" name="s_{i}_role" value="{esc(str(s.get('role','')))}"></td>
<td><input type="text" name="s_{i}_notes" value="{esc(str(s.get('notes','')))}"></td>
<input type="hidden" name="s_{i}_extra" value="{esc(json.dumps(extra, ensure_ascii=False))}">
</tr>"""

    rows = [storage_row(i, s) for i, s in enumerate(storages)]
    if template:
        rows.append(storage_row(len(storages), template))
    else:
        rows.append(storage_row(len(storages), {}))
    parts = ["<h2>Facilities editor (storages & nodes)</h2>",
             "<p class='small muted'>One blank row is kept for adding a new storage; empty id rows are ignored.</p>",
             f"<form hx-post='/api/actions/preview' hx-target='#action-result'>",
             "<input type='hidden' name='action' value='edit.facilities'>",
             f"<input type='hidden' name='storage_rows' value='{len(rows)}'>",
             "<table><tr><th>id</th><th>class</th><th>node</th><th>protocol(s)</th><th>host</th>"
             "<th>path</th><th>io</th><th>role</th><th>notes</th></tr>",
             "".join(rows), "</table>"]
    node_rows = []
    for i, n in enumerate(nodes + [{}]):
        access = n.get("access") or {}
        node_rows.append(f"""<tr>
<td><input type="text" name="n_{i}_id" value="{esc(str(n.get('id','')))}" style="width:120px"></td>
<td><input type="text" name="n_{i}_title" value="{esc(str(n.get('title','')))}"></td>
<td><input type="text" name="n_{i}_role" value="{esc(str(n.get('role','')))}"></td>
<td><input type="text" name="n_{i}_protocol" value="{esc(str(access.get('protocol','')))}" style="width:90px"></td>
<td><input type="text" name="n_{i}_alias" value="{esc(str(access.get('alias','')))}" style="width:110px"></td>
</tr>""")
    parts.append(f"<h3>Nodes</h3><input type='hidden' name='node_rows' value='{len(node_rows)}'>"
                 "<table><tr><th>id</th><th>title</th><th>role</th><th>protocol</th><th>alias</th></tr>"
                 + "".join(node_rows) + "</table>")
    parts.append("<p><button class='primary'>Preview changes…</button></p></form>")
    parts.append(f"<details><summary>current config.yaml</summary><pre>{esc(raw_text)}</pre></details>")
    return "\n".join(parts)


def render_config_slices(app: WebApp, query: dict) -> str:
    edit_id = (query.get("edit") or [None])[0]
    is_new = "new" in query
    app.slices_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(app.slices_dir.glob("*.yaml"))
    parts = ["<h2>Slice editor</h2>",
             "<p class='small muted'>Specs live in slices/&lt;id&gt;.yaml; exports land in M3.</p>"]
    if files:
        rows = []
        for p in files:
            rows.append(f"<tr><td class='mono'>{esc(p.stem)}</td>"
                        f"<td><a class='btn small' href='/config/slices?edit={esc(p.stem)}'>edit</a></td>"
                        f"<td><form class='inline' hx-post='/api/actions/preview' hx-target='#action-result'>"
                        f"<input type='hidden' name='action' value='slice'>"
                        f"<input type='hidden' name='ids' value='{esc(p.stem)}'>"
                        f"<button>plan…</button></form></td></tr>")
        parts.append("<table><tr><th>id</th><th></th><th></th></tr>" + "".join(rows) + "</table>")
    else:
        parts.append("<p class='muted'>no slice specs yet</p>")
    parts.append("<p><a class='btn' href='/config/slices?new=1'>+ new slice</a></p>")
    parts.append("""
<h3>Run group (specs sharing a source scan once)</h3>
<form hx-post="/api/actions/preview" hx-target="#action-result">
<input type="hidden" name="action" value="slice">
<label>slice ids (comma separated)</label>
<input type="text" name="ids" value="gaia_t1, gaia_t2, gaia_t3">
<label>chunks (optional; e.g. 0-99 for a partial test run)</label>
<input type="text" name="chunks" value="">
<p><button class="primary">Plan export…</button>
   <span class="muted small">preview → confirm starts a background task (watch it on the tasks page)</span></p>
</form>""")
    if edit_id or is_new:
        slice_id = edit_id or ""
        if edit_id:
            path = app.slices_dir / f"{edit_id}.yaml"
            content = read_with_mtime(path)[0] or ""
        else:
            content = ("id: gaia_t1\nsource: gaia_gdr3_gaia_source\n"
                       "select:\n  - {column: source_id, op: in_range, value: [0, 1000]}\n"
                       "output: {storage: raid0_scratch, path: catalogs/gaia/t1, filename: gaia_t1.csv.gz}\n")
        parts.append(f"""
<form hx-post="/api/actions/preview" hx-target="#action-result">
<input type="hidden" name="action" value="edit.slice">
<label>slice id (filename)</label>
<input type="text" name="slice_id" value="{esc(slice_id)}" {'readonly' if edit_id else ''}>
<label>spec (YAML)</label>
<textarea class="yaml" name="content">{esc(content)}</textarea>
<p><button class="primary">Preview save…</button></p>
</form>""")
    return "\n".join(parts)


# ── task workers ────────────────────────────────────────────────
def _probe_worker(app: WebApp):
    def worker(task: Task, emit) -> int:
        params = task.params
        inv = app.inventory()
        ids = list(params.get("ids") or [])
        rc = 0
        for ds_id, results in probe_inventory(inv.datasets, ids,
                                              channel_id=params.get("channel"),
                                              timeout=float(params.get("timeout") or 10.0)):
            emit("log", {"text": f"== {ds_id}"})
            for res in results:
                line = f"   {res.channel_id} [{res.protocol}] {res.state.upper()}"
                if res.version:
                    line += f" version: {res.version}"
                if res.detail:
                    line += f" ({res.detail})"
                emit("log", {"text": line})
                if res.state == "fail":
                    rc = 1
        emit("progress", {"done": len(ids), "total": len(ids)})
        return rc
    return worker


_task_workers = {"probe": _probe_worker}


def _slice_worker(app: WebApp):
    def worker(task: Task, emit) -> int:
        params = task.params
        specs = [slice_export.load_spec(app.slices_dir / f"{sid}.yaml")
                 for sid in params.get("ids") or []]
        inv = app.inventory()
        storages = load_storages(app.config_path)
        return slice_export.run_slices(specs, inv, storages, task.dir, emit,
                                       chunk_text=params.get("chunks") or None)
    return worker


_task_workers["slice_run"] = _slice_worker


# ── HTTP layer ──────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    app: WebApp
    server_version = "oasis-datasets-web/0.2"

    # -- plumbing ------------------------------------------------
    def _send(self, code: int, body: str | bytes, ctype: str = "text/html; charset=utf-8") -> None:
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, code: int, obj) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False, indent=2),
                   "application/json; charset=utf-8")

    def _read_params(self) -> tuple[dict, str]:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else ""
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip()
        if ctype == "application/json":
            return (json.loads(raw) if raw else {}), "json"
        parsed = urllib.parse.parse_qs(raw, keep_blank_values=True)
        return {k: (v[0] if len(v) == 1 else v) for k, v in parsed.items()}, "form"

    # -- GET -----------------------------------------------------
    def do_GET(self) -> None:  # noqa: N802
        url = urllib.parse.urlparse(self.path)
        path, query = url.path, urllib.parse.parse_qs(url.query)
        app = self.app
        try:
            if path.startswith("/static/"):
                return self._static(path[len("/static/"):])
            if path.startswith("/api/events/"):
                return self._sse(path.rsplit("/", 1)[-1])
            if path == "/api/inventory":
                inv = app.inventory()
                return self._json(200, {"path": str(app.inv_path), "datasets": inv.datasets,
                                        "proposals": inv.proposals})
            if path == "/api/storages":
                return self._json(200, build_view(load_storages(app.config_path)))
            if path == "/api/tasks":
                return self._json(200, app.tasks.list_tasks())
            if path.startswith("/api/tasks/"):
                task = app.tasks.get(path.rsplit("/", 1)[-1])
                if task is None:
                    return self._json(404, {"error": "unknown task"})
                return self._json(200, {"task": task.public(),
                                        "events": app.tasks.events(task.id)})
            if path == "/":
                return self._send(200, _shell("overview", "/", render_overview(app)))
            if path == "/inventory":
                return self._send(200, _shell("inventory", "/inventory", render_inventory(app)))
            if path == "/storages":
                return self._send(200, _shell("storages", "/storages", render_storages(app)))
            if path == "/logs":
                return self._send(200, _shell("audit", "/logs", render_logs(app)))
            if path == "/tasks":
                return self._send(200, _shell("tasks", "/tasks", render_tasks(app)))
            if path.startswith("/tasks/"):
                return self._send(200, _shell("task", "/tasks",
                                              render_task(app, path.rsplit("/", 1)[-1])))
            if path == "/config/inventory":
                return self._send(200, _shell("edit inventory", "/config/inventory",
                                              render_config_inventory(app, query)))
            if path == "/config/facilities":
                return self._send(200, _shell("edit facilities", "/config/facilities",
                                              render_config_facilities(app, query)))
            if path == "/config/slices":
                return self._send(200, _shell("edit slices", "/config/slices",
                                              render_config_slices(app, query)))
            return self._send(404, _shell("not found", "", "<p>not found</p>"))
        except Exception as exc:  # noqa: BLE001 - dev-friendly 500s
            import traceback
            traceback.print_exc()
            return self._send(500, _shell("error", "", _flash("err", f"{type(exc).__name__}: {exc}")))

    def _static(self, name: str) -> None:
        allowed = {"htmx.min.js": "application/javascript; charset=utf-8",
                   "app.css": "text/css; charset=utf-8"}
        if name not in allowed:
            return self._send(404, "not found", "text/plain; charset=utf-8")
        path = STATIC_DIR / name
        if not path.is_file():
            return self._send(404, "not found", "text/plain; charset=utf-8")
        return self._send(200, path.read_bytes(), allowed[name])

    def _sse(self, task_id: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        after = 0
        try:
            while True:
                events = self.app.tasks.events(task_id, after)
                if events:
                    for event in events:
                        after = event["seq"]
                        payload = json.dumps(event, ensure_ascii=False)
                        self.wfile.write(f"id: {event['seq']}\ndata: {payload}\n\n".encode("utf-8"))
                    self.wfile.flush()
                    last = events[-1]
                    if last["type"] == "state" and last["data"].get("state") in ("done", "failed", "cancelled"):
                        break
                    continue
                self.app.tasks.wait_events(task_id, after, timeout=15)
                fresh = self.app.tasks.events(task_id, after)
                if not fresh:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    # -- POST ----------------------------------------------------
    def do_POST(self) -> None:  # noqa: N802
        url = urllib.parse.urlparse(self.path)
        path = url.path
        app = self.app
        try:
            params, flavor = self._read_params()
        except (json.JSONDecodeError, UnicodeDecodeError):
            return self._json(400, {"error": "invalid request body"})
        try:
            if path == "/api/actions/preview":
                plan, fragment = app.preview(params)
                if flavor == "json":
                    if plan is None:
                        return self._json(400, {"error": fragment})
                    return self._json(200, plan)
                if plan is None:
                    return self._send(200, _flash("err", fragment))
                return self._send(200, fragment)
            if path == "/api/actions/execute":
                session = app.get_token(str(params.get("token") or ""))
                if session is None:
                    msg = "token invalid or expired (re-run preview)"
                    if flavor == "json":
                        return self._json(409, {"ok": False, "detail": msg})
                    return self._send(200, _flash("err", msg))
                result = app.execute(session)
                if flavor == "json":
                    return self._json(200 if result["ok"] else 409, result)
                fragment = _flash("ok" if result["ok"] else "err", result["detail"])
                if result.get("task_id"):
                    fragment += (f"<p><a href='/tasks/{esc(result['task_id'])}'>"
                                 f"open task {esc(result['task_id'])}</a></p>")
                return self._send(200, fragment)
            if path == "/api/review":
                session = app.get_token(str(params.get("token") or ""))
                if session is None or not session.action.startswith("review."):
                    return self._json(409, {"ok": False, "detail": "valid review token required (preview first)"})
                expected_op = f"review.{params.get('op')}"
                if session.action != expected_op:
                    return self._json(409, {"ok": False, "detail": f"token is for {session.action}, not {expected_op}"})
                result = app.execute(session)
                return self._json(200 if result["ok"] else 409, result)
            return self._json(404, {"error": "not found"})
        except Exception as exc:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            return self._json(500, {"error": f"{type(exc).__name__}: {exc}"})


def serve(config_path: Path, port: int = 8787, open_browser: bool = True,
          tasks_root: Path | None = None) -> int:
    app = WebApp(config_path, tasks_root)
    Handler.app = app
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    httpd.daemon_threads = True
    url = f"http://127.0.0.1:{port}/"
    print(f"oasis-datasets web listening on {url}")
    print(f"config: {app.config_path}")
    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("shutting down")
    finally:
        httpd.server_close()
    return 0
