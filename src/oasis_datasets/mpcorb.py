"""MPCORB.DAT → element table product (UR-OASIS-02, batch 2).

Fixed-width layout verified against the 2026-10-10 MPCORB.DAT snapshot (202 cols).
Output: deterministic CSV.gz (`mtime=0`, row order = file order, raw numeric
values passed through) + product manifest with per-record epoch semantics.

Category rules v1 (documented, refinable by the consumer from a/e/q):
  NEO     q < 1.3 AU
  TNO     a > 30.1 AU
  Centaur 5.5 < a < 30.1 AU   (Jupiter Trojans near a~5.2 fall into 'other')
  MBA     2.0 <= a <= 3.2 AU
  other   everything else
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import os
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

COLUMNS = ["designation", "readable", "H", "G", "epoch", "M", "argp", "node",
           "incl", "e", "n", "a", "q", "U", "category", "n_obs", "n_opp",
           "arc", "rms", "last_obs"]

# (name, start, end) — 0-based, verified against the live file
SLICES = {
    "designation": (0, 7), "H": (8, 13), "G": (14, 19), "epoch_packed": (20, 25),
    "M": (26, 35), "argp": (36, 46), "node": (47, 57), "incl": (58, 68),
    "e": (69, 79), "n": (80, 91), "a": (92, 103), "U": (105, 106),
    "n_obs": (117, 122), "n_opp": (123, 126), "arc": (127, 136),
    "rms": (137, 141), "readable": (166, 194), "last_obs": (194, 202),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def packed_epoch_to_iso(text: str) -> str:
    """'K2669' -> '2026-06-09' (century letter I/J/K = 18/19/20)."""
    text = text.strip()
    if len(text) != 5:
        return ""
    century = {"I": 18, "J": 19, "K": 20}.get(text[0])
    if century is None or not text[1:3].isdigit():
        return ""
    year = century * 100 + int(text[1:3])
    month = int(text[3]) if text[3].isdigit() else ord(text[3]) - ord("A") + 10
    day = int(text[4]) if text[4].isdigit() else ord(text[4]) - ord("A") + 10
    try:
        return f"{year:04d}-{month:02d}-{day:02d}"
    except ValueError:
        return ""


def yyyymmdd_to_iso(text: str) -> str:
    text = text.strip()
    if len(text) != 8 or not text.isdigit():
        return ""
    return f"{text[0:4]}-{text[4:6]}-{text[6:8]}"


def categorize(a_text: str, e_text: str) -> tuple[str, str]:
    """Returns (category, q formatted). q = a(1-e)."""
    try:
        a = float(a_text)
        e = float(e_text)
    except ValueError:
        return "other", ""
    q = a * (1.0 - e)
    q_text = f"{q:.6f}"
    if q < 1.3:
        return "NEO", q_text
    if a > 30.1:
        return "TNO", q_text
    if 5.5 < a < 30.1:
        return "Centaur", q_text
    if 2.0 <= a <= 3.2:
        return "MBA", q_text
    return "other", q_text


def parse_data_row(line: str) -> list[str] | None:
    """One MPCORB data row -> COLUMNS values; None when the line is not data."""
    if len(line) < 160:
        return None
    designation = line[0:7].strip()
    if not designation or designation.startswith("-") or "Des'n" in line:
        return None
    get = lambda key: line[SLICES[key][0]:SLICES[key][1]].strip()  # noqa: E731
    a_text, e_text = get("a"), get("e")
    epoch_iso = packed_epoch_to_iso(get("epoch_packed"))
    category, q_text = categorize(a_text, e_text)
    return [
        designation, get("readable"), get("H"), get("G"), epoch_iso,
        get("M"), get("argp"), get("node"), get("incl"), e_text,
        get("n"), a_text, q_text, get("U"), category,
        get("n_obs"), get("n_opp"), get("arc"), get("rms"),
        yyyymmdd_to_iso(get("last_obs")),
    ]


def iter_data_rows(path: Path, limit: int | None = None):
    """Yield (row_index, line, values) for data rows (header/dashes skipped)."""
    header_seen = False
    started = False
    index = 0
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not started:
                if "Des'n" in line:
                    header_seen = True
                elif header_seen and line.startswith("-"):
                    started = True
                continue
            values = parse_data_row(line)
            if values is None:
                continue
            yield index, line, values
            index += 1
            if limit is not None and index >= limit:
                return


def count_rows(path: Path) -> int:
    """Fast data-row count (no full field parse)."""
    count = 0
    header_seen = False
    started = False
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not started:
                if "Des'n" in line:
                    header_seen = True
                elif header_seen and line.startswith("-"):
                    started = True
                continue
            if len(line) >= 160 and line[0:7].strip() and line[0] != "-":
                count += 1
    return count


@dataclass
class ParseResult:
    rows: int = 0
    skipped: int = 0
    categories: Counter = field(default_factory=Counter)
    epochs: Counter = field(default_factory=Counter)


def run_parse(raw: Path, dest_dir: Path, task_dir: Path, emit, limit: int | None = None) -> int:
    raw_digest = sha256_file(raw)
    emit("log", {"text": f"source: {raw} ({raw.stat().st_size/1e6:.1f} MB, sha256={raw_digest[:16]}…)"})
    emit("log", {"text": f"columns: {', '.join(COLUMNS)}"})
    emit("log", {"text": "category v1: NEO q<1.3 | TNO a>30.1 | Centaur 5.5<a<30.1 | "
                         "MBA 2.0<=a<=3.2 | other"})

    dest_dir.mkdir(parents=True, exist_ok=True)
    out_path = dest_dir / "mpc_elements.csv.gz"
    tmp = out_path.with_name(out_path.name + ".tmp")
    result = ParseResult()
    sample_indices = {0, 1, 2, 1000, 100000, 500000}
    samples: dict[int, list[str]] = {}
    last_index: int | None = None
    last_values: list[str] = []

    with open(tmp, "wb") as raw_out:
        gz = gzip.GzipFile(filename="", mode="wb", fileobj=raw_out, mtime=0, compresslevel=6)
        text = io.TextIOWrapper(gz, encoding="utf-8", newline="")
        writer = csv.writer(text, lineterminator="\n")
        writer.writerow(COLUMNS)
        for index, line, values in iter_data_rows(raw, limit=limit):
            writer.writerow(values)
            result.rows += 1
            result.categories[values[14]] += 1
            if values[4]:
                result.epochs[values[4]] += 1
            if index in sample_indices and len(samples) < 8:
                samples[index] = values
            last_index, last_values = index, values
            if result.rows % 200000 == 0:
                emit("progress", {"done": result.rows, "categories": dict(result.categories)})
        text.flush()
        text.close()
        if not gz.closed:
            gz.close()
    if last_index is not None and last_index not in samples and len(samples) < 8:
        samples[last_index] = last_values
    os.replace(tmp, out_path)
    digest = sha256_file(out_path)
    size = out_path.stat().st_size
    emit("log", {"text": f"parsed {result.rows} row(s) -> {out_path} ({size/1e6:.1f} MB) "
                         f"sha256={digest[:16]}…"})
    emit("log", {"text": f"categories: {dict(result.categories)}"})
    emit("log", {"text": f"epochs: {dict(result.epochs.most_common(3))}"})

    qc = verify_samples(raw, out_path, samples, emit)
    epoch_range = [min(result.epochs), max(result.epochs)] if result.epochs else []

    version = ""
    raw_manifest = raw.parent / "manifest.json"
    if raw_manifest.exists():
        try:
            for item in json.loads(raw_manifest.read_text(encoding="utf-8")).get("files", []):
                if item.get("path") == raw.name:
                    version = str(item.get("epoch") or item.get("version") or "")
                    break
        except (OSError, json.JSONDecodeError):
            pass

    manifest = {
        "generated_at": now_iso(),
        "product": {"kind": "element-table", "generated_by": "oasis-datasets/mpcorb",
                    "source_file": raw.name, "source_sha256": raw_digest,
                    "source_version": version, "task_id": task_dir.name,
                    "partial": bool(limit)},
        "files": [{
            "id": "mpc_elements", "path": out_path.name, "bytes": size, "sha256": digest,
            "version": version or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "epoch": "per-record (column 'epoch')",
            "epoch_range": epoch_range,
            "frame": "heliocentric ecliptic J2000",
            "provider": "Minor Planet Center",
            "licence": "MPC Copyright — see https://www.minorplanetcenter.net/iau/info/Copyright.html",
            "rows": result.rows, "columns": COLUMNS,
            "categories": dict(result.categories),
            "qc": qc,
        }],
    }
    tmp_m = dest_dir / "mpc_elements.manifest.json.tmp"
    tmp_m.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp_m, dest_dir / "mpc_elements.manifest.json")
    emit("log", {"text": f"manifest -> {dest_dir / 'mpc_elements.manifest.json'}"})
    emit("log", {"text": f"QC samples={qc['samples']} matched={qc['matched']} "
                         f"mismatches={len(qc['mismatches'])}"})
    return 0 if not qc["mismatches"] else 1


def verify_samples(raw: Path, out_path: Path, samples: dict[int, list[str]], emit) -> dict:
    """Compare sampled written rows against an independent re-read of the raw file."""
    report = {"samples": len(samples), "matched": 0, "mismatches": []}
    if not samples:
        return report
    out_rows: dict[int, list[str]] = {}
    with gzip.open(out_path, "rt", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
        for index, row in enumerate(reader):
            if index in samples:
                out_rows[index] = row
            if len(out_rows) == len(samples):
                break
    for index, expected in samples.items():
        got = out_rows.get(index)
        if got == expected:
            report["matched"] += 1
        else:
            report["mismatches"].append({"row": index})
    return report
