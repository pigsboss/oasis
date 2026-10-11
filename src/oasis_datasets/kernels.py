"""SPICE kernel registry & supply — the ecosystem's "asset/supply plane" (裁决七).

Registry lives at `~/.config/oasis/kernels.yaml`, parallel to `inventory.yaml`:
kernels are NOT datasets (no catalogue semantics); long-term support stays with
the publication channels (NAIF / JPL), local files are working copies.

Commands (via `oasis-datasets kernels ...`):
  list    registry + store status
  verify  [dirs...]   checksum verification (store by default, arbitrary dirs otherwise)
  fetch   <ids|all>   channel -> store (parallel ranges, resume, verify, record sha256)
  send    <ids|all> --app DIR   store -> <app>/spice_kernels (verify + manifest)
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

from . import mirror
from .confedit import atomic_write

REGISTRY_NAME = "kernels.yaml"
DEFAULT_STORE = "/Volumes/ArecaStudio/Datasets/SPICE Kernels"  # 生态数据区命名约定
CATEGORIES = ("lsk", "pck", "spk", "fk", "stars")
KERNEL_SUFFIXES = (".bsp", ".tls", ".tpc", ".tf", ".bpc", ".bc", ".xdb", ".ker")


def _is_kernel_like(name: str) -> bool:
    lower = name.lower()
    return lower.endswith(KERNEL_SUFFIXES) or lower.endswith(".xdb.z")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _human(nbytes: int) -> str:
    value = float(nbytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1000 or unit == "TB":
            return f"{value:.1f} {unit}"
        value /= 1000
    return f"{value:.1f} TB"


def file_md5(path: Path) -> str:
    digest = hashlib.md5()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


# ── registry ────────────────────────────────────────────────────
@dataclass
class KernelsRegistry:
    path: Path
    store_root: Path
    store_text: str = DEFAULT_STORE
    kernels: list[dict] = field(default_factory=list)

    def by_id(self, kernel_id: str) -> dict | None:
        return next((k for k in self.kernels if k.get("id") == kernel_id), None)

    def select(self, ids: list[str]) -> tuple[list[dict], list[str]]:
        if not ids or "all" in ids:
            return list(self.kernels), []
        picked, unknown = [], []
        for kernel_id in ids:
            entry = self.by_id(kernel_id)
            if entry is None:
                unknown.append(kernel_id)
            else:
                picked.append(entry)
        return picked, unknown


def load_registry(path: Path) -> KernelsRegistry:
    if not path.exists():
        return KernelsRegistry(path=path, store_root=Path(DEFAULT_STORE).expanduser())
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    store_text = str(raw.get("store_root", DEFAULT_STORE))
    return KernelsRegistry(path=path, store_root=Path(store_text).expanduser(),
                           store_text=store_text,
                           kernels=list(raw.get("kernels") or []))


def dump_registry(reg: KernelsRegistry) -> str:
    payload = {"kernels_version": "0.1", "store_root": reg.store_text,
               "kernels": reg.kernels}
    return yaml.safe_dump(payload, allow_unicode=True, sort_keys=False)


def save_registry(reg: KernelsRegistry) -> Path | None:
    return atomic_write(reg.path, dump_registry(reg))


def store_path(reg: KernelsRegistry, entry: dict) -> Path:
    return reg.store_root / str(entry.get("category", "misc")) / str(entry["filename"])


# ── verification ────────────────────────────────────────────────
def verify_file(entry: dict, path: Path) -> tuple[str, list[str]]:
    """Returns (status, problems); status in {ok, mismatch, missing}."""
    if not path.exists():
        return "missing", [f"not found: {path}"]
    problems: list[str] = []
    size = path.stat().st_size
    expected_bytes = entry.get("bytes")
    if expected_bytes and size != int(expected_bytes):
        problems.append(f"size {size} != {expected_bytes}")
    official = entry.get("official_checksum") or {}
    if official.get("value"):
        got = file_md5(path) if official.get("type") == "md5" else file_sha256(path)
        if got != official["value"]:
            problems.append(f"official {official.get('type')} mismatch")
    if entry.get("sha256"):
        if file_sha256(path) != entry["sha256"]:
            problems.append("sha256 mismatch")
    return ("mismatch" if problems else "ok"), problems


# ── commands ────────────────────────────────────────────────────
def cmd_list(reg: KernelsRegistry, as_json: bool = False) -> int:
    rows = []
    for entry in reg.kernels:
        path = store_path(reg, entry)
        status, _ = verify_file(entry, path) if entry.get("stored") or path.exists() \
            else ("not-fetched", [])
        rows.append({
            "id": entry.get("id"), "category": entry.get("category"),
            "status": status, "bytes": entry.get("bytes"),
            "sha256": (entry.get("sha256") or "")[:16],
            "source": entry.get("source_url"), "used_by": entry.get("used_by") or [],
        })
    if as_json:
        print(json.dumps({"store_root": reg.store_text, "kernels": rows},
                         indent=2, ensure_ascii=False))
        return 0
    print(f"store_root: {reg.store_text}")
    for row in rows:
        used = ",".join(row["used_by"]) or "-"
        size = _human(int(row["bytes"])) if row["bytes"] else "-"
        print(f"{row['id']:12s} {row['category']:6s} {row['status']:11s} {size:>9s} "
              f"sha256={row['sha256'] or '-':16s} used_by={used}")
    return 0


def cmd_verify(reg: KernelsRegistry, dirs: list[str], as_json: bool = False) -> int:
    rc = 0
    report: list[dict] = []
    if not dirs:
        for entry in reg.kernels:
            path = store_path(reg, entry)
            status, problems = verify_file(entry, path)
            report.append({"id": entry.get("id"), "path": str(path),
                           "status": status, "problems": problems})
            if status == "mismatch":
                rc = 1
    else:
        by_name = {str(e["filename"]): e for e in reg.kernels}
        for directory in dirs:
            root = Path(directory).expanduser()
            if not root.exists():
                print(f"error: {root} not found", file=sys.stderr)
                rc = 1
                continue
            for path in sorted(p for p in root.rglob("*") if p.is_file()):
                entry = by_name.get(path.name)
                if entry is None:
                    if _is_kernel_like(path.name):
                        report.append({"id": None, "path": str(path),
                                       "status": "unregistered", "problems": []})
                    continue
                status, problems = verify_file(entry, path)
                report.append({"id": entry.get("id"), "path": str(path),
                               "status": status, "problems": problems})
                if status == "mismatch":
                    rc = 1
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return rc
    for row in report:
        name = row["id"] or "(unregistered)"
        extra = f"  {'; '.join(row['problems'])}" if row["problems"] else ""
        print(f"{row['status']:12s} {name:12s} {row['path']}{extra}")
    ok = sum(1 for r in report if r["status"] == "ok")
    unreg = sum(1 for r in report if r["status"] == "unregistered")
    print(f"\n{len(report)} file(s): ok={ok} mismatched="
          f"{sum(1 for r in report if r['status'] == 'mismatch')} "
          f"missing={sum(1 for r in report if r['status'] == 'missing')} unregistered={unreg}")
    return rc


def _emit(etype: str, data: dict) -> None:
    if etype == "log":
        print("   " + str(data.get("text", "")), flush=True)
    elif etype == "error":
        print("   ERROR " + str(data.get("message", "")), file=sys.stderr, flush=True)


def cmd_fetch(reg: KernelsRegistry, ids: list[str], parallel: int = 8,
              apply: bool = False) -> int:
    picked, unknown = reg.select(ids)
    if unknown:
        print(f"error: unknown kernel id(s): {', '.join(unknown)}", file=sys.stderr)
        return 2
    if not picked:
        print("no kernels selected")
        return 2
    rc = 0
    for entry in picked:
        dest = store_path(reg, entry)
        status, _ = verify_file(entry, dest) if dest.exists() else ("missing", [])
        if status == "ok":
            print(f"{entry['id']}: up-to-date ({dest})")
            continue
        try:
            info = mirror.head(str(entry["source_url"]))
        except Exception as exc:  # noqa: BLE001 - report probe failure per entry
            print(f"{entry['id']}: FAIL probe: {type(exc).__name__}: {exc}", file=sys.stderr)
            rc = 1
            continue
        size = int(info.get("content-length") or 0)
        ranges = "bytes" in str(info.get("accept-ranges", "")).lower()
        print(f"{entry['id']}: {entry['source_url']}")
        print(f"   -> {dest} ({_human(size)}, ranges={ranges}, parallel={parallel})")
        if not apply:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        started = time.time()
        try:
            mirror.download(str(entry["source_url"]), dest, size, ranges, parallel, _emit)
        except Exception as exc:  # noqa: BLE001 - keep part files, report failure
            print(f"{entry['id']}: FAIL download: {type(exc).__name__}: {exc} "
                  "(part files kept for resume)", file=sys.stderr)
            rc = 1
            continue
        status, problems = verify_file(entry, dest)
        if problems:
            print(f"{entry['id']}: FAIL verify: {'; '.join(problems)} "
                  "(file kept; registry not updated)", file=sys.stderr)
            rc = 1
            continue
        digest = file_sha256(dest)
        # long downloads may overlap with other registry edits (e.g. new registrations):
        # re-load, merge this entry, then save so nothing else is lost
        fresh = load_registry(reg.path)
        target = fresh.by_id(entry["id"]) or entry
        target["bytes"] = dest.stat().st_size
        target["sha256"] = digest
        target["stored"] = {"path": str(dest), "sha256": digest,
                            "bytes": target["bytes"], "fetched_at": now_iso()}
        save_registry(fresh)
        reg = fresh
        print(f"{entry['id']}: done {_human(target['bytes'])} in {time.time()-started:.1f}s "
              f"sha256={digest[:16]}…")
    if not apply:
        print("(dry-run: plan only; add --apply to fetch)")
    return rc


def cmd_send(reg: KernelsRegistry, ids: list[str], app: str, apply: bool = False) -> int:
    picked, unknown = reg.select(ids)
    if unknown:
        print(f"error: unknown kernel id(s): {', '.join(unknown)}", file=sys.stderr)
        return 2
    if not picked:
        print("no kernels selected")
        return 2
    dest_base = Path(app).expanduser() / "spice_kernels"
    rc = 0
    sent: list[dict] = []
    for entry in picked:
        src = store_path(reg, entry)
        status, problems = verify_file(entry, src)
        if status != "ok":
            print(f"{entry['id']}: FAIL store copy is {status} ({src}) — run fetch first",
                  file=sys.stderr)
            rc = 1
            continue
        dst = dest_base / str(entry.get("category", "misc")) / str(entry["filename"])
        print(f"{entry['id']}: {src} -> {dst}")
        if not apply:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        if file_sha256(dst) != entry["sha256"]:
            print(f"{entry['id']}: FAIL post-copy sha256 mismatch", file=sys.stderr)
            rc = 1
            continue
        sent.append({"id": entry["id"], "path": str(dst.relative_to(dest_base)),
                     "sha256": entry["sha256"], "bytes": entry.get("bytes"),
                     "source_url": entry.get("source_url")})
    if apply and sent:
        manifest = {"generated_at": now_iso(), "tool": "oasis-datasets kernels send",
                    "app": str(Path(app).expanduser()), "entries": sent}
        manifest_path = dest_base / "oasis-manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                                 encoding="utf-8")
        print(f"manifest -> {manifest_path}")
    elif not apply:
        print("(dry-run: plan only; add --apply to send)")
    return rc
