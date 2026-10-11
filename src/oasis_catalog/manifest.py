"""Delivery manifest I/O.

Header: generated_at + target_dir.
Files:  id | path | bytes | sha256 | version | epoch | provider | licence | source_url
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

MANIFEST_NAME = "manifest.json"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class FileEntry:
    id: str
    path: str
    bytes: int
    sha256: str
    version: str
    epoch: str
    provider: str
    licence: str
    source_url: str = ""


@dataclass
class Manifest:
    generated_at: str
    target_dir: str
    files: list[FileEntry] = field(default_factory=list)


def load_manifest(target_dir: Path) -> Manifest | None:
    p = target_dir / MANIFEST_NAME
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    files = [
        FileEntry(
            id=str(fe.get("id", "")),
            path=str(fe.get("path", "")),
            bytes=int(fe.get("bytes", 0)),
            sha256=str(fe.get("sha256", "")),
            version=str(fe.get("version", "")),
            epoch=str(fe.get("epoch", "")),
            provider=str(fe.get("provider", "")),
            licence=str(fe.get("licence", "")),
            source_url=str(fe.get("source_url", "")),
        )
        for fe in data.get("files", [])
    ]
    # tolerate the early v0.1 header key ("catalogue") for forward compatibility
    tdir = str(data.get("target_dir") or data.get("catalogue") or "")
    return Manifest(generated_at=str(data.get("generated_at", "")), target_dir=tdir, files=files)


def save_manifest(target_dir: Path, manifest: Manifest) -> Path:
    p = target_dir / MANIFEST_NAME
    payload = {
        "generated_at": manifest.generated_at,
        "target_dir": manifest.target_dir,
        "files": [asdict(f) for f in manifest.files],
    }
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p
