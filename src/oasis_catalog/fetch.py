"""HTTP fetch with resume support and snapshot metadata (stdlib only)."""

from __future__ import annotations

import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

USER_AGENT = "oasis-catalog/0.1 (+https://github.com/pigsboss/oasis)"
CHUNK = 1 << 16
PROGRESS_STEP = 8 << 20  # print progress every 8 MiB


@dataclass
class DownloadInfo:
    path: Path
    bytes: int
    last_modified: str
    fetched_at: str
    resumed_from: int


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def download(url: str, dest: Path, force: bool = False, timeout: int = 120) -> DownloadInfo:
    part = dest.parent / (dest.name + ".part")
    if force:
        for p in (dest, part):
            if p.exists():
                p.unlink()

    initial = part.stat().st_size if part.exists() else 0
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    if initial > 0:
        req.add_header("Range", f"bytes={initial}-")

    fetched_at = now_iso()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        code = resp.getcode()
        last_modified = resp.headers.get("Last-Modified") or ""
        if code == 206:
            content_range = resp.headers.get("Content-Range") or ""
            total = int(content_range.rsplit("/", 1)[1]) if "/" in content_range else None
            mode, done = "ab", initial
        else:  # server ignored Range: restart from scratch
            length = resp.headers.get("Content-Length")
            total = int(length) if length and length.isdigit() else None
            mode, done = "wb", 0

        next_report = (done // PROGRESS_STEP + 1) * PROGRESS_STEP
        with open(part, mode) as fh:
            while True:
                chunk = resp.read(CHUNK)
                if not chunk:
                    break
                fh.write(chunk)
                done += len(chunk)
                if done >= next_report:
                    if total:
                        print(f"    ... {done / 1048576:.1f}/{total / 1048576:.1f} MiB ({100.0 * done / total:.0f}%)")
                    else:
                        print(f"    ... {done / 1048576:.1f} MiB")
                    next_report += PROGRESS_STEP

    size = part.stat().st_size
    if total is not None and size != total:
        raise OSError(f"incomplete download: {size} bytes != expected {total} ({url})")
    part.replace(dest)
    return DownloadInfo(path=dest, bytes=size, last_modified=last_modified,
                        fetched_at=fetched_at, resumed_from=initial)


def is_unchanged(url: str, since: str, timeout: int = 30) -> bool:
    """True when the remote resource is unchanged since `since` (RFC 1123 date)."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "If-Modified-Since": since, "Range": "bytes=0-0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.getcode() == 304
    except urllib.error.HTTPError as exc:
        return exc.code == 304
    except Exception:
        return False
