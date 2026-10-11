"""Remote→local mirror: parallel range download + resume (DSM-002 §3.2).

Layout: <storage>/oasis-datasets/<dataset_id>/<version>/<filename> + manifest.json
(store manifest protocol + `product` block). Safety: dry-run unless apply;
*.part files are used for resume and removed on success; sha256 recorded.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import socket
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

UA = "oasis-datasets-mirror/0.1"
MIN_PARALLEL_BYTES = 8 * 1024 * 1024   # below this, a single stream is used


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _version_token(last_modified: str | None, fallback: str | None = None) -> str:
    if last_modified:
        try:
            ts = parsedate_to_datetime(last_modified).astimezone(timezone.utc)
            return ts.strftime("%Y%m%dT%H%M%SZ")
        except (TypeError, ValueError):
            pass
    if fallback:
        safe = re.sub(r"[^0-9A-Za-z]+", "-", fallback).strip("-")
        if safe:
            return safe
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def head(url: str, timeout: float = 20.0) -> dict:
    """HEAD probe; falls back to a 1-byte Range GET. Returns lowercase headers."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {k.lower(): v for k, v in resp.headers.items()}
    except urllib.error.HTTPError as exc:
        if exc.code not in (403, 405, 501):
            raise
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Range": "bytes=0-0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return {k.lower(): v for k, v in resp.headers.items()}


def plan(dataset: dict, channel: dict, storage: dict) -> dict:
    """Dry-run plan: network probe + destination layout (read-only)."""
    url = str(channel.get("url", ""))
    info = head(url)
    size = int(info.get("content-length") or 0)
    version = _version_token(info.get("last-modified"))
    base = Path(str((storage.get("access") or {}).get("path", ""))).expanduser()
    filename = Path(urllib.parse.urlparse(url).path).name or f"{dataset.get('id')}.bin"
    dest_dir = base / "oasis-datasets" / str(dataset.get("id")) / version
    return {"url": url, "size": size, "version": version, "dest_dir": dest_dir,
            "dest_file": dest_dir / filename,
            "accept_ranges": "bytes" in str(info.get("accept-ranges", "")).lower()}


def _chunk_ranges(size: int, parallel: int) -> list[tuple[int, int]]:
    parts = max(1, min(parallel, size // MIN_PARALLEL_BYTES or 1))
    step = (size + parts - 1) // parts
    ranges = []
    start = 0
    while start < size:
        end = min(start + step, size) - 1
        ranges.append((start, end))
        start = end + 1
    return ranges


def _fetch_range(url: str, start: int, end: int, part: Path, timeout: float, emit) -> int:
    existing = part.stat().st_size if part.exists() else 0
    expect = end - start + 1
    if existing >= expect:
        return 0
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Range": f"bytes={start + existing}-{end}"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        mode = "ab" if existing else "wb"
        if existing and resp.status == 200:
            mode = "wb"   # server ignored Range: restart this part to avoid duplication
        with open(part, mode) as out:
            while True:
                block = resp.read(1 << 20)
                if not block:
                    break
                out.write(block)
    got = part.stat().st_size
    if got != expect:
        raise OSError(f"part short: {got}/{expect} ({part.name})")
    return got


def download(url: str, dest_file: Path, size: int, accept_ranges: bool, parallel: int,
             emit, timeout: float = 60.0) -> None:
    """Parallel (or single) download with resume via .part files."""
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    if accept_ranges and size >= MIN_PARALLEL_BYTES:
        ranges = _chunk_ranges(size, parallel)
        parts = [dest_file.with_suffix(dest_file.suffix + f".part{i}") for i in range(len(ranges))]
        with ThreadPoolExecutor(max_workers=len(ranges)) as pool:
            futures = {pool.submit(_fetch_range, url, start, end, part, timeout, emit): i
                       for i, ((start, end), part) in enumerate(zip(ranges, parts))}
            done = 0
            for future in as_completed(futures):
                index = futures[future]
                got = future.result()
                done += 1
                emit("log", {"text": f"part {index + 1}/{len(parts)} "
                                     f"({'resumed' if got == 0 else 'fetched'}) "
                                     f"{_human(parts[index].stat().st_size)}"})
                emit("progress", {"done": done, "total": len(parts)})
        tmp = dest_file.with_suffix(dest_file.suffix + ".assembling")
        with open(tmp, "wb") as out:
            for part in parts:
                with open(part, "rb") as fh:
                    shutil.copyfileobj(fh, out, length=1 << 20)
        os.replace(tmp, dest_file)
        for part in parts:
            part.unlink(missing_ok=True)
    else:
        part = dest_file.with_suffix(dest_file.suffix + ".part0")
        if size:
            _fetch_range(url, 0, size - 1, part, timeout, emit)
        else:
            # unknown length: stream the whole body, no Range
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp, open(part, "wb") as out:
                while True:
                    block = resp.read(1 << 20)
                    if not block:
                        break
                    out.write(block)
        os.replace(part, dest_file)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def mirror_one(dataset: dict, channel: dict, storage: dict, emit,
               parallel: int = 8) -> tuple[int, dict | None]:
    url = str(channel.get("url", ""))
    try:
        info = head(url)
    except (urllib.error.URLError, socket.timeout, ssl.SSLError, OSError) as exc:
        emit("error", {"message": f"{dataset.get('id')}: HEAD failed: {exc}"})
        return 1, None
    size = int(info.get("content-length") or 0)
    accept_ranges = "bytes" in str(info.get("accept-ranges", "")).lower()
    version = _version_token(info.get("last-modified"))
    base = Path(str((storage.get("access") or {}).get("path", ""))).expanduser()
    filename = Path(urllib.parse.urlparse(url).path).name or f"{dataset.get('id')}.bin"
    dest_dir = base / "oasis-datasets" / str(dataset.get("id")) / version
    dest_file = dest_dir / filename
    if dest_file.exists():
        digest = sha256_file(dest_file)
        emit("log", {"text": f"{dataset.get('id')}: already present "
                             f"({_human(dest_file.stat().st_size)}, sha256={digest[:16]}…) -> {dest_file}"})
        return 0, {"file": dest_file, "sha256": digest, "size": dest_file.stat().st_size,
                   "version": version, "url": url, "exists": True}
    emit("log", {"text": f"{dataset.get('id')}: {url} -> {dest_file} "
                         f"({_human(size)}, ranges={accept_ranges}, parallel={parallel})"})
    started = time.monotonic()
    try:
        download(url, dest_file, size, accept_ranges, parallel, emit)
    except (urllib.error.URLError, socket.timeout, ssl.SSLError, OSError) as exc:
        emit("error", {"message": f"{dataset.get('id')}: download failed: {exc} "
                                  "(part files kept for resume)"})
        return 1, None
    elapsed = time.monotonic() - started
    if size and dest_file.stat().st_size != size:
        emit("error", {"message": f"{dataset.get('id')}: size mismatch "
                                  f"{dest_file.stat().st_size}/{size}"})
        return 1, None
    digest = sha256_file(dest_file)
    emit("log", {"text": f"{dataset.get('id')}: done {_human(dest_file.stat().st_size)} in "
                         f"{elapsed:.1f}s ({_human(int(dest_file.stat().st_size / max(elapsed, 1e-6)))}/s) "
                         f"sha256={digest[:16]}…"})
    return 0, {"file": dest_file, "sha256": digest, "size": dest_file.stat().st_size,
               "version": version, "url": url, "exists": False}


def write_manifest(dataset: dict, results: list[dict], emit) -> Path | None:
    if not results:
        return None
    dest_dir = results[0]["file"].parent
    files = []
    for item in results:
        files.append({
            "id": str(dataset.get("id")),
            "path": item["file"].name,
            "bytes": item["size"],
            "sha256": item["sha256"],
            "version": item["version"],
            "epoch": item["version"],
            "provider": dataset.get("publisher", ""),
            "licence": (dataset.get("licence") or {}).get("name", ""),
            "source_url": item.get("url", ""),
        })
    manifest = {
        "generated_at": now_iso(),
        "target_dir": str(dest_dir),
        "product": {"kind": "mirror", "source_dataset": str(dataset.get("id")),
                    "generated_by": "oasis-datasets/mirror"},
        "files": files,
    }
    path = dest_dir / "manifest.json"
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)
    emit("log", {"text": f"manifest -> {path}"})
    return path


def _human(nbytes: int | float) -> str:
    value = float(nbytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1000 or unit == "TB":
            return f"{value:.1f} {unit}"
        value /= 1000
    return f"{value:.1f} TB"
