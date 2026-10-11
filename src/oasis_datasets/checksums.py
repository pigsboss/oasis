"""Checksum manifest discovery, parsing, file matching, and hashing.

Manifest conventions (auto-discovered at the catalogue path, depth 1-2):
  _MD5SUM.txt  MD5SUM.txt  md5sum.txt  *.md5.txt  *.md5sum.txt  *.sha256  *.sha256sum

Hash-content semantics are auto-calibrated per manifest: Gaia/WISE digest the
compressed bytes; TESS digests the decompressed stream (see DSM-001 §2).
"""

from __future__ import annotations

import bz2
import gzip
import hashlib
import lzma
import re
from dataclasses import dataclass, field
from pathlib import Path

MANIFEST_PATTERNS = (
    "_MD5SUM.txt", "MD5SUM.txt", "md5sum.txt",
    "*.md5.txt", "*.md5sum.txt", "*.sha256", "*.sha256sum",
)
_LINE = re.compile(r"^([0-9a-fA-F]{32}|[0-9a-fA-F]{64})[ \t]+\*?(.+?)\s*$")
_OPENERS = {".gz": gzip.open, ".bz2": bz2.open, ".xz": lzma.open}
CANDIDATE_SUFFIXES = ("", ".gz", ".bz2", ".xz")


@dataclass
class ManifestEntry:
    digest: str
    name: str

    @property
    def alg(self) -> str:
        return "md5" if len(self.digest) == 32 else "sha256"


@dataclass
class Manifest:
    path: Path
    root: Path
    entries: list[ManifestEntry] = field(default_factory=list)
    content: str = "unknown"  # compressed | decompressed


def discover(catalogue_root: Path) -> list[Path]:
    """Find checksum manifests at the root and one directory below."""
    if not catalogue_root.is_dir():
        return []
    found: list[Path] = []

    def scan(directory: Path) -> None:
        for pattern in MANIFEST_PATTERNS:
            found.extend(sorted(directory.glob(pattern)))

    scan(catalogue_root)
    for sub in sorted(p for p in catalogue_root.iterdir() if p.is_dir()):
        scan(sub)

    out: list[Path] = []
    seen: set[Path] = set()
    for path in found:
        key = path.resolve()
        if key not in seen:
            seen.add(key)
            out.append(path)
    return out


def parse(path: Path, root: Path) -> Manifest:
    entries: list[ManifestEntry] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = _LINE.match(line)
        if match:
            entries.append(ManifestEntry(digest=match.group(1).lower(), name=match.group(2)))
    return Manifest(path=path, root=root, entries=entries)


def resolve_file(root: Path, name: str) -> Path | None:
    for suffix in CANDIDATE_SUFFIXES:
        candidate = root / (name + suffix)
        if candidate.is_file():
            return candidate
    return None


def hash_file(path: Path, alg: str, content: str) -> str:
    h = hashlib.new(alg)
    if content == "decompressed" and path.suffix in _OPENERS:
        with _OPENERS[path.suffix](path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
    else:
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
    return h.hexdigest()


def calibrate(manifest: Manifest, probe_pool: int = 12) -> str:
    """Decide whether digests cover compressed bytes or the decompressed stream.

    Probes the smallest existing file among the first `probe_pool` entries;
    defaults to "compressed" when unverifiable.
    """
    if manifest.content != "unknown":
        return manifest.content
    pairs: list[tuple[ManifestEntry, Path]] = []
    for entry in manifest.entries[:probe_pool]:
        path = resolve_file(manifest.root, entry.name)
        if path:
            pairs.append((entry, path))
    if not pairs:
        manifest.content = "compressed"
        return manifest.content
    entry, probe = min(pairs, key=lambda pair: pair[1].stat().st_size)
    if hash_file(probe, entry.alg, "compressed") == entry.digest:
        manifest.content = "compressed"
    elif probe.suffix in _OPENERS and hash_file(probe, entry.alg, "decompressed") == entry.digest:
        manifest.content = "decompressed"
    else:
        manifest.content = "compressed"  # unverifiable: assume default
    return manifest.content
