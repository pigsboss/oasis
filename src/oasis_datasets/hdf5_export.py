"""CSV.gz → HDF5 rendition (optional format; canonical delivery stays CSV.gz).

One compound dataset per file (`/table`), chunked + gzip, `track_times=False`
for byte-level reproducibility. Column types inferred from a sample (int64 /
float64 with NaN for nulls / UTF-8 vlen strings), validated strictly on write.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import os
from pathlib import Path

import h5py
import numpy as np

NULLS = {"", "null", "nan", "na"}
SAMPLE_ROWS = 20000
CHUNK_ROWS = 65536


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _is_int(text: str) -> bool:
    body = text[1:] if text.startswith(("-", "+")) else text
    return body.isdigit()


def scan_file(csv_gz: Path) -> tuple[list[str], list[str], int, list[int]]:
    """(header, types, rows, maxlens) — exact full-scan inference.

    Sampling is not enough: sparse empties and late-arriving packed
    designations (D4340) would be missed. Columns that can no longer be
    numeric are dropped from further checks, so the extra cost is small.
    maxlens tracks the UTF-8 byte length of string columns (fixed-width
    storage keeps HDF5 compact and compressible; vlen data bypasses gzip).
    """
    with gzip.open(csv_gz, "rt", encoding="utf-8", errors="replace") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        flags = [{"int": True, "float": True, "empty": False} for _ in header]
        maxlens = [0] * len(header)
        rows = 0
        for row in reader:
            rows += 1
            for col, value in enumerate(row):
                if col >= len(flags):
                    continue
                flag = flags[col]
                if not (flag["int"] or flag["float"]):
                    length = len(value.encode("utf-8"))
                    if length > maxlens[col]:
                        maxlens[col] = length
                    continue
                if value.lower() in NULLS:
                    flag["empty"] = True
                    flag["int"] = False
                    continue
                if flag["int"] and not _is_int(value):
                    flag["int"] = False
                if flag["float"]:
                    try:
                        float(value)
                    except ValueError:
                        flag["float"] = False
    types = []
    for index, flag in enumerate(flags):
        if flag["int"] and not flag["empty"]:
            types.append("int64")
        elif flag["float"]:
            types.append("float64")
        else:
            types.append("str")
    return header, types, rows, maxlens


def _numpy_dtype(header: list[str], types: list[str], maxlens: list[int]) -> np.dtype:
    fields = []
    for name, kind, length in zip(header, types, maxlens):
        if kind == "int64":
            fields.append((name, np.int64))
        elif kind == "float64":
            fields.append((name, np.float64))
        else:
            fields.append((name, np.dtype(f"S{max(1, length)}")))
    return np.dtype(fields)


def convert(csv_gz: Path, out_path: Path, emit) -> dict:
    header, types, rows, maxlens = scan_file(csv_gz)
    dtype = _numpy_dtype(header, types, maxlens)
    emit("log", {"text": f"{csv_gz.name}: {rows} rows, columns: "
                         + ", ".join(f"{n}({t})" for n, t in zip(header, types))})

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_name(out_path.name + ".tmp")
    written = 0
    try:
        with h5py.File(tmp, "w", track_times=False) as fh5:
            ds = fh5.create_dataset("table", shape=(rows,), dtype=dtype,
                                    chunks=(min(CHUNK_ROWS, max(rows, 1)),),
                                    compression="gzip", compression_opts=6,
                                    track_times=False)
            fh5.attrs["columns"] = np.array(header, dtype=h5py.string_dtype("utf-8"))
            fh5.attrs["rows"] = rows
            fh5.attrs["types"] = np.array(types, dtype=h5py.string_dtype("utf-8"))
            fh5.attrs["source"] = csv_gz.name
            fh5.attrs["source_sha256"] = sha256_file(csv_gz)
            fh5.attrs["generated_by"] = "oasis-datasets/hdf5"
            fh5.attrs["dataset_name"] = "table"
            fh5.attrs["note"] = "canonical format is CSV.gz; this HDF5 is an optional rendition"

            buffer: list[list[str]] = []

            def flush(block: list[list[str]]) -> None:
                nonlocal written
                array = np.empty(len(block), dtype=dtype)
                for col, (name, kind) in enumerate(zip(header, types)):
                    values = [row[col] if col < len(row) else "" for row in block]
                    if kind == "int64":
                        array[name] = [int(v) for v in values]
                    elif kind == "float64":
                        array[name] = [np.nan if v.lower() in NULLS else float(v) for v in values]
                    else:
                        width = array.dtype[name].itemsize
                        array[name] = np.array([v.encode("utf-8") for v in values],
                                               dtype=f"S{width}")
                ds[written:written + len(block)] = array
                written += len(block)

            with gzip.open(csv_gz, "rt", encoding="utf-8", errors="replace") as fh:
                reader = csv.reader(fh)
                next(reader)
                for row in reader:
                    buffer.append(row)
                    if len(buffer) >= CHUNK_ROWS:
                        flush(buffer)
                        buffer = []
                if buffer:
                    flush(buffer)
        if written != rows:
            raise RuntimeError(f"row mismatch: wrote {written}, expected {rows}")
        os.replace(tmp, out_path)
    except BaseException:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    digest = sha256_file(out_path)
    size = out_path.stat().st_size
    emit("log", {"text": f"{out_path.name}: written ({size/1e6:.1f} MB) sha256={digest[:16]}…"})
    return {"path": out_path, "bytes": size, "sha256": digest, "rows": rows,
            "columns": header, "types": types}


def verify_readback(csv_gz: Path, out_path: Path, sample: int = 3) -> list[str]:
    """Compare the first `sample` rows against the CSV source; returns problems."""
    problems: list[str] = []
    with gzip.open(csv_gz, "rt", encoding="utf-8", errors="replace") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        csv_rows = [next(reader) for _ in range(sample)]
    with h5py.File(out_path, "r") as fh5:
        ds = fh5["table"]
        if ds.shape[0] < sample:
            problems.append(f"{out_path.name}: too few rows in hdf5")
            return problems
        for i in range(sample):
            h5row = ds[i]
            for col, name in enumerate(header):
                a = h5row[name]
                b = csv_rows[i][col]
                if isinstance(a, bytes):
                    a = a.decode("utf-8")
                if isinstance(a, np.floating):
                    if b.lower() in NULLS:
                        if not np.isnan(a):
                            problems.append(f"{out_path.name} row {i} col {name}: {a} != null")
                    elif abs(float(a) - float(b)) > 1e-12 * max(1.0, abs(float(b))):
                        problems.append(f"{out_path.name} row {i} col {name}: {a} != {b}")
                elif isinstance(a, (np.integer,)):
                    if str(a) != str(b):
                        problems.append(f"{out_path.name} row {i} col {name}: {a} != {b}")
                elif str(a) != b:
                    problems.append(f"{out_path.name} row {i} col {name}: {a!r} != {b!r}")
    return problems
