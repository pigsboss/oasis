"""Consolidate: bring a catalogue (any format) into an application workspace
as a PyTables working set (M5 implementation of F-09/F-10).

Semantics (DSM-004 §6 裁决六, FCP-consolidate): the master stays at the
publication channel; the consolidated copy is a regenerable, self-contained
working set for one application. Modes: full (default) | trim (region x attributes).
Source catalogues are read-only; CSV.gz remains the canonical delivery format.

Profiles describe the on-disk layout: delimiter, header mode, column names,
position columns, id/sort keys, epoch/frame. Builtin profiles cover the
catalogues we have; ad-hoc profiles can be given as a YAML file.
"""

from __future__ import annotations

import bz2
import csv
import gzip
import hashlib
import io
import json
import lzma
import math
import os
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import tables
import yaml

NULL_TOKENS = {"", "\\n", "null", "nan", "na"}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── profiles ────────────────────────────────────────────────────
@dataclass
class Profile:
    name: str = "custom"
    delimiter: str = ","
    header: str = "first_row"          # first_row | external | none | ecsv
    header_file: str | None = None     # external: file name next to the shards
    header_kind: str = "lines"         # lines | tic_bracket | sql_schema
    columns: list[str] = field(default_factory=list)   # used when header == none
    glob: str = "*.csv.gz"             # used when the source is a directory
    positions: dict = field(default_factory=dict)      # {"ra": col, "dec": col}
    id_key: str | None = None
    sort_key: str | None = None
    epoch: dict = field(default_factory=dict)          # {"mode": ..., "ref": ...}
    frame: str = ""


BUILTIN_PROFILES: dict[str, Profile] = {
    "gaia_tier": Profile(
        name="gaia_tier", delimiter=",", header="first_row", glob="*.csv.gz",
        positions={"ra": "ra", "dec": "dec"}, id_key="source_id", sort_key="source_id",
        epoch={"mode": "global", "ref": "J2016.0"}, frame="ICRS"),
    "tess_tic": Profile(
        name="tess_tic", delimiter=",", header="external", header_file="header.csv",
        header_kind="tic_bracket", glob="tic_dec*.csv.gz",
        positions={"ra": "ra", "dec": "dec"}, id_key="ID", sort_key="ID",
        epoch={"mode": "global", "ref": "J2000 (approx.)"}, frame="ICRS"),
    "twomass_psc": Profile(
        name="twomass_psc", delimiter="|", header="external",
        header_file="twomass_psc_schema", header_kind="sql_schema", glob="psc_*.gz",
        positions={"ra": "ra", "dec": "decl"}, id_key="designation", sort_key="designation",
        epoch={"mode": "global", "ref": "J2000"}, frame="ICRS"),
}


DATASET_PROFILE = {
    "gaia_gdr3_gaia_source": "gaia_tier",
    "gaia_gdr2_gaia_source": "gaia_tier",
    "tess_tic": "tess_tic",
    "twomass_psc": "twomass_psc",
}


def load_profile(spec: str | None, dataset_id: str | None = None) -> Profile:
    if spec is None:
        if dataset_id in DATASET_PROFILE:
            return BUILTIN_PROFILES[DATASET_PROFILE[dataset_id]]
        if dataset_id and dataset_id in BUILTIN_PROFILES:
            return BUILTIN_PROFILES[dataset_id]
        raise ValueError(f"no builtin profile for '{dataset_id}', use --profile")
    if spec in BUILTIN_PROFILES:
        return BUILTIN_PROFILES[spec]
    path = Path(spec).expanduser()
    if path.is_file():
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        known = {f for f in Profile.__dataclass_fields__}
        return Profile(**{k: v for k, v in raw.items() if k in known})
    raise ValueError(f"unknown profile '{spec}' (not builtin, not a file)")


def parse_region(spec: str | None):
    """'cone:RA,DEC,R_DEG' or 'box:RA1,RA2,DEC1,DEC2' -> tuple or None."""
    if not spec:
        return None
    kind, _, rest = spec.partition(":")
    nums = [float(x) for x in rest.split(",")]
    if kind == "cone" and len(nums) == 3:
        return ("cone", *nums)
    if kind == "box" and len(nums) == 4:
        return ("box", *nums)
    raise ValueError(f"bad region spec '{spec}'")


def region_mask(region, ra: np.ndarray, dec: np.ndarray) -> np.ndarray:
    if region is None:
        return np.ones(len(ra), dtype=bool)
    if region[0] == "cone":
        _, ra0, dec0, radius = region
        d2r = math.pi / 180.0
        cosd = (np.cos(dec * d2r) * math.cos(dec0 * d2r) * np.cos(ra * d2r - ra0 * d2r)
                + np.sin(dec * d2r) * math.sin(dec0 * d2r))
        return cosd >= math.cos(radius * d2r)
    _, ra1, ra2, d1, d2 = region
    return (ra >= ra1) & (ra <= ra2) & (dec >= d1) & (dec <= d2)


# ── source resolution / reading ─────────────────────────────────
def resolve_sources(source: Path, profile: Profile) -> list[Path]:
    source = Path(source).expanduser()
    if source.is_file():
        return [source]
    if source.is_dir():
        files = sorted(p for p in source.glob(profile.glob) if p.is_file())
        if not files:
            raise ValueError(f"no files matching '{profile.glob}' under {source}")
        return files
    raise ValueError(f"source not found: {source}")


def _open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    if path.suffix == ".bz2":
        return bz2.open(path, "rt", encoding="utf-8", errors="replace")
    if path.suffix == ".xz":
        return lzma.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "rt", encoding="utf-8", errors="replace")


_TYPE_MAP = {"integer": "int", "smallint": "int", "int": "int",
             "float": "float", "double": "float", "double precision": "float",
             "real": "float", "string": "str", "str": "str", "char": "str"}


def _parse_tic_header(text: str) -> tuple[list[str], dict[str, str]]:
    names, hints = [], {}
    for token in text.split(","):
        m = re.search(r"\[([^\]]+)\]", token)
        name = (m.group(1) if m else token).strip()
        names.append(name)
        tm = re.search(r":\s*([A-Za-z]+)", token)
        if tm and tm.group(1).lower() in _TYPE_MAP:
            hints[name] = _TYPE_MAP[tm.group(1).lower()]
    return names, hints


def _parse_sql_schema(text: str) -> tuple[list[str], dict[str, str]]:
    names, hints = [], {}
    for line in text.splitlines():
        m = re.match(r"\s+([A-Za-z_][A-Za-z0-9_]*)\s+"
                     r"(double\s+precision|real|smallint|integer|character\(\d+\)|date)",
                     line, re.I)
        if m:
            names.append(m.group(1))
            sqltype = re.sub(r"character\(\d+\)", "string", m.group(2).lower())
            hints[m.group(1)] = _TYPE_MAP.get(sqltype, "str")
    return names, hints


def read_header_columns(profile: Profile, sample_file: Path
                        ) -> tuple[list[str], dict[str, str]]:
    if profile.header == "none":
        if not profile.columns:
            raise ValueError("header 'none' requires explicit columns in the profile")
        return list(profile.columns), {}
    if profile.header == "external":
        if not profile.header_file:
            raise ValueError("header 'external' requires header_file")
        header_path = sample_file.parent / profile.header_file
        text = header_path.read_text(encoding="utf-8")
        if profile.header_kind == "tic_bracket":
            return _parse_tic_header(text)
        if profile.header_kind == "sql_schema":
            return _parse_sql_schema(text)
        return [line.strip() for line in text.splitlines() if line.strip()], {}
    # first_row | ecsv
    with _open_text(sample_file) as fh:
        reader = csv.reader(fh, delimiter=profile.delimiter)
        for row in reader:
            if profile.header == "ecsv" and row and row[0].startswith("#"):
                continue
            if row:
                return [name.strip() for name in row], {}
    raise ValueError(f"no header row found in {sample_file}")


def iter_rows(path: Path, profile: Profile, columns: list[str],
              only: dict[str, int] | None = None, limit: int | None = None):
    """Yield parsed rows as lists; `only` maps column -> source index (subset read)."""
    with _open_text(path) as fh:
        reader = csv.reader(fh, delimiter=profile.delimiter)
        if profile.header in ("first_row", "ecsv"):
            for row in reader:
                if profile.header == "ecsv" and row and row[0].startswith("#"):
                    continue
                break  # consumed the header row
        count = 0
        for row in reader:
            if len(row) < len(columns):
                # pad short rows (rare malformed lines) instead of dropping silently
                row = row + [""] * (len(columns) - len(row))
            if only is None:
                yield row
            else:
                yield [row[i] if i < len(row) else "" for i in only.values()]
            count += 1
            if limit is not None and count >= limit:
                return


# ── type inference ──────────────────────────────────────────────
def _is_int(text: str) -> bool:
    body = text[1:] if text.startswith(("-", "+")) else text
    return body.isdigit()


def infer_types(source_files: list[Path], profile: Profile, columns: list[str],
                only: dict[str, int] | None, limit: int | None, emit,
                hints: dict[str, str] | None = None
                ) -> tuple[list[str], list[int]]:
    flags = [{"int": True, "float": True, "empty": False} for _ in columns]
    hints = hints or {}
    hinted = 0
    for i, col in enumerate(columns):
        hint = hints.get(col)
        if hint == "str":
            flags[i]["int"] = flags[i]["float"] = False
            hinted += 1
        elif hint == "float":
            flags[i]["int"] = False
            hinted += 1
    maxlens = [0] * len(columns)
    rows = 0
    for path in source_files:
        for row in iter_rows(path, profile, columns, only=only):
            rows += 1
            for i, value in enumerate(row):
                value = value.strip()
                flag = flags[i]
                if flag["int"] or flag["float"]:
                    if value.lower() in NULL_TOKENS:
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
                    continue
                length = len(value.encode("utf-8"))
                if length > maxlens[i]:
                    maxlens[i] = length
            if limit is not None and rows >= limit:
                break
        if limit is not None and rows >= limit:
            break
    types = []
    for i, flag in enumerate(flags):
        if flag["int"] and not flag["empty"]:
            types.append("int64")
        elif flag["float"]:
            types.append("float64")
        else:
            types.append("str")
    note = f" ({hinted} column(s) pinned by header type hints)" if hinted else ""
    emit("log", {"text": f"scanned {rows} row(s); types: "
                         + ", ".join(f"{c}({t})" for c, t in zip(columns, types)) + note})
    return types, maxlens


def _numpy_dtype(columns: list[str], types: list[str], maxlens: list[int]) -> np.dtype:
    fields = []
    for name, kind, length in zip(columns, types, maxlens):
        if kind == "int64":
            fields.append((name, np.int64))
        elif kind == "float64":
            fields.append((name, np.float64))
        else:
            fields.append((name, np.dtype(f"S{max(1, length)}")))
    return np.dtype(fields)


def _coerce(values: list[str], kind: str, width: int):
    if kind == "int64":
        return np.array([int(v) for v in values], dtype=np.int64)
    if kind == "float64":
        return np.array([np.nan if v.lower() in NULL_TOKENS else float(v) for v in values],
                        dtype=np.float64)
    return np.array([v.encode("utf-8") for v in values], dtype=f"S{width}")


# ── the consolidate run ─────────────────────────────────────────
@dataclass
class ConsolidatePlan:
    name: str
    source_files: list[Path]
    columns: list[str]
    profile: Profile
    dest_dir: Path
    dest_h5: Path
    dest_manifest: Path
    region: tuple | None
    attributes: list[str] | None
    limit: int | None
    type_hints: dict = field(default_factory=dict)

    @property
    def mode(self) -> str:
        return "trim" if (self.region or self.attributes) else "full"


def build_plan(source: Path | None, dataset_path: Path | None, app: Path,
               profile_spec: str | None, dataset_id: str | None,
               region_spec: str | None, attributes: str | None,
               limit: int | None, name: str | None) -> tuple[ConsolidatePlan | None, str]:
    dataset_id = dataset_id or None
    try:
        profile = load_profile(profile_spec, dataset_id)
    except ValueError as exc:
        return None, str(exc)
    src = source or dataset_path
    if src is None:
        return None, "no source (give --from or an inventory dataset id)"
    src = Path(src).expanduser()
    try:
        source_files = resolve_sources(src, profile)
    except ValueError as exc:
        return None, str(exc)
    columns, type_hints = read_header_columns(profile, source_files[0])
    # sanity: column count vs first data row
    try:
        region = parse_region(region_spec)
    except ValueError as exc:
        return None, str(exc)
    attrs = [a.strip() for a in attributes.split(",")] if attributes else None
    if attrs:
        missing = [a for a in attrs if a not in columns]
        if missing:
            return None, f"attributes not in catalogue: {', '.join(missing)}"
    if region and not (profile.positions.get("ra") in columns
                       and profile.positions.get("dec") in columns):
        return None, ("region filter requires position columns "
                      f"{profile.positions} present in the catalogue")
    stem = name or dataset_id or (src.stem.split(".")[0] if src.is_file() else src.name)
    dest_dir = Path(app).expanduser() / "consolidated"
    return ConsolidatePlan(
        name=str(stem), source_files=source_files, columns=columns, profile=profile,
        dest_dir=dest_dir, dest_h5=dest_dir / f"{stem}.h5",
        dest_manifest=dest_dir / f"{stem}.manifest.json",
        region=region, attributes=attrs, limit=limit,
        type_hints=type_hints), ""


def run_consolidate(plan: ConsolidatePlan, emit) -> int:
    profile = plan.profile
    started = time.time()
    plan.dest_dir.mkdir(parents=True, exist_ok=True)

    # column subset actually parsed/written
    written = plan.attributes or plan.columns
    parse_cols = list(dict.fromkeys(written + [c for c in profile.positions.values()
                                               if c and c not in written]))
    index = {c: plan.columns.index(c) for c in parse_cols}
    ra_col, dec_col = profile.positions.get("ra"), profile.positions.get("dec")

    types, maxlens = infer_types(plan.source_files, profile, plan.columns, index,
                                 plan.limit, emit, hints=plan.type_hints)
    dtype = _numpy_dtype(parse_cols, types, maxlens)
    widths = {c: max(1, ml) for c, ml in zip(parse_cols, maxlens)}
    kinds = {c: t for c, t in zip(parse_cols, types)}

    tmp = plan.dest_h5.with_name(plan.dest_h5.name + ".tmp")
    filters = None
    try:
        filters = tables.Filters(complevel=5, complib="blosc")
    except Exception:  # noqa: BLE001 - fall back when blosc is unavailable
        filters = tables.Filters(complevel=6, complib="zlib")

    rows_in = rows_out = 0
    shard_counts: dict[str, int] = {}
    block: list[list[str]] = []
    block_rows = 20000
    sample_rows: list[list[str]] = []
    with tables.open_file(tmp, "w") as h5:
        table = h5.create_table("/", "table", dtype, title=f"consolidated {plan.name}",
                                filters=filters)
        for path in plan.source_files:
            shard_count = 0
            for row in iter_rows(path, profile, plan.columns, only=index,
                                 limit=(plan.limit - rows_in) if plan.limit else None):
                if plan.limit is not None and rows_in >= plan.limit:
                    break
                rows_in += 1
                values = [v.strip() for v in row]
                if plan.region is not None:
                    ra_i, dec_i = parse_cols.index(ra_col), parse_cols.index(dec_col)
                    try:
                        ra_v, dec_v = float(values[ra_i]), float(values[dec_i])
                    except ValueError:
                        continue
                    mask = region_mask(plan.region, np.array([ra_v]), np.array([dec_v]))[0]
                    if not mask:
                        continue
                block.append(values)
                if len(sample_rows) < 3:
                    sample_rows.append(list(values))
                rows_out += 1
                shard_count += 1
                if len(block) >= block_rows:
                    _append_block(table, block, parse_cols, kinds, widths)
                    block = []
                if rows_in % 500000 == 0:
                    emit("progress", {"done": rows_in, "written": rows_out})
            shard_counts[path.name] = shard_count
            if plan.limit is not None and rows_in >= plan.limit:
                break
        if block:
            _append_block(table, block, parse_cols, kinds, widths)
        emit("log", {"text": f"written {rows_out} row(s) of {rows_in} scanned"})

        # metadata
        h5.root._v_attrs["consolidate"] = json.dumps({
            "kind": "consolidated", "name": plan.name, "mode": plan.mode,
            "profile": profile.name, "created": now_iso(),
            "region": plan.region, "attributes": plan.attributes, "limit": plan.limit,
            "sources": [p.name for p in plan.source_files],
        }, ensure_ascii=False)
        table.attrs.columns = np.array([c.encode("utf-8") for c in parse_cols], dtype="S64")
        table.attrs.types = np.array([kinds[c].encode("utf-8") for c in parse_cols], dtype="S8")
        table.attrs.rows = rows_out
        table.attrs.epoch = json.dumps(profile.epoch, ensure_ascii=False)
        table.attrs.frame = profile.frame
        table.attrs.sort_key = profile.sort_key or ""
        table.attrs.id_key = profile.id_key or ""

        if profile.sort_key and profile.sort_key in parse_cols and rows_out > 0:
            t0 = time.time()
            try:
                getattr(table.cols, profile.sort_key).create_csindex()
                emit("log", {"text": f"CSI on {profile.sort_key}: {time.time()-t0:.1f}s"})
            except Exception as exc:  # noqa: BLE001 - string columns may be unsupported
                emit("log", {"text": f"CSI skipped on {profile.sort_key}: "
                                     f"{type(exc).__name__}: {exc}"})
    os.replace(tmp, plan.dest_h5)

    digest = sha256_file(plan.dest_h5)
    size = plan.dest_h5.stat().st_size
    emit("log", {"text": f"{plan.dest_h5.name}: {size/1e6:.1f} MB  sha256={digest[:16]}…"})

    qc = verify_samples(plan, parse_cols, sample_rows)
    manifest = {
        "generated_at": now_iso(),
        "kind": "consolidated",
        "mode": plan.mode,
        "name": plan.name,
        "workspace": str(plan.dest_dir.parent),
        "source": {
            "files": [str(p) for p in plan.source_files],
            "profile": profile.name,
            "epoch": profile.epoch, "frame": profile.frame,
            "note": "master stays at the publication channel; this copy is regenerable",
        },
        "params": {"region": plan.region, "attributes": plan.attributes,
                   "limit": plan.limit},
        "table": {"file": plan.dest_h5.name, "node": "/table", "rows": rows_out,
                  "columns": parse_cols, "types": [kinds[c] for c in parse_cols],
                  "bytes": size, "sha256": digest,
                  "index": (f"CSI({profile.sort_key})" if profile.sort_key else None)},
        "shards": shard_counts,
        "partial": bool(plan.limit),
        "qc": qc,
        "elapsed_s": round(time.time() - started, 1),
    }
    tmp_m = plan.dest_manifest.with_name(plan.dest_manifest.name + ".tmp")
    tmp_m.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp_m, plan.dest_manifest)
    emit("log", {"text": f"manifest -> {plan.dest_manifest}"})
    emit("log", {"text": f"QC samples={qc['samples']} matched={qc['matched']} "
                         f"mismatches={len(qc['mismatches'])}"})
    return 0 if not qc["mismatches"] else 1


def _append_block(table, block: list[list[str]], cols: list[str],
                  kinds: dict, widths: dict) -> None:
    array = np.empty(len(block), dtype=table.dtype)
    for i, col in enumerate(cols):
        values = [row[i] for row in block]
        array[col] = _coerce(values, kinds[col], widths[col])
    table.append(array)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_samples(plan: ConsolidatePlan, cols: list[str],
                   samples: list[list[str]]) -> dict:
    """Compare the first written rows against a fresh read of the source."""
    report = {"samples": 0, "matched": 0, "mismatches": []}
    if not samples:
        return report
    with tables.open_file(plan.dest_h5, "r") as h5:
        table = h5.get_node("/table")
        read_back = table[:len(samples)]
    for i, expected in enumerate(samples):
        got = read_back[i]
        report["samples"] += 1
        ok = True
        for j, col in enumerate(cols):
            a = got[col]
            b = expected[j]
            if isinstance(a, bytes):
                a = a.decode("utf-8")
                if a != b:
                    ok = False
            elif isinstance(a, np.floating):
                if b.lower() in NULL_TOKENS:
                    ok = ok and bool(np.isnan(a))
                else:
                    ok = ok and abs(float(a) - float(b)) <= 1e-9 * max(1.0, abs(float(b)))
            else:  # integer
                if str(a) != str(b):
                    ok = False
            if not ok:
                report["mismatches"].append({"row": i, "column": col})
                break
        if ok:
            report["matched"] += 1
    return report
