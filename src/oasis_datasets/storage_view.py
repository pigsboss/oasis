"""Local file-system view: registered storages vs mounted reality.

Sources: /Volumes enumeration, mount-point walk-up for capacity, and
`diskutil list` (macOS) to catch volumes that are attached but not mounted.
States: mounted | attached_unmounted | absent | remote | unconfigured.

Read-only; `diskutil` absence degrades gracefully.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

STATE_MOUNTED = "mounted"
STATE_ATTACHED_UNMOUNTED = "attached_unmounted"
STATE_ABSENT = "absent"
STATE_REMOTE = "remote"
STATE_UNCONFIGURED = "unconfigured"

_VOLUME_LINE = re.compile(
    r"^\s+\d+:\s+(?P<rest>.+)\s+(?P<size>[*+]?[\d.]+\s+[KMGTP]?B)\s+(?P<device>disk\d+(?:s\d+)*)\s*$")
_GROUP_LINE = re.compile(r"^/dev/(?P<device>disk\d+)\s+\((?P<group>[^)]*)\):")
# volume-bearing types (longest first for prefix matching); containers/partitions excluded
_VOLUME_TYPES = ("Microsoft Basic Data", "Apple_APFS Container", "APFS Container Scheme",
                 "Linux Filesystem", "Apple_APFS_ISC", "Apple_HFS", "APFS Volume",
                 "GUID_partition_scheme", "Apple_RAID", "Apple_Boot", "EFI", "ExFAT")
_SKIP_TYPES = ("GUID_partition_scheme", "APFS Container Scheme", "Apple_APFS Container",
               "Apple_APFS_ISC", "Apple_APFS_Recovery", "EFI", "Apple_Boot")


def _human(nbytes: int) -> str:
    value = float(nbytes)
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if value < 1000 or unit == "PB":
            return f"{value:.1f} {unit}"
        value /= 1000
    return f"{value:.1f} PB"


def list_mounted_volumes() -> dict[str, str]:
    """Volume name -> mount path, from /Volumes (symlinks and dot entries skipped)."""
    out: dict[str, str] = {}
    root = Path("/Volumes")
    if not root.is_dir():
        return out
    for entry in sorted(root.iterdir()):
        if entry.name.startswith(".") or entry.is_symlink():
            continue
        if os.path.ismount(entry):
            out[entry.name] = str(entry)
    return out


def list_attached_volumes() -> list[dict]:
    """Attached volumes from `diskutil list` (name, size, device, group).

    EFI/Apple_Boot system partitions are excluded: they are unmounted by design.
    """
    try:
        proc = subprocess.run(["diskutil", "list"], capture_output=True, text=True, timeout=15)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return []
    if proc.returncode != 0:
        return []
    volumes: list[dict] = []
    group = ""
    for line in proc.stdout.splitlines():
        match = _GROUP_LINE.match(line.strip())
        if match:
            group = match.group("group")
            continue
        match = _VOLUME_LINE.match(line)
        if not match:
            continue
        rest = match.group("rest").strip()
        vtype = next((t for t in _VOLUME_TYPES if rest == t or rest.startswith(t + " ")), None)
        if vtype is None or vtype in _SKIP_TYPES:
            continue
        name = rest[len(vtype):].strip()
        if not name:
            continue
        volumes.append({"name": name, "size": match.group("size").lstrip("*+"),
                        "device": match.group("device"), "group": group})
    return volumes


def _mount_root(path: Path) -> Path:
    probe = path if path.exists() else path.parent
    while not probe.exists() and probe.parent != probe:
        probe = probe.parent
    while not os.path.ismount(probe) and probe.parent != probe:
        probe = probe.parent
    return probe


def _volume_name_from_path(path: Path) -> str | None:
    parts = path.parts
    if len(parts) >= 3 and parts[1] == "Volumes":
        return parts[2]
    return None


def build_view(storages: dict[str, dict]) -> dict:
    mounted = list_mounted_volumes()
    attached = list_attached_volumes()
    attached_names = {v["name"] for v in attached if "external" in v["group"] or "disk image" in v["group"]}
    attached_unmounted = [v for v in attached if v["name"] in attached_names and v["name"] not in mounted]
    registered_names: set[str] = set()
    rows: list[dict] = []

    for sid in sorted(storages):
        item = storages[sid]
        access = item.get("access") or {}
        protocols = list(access.get("protocols") or [])
        if not protocols and access.get("protocol"):
            protocols = [str(access["protocol"])]
        raw_path = str(access.get("path", ""))
        row = {"id": sid, "class": item.get("class", ""), "node": item.get("node", ""),
               "protocols": protocols, "state": STATE_REMOTE, "path": raw_path or None,
               "mount": None, "capacity": None, "detail": ""}

        if "file" in protocols and raw_path:
            if "<TODO" in raw_path:
                row["state"] = STATE_UNCONFIGURED
                row["detail"] = "path not configured"
            else:
                path = Path(raw_path).expanduser()
                vol = _volume_name_from_path(path)
                if vol:
                    registered_names.add(vol)
                if path.exists():
                    row["state"] = STATE_MOUNTED
                    mount = _mount_root(path)
                    row["mount"] = str(mount)
                    try:
                        usage = shutil.disk_usage(mount)
                        row["capacity"] = {"total": usage.total, "used": usage.used, "free": usage.free}
                    except OSError:
                        pass
                elif vol and vol in {v["name"] for v in attached_unmounted}:
                    row["state"] = STATE_ATTACHED_UNMOUNTED
                    row["detail"] = f"volume '{vol}' attached but not mounted"
                else:
                    row["state"] = STATE_ABSENT
                    row["detail"] = f"path missing ({path})"
        elif "file" in protocols:
            row["state"] = STATE_UNCONFIGURED
            row["detail"] = "portable/adhoc: mount point resolved at use time (--to-path)"
        elif protocols:
            host = str(access.get("host", ""))
            row["detail"] = f"{'/'.join(protocols)} {host}".strip() + " (not probed)"

        rows.append(row)

    unregistered_mounted = []
    for name, path in mounted.items():
        if name in registered_names:
            continue
        item: dict = {"name": name, "mount": path}
        usage = _usage(path)
        if usage:
            item["capacity"] = {"total": usage.total, "free": usage.free}
        unregistered_mounted.append(item)
    return {
        "storages": rows,
        "volumes": {
            "mounted": sorted(mounted),
            "attached_unmounted": attached_unmounted,
            "unregistered_mounted": unregistered_mounted,
        },
    }


def _usage(path: str):
    try:
        return shutil.disk_usage(path)
    except OSError:
        return None


def render_text(view: dict) -> str:
    lines: list[str] = [f"storages ({len(view['storages'])} registered):"]
    for row in view["storages"]:
        flags = f"[{row['state']}]".ljust(21)
        where = row["mount"] or row["path"] or row["detail"]
        extra = ""
        if row["capacity"]:
            extra = f"  free {_human(row['capacity']['free'])} / {_human(row['capacity']['total'])}"
        detail = f"  — {row['detail']}" if row["detail"] and row["detail"] != where else ""
        lines.append(f"  {row['id']:16s} {flags} {where}{extra}{detail}")
    volumes = view["volumes"]
    lines.append("")
    lines.append(f"volumes mounted (/Volumes): {', '.join(volumes['mounted']) or '-'}")
    if volumes["unregistered_mounted"]:
        def _vol_label(v: dict) -> str:
            if v.get("capacity"):
                return (f"{v['name']} ({_human(v['capacity']['total'])}, "
                        f"{_human(v['capacity']['free'])} free)")
            return str(v["name"])
        unreg = ", ".join(_vol_label(v) for v in volumes["unregistered_mounted"])
        lines.append(f"mounted but not registered: {unreg}")
    if volumes["attached_unmounted"]:
        attached = ", ".join(f"{v['name']} ({v['size']}, {v['device']})" for v in volumes["attached_unmounted"])
        lines.append(f"attached but not mounted: {attached}")
    return "\n".join(lines)
