"""On-demand delivery refresh for UR-2026-1012 (manual runs; no automation).

Usage (via tools/refresh-delivery):
    mpc                # store update -> copy raw -> reparse -> HDF5 -> self-verify
    gaia [--skip-export]  # re-export tiers (or reuse existing) -> assemble -> HDF5 -> self-verify
    verify             # just run the delivery verifier

English output (CODING_STANDARDS §2.2). All writes are to the delivery dir
(~/Datasets/catalogs) and the task store; source data stays read-only.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DELIVERY = Path.home() / "Datasets/catalogs"
STORE_MPC = Path.home() / "oasis-catalog-store/catalogs/mpc/elements"
DWB_GAIA = Path("/Volumes/DWB/catalogs/gaia")
TOOLS = Path(__file__).resolve().parents[2] / "tools"

USAGE = "usage: refresh-delivery mpc | gaia [--skip-export] | verify"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run(cmd: list) -> int:
    print("$ " + " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd]).returncode


def _tool(name: str) -> Path:
    return TOOLS / name


def verify() -> int:
    return _run(["python3", DELIVERY / "verify.py"])


def _hdf5(files: list[Path]) -> int:
    return _run([_tool("oasis-datasets"), "hdf5", *files, "--apply"])


def _task_dir() -> Path:
    from .tasks import new_task_id
    path = Path.home() / ".local/state/oasis/tasks" / new_task_id()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _emit(etype: str, data: dict) -> None:
    if etype == "log":
        print("   " + str(data.get("text", "")), flush=True)
    elif etype == "error":
        print("   ERROR " + str(data.get("message", "")), file=sys.stderr, flush=True)


# ── MPC ─────────────────────────────────────────────────────────
def refresh_mpc() -> int:
    print("== refresh: mpc elements ==")
    rc = _run([_tool("oasis-catalog"), "update", "mpc"])
    if rc:
        return rc
    dest = DELIVERY / "mpc/elements"
    for name in ("MPCORB.DAT.gz", "CometEls.txt", "manifest.json"):
        shutil.copy2(STORE_MPC / name, dest / name)
    print(f"   raw copied from store -> {dest}")

    from . import mpcorb
    rc = mpcorb.run_parse(dest / "MPCORB.DAT.gz", dest, _task_dir(), _emit)
    if rc:
        return rc
    rc = _hdf5([dest / "mpc_elements.csv.gz"])
    if rc:
        return rc

    # registrations: manifest renditions entry for the HDF5 rendition
    manifest_path = dest / "mpc_elements.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    h5 = dest / "mpc_elements.h5"
    manifest["renditions"] = [{
        "id": "mpc_elements_h5", "path": "mpc_elements.h5", "format": "hdf5",
        "of": "mpc_elements.csv.gz", "dataset": "table",
        "bytes": h5.stat().st_size, "sha256": sha256(h5),
        "note": "optional rendition; canonical format is CSV.gz"}]
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                             encoding="utf-8")
    print(f"   rendition registered -> {manifest_path.name}")
    return verify()


# ── Gaia ────────────────────────────────────────────────────────
def refresh_gaia(export: bool = True) -> int:
    print("== refresh: gaia tiers ==")
    if export:
        rc = _run([_tool("oasis-datasets"), "slice", "run",
                   "gaia_t1", "gaia_t2", "gaia_t3", "--apply"])
        if rc:
            return rc
    else:
        print("   (--skip-export: reusing existing tier products in "
              f"{DWB_GAIA})")
    dest = DELIVERY / "gaia"
    for tier in ("t1", "t2", "t3"):
        (dest / tier).mkdir(parents=True, exist_ok=True)
        for name in (f"gaia_{tier}.csv.gz", "CREDITS.txt"):
            shutil.copy2(DWB_GAIA / tier / name, dest / tier / name)
    print(f"   tiers copied -> {dest}")

    rc = _hdf5([dest / tier / f"gaia_{tier}.csv.gz" for tier in ("t1", "t2", "t3")])
    if rc:
        return rc
    _build_gaia_manifest()
    return verify()


def _build_gaia_manifest() -> None:
    """Rebuild the batch manifest (epoch/frame + renditions) from the export manifest."""
    source = json.loads((DWB_GAIA / "t1/manifest.json").read_text(encoding="utf-8"))
    dest = DELIVERY / "gaia"
    tier_of = {"gaia_t1": "t1", "gaia_t2": "t2", "gaia_t3": "t3"}
    files = []
    for item in source["files"]:
        tier = tier_of[item["id"]]
        rel = f"{tier}/{item['path']}"
        if sha256(dest / rel) != item["sha256"]:
            raise SystemExit(f"copy mismatch, refusing to write manifest: {rel}")
        files.append({
            "id": item["id"], "path": rel, "bytes": item["bytes"], "sha256": item["sha256"],
            "version": item["version"], "epoch": "J2016.0", "frame": "ICRS",
            "provider": item["provider"], "licence": item["licence"],
            "rows": item["rows"], "columns": item["columns"], "select": item["select"],
            "gmin": item.get("gmin"), "gmax": item.get("gmax"),
            "source_dataset": item["source_dataset"],
            "source_snapshot": item["epoch"],
            "qc": source["qc"].get(item["id"], {}),
        })
    renditions = []
    for tier in ("t1", "t2", "t3"):
        h5 = dest / tier / f"gaia_{tier}.h5"
        renditions.append({
            "id": f"gaia_{tier}_h5", "path": f"{tier}/gaia_{tier}.h5", "format": "hdf5",
            "of": f"{tier}/gaia_{tier}.csv.gz", "dataset": "table",
            "bytes": h5.stat().st_size, "sha256": sha256(h5),
            "note": "optional rendition; canonical format is CSV.gz"})
    manifest = {
        "package": "UR-2026-1012 batch 1 — Gaia DR3 bright tiers (T1/T2/T3)",
        "generated_at": now_iso(),
        "product": {
            "kind": "slice-batch",
            "source_dataset": source["product"]["source_dataset"],
            "source_path": "/Volumes/ArecaStudio/Datasets/Gaia/gdr3/gaia_source",
            "generated_by": source["product"]["generated_by"],
            "task_id": source["product"]["task_id"],
            "specs": ["gaia_t1", "gaia_t2", "gaia_t3"],
            "partial": False,
            "note": "values passed through unmodified; rows filtered by phot_g_mean_mag",
        },
        "epoch": "J2016.0", "frame": "ICRS",
        "files": files,
        "renditions": renditions,
    }
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                                        encoding="utf-8")
    print(f"   batch manifest rebuilt -> {dest / 'manifest.json'}")


# ── entry point ─────────────────────────────────────────────────
def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(USAGE)
        return 2
    command = argv[0]
    if command == "mpc":
        return refresh_mpc()
    if command == "gaia":
        return refresh_gaia(export="--skip-export" not in argv)
    if command == "verify":
        return verify()
    print(USAGE)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
