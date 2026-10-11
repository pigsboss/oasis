"""System configuration for OASIS datasets & catalogues.

Location convention: ~/.config/oasis/config.yaml (override via --config or $OASIS_CONFIG;
repo-local ./catalogues.yaml is used as a fallback example).

The registry answers three questions:
  datasets      — which datasets exist
  access        — how to access them (file path / https endpoint)
  catalogues    — which source tables each dataset contains
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

USER_CONFIG = Path("~/.config/oasis/config.yaml")
REPO_FALLBACK = Path("catalogues.yaml")
VALID_KINDS = {"local_volume", "remote", "local_store"}


class ConfigError(Exception):
    """Raised when the configuration file is missing or malformed."""


def resolve_config_path(explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    env = os.environ.get("OASIS_CONFIG")
    if env:
        return Path(env).expanduser()
    user = USER_CONFIG.expanduser()
    if user.exists():
        return user
    return REPO_FALLBACK


@dataclass
class CatalogueEntry:
    id: str
    title: str = ""
    url: str = ""
    target_dir: str = ""
    path: str = ""
    format: str = ""
    size_hint: str = ""
    notes: str = ""
    manifest: str = "manifest.json"
    provider: str = ""
    licence: str = ""
    dataset_id: str = field(default="", repr=False)

    @property
    def updatable(self) -> bool:
        return bool(self.url and self.target_dir)


@dataclass
class Dataset:
    id: str
    title: str = ""
    kind: str = ""
    access: dict = field(default_factory=dict)
    provider: str = ""
    licence: str = ""
    catalogues: list[CatalogueEntry] = field(default_factory=list)

    def access_path(self) -> Path | None:
        p = self.access.get("path")
        return Path(str(p)).expanduser() if p else None

    def access_summary(self) -> str:
        if self.kind == "remote":
            proto = self.access.get("protocol", "https")
            base = self.access.get("base_url", "")
            auth = self.access.get("auth", "none")
            return f"{proto}:{base} (auth={auth})"
        return f"{self.access.get('protocol', 'file')}:{self.access.get('path', '')}"


@dataclass
class Config:
    store_root: Path
    datasets: list[Dataset]
    config_path: Path | None = None

    def select_updatable(self, ids: list[str]) -> list[tuple[Dataset, CatalogueEntry]]:
        out: list[tuple[Dataset, CatalogueEntry]] = []
        for ds in self.datasets:
            if ds.kind != "remote":
                continue
            for c in ds.catalogues:
                if not c.updatable:
                    continue
                if ids and c.id not in ids and ds.id not in ids:
                    continue
                out.append((ds, c))
        return out

    def select_tracked(self, ids: list[str]) -> list[tuple[Dataset, CatalogueEntry, str]]:
        out: list[tuple[Dataset, CatalogueEntry, str]] = []
        for ds in self.datasets:
            for c in ds.catalogues:
                tdir = c.target_dir or (c.path if ds.kind == "local_store" else "")
                if not tdir:
                    continue
                if ids and c.id not in ids and ds.id not in ids:
                    continue
                out.append((ds, c, tdir))
        return out


def _entry(ds: Dataset, raw: dict, kind: str) -> CatalogueEntry:
    entry = CatalogueEntry(
        id=str(raw.get("id", "")),
        title=str(raw.get("title", "")),
        url=str(raw.get("url", "")),
        target_dir=str(raw.get("target_dir", "")),
        path=str(raw.get("path", "")),
        format=str(raw.get("format", "")),
        size_hint=str(raw.get("size_hint", "")),
        notes=str(raw.get("notes", "")),
        manifest=str(raw.get("manifest", "manifest.json")),
        provider=str(raw.get("provider", ds.provider)),
        licence=str(raw.get("licence", ds.licence)),
        dataset_id=ds.id,
    )
    if not entry.id:
        raise ConfigError(f"catalogue entry without id under dataset '{ds.id}'")
    if kind == "remote" and not entry.updatable:
        raise ConfigError(f"remote catalogue '{entry.id}' requires 'url' and 'target_dir'")
    if kind in ("local_volume", "local_store") and not entry.path:
        raise ConfigError(f"local catalogue '{entry.id}' requires 'path'")
    return entry


def load_config(path: str | Path) -> Config:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise ConfigError(f"config file not found: {p}")
    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}

    store_root = Path(str(raw.get("store_root", "~/oasis-catalog-store"))).expanduser()
    if not store_root.is_absolute():
        store_root = (p.parent / store_root).resolve()

    datasets: list[Dataset] = []
    for item in raw.get("datasets") or []:
        kind = str(item.get("kind", ""))
        if kind not in VALID_KINDS:
            raise ConfigError(f"dataset '{item.get('id', '?')}': invalid kind '{kind}'")
        ds = Dataset(
            id=str(item.get("id", "")),
            title=str(item.get("title", "")),
            kind=kind,
            access=dict(item.get("access") or {}),
            provider=str(item.get("provider", "")),
            licence=str(item.get("licence", "")),
        )
        if not ds.id:
            raise ConfigError("dataset entry without id")
        if kind == "remote" and not ds.access.get("base_url"):
            raise ConfigError(f"dataset '{ds.id}': remote requires access.base_url")
        if kind in ("local_volume", "local_store") and not ds.access.get("path"):
            raise ConfigError(f"dataset '{ds.id}': {kind} requires access.path")
        ds.catalogues = [_entry(ds, c, kind) for c in item.get("catalogues") or []]
        datasets.append(ds)

    return Config(store_root=store_root, datasets=datasets, config_path=p)
