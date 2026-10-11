"""Inventory-first resolution with legacy config fallback (DSM-002 §3.8).

Read-path rule: when inventory.yaml has datasets, list/verify/sync resolve
against it; otherwise they fall back to the legacy `config.datasets` for one
version cycle. `oasis-catalog update` keeps using the legacy config (store
layout lives there).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from oasis_catalog.config import Config

from . import inventory as inv_mod

INVENTORY_NAME = "inventory.yaml"
LOCAL_KINDS = ("local_volume", "local_store")


@dataclass
class LocalRef:
    """A locally-addressable dataset/channel pair for verify/sync."""
    ds_id: str
    cid: str
    title: str
    root: Path
    rel_path: str          # legacy relative path when known (dest layout)
    origin: str            # inventory | config


def load_inventory_for(config_path: Path):
    return inv_mod.load_inventory(Path(config_path).parent / INVENTORY_NAME)


def local_refs(cfg: Config, inv, ids: list[str]) -> list[LocalRef]:
    """Local (file) refs, filtered by dataset id or channel id."""
    def wanted(ds_id: str, cid: str) -> bool:
        return not ids or ds_id in ids or cid in ids

    out: list[LocalRef] = []
    if inv.datasets:
        legacy_rel = {c.id: c.path for ds in cfg.datasets for c in ds.catalogues if c.path}
        for ds in inv.datasets:
            ds_id = str(ds.get("id", ""))
            if ds.get("status") == "deprecated":
                continue
            for channel in ds.get("channels") or []:
                if channel.get("protocol") != "file" or not channel.get("path"):
                    continue
                cid = str(channel.get("id", "?"))
                if not wanted(ds_id, cid):
                    continue
                out.append(LocalRef(ds_id, cid, str(ds.get("title", ds_id)),
                                    Path(str(channel["path"])).expanduser(),
                                    legacy_rel.get(ds_id, ""), "inventory"))
        return out

    for ds in cfg.datasets:
        for c in ds.catalogues:
            if not wanted(ds.id, c.id):
                continue
            base = ds.access_path()
            if ds.kind not in LOCAL_KINDS or base is None:
                continue
            out.append(LocalRef(ds.id, c.id, c.title or c.id, base / c.path, c.path, "config"))
    return out


def dest_for(base: Path, ref: LocalRef) -> Path:
    """Destination root for sync: base/oasis-datasets/<rel_path or dataset id>."""
    return base / "oasis-datasets" / (ref.rel_path or ref.ds_id)
