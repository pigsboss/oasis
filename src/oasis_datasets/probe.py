"""Channel probing: connectivity test + version determination (DSM-003 §6 `probe`).

Per protocol:
  https — HEAD, falling back to a 1-byte Range GET when HEAD is refused;
          version from Last-Modified / ETag per version_rule.
  file  — path readable + containing volume mounted + free capacity;
          version from mtime / checksum-manifest mtime.
  ssh   — non-interactive `ssh test -e` against host+path (BatchMode).

Read-only: never writes to the channel; network calls are timeout-bounded.
"""

from __future__ import annotations

import os
import shlex
import shutil
import socket
import ssl
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

PLACEHOLDER = "<todo"
UA = "oasis-datasets-probe/0.1"


@dataclass
class ProbeResult:
    channel_id: str
    protocol: str
    state: str                  # ok | fail | skipped
    version: str | None = None
    detail: str = ""
    latency_ms: int | None = None


def _iso_mtime(path: Path) -> str:
    ts = path.stat().st_mtime
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _mount_root(path: Path) -> Path:
    """Closest existing ancestor that is a mount point (capacity reporting)."""
    probe = path if path.exists() else path.parent
    while not probe.exists() and probe.parent != probe:
        probe = probe.parent
    while not os.path.ismount(probe) and probe.parent != probe:
        probe = probe.parent
    return probe


def _human(nbytes: int) -> str:
    value = float(nbytes)
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if value < 1000 or unit == "PB":
            return f"{value:.1f} {unit}"
        value /= 1000
    return f"{value:.1f} PB"


def _is_placeholder(text: str) -> bool:
    return PLACEHOLDER in str(text).lower()


def _file_version(rule: dict, path: Path) -> str | None:
    rtype = (rule or {}).get("type")
    if rtype == "release":
        return (rule or {}).get("value")
    if rtype in ("last_modified", "checksum_mtime"):
        return f"mtime={_iso_mtime(path)}" if path.exists() else None
    return None


def _https_version(rule: dict, last_modified: str | None, etag: str | None) -> str | None:
    rtype = (rule or {}).get("type")
    if rtype == "last_modified":
        return last_modified
    if rtype == "etag":
        return etag
    if rtype == "release":
        return (rule or {}).get("value")
    return None


def probe_file(channel: dict, timeout: float = 10.0) -> ProbeResult:
    cid = str(channel.get("id", "?"))
    raw = str(channel.get("path", ""))
    if not raw or _is_placeholder(raw):
        return ProbeResult(cid, "file", "skipped", detail=f"path not configured ({raw or 'empty'})")
    path = Path(raw).expanduser()
    if not path.exists():
        mount = _mount_root(path)
        if os.path.ismount(mount):
            return ProbeResult(cid, "file", "fail",
                               detail=f"path missing ({path}); volume {mount} is mounted")
        return ProbeResult(cid, "file", "fail", detail=f"path missing and volume not mounted ({path})")
    if path.is_dir() and not os.access(path, os.R_OK | os.X_OK):
        return ProbeResult(cid, "file", "fail", detail=f"not readable ({path})")
    if path.is_file() and not os.access(path, os.R_OK):
        return ProbeResult(cid, "file", "fail", detail=f"not readable ({path})")

    mount = _mount_root(path)
    try:
        usage = shutil.disk_usage(mount)
        cap = f"volume {mount}: {_human(usage.free)} free / {_human(usage.total)}"
    except OSError:
        cap = f"volume {mount}: capacity unknown"
    version = _file_version(channel.get("version_rule") or {}, path)
    detail = cap
    checksum = channel.get("checksum") or {}
    manifest = checksum.get("manifest")
    if manifest:
        manifest_path = path / str(manifest) if path.is_dir() else path.parent / str(manifest)
        if manifest_path.is_file():
            detail += f"  manifest={manifest} ({_iso_mtime(manifest_path)})"
        else:
            detail += f"  manifest={manifest} (not found)"
    return ProbeResult(cid, "file", "ok", version=version, detail=detail)


def _http_probe(url: str, timeout: float) -> tuple[str, dict[str, str], int]:
    """Return (method used, headers, status). HEAD first, Range-GET fallback."""
    headers: dict[str, str] = {}
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return "HEAD", headers, resp.status
    except urllib.error.HTTPError as exc:
        if exc.code not in (403, 405, 501):
            raise
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Range": "bytes=0-0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        headers = {k.lower(): v for k, v in resp.headers.items()}
        # do not read the body: servers that ignore Range must not be drained
        return "Range", headers, resp.status


def probe_https(channel: dict, timeout: float = 10.0) -> ProbeResult:
    cid = str(channel.get("id", "?"))
    url = str(channel.get("url", ""))
    if not url or _is_placeholder(url):
        return ProbeResult(cid, "https", "skipped", detail=f"url not configured ({url or 'empty'})")
    started = time.monotonic()
    try:
        method, headers, status = _http_probe(url, timeout)
    except urllib.error.HTTPError as exc:
        return ProbeResult(cid, "https", "fail", detail=f"HTTP {exc.code} {exc.reason}",
                           latency_ms=int((time.monotonic() - started) * 1000))
    except (urllib.error.URLError, socket.timeout, ssl.SSLError, OSError) as exc:
        return ProbeResult(cid, "https", "fail", detail=f"{type(exc).__name__}: {exc}",
                           latency_ms=int((time.monotonic() - started) * 1000))
    latency = int((time.monotonic() - started) * 1000)
    lat = headers.get("last-modified")
    etag = headers.get("etag")
    size = headers.get("content-length")
    version = _https_version(channel.get("version_rule") or {}, lat, etag)
    notes = [f"HTTP {status} ({method})"]
    if size:
        notes.append(f"size={_human(int(size))}")
    return ProbeResult(cid, "https", "ok", version=version, detail="  ".join(notes), latency_ms=latency)


def probe_ssh(channel: dict, timeout: float = 10.0) -> ProbeResult:
    cid = str(channel.get("id", "?"))
    host = str(channel.get("host", ""))
    path = str(channel.get("path", ""))
    if not host or not path or _is_placeholder(host) or _is_placeholder(path):
        return ProbeResult(cid, "ssh", "skipped",
                           detail=f"host/path not configured ({host or '?'}:{path or '?'})")
    cmd = ["ssh", "-o", "BatchMode=yes", "-o", f"ConnectTimeout={int(timeout)}",
           "-o", "StrictHostKeyChecking=accept-new", host,
           f"test -e {shlex.quote(path)} && echo OK"]
    started = time.monotonic()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
    except subprocess.TimeoutExpired:
        return ProbeResult(cid, "ssh", "fail", detail=f"ssh timeout (>{int(timeout)}s)",
                           latency_ms=int((time.monotonic() - started) * 1000))
    latency = int((time.monotonic() - started) * 1000)
    if proc.returncode == 0 and "OK" in proc.stdout:
        return ProbeResult(cid, "ssh", "ok", detail=f"{host}:{path} reachable", latency_ms=latency)
    err = (proc.stderr or proc.stdout).strip().splitlines()
    if err:
        detail = f"{host}: {err[-1]}"
    elif proc.returncode == 1:
        detail = f"{host}: path not found ({path})"
    else:
        detail = f"{host}: exit {proc.returncode}"
    return ProbeResult(cid, "ssh", "fail", detail=detail, latency_ms=latency)


def probe_channel(channel: dict, timeout: float = 10.0) -> ProbeResult:
    protocol = channel.get("protocol")
    if protocol == "file":
        return probe_file(channel, timeout)
    if protocol == "https":
        return probe_https(channel, timeout)
    if protocol == "ssh":
        return probe_ssh(channel, timeout)
    return ProbeResult(str(channel.get("id", "?")), str(protocol), "fail",
                       detail=f"unsupported protocol '{protocol}'")


def probe_inventory(datasets: list[dict], ids: list[str], channel_id: str | None = None,
                    timeout: float = 10.0) -> list[tuple[str, list[ProbeResult]]]:
    out = []
    for ds in datasets:
        ds_id = str(ds.get("id", "?"))
        if ids and ds_id not in ids:
            continue
        results = []
        for channel in ds.get("channels") or []:
            if channel_id and channel.get("id") != channel_id:
                continue
            results.append(probe_channel(channel, timeout=timeout))
        out.append((ds_id, results))
    return out
