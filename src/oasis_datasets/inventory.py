"""Inventory registry: load / validate / save and proposal lifecycle (DSM-003 §2).

V-rules implemented: V-01 ids, V-02 storage_pref refs, V-03 channel fields,
V-04 version_rule, V-05 unknown fields (x- allowed), V-06 id collisions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .confedit import atomic_write

ID_RE = re.compile(r"^[a-z0-9_]+$")
PROTOCOLS = {"file", "https", "ssh"}
VERSION_RULE_TYPES = {"last_modified", "etag", "checksum_mtime", "release", "none"}
CHECKSUM_FORMATS = {"auto", "md5sum", "sha256sum"}
CHECKSUM_CONTENTS = {"auto", "compressed", "decompressed"}
STATUSES = {"active", "deprecated"}

COMMON_KEYS = {"id", "title", "publisher", "licence", "fmt", "storage_pref", "channels", "notes"}
DATASET_KEYS = COMMON_KEYS | {"status", "added", "added_by"}
PROPOSAL_KEYS = COMMON_KEYS | {"reason", "proposed_at", "proposed_by"}
CHANNEL_KEYS = {"id", "protocol", "path", "url", "host", "notes", "checksum", "version_rule"}
CHECKSUM_KEYS = {"manifest", "format", "content"}
FMT_KEYS = {"type", "files", "size_hint", "columns_ref"}
LICENCE_KEYS = {"name", "url"}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Inventory:
    path: Path
    version: str = "0.1"
    datasets: list[dict] = field(default_factory=list)
    proposals: list[dict] = field(default_factory=list)


def load_inventory(path: Path) -> Inventory:
    if not path.exists():
        return Inventory(path=path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return Inventory(
        path=path,
        version=str(raw.get("inventory_version", "0.1")),
        datasets=list(raw.get("datasets") or []),
        proposals=list(raw.get("proposals") or []),
    )


def dump_inventory(inv: Inventory) -> str:
    payload = {"inventory_version": inv.version, "datasets": inv.datasets, "proposals": inv.proposals}
    return yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, default_flow_style=False)


def save_inventory(inv: Inventory) -> Path | None:
    return atomic_write(inv.path, dump_inventory(inv))


def _unknown_keys(errors: list[str], obj: dict, allowed: set[str], where: str) -> None:
    for key in obj:
        if key not in allowed and not str(key).startswith("x-"):
            errors.append(f"{where}: unknown field '{key}'")


def _validate_channel(channel: dict, where: str, errors: list[str]) -> None:
    if not isinstance(channel, dict):
        errors.append(f"{where}: channel must be a mapping")
        return
    _unknown_keys(errors, channel, CHANNEL_KEYS, where)
    cid = channel.get("id", "")
    if not isinstance(cid, str) or not cid:
        errors.append(f"{where}: channel id required")
    protocol = channel.get("protocol")
    if protocol not in PROTOCOLS:
        errors.append(f"{where}: invalid protocol '{protocol}'")
    elif protocol == "file" and not channel.get("path"):
        errors.append(f"{where}: file channel requires 'path'")
    elif protocol == "https":
        url = str(channel.get("url", ""))
        if not url.startswith("https://"):
            errors.append(f"{where}: https channel requires an https:// url")
    elif protocol == "ssh" and not (channel.get("host") and channel.get("path")):
        errors.append(f"{where}: ssh channel requires 'host' and 'path'")
    checksum = channel.get("checksum")
    if checksum is not None:
        if not isinstance(checksum, dict) or not checksum.get("manifest"):
            errors.append(f"{where}: checksum requires 'manifest'")
        else:
            _unknown_keys(errors, checksum, CHECKSUM_KEYS, f"{where}.checksum")
            if checksum.get("format", "auto") not in CHECKSUM_FORMATS:
                errors.append(f"{where}.checksum: invalid format")
            if checksum.get("content", "auto") not in CHECKSUM_CONTENTS:
                errors.append(f"{where}.checksum: invalid content")
    rule = channel.get("version_rule")
    if not isinstance(rule, dict) or rule.get("type") not in VERSION_RULE_TYPES:
        errors.append(f"{where}: version_rule.type required (one of {sorted(VERSION_RULE_TYPES)})")
    elif rule.get("type") == "release" and not rule.get("value"):
        errors.append(f"{where}: release version_rule requires 'value'")


def validate_entry(entry: dict, kind: str, storage_ids: set[str], where: str) -> tuple[list[str], list[str]]:
    """Validate one dataset/proposal entry. Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(entry, dict):
        return [f"{where}: entry must be a mapping"], []
    _unknown_keys(errors, entry, DATASET_KEYS if kind == "dataset" else PROPOSAL_KEYS, where)

    entry_id = entry.get("id", "")
    if not isinstance(entry_id, str) or not ID_RE.match(entry_id):
        errors.append(f"{where}: id must match [a-z0-9_]+")
    if not entry.get("title"):
        errors.append(f"{where}: title required")
    if not entry.get("publisher"):
        errors.append(f"{where}: publisher required")

    licence = entry.get("licence")
    if not isinstance(licence, dict) or not licence.get("name"):
        errors.append(f"{where}: licence.name required")
    else:
        _unknown_keys(errors, licence, LICENCE_KEYS, f"{where}.licence")
        if not licence.get("url"):
            warnings.append(f"{where}: licence.url empty (to be completed)")

    fmt = entry.get("fmt")
    if fmt is not None:
        if not isinstance(fmt, dict):
            errors.append(f"{where}.fmt must be a mapping")
        else:
            _unknown_keys(errors, fmt, FMT_KEYS, f"{where}.fmt")

    prefs = entry.get("storage_pref") or []
    if not isinstance(prefs, list):
        errors.append(f"{where}: storage_pref must be a list")
    else:
        for pref in prefs:
            if pref not in storage_ids:
                errors.append(f"{where}: storage_pref references unknown storage '{pref}'")

    channels = entry.get("channels")
    if not isinstance(channels, list) or not channels:
        errors.append(f"{where}: at least one channel required")
    else:
        seen: set[str] = set()
        for i, channel in enumerate(channels):
            _validate_channel(channel, f"{where}.channels[{i}]", errors)
            cid = channel.get("id") if isinstance(channel, dict) else None
            if cid in seen:
                errors.append(f"{where}: duplicate channel id '{cid}'")
            seen.add(cid)

    if kind == "dataset" and entry.get("status", "active") not in STATUSES:
        errors.append(f"{where}: invalid status '{entry.get('status')}'")
    return errors, warnings


def validate_inventory(inv: Inventory, storage_ids: set[str]) -> tuple[list[str], list[str]]:
    """V-01…V-06 across the whole inventory."""
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()

    for entry in inv.datasets:
        eid = entry.get("id") if isinstance(entry, dict) else None
        e, w = validate_entry(entry, "dataset", storage_ids, f"dataset '{eid}'")
        errors += e
        warnings += w
        if eid in seen_ids:
            errors.append(f"V-01: duplicate id '{eid}'")
        seen_ids.add(eid)

    for entry in inv.proposals:
        pid = entry.get("id") if isinstance(entry, dict) else None
        e, w = validate_entry(entry, "proposal", storage_ids, f"proposal '{pid}'")
        errors += e
        warnings += w
        if not entry.get("reason"):
            errors.append(f"proposal '{pid}': reason required")
        if pid in seen_ids:
            errors.append(f"V-06: proposal id '{pid}' collides with an existing id")
        seen_ids.add(pid)

    return errors, warnings


def propose(inv: Inventory, entry: dict, by: str = "owner") -> dict:
    item = dict(entry)
    item["proposed_at"] = now_iso()
    item["proposed_by"] = by
    inv.proposals.append(item)
    return item


def approve(inv: Inventory, entry_id: str, by: str = "owner") -> dict:
    for i, item in enumerate(inv.proposals):
        if item.get("id") == entry_id:
            dataset = {k: v for k, v in item.items() if k not in ("reason", "proposed_at", "proposed_by")}
            dataset["status"] = "active"
            dataset["added"] = now_iso()
            dataset["added_by"] = by
            inv.datasets.append(dataset)
            inv.proposals.pop(i)
            return dataset
    raise KeyError(f"proposal '{entry_id}' not found")


def reject(inv: Inventory, entry_id: str) -> dict:
    for i, item in enumerate(inv.proposals):
        if item.get("id") == entry_id:
            return inv.proposals.pop(i)
    raise KeyError(f"proposal '{entry_id}' not found")


def deprecate(inv: Inventory, entry_id: str) -> dict:
    for item in inv.datasets:
        if item.get("id") == entry_id:
            item["status"] = "deprecated"
            return item
    raise KeyError(f"dataset '{entry_id}' not found")
