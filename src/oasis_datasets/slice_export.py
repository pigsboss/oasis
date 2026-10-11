"""Slice export engine (DSM-002 §3.4, DSM-003 §5) — M3.

Pipeline: per-chunk parallel map (parse → filter → per-chunk tmp CSV.gz, mtime=0)
→ ordered concatenation (multi-member gzip; gzip -d compatible; byte-level
deterministic) → QC (counts + sample trace back to source) → manifest + CREDITS.

Specs sharing (source, channel) are produced in a single scan (Gaia T1/T2/T3).
Resume: per-chunk accounting in the task dir (chunks.jsonl); temps staged next
to the output under .oasis-staging-<task_id>/.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import os
import re
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

OPS = {"le", "lt", "ge", "gt", "eq", "ne", "between", "in"}
SPEC_KEYS = {"id", "source", "channel", "select", "columns", "output", "determinism",
             "qc", "execution", "x-note"}
SELECT_KEYS = {"column", "op", "value"}
OUTPUT_KEYS = {"storage", "to_path", "path", "filename"}
DETERMINISM_KEYS = {"sort_by", "gzip_mtime"}
QC_KEYS = {"sample", "source_trace"}
EXECUTION_KEYS = {"parallel", "resume"}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_spec(path: Path) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: slice spec must be a mapping")
    return data


def _unknown(errors: list[str], obj: dict, allowed: set[str], where: str) -> None:
    for key in obj:
        if key not in allowed and not str(key).startswith("x-"):
            errors.append(f"{where}: unknown field '{key}'")


def validate_spec(spec: dict, inventory_ids: set[str], storage_ids: set[str],
                  slice_id: str | None = None) -> tuple[list[str], list[str]]:
    """Structural validation per DSM-003 §5; heavy checks (columns/header) live in check_source."""
    errors: list[str] = []
    warnings: list[str] = []
    _unknown(errors, spec, SPEC_KEYS, "slice")
    sid = str(spec.get("id", ""))
    if not re.match(r"^[a-z0-9_]+$", sid):
        errors.append("slice: id must match [a-z0-9_]+")
    if slice_id and sid != slice_id:
        errors.append(f"slice: id '{sid}' must equal file id '{slice_id}'")
    source = spec.get("source")
    if not source:
        errors.append("slice: source required")
    elif source not in inventory_ids:
        errors.append(f"slice: source '{source}' not in inventory")
    columns = spec.get("columns")
    if not isinstance(columns, list) or not columns or not all(isinstance(c, str) for c in columns):
        errors.append("slice: columns must be a non-empty list of strings")
    else:
        if len(set(columns)) != len(columns):
            warnings.append("slice: duplicate column names")
    select = spec.get("select") or []
    if not isinstance(select, list):
        errors.append("slice: select must be a list")
    else:
        for i, rule in enumerate(select):
            where = f"slice.select[{i}]"
            if not isinstance(rule, dict):
                errors.append(f"{where}: must be a mapping")
                continue
            _unknown(errors, rule, SELECT_KEYS, where)
            if not rule.get("column"):
                errors.append(f"{where}: column required")
            op = rule.get("op")
            if op not in OPS:
                errors.append(f"{where}: op must be one of {sorted(OPS)}")
                continue
            value = rule.get("value", None)
            if op == "between" and not (isinstance(value, list) and len(value) == 2):
                errors.append(f"{where}: between requires [lo, hi]")
            if op == "in" and not isinstance(value, list):
                errors.append(f"{where}: in requires a list")
    output = spec.get("output")
    if not isinstance(output, dict):
        errors.append("slice: output mapping required")
    else:
        _unknown(errors, output, OUTPUT_KEYS, "slice.output")
        storage = output.get("storage")
        to_path = output.get("to_path")
        if storage and storage not in storage_ids:
            errors.append(f"slice.output: storage '{storage}' not registered")
        if not storage and not to_path:
            errors.append("slice.output: storage or to_path required")
        if not output.get("path"):
            errors.append("slice.output: path required")
    for block, allowed in (("determinism", DETERMINISM_KEYS), ("qc", QC_KEYS),
                           ("execution", EXECUTION_KEYS)):
        value = spec.get(block)
        if value is not None and not isinstance(value, dict):
            errors.append(f"slice: {block} must be a mapping")
        elif isinstance(value, dict):
            _unknown(errors, value, allowed, f"slice.{block}")
    return errors, warnings


# ── source access ───────────────────────────────────────────────
@dataclass
class Source:
    dataset_id: str
    channel_id: str
    root: Path
    chunks: list[Path] = field(default_factory=list)


def resolve_source(spec: dict, inventory) -> tuple[Source | None, str]:
    ds = next((d for d in inventory.datasets if d.get("id") == spec.get("source")), None)
    if ds is None:
        return None, f"source dataset '{spec.get('source')}' not found in inventory"
    channel_id = spec.get("channel")
    channels = [c for c in (ds.get("channels") or [])
                if c.get("protocol") == "file" and c.get("path")]
    if channel_id:
        channels = [c for c in channels if c.get("id") == channel_id]
    if not channels:
        return None, "no usable file channel (check 'channel' or inventory)"
    channel = channels[0]
    root = Path(str(channel["path"])).expanduser()
    if not root.is_dir():
        return None, f"channel path is not a directory: {root}"
    chunks = sorted(p for p in root.glob("*.csv.gz") if p.is_file())
    if not chunks:
        return None, f"no *.csv.gz chunks under {root}"
    return Source(str(ds.get("id")), str(channel.get("id")), root, chunks), ""


def read_header(chunk: Path) -> list[str]:
    """ECSV: skip '#' metadata lines; the first plain line is the CSV header."""
    with gzip.open(chunk, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            return next(csv.reader([line.rstrip("\n")]))
    return []


def check_columns(spec: dict, source: Source) -> list[str]:
    header = read_header(source.chunks[0])
    if not header:
        return [f"cannot read header from {source.chunks[0].name}"]
    columns = set(header)
    missing = [c for c in spec.get("columns") or [] if c not in columns]
    errors = [f"column '{c}' not in source header" for c in missing]
    for rule in spec.get("select") or []:
        col = rule.get("column")
        if col and col not in columns:
            errors.append(f"select column '{col}' not in source header")
    return errors


# ── row filtering ───────────────────────────────────────────────
def _to_number(text: str):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def _match(rule: dict, values: dict[str, str]) -> bool | None:
    """True/False, or None when the referenced value is missing (row dropped+counted)."""
    raw = values.get(str(rule.get("column")))
    if raw is None or raw == "" or raw.lower() == "null":
        return None
    op = rule.get("op")
    value = rule.get("value")
    if op in ("between", "in") or isinstance(value, (int, float)):
        num = _to_number(raw)
        if op == "between":
            low, high = _to_number(str(value[0])), _to_number(str(value[1]))
            if num is None or low is None or high is None:
                return None
            return low <= num <= high
        if op == "in":
            candidates = [_to_number(str(v)) for v in value]
            if num is None or any(c is None for c in candidates):
                return raw in [str(v) for v in value]
            return any(num == c for c in candidates)
        target = _to_number(str(value))
        if num is None or target is None:
            return None
        return {"le": num <= target, "lt": num < target, "ge": num >= target,
                "gt": num > target, "eq": num == target, "ne": num != target}[op]
    return {"eq": raw == str(value), "ne": raw != str(value)}.get(op, True)


# ── per-chunk processing ────────────────────────────────────────
@dataclass
class ChunkResult:
    chunk: int
    rows_total: int = 0
    per_spec: dict = field(default_factory=dict)   # spec_id -> {"rows": n, "null": n, "min": .., "max": ..}
    temp_files: dict = field(default_factory=dict)  # spec_id -> Path
    sizes: dict = field(default_factory=dict)       # spec_id -> bytes
    provenance: dict = field(default_factory=dict)  # spec_id -> [(line_no, values list)]


def process_chunk(chunk_index: int, chunk_path: Path, specs: list[dict],
                  temps_dir: Path, sample_n: int) -> ChunkResult:
    """Parse one chunk once; write one tmp gz per spec; collect QC provenance."""
    header = read_header(chunk_path)
    if not header:
        raise ValueError(f"cannot read header from {chunk_path.name}")
    full_map = {col: i for i, col in enumerate(header)}
    out_maps = [{col: full_map[col] for col in spec["columns"]} for spec in specs]

    writers, handles = {}, {}
    result = ChunkResult(chunk=chunk_index)
    for spec in specs:
        spec_id = spec["id"]
        temp = temps_dir / spec_id / f"{chunk_index:05d}.csv.gz"
        temp.parent.mkdir(parents=True, exist_ok=True)
        raw = open(temp, "wb")
        gz = gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=6)
        text = io.TextIOWrapper(gz, encoding="utf-8", newline="")
        handles[spec_id] = (raw, gz, text)
        writers[spec_id] = csv.writer(text, lineterminator="\n")
        result.per_spec[spec_id] = {"rows": 0, "null": 0, "min": None, "max": None}
        result.temp_files[spec_id] = temp
        result.provenance[spec_id] = []

    try:
        with gzip.open(chunk_path, "rt", encoding="utf-8", errors="replace") as fh:
            reader = csv.reader(fh)
            header_seen = False
            for line_no, row in enumerate(reader, 0):
                if not header_seen:
                    if not row or row[0].startswith("#"):
                        continue
                    header_seen = True
                    continue
                if not row:
                    continue
                result.rows_total += 1
                for spec, out_map in zip(specs, out_maps):
                    matched = True
                    dropped_null = False
                    for rule in spec.get("select") or []:
                        col = str(rule.get("column"))
                        pos = full_map.get(col, -1)
                        raw_value = row[pos] if 0 <= pos < len(row) else "null"
                        verdict = _match(rule, {col: raw_value})
                        if verdict is None:
                            dropped_null = True
                            break
                        if not verdict:
                            matched = False
                            break
                    stats = result.per_spec[spec["id"]]
                    if dropped_null:
                        stats["null"] += 1
                        continue
                    if not matched:
                        continue
                    out_values = [row[out_map[col]] if out_map[col] < len(row) else ""
                                  for col in spec["columns"]]
                    writers[spec["id"]].writerow(out_values)
                    stats["rows"] += 1
                    mag_pos = full_map.get("phot_g_mean_mag", -1)
                    if 0 <= mag_pos < len(row):
                        mag = _to_number(row[mag_pos])
                        if mag is not None:
                            if stats["min"] is None or mag < stats["min"]:
                                stats["min"] = mag
                            if stats["max"] is None or mag > stats["max"]:
                                stats["max"] = mag
                    if sample_n and len(result.provenance[spec["id"]]) < sample_n:
                        result.provenance[spec["id"]].append((line_no, out_values))
    finally:
        for raw, gz, text in handles.values():
            text.flush()
            text.close()   # flushes text into gz, closes gz (writes gzip footer)
            if not gz.closed:
                gz.close()
            raw.close()

    for spec in specs:
        spec_id = spec["id"]
        path = result.temp_files[spec_id]
        result.sizes[spec_id] = path.stat().st_size
    return result

# ── output layout / staging ─────────────────────────────────────
def dest_dir(spec: dict, storages: dict[str, dict]) -> Path:
    output = spec["output"]
    if output.get("to_path"):
        base = Path(str(output["to_path"])).expanduser()
    else:
        access = (storages.get(output["storage"]) or {}).get("access") or {}
        base = Path(str(access.get("path", ""))).expanduser()
    return base / str(output["path"])


def output_file(spec: dict, storages: dict[str, dict]) -> Path:
    name = spec["output"].get("filename") or f"{spec['id']}.csv.gz"
    return dest_dir(spec, storages) / name


def staging_dir(spec: dict, storages: dict[str, dict]) -> Path:
    return dest_dir(spec, storages).parent / ".oasis-staging"


def parse_chunks(text: str | None, total: int) -> list[int] | None:
    """'0-99,200' -> [0..99, 200]; None/empty -> all chunks."""
    if not text:
        return None
    out: list[int] = []
    for part in str(text).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            out.extend(range(int(lo), int(hi) + 1))
        else:
            out.append(int(part))
    picked = sorted({i for i in out if 0 <= i < total})
    if not picked:
        raise ValueError(f"chunk selection matches nothing (total={total})")
    return picked


# ── QC ──────────────────────────────────────────────────────────
def verify_samples(spec: dict, source: Source, provenance: list[tuple[int, list[str]]],
                   output_path: Path, emit) -> dict:
    """Two-sided QC: output rows == captured rows; source line == captured row."""
    report = {"samples": len(provenance), "output_ok": 0, "source_ok": 0, "mismatches": []}
    columns = spec["columns"]
    with gzip.open(output_path, "rt", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
        out_rows = []
        for i, row in enumerate(reader):
            if i >= len(provenance):
                break
            out_rows.append(row)
    for (line_no, values), out_row in zip(provenance, out_rows):
        if out_row == values:
            report["output_ok"] += 1
        else:
            report["mismatches"].append({"side": "output", "chunk_line": line_no})
    full_map_cache: dict[int, dict[str, int]] = {}
    for line_no, values in provenance:
        chunk_index, _, target_line = _decode_provenance(line_no)
        chunk_path = source.chunks[chunk_index] if chunk_index < len(source.chunks) else None
        if chunk_path is None:
            report["mismatches"].append({"side": "source", "chunk_line": line_no})
            continue
        if chunk_index not in full_map_cache:
            header = read_header(chunk_path)
            full_map_cache[chunk_index] = {col: i for i, col in enumerate(header)}
        full_map = full_map_cache[chunk_index]
        found = None
        with gzip.open(chunk_path, "rt", encoding="utf-8", errors="replace") as fh:
            reader = csv.reader(fh)
            header_seen = False
            for idx, row in enumerate(reader, 0):
                if not header_seen:
                    if not row or row[0].startswith("#"):
                        continue
                    header_seen = True
                    continue
                if idx == target_line:
                    found = row
                    break
        if found is None:
            report["mismatches"].append({"side": "source", "chunk_line": line_no})
            continue
        same = all(
            (found[full_map[c]] if full_map.get(c, -1) >= 0 and full_map[c] < len(found) else "") == value
            for c, value in zip(columns, values))
        if same:
            report["source_ok"] += 1
        else:
            report["mismatches"].append({"side": "source", "chunk_line": line_no})
    return report


def _encode_provenance(chunk_index: int, line_no: int) -> int:
    return chunk_index * 10_000_000 + line_no


def _decode_provenance(value: int) -> tuple[int, int, int]:
    chunk_index, line_no = divmod(value, 10_000_000)
    return chunk_index, 0, line_no


# ── assembly / artefacts ────────────────────────────────────────
def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _gz_member(payload: bytes) -> bytes:
    """Deterministic gzip member (mtime=0) wrapping `payload`."""
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0, compresslevel=6) as gz:
        gz.write(payload)
    return buf.getvalue()


def assemble(spec: dict, chunks_in_order: list[int], temps_dir: Path, final: Path) -> tuple[int, str]:
    """Header member + data members concatenated in chunk order (multi-member gzip)."""
    final.parent.mkdir(parents=True, exist_ok=True)
    header_member = _gz_member((",".join(spec["columns"]) + "\n").encode("utf-8"))
    tmp = final.with_name(final.name + ".tmp")
    with open(tmp, "wb") as out:
        out.write(header_member)
        for index in chunks_in_order:
            part = temps_dir / f"{index:05d}.csv.gz"
            if not part.exists():
                raise FileNotFoundError(f"missing staged chunk {part}")
            with open(part, "rb") as fh:
                shutil.copyfileobj(fh, out, length=1 << 20)
    os.replace(tmp, final)
    return final.stat().st_size, sha256_file(final)


def write_credits(spec: dict, dataset: dict, dest: Path) -> None:
    licence = dataset.get("licence") or {}
    text = (
        f"{spec['id']} — slice export of dataset '{spec['source']}'\n"
        f"publisher: {dataset.get('publisher', 'unknown')}\n"
        f"licence: {licence.get('name', 'see source')}\n"
        f"licence url: {licence.get('url', '') or '-'}\n"
        f"generated: {now_iso()} by oasis-datasets (slice_export)\n"
        "This product contains a filtered subset with columns/rows selected per its spec; "
        "values are passed through unmodified. Please cite the original survey/archive.\n"
    )
    (dest / "CREDITS.txt").write_text(text, encoding="utf-8")


def _source_epoch(source: Source, channel: dict) -> str:
    manifest = ((channel.get("checksum") or {}).get("manifest"))
    if manifest:
        path = source.root / str(manifest)
        if path.is_file():
            ts = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            return ts.strftime("%Y-%m-%dT%H:%M:%SZ")
    if source.chunks:
        ts = datetime.fromtimestamp(max(p.stat().st_mtime for p in source.chunks), tz=timezone.utc)
        return ts.strftime("%Y-%m-%dT%H:%M:%SZ")
    return ""


# ── the group run ───────────────────────────────────────────────
def run_slices(specs: list[dict], inventory, storages: dict[str, dict], task_dir: Path,
               emit, chunks: list[int] | None = None, chunk_text: str | None = None) -> int:
    """Run one or more specs sharing (source, channel) in a single scan."""
    if not specs:
        return 1
    source, err = resolve_source(specs[0], inventory)
    if source is None:
        emit("error", {"message": err})
        return 1
    for spec in specs[1:]:
        other, err2 = resolve_source(spec, inventory)
        if other is None or (other.dataset_id, other.channel_id, other.root) != \
                (source.dataset_id, source.channel_id, source.root):
            emit("error", {"message": f"spec '{spec['id']}' does not share source/(channel) "
                                      "with the group; run it separately"})
            return 1
    for spec in specs:
        problems = check_columns(spec, source)
        if problems:
            emit("error", {"message": f"{spec['id']}: " + "; ".join(problems)})
            return 1

    dataset = next(d for d in inventory.datasets if d.get("id") == source.dataset_id)
    channel = next(c for c in (dataset.get("channels") or []) if c.get("id") == source.channel_id)
    total_chunks = len(source.chunks)
    selected = chunks if chunks is not None else parse_chunks(chunk_text, total_chunks)
    partial = selected is not None
    chunk_list = selected if selected is not None else list(range(total_chunks))
    parallel = int((specs[0].get("execution") or {}).get("parallel") or 8)
    sample_n = int((specs[0].get("qc") or {}).get("sample", 8))
    sort_by = (specs[0].get("determinism") or {}).get("sort_by", "source_id")

    emit("log", {"text": f"source: {source.dataset_id} [{source.channel_id}] {source.root}"})
    emit("log", {"text": f"chunks: {len(chunk_list)}/{total_chunks}"
                         + (f" (partial selection)" if partial else "")
                         + f"  parallel: {parallel}  specs: {', '.join(s['id'] for s in specs)}"})
    emit("log", {"text": f"determinism: sort_by={sort_by} (source ordered by chunk range), "
                         "gzip mtime=0, multi-member concat in chunk order"})

    staging = staging_dir(specs[0], storages)
    accounting = staging / "chunks.jsonl"
    done_records: dict[tuple[str, int], dict] = {}
    if accounting.exists():
        for line in accounting.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            done_records[(record["spec"], int(record["chunk"]))] = record

    # resume bookkeeping: a chunk counts as done for a spec only when its staged
    # file still matches the recorded sha256 (partial reruns then don't double-count)
    done_ok: dict[str, set[int]] = {spec["id"]: set() for spec in specs}
    for spec in specs:
        for index in chunk_list:
            record = done_records.get((spec["id"], index))
            if not record:
                continue
            temp = staging / spec["id"] / f"{index:05d}.csv.gz"
            if temp.exists() and sha256_file(temp) == record.get("sha256"):
                done_ok[spec["id"]].add(index)

    per_spec_totals = {spec["id"]: {"rows": 0, "null": 0, "min": None, "max": None,
                                    "provenance": []} for spec in specs}
    provenance_by_chunk: dict[str, dict[int, list]] = {spec["id"]: {} for spec in specs}
    for spec in specs:
        spec_id = spec["id"]
        agg = per_spec_totals[spec_id]
        for index in sorted(done_ok[spec_id]):
            record = done_records[(spec_id, index)]
            agg["rows"] += int(record.get("rows", 0))
            agg["null"] += int(record.get("null", 0))
            if record.get("min") is not None:
                agg["min"] = record["min"] if agg["min"] is None else min(agg["min"], record["min"])
            if record.get("max") is not None:
                agg["max"] = record["max"] if agg["max"] is None else max(agg["max"], record["max"])
            provenance_by_chunk[spec_id][index] = [(int(item[0]), list(item[1]))
                                                   for item in record.get("provenance", [])]

    pending: list[int] = []
    for index in chunk_list:
        if any(index not in done_ok[spec["id"]] for spec in specs):
            pending.append(index)
    emit("log", {"text": f"resume: {len(chunk_list) - len(pending)} chunk(s) already staged, "
                         f"{len(pending)} to process"})

    finished = 0
    rc = 0
    if pending:
        # processes, not threads: per-row parsing holds the GIL, so threads give ~1x
        workers = max(1, min(parallel, os.cpu_count() or 8))
        emit("log", {"text": f"workers: {workers} process(es)"})
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = {}
            for index in pending:
                needed = [spec for spec in specs if index not in done_ok[spec["id"]]]
                futures[pool.submit(process_chunk, index, source.chunks[index], needed,
                                    staging, sample_n)] = (index, needed)
            for future in as_completed(futures):
                index, needed = futures[future]
                try:
                    result = future.result()
                except Exception as exc:  # noqa: BLE001 - report per-chunk failure, keep others
                    emit("error", {"message": f"chunk {index} failed: {type(exc).__name__}: {exc}"})
                    rc = 1
                    continue
                finished += 1
                for spec in needed:
                    spec_id = spec["id"]
                    stats = result.per_spec[spec_id]
                    agg = per_spec_totals[spec_id]
                    agg["rows"] += stats["rows"]
                    agg["null"] += stats["null"]
                    if stats["min"] is not None:
                        agg["min"] = stats["min"] if agg["min"] is None else min(agg["min"], stats["min"])
                    if stats["max"] is not None:
                        agg["max"] = stats["max"] if agg["max"] is None else max(agg["max"], stats["max"])
                    provenance_by_chunk[spec_id][index] = [
                        (_encode_provenance(index, ln), list(vals))
                        for ln, vals in result.provenance[spec_id]]
                    record = {"spec": spec_id, "chunk": index, "rows": stats["rows"],
                              "null": stats["null"], "min": stats["min"], "max": stats["max"],
                              "bytes": result.sizes.get(spec_id, 0),
                              "sha256": sha256_file(result.temp_files[spec_id]),
                              "provenance": [[_encode_provenance(index, ln), vals]
                                             for ln, vals in result.provenance[spec_id]]}
                    accounting.parent.mkdir(parents=True, exist_ok=True)
                    with open(accounting, "a", encoding="utf-8") as fh:
                        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
                processed = len(chunk_list) - len(pending) + finished
                if finished % 10 == 0 or processed == len(chunk_list):
                    emit("progress", {"done": processed, "total": len(chunk_list),
                                      "kept": {s["id"]: per_spec_totals[s["id"]]["rows"] for s in specs}})
    if rc != 0:
        emit("log", {"text": "some chunks failed; staged chunks kept for resume"})
        return rc

    # deterministic QC sample: first `sample_n` kept rows in chunk-index order
    for spec in specs:
        agg = per_spec_totals[spec["id"]]
        agg["provenance"] = []
        for index in chunk_list:
            for item in provenance_by_chunk[spec["id"]].get(index, []):
                if len(agg["provenance"]) >= sample_n:
                    break
                agg["provenance"].append(item)
            if len(agg["provenance"]) >= sample_n:
                break

    # keep a task-dir copy of the chunk accounting before staging may be cleaned
    if task_dir.exists() and accounting.exists():
        try:
            shutil.copy2(accounting, task_dir / "slice-chunks.jsonl")
        except OSError:
            pass

    # assemble per spec
    manifests_files = []
    qc_report = {}
    for spec in specs:
        spec_id = spec["id"]
        temps_dir = staging / spec_id
        final = output_file(spec, storages)
        size, digest = assemble(spec, chunk_list, temps_dir, final)
        agg = per_spec_totals[spec_id]
        qc = verify_samples(spec, source, agg["provenance"], final, emit)
        qc_report[spec_id] = {"rows_kept": agg["rows"], "rows_null": agg["null"],
                              "gmin": agg["min"], "gmax": agg["max"], **qc}
        emit("log", {"text": f"{spec_id}: rows={agg['rows']} (null-dropped={agg['null']}) "
                             f"-> {final} ({size/1e6:.2f} MB) sha256={digest[:16]}…"})
        emit("log", {"text": f"{spec_id}: QC samples={qc['samples']} output_ok={qc['output_ok']} "
                             f"source_ok={qc['source_ok']} mismatches={len(qc['mismatches'])}"})
        if qc["mismatches"]:
            rc = 1
        manifests_files.append({
            "id": spec_id, "path": final.name, "bytes": size, "sha256": digest,
            "version": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "epoch": _source_epoch(source, channel),
            "provider": dataset.get("publisher", ""),
            "licence": (dataset.get("licence") or {}).get("name", ""),
            "source_dataset": source.dataset_id,
            "rows": agg["rows"], "columns": spec["columns"],
            "select": spec.get("select") or [],
            "gmin": agg["min"], "gmax": agg["max"],
        })
    if rc == 0:
        manifest = {
            "generated_at": now_iso(),
            "product": {"kind": "slice", "source_dataset": source.dataset_id,
                        "generated_by": "oasis-datasets/slice_export",
                        "task_id": task_dir.name, "partial": partial,
                        "chunks": f"{chunk_list[0]}-{chunk_list[-1]}" if partial else "all"},
            "files": manifests_files,
            "qc": qc_report,
        }
        manifest_path = dest_dir(specs[0], storages) / "manifest.json"
        tmp = manifest_path.with_name(manifest_path.name + ".tmp")
        tmp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, manifest_path)
        dataset0 = dataset
        for spec in specs:
            write_credits(spec, dataset0, dest_dir(spec, storages))
        if not partial:
            shutil.rmtree(staging, ignore_errors=True)
        emit("log", {"text": f"manifest -> {manifest_path}"})
    return rc
