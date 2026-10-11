"""Migrate legacy `config.datasets` into `inventory.yaml` (DSM-002 §3.8).

Mapping rules:
  local_volume catalogues  -> inventory datasets (channel: file; checksum auto-discovered)
  remote catalogues        -> inventory datasets (channel: https; version_rule: last_modified)
  local_store entries      -> skipped (products zone, not a published dataset)
"""

from __future__ import annotations

from pathlib import Path

from oasis_catalog.config import Config

from .checksums import discover, parse

PUBLISHER = {
    "gaia_gdr3_gaia_source": "ESA / Gaia DPAC",
    "gaia_gdr2_gaia_source": "ESA / Gaia DPAC",
    "tess_tic": "NASA / MIT (TESS)",
    "wise_allwise": "NASA / IRSA",
    "twomass_psc": "UMass / IPAC (2MASS)",
    "seds_templates": "SVO / PhoSim template bundle",
    "mpcorb": "Minor Planet Center",
    "cometels": "Minor Planet Center",
}
LICENCE = {
    "gaia_gdr3_gaia_source": {"name": "Gaia data licence (see credits)",
                              "url": "https://www.cosmos.esa.int/web/gaia-users/credits"},
    "gaia_gdr2_gaia_source": {"name": "Gaia data licence (see credits)",
                              "url": "https://www.cosmos.esa.int/web/gaia-users/credits"},
    "tess_tic": {"name": "TESS data products", "url": "https://archive.stsci.edu/tess/"},
    "wise_allwise": {"name": "AllWISE Source Catalog",
                     "url": "https://wise2.ipac.caltech.edu/docs/release/allwise/"},
    "twomass_psc": {"name": "2MASS All-Sky Data Release",
                    "url": "https://irsa.ipac.caltech.edu/Missions/2mass.html"},
    "seds_templates": {"name": "Theoretical SED templates (see archive README)", "url": ""},
    "mpcorb": {"name": "MPC Copyright",
               "url": "https://www.minorplanetcenter.net/iau/info/Copyright.html"},
    "cometels": {"name": "MPC Copyright",
                 "url": "https://www.minorplanetcenter.net/iau/info/Copyright.html"},
}
FMT_TYPE = {
    "gaia_gdr3_gaia_source": "ecsv.gz",
    "gaia_gdr2_gaia_source": "csv.gz",
    "tess_tic": "csv.gz",
    "wise_allwise": "bz2",
    "twomass_psc": "gz (fixed-width text)",
    "seds_templates": "tar.gz",
    "mpcorb": "gz (fixed-width text)",
    "cometels": "fixed-width text",
}
KNOWN_FILES = {"gaia_gdr3_gaia_source": 3386, "tess_tic": 90, "wise_allwise": 48,
               "twomass_psc": 95, "mpcorb": 1, "cometels": 1}
PREF_LOCAL = ["raid5_archive", "zfs_nas"]
PREF_REMOTE = ["macbook_ssd", "zfs_nas"]


def _pref(candidates: list[str], storage_ids: set[str]) -> list[str]:
    """Candidate storage prefs filtered to registered storages (V-02-safe)."""
    picked = [s for s in candidates if s in storage_ids]
    return picked or sorted(storage_ids)


def _best_checksum(root: Path) -> dict | None:
    """Pick the manifest with the most entries among discovered ones."""
    best = None
    best_count = -1
    for manifest_path in discover(root):
        manifest = parse(manifest_path, root)
        if len(manifest.entries) > best_count:
            best = manifest_path
            best_count = len(manifest.entries)
    if best is None:
        return None
    try:
        rel = str(best.relative_to(root))
    except ValueError:
        rel = str(best)
    return {"manifest": rel, "format": "auto", "content": "auto"}


def build_inventory(config: Config, storage_ids: set[str]) -> tuple[dict, list[dict]]:
    """Return (inventory payload, review-log entries)."""
    datasets: list[dict] = []
    logs: list[dict] = []

    for ds in config.datasets:
        if ds.kind == "local_volume":
            base = ds.access_path()
            for c in ds.catalogues:
                root = (base / c.path) if base else None
                channel = {"id": "local", "protocol": "file",
                           "path": str(root) if root else c.path,
                           "version_rule": {"type": "none"}}
                if root and root.is_dir():
                    checksum = _best_checksum(root)
                    if checksum:
                        channel["checksum"] = checksum
                        channel["version_rule"] = {"type": "checksum_mtime"}
                entry = {
                    "id": c.id,
                    "title": c.title or c.id,
                    "publisher": PUBLISHER.get(c.id, ds.provider or "unknown"),
                    "licence": LICENCE.get(c.id, {"name": ds.licence or "see source", "url": ""}),
                    "fmt": {k: v for k, v in {
                        "type": FMT_TYPE.get(c.id, "unknown"),
                        "files": KNOWN_FILES.get(c.id),
                        "size_hint": c.size_hint or None,
                        "columns_ref": None,
                    }.items() if v},
                    "storage_pref": _pref(PREF_LOCAL, storage_ids),
                    "status": "active",
                    "channels": [channel],
                }
                if c.notes:
                    entry["notes"] = c.notes
                if c.format:
                    entry["x-source-format"] = c.format
                datasets.append(entry)
                logs.append({"action": "approve", "target": f"dataset:{c.id}",
                             "note": "migrated from legacy config.datasets"})

        elif ds.kind == "remote":
            for c in ds.catalogues:
                entry = {
                    "id": c.id,
                    "title": c.title or c.id,
                    "publisher": PUBLISHER.get(c.id, ds.provider or "unknown"),
                    "licence": LICENCE.get(c.id, {"name": ds.licence or "see source", "url": ""}),
                    "fmt": {k: v for k, v in {
                        "type": FMT_TYPE.get(c.id, "unknown"),
                        "files": KNOWN_FILES.get(c.id),
                        "size_hint": c.size_hint or None,
                    }.items() if v},
                    "storage_pref": _pref(PREF_REMOTE, storage_ids),
                    "status": "active",
                    "channels": [{
                        "id": "primary", "protocol": "https", "url": c.url,
                        "version_rule": {"type": "last_modified"},
                    }],
                }
                if c.format:
                    entry["x-source-format"] = c.format
                datasets.append(entry)
                logs.append({"action": "approve", "target": f"dataset:{c.id}",
                             "note": "migrated from legacy config.datasets"})

        # local_store entries are the products zone -> intentionally skipped

    logs.append({"action": "edit", "target": "config:inventory",
                 "note": "initial migration from legacy config.datasets"})
    return {"inventory_version": "0.1", "datasets": datasets, "proposals": []}, logs
