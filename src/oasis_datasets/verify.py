"""Dataset verification: manifest discovery + sampled or full digest checking."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .checksums import Manifest, calibrate, discover, hash_file, parse, resolve_file


@dataclass
class FileResult:
    name: str
    status: str  # OK | FAIL | MISSING
    detail: str = ""


@dataclass
class ManifestReport:
    manifest: Manifest
    listed: int
    missing_listed: int = 0
    results: list[FileResult] = field(default_factory=list)


def verify(catalogue_root: Path, sample: int = 8, full: bool = False) -> tuple[list[ManifestReport], int]:
    """Verify listed files against discovered manifests.

    Returns (reports, failures). failures: number of problems (0 = clean);
    2 is returned via reports==[] when no manifest was found.
    """
    manifests = [parse(path, catalogue_root) for path in discover(catalogue_root)]
    if not manifests:
        return [], 2

    reports: list[ManifestReport] = []
    failures = 0
    for manifest in manifests:
        mode = calibrate(manifest)
        existing: list[tuple] = []
        missing = 0
        for entry in manifest.entries:
            path = resolve_file(manifest.root, entry.name)
            if path:
                existing.append((entry, path))
            else:
                missing += 1

        report = ManifestReport(manifest=manifest, listed=len(manifest.entries), missing_listed=missing)
        if missing:
            failures += 1
            report.results.append(FileResult(name=f"[{missing} listed file(s) not found]", status="MISSING"))

        if full:
            chosen = existing
        else:
            n = max(1, sample)
            if len(existing) <= n:
                chosen = existing
            else:
                step = len(existing) / n
                indices = sorted({int(i * step) for i in range(n)})
                chosen = [existing[i] for i in indices]

        for entry, path in chosen:
            digest = hash_file(path, entry.alg, mode)
            ok = digest == entry.digest
            if not ok:
                failures += 1
            report.results.append(
                FileResult(name=entry.name, status="OK" if ok else "FAIL",
                           detail="" if ok else f"{entry.alg} mismatch ({digest[:12]}… vs {entry.digest[:12]}…)")
            )
        reports.append(report)
    return reports, failures
