"""Consolidate: bring a catalogue (any format) into an application workspace
as a PyTables working set (M5 implementation of F-09/F-10).

Semantics (DSM-004 §6 裁决六, FCP-consolidate): the master stays at the
publication channel; the consolidated copy is a regenerable, self-contained
working set for one application. Modes: full (default) | trim (region x attributes).
Source catalogues are read-only; CSV.gz remains the canonical delivery format.

Profiles describe the on-disk layout: delimiter, header mode, column names,
position columns, id/sort keys, epoch/frame. Builtin profiles cover the
catalogues we have; ad-hoc profiles can be given as a YAML file.

For Gaia, the default is a ``core`` column set and a spatial layout: an actual
HEALPix ``ipix`` column is computed from RA/Dec, the table is sorted by
``ipix``, and a sparse ``ipix_pixels``/``ipix_offsets`` index is written.
``source_id`` and ``phot_g_mean_mag`` get PyTables CSIs for fast selection.
``oasis_datasets.select`` provides ID/cone/box/where selection.
"""

from __future__ import annotations

import bz2
import copy
import csv
import gzip
import hashlib
import io
import json
import lzma
import multiprocessing as mp
import traceback
from multiprocessing import shared_memory
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

from . import hpx

NULL_TOKENS = {"", "\\n", "\\N", "null", "nan", "na", "nnnn", "nnn", "n"}
PROFILE = os.environ.get("OASIS_CONSOLIDATE_PROFILE") == "1"

#: Default Gaia working set for sky work.  Missing columns are dropped with a
#: warning; source_id/ra/dec are mandatory.
GAIA_CORE_COLUMNS = [
    "source_id", "ra", "dec", "ref_epoch",
    "parallax", "pmra", "pmdec",
    "phot_g_mean_mag", "phot_bp_mean_mag", "phot_rp_mean_mag", "bp_rp",
    "ruwe", "duplicated_source", "phot_variable_flag",
]

ALLWISE_COLUMNS = [
    'designation', 'ra', 'dec', 'sigra', 'sigdec', 'sigradec', 'glon', 'glat',
    'elon', 'elat', 'wx', 'wy', 'cntr', 'source_id', 'coadd_id', 'src',
    'w1mpro', 'w1sigmpro', 'w1snr', 'w1rchi2', 'w2mpro', 'w2sigmpro', 'w2snr', 'w2rchi2',
    'w3mpro', 'w3sigmpro', 'w3snr', 'w3rchi2', 'w4mpro', 'w4sigmpro', 'w4snr', 'w4rchi2',
    'rchi2', 'nb', 'na', 'w1sat', 'w2sat', 'w3sat', 'w4sat', 'satnum',
    'ra_pm', 'dec_pm', 'sigra_pm', 'sigdec_pm', 'sigradec_pm', 'pmra', 'sigpmra', 'pmdec',
    'sigpmdec', 'w1rchi2_pm', 'w2rchi2_pm', 'w3rchi2_pm', 'w4rchi2_pm', 'rchi2_pm', 'pmcode', 'cc_flags',
    'rel', 'ext_flg', 'var_flg', 'ph_qual', 'det_bit', 'moon_lev', 'w1nm', 'w1m',
    'w2nm', 'w2m', 'w3nm', 'w3m', 'w4nm', 'w4m', 'w1cov', 'w2cov',
    'w3cov', 'w4cov', 'w1cc_map', 'w1cc_map_str', 'w2cc_map', 'w2cc_map_str', 'w3cc_map', 'w3cc_map_str',
    'w4cc_map', 'w4cc_map_str', 'best_use_cntr', 'ngrp', 'w1flux', 'w1sigflux', 'w1sky', 'w1sigsk',
    'w1conf', 'w2flux', 'w2sigflux', 'w2sky', 'w2sigsk', 'w2conf', 'w3flux', 'w3sigflux',
    'w3sky', 'w3sigsk', 'w3conf', 'w4flux', 'w4sigflux', 'w4sky', 'w4sigsk', 'w4conf',
    'w1mag', 'w1sigm', 'w1flg', 'w1mcor', 'w2mag', 'w2sigm', 'w2flg', 'w2mcor',
    'w3mag', 'w3sigm', 'w3flg', 'w3mcor', 'w4mag', 'w4sigm', 'w4flg', 'w4mcor',
    'w1mag_1', 'w1sigm_1', 'w1flg_1', 'w2mag_1', 'w2sigm_1', 'w2flg_1', 'w3mag_1', 'w3sigm_1',
    'w3flg_1', 'w4mag_1', 'w4sigm_1', 'w4flg_1', 'w1mag_2', 'w1sigm_2', 'w1flg_2', 'w2mag_2',
    'w2sigm_2', 'w2flg_2', 'w3mag_2', 'w3sigm_2', 'w3flg_2', 'w4mag_2', 'w4sigm_2', 'w4flg_2',
    'w1mag_3', 'w1sigm_3', 'w1flg_3', 'w2mag_3', 'w2sigm_3', 'w2flg_3', 'w3mag_3', 'w3sigm_3',
    'w3flg_3', 'w4mag_3', 'w4sigm_3', 'w4flg_3', 'w1mag_4', 'w1sigm_4', 'w1flg_4', 'w2mag_4',
    'w2sigm_4', 'w2flg_4', 'w3mag_4', 'w3sigm_4', 'w3flg_4', 'w4mag_4', 'w4sigm_4', 'w4flg_4',
    'w1mag_5', 'w1sigm_5', 'w1flg_5', 'w2mag_5', 'w2sigm_5', 'w2flg_5', 'w3mag_5', 'w3sigm_5',
    'w3flg_5', 'w4mag_5', 'w4sigm_5', 'w4flg_5', 'w1mag_6', 'w1sigm_6', 'w1flg_6', 'w2mag_6',
    'w2sigm_6', 'w2flg_6', 'w3mag_6', 'w3sigm_6', 'w3flg_6', 'w4mag_6', 'w4sigm_6', 'w4flg_6',
    'w1mag_7', 'w1sigm_7', 'w1flg_7', 'w2mag_7', 'w2sigm_7', 'w2flg_7', 'w3mag_7', 'w3sigm_7',
    'w3flg_7', 'w4mag_7', 'w4sigm_7', 'w4flg_7', 'w1mag_8', 'w1sigm_8', 'w1flg_8', 'w2mag_8',
    'w2sigm_8', 'w2flg_8', 'w3mag_8', 'w3sigm_8', 'w3flg_8', 'w4mag_8', 'w4sigm_8', 'w4flg_8',
    'w1magp', 'w1sigp1', 'w1sigp2', 'w1k', 'w1ndf', 'w1mlq', 'w1mjdmin', 'w1mjdmax',
    'w1mjdmean', 'w2magp', 'w2sigp1', 'w2sigp2', 'w2k', 'w2ndf', 'w2mlq', 'w2mjdmin',
    'w2mjdmax', 'w2mjdmean', 'w3magp', 'w3sigp1', 'w3sigp2', 'w3k', 'w3ndf', 'w3mlq',
    'w3mjdmin', 'w3mjdmax', 'w3mjdmean', 'w4magp', 'w4sigp1', 'w4sigp2', 'w4k', 'w4ndf',
    'w4mlq', 'w4mjdmin', 'w4mjdmax', 'w4mjdmean', 'rho12', 'rho23', 'rho34', 'q12',
    'q23', 'q34', 'xscprox', 'w1rsemi', 'w1ba', 'w1pa', 'w1gmag', 'w1gerr',
    'w1gflg', 'w2rsemi', 'w2ba', 'w2pa', 'w2gmag', 'w2gerr', 'w2gflg', 'w3rsemi',
    'w3ba', 'w3pa', 'w3gmag', 'w3gerr', 'w3gflg', 'w4rsemi', 'w4ba', 'w4pa',
    'w4gmag', 'w4gerr', 'w4gflg', 'tmass_key', 'r_2mass', 'pa_2mass', 'n_2mass', 'j_m_2mass',
    'j_msig_2mass', 'h_m_2mass', 'h_msig_2mass', 'k_m_2mass', 'k_msig_2mass', 'x', 'y', 'z',
    'spt_ind', 'htm20',
]

ALLWISE_NIR_COLUMNS = [
    'designation', 'ra', 'dec', 'sigra', 'sigdec', 'sigradec', 'glon', 'glat', 'elon', 'elat', 'wx', 'wy', 'cntr', 'source_id', 'coadd_id', 'src', 'w1mpro', 'w1sigmpro', 'w1snr', 'w1rchi2', 'w2mpro', 'w2sigmpro', 'w2snr', 'w2rchi2', 'w3mpro', 'w3sigmpro', 'w3snr', 'w3rchi2', 'w4mpro', 'w4sigmpro', 'w4snr', 'w4rchi2', 'ph_qual', 'cc_flags', 'ext_flg', 'var_flg',
]

TWOMASS_NIR_COLUMNS = [
    'designation', 'ra', 'decl', 'j_m', 'h_m', 'k_m', 'j_msigcom', 'h_msigcom', 'k_msigcom', 'j_snr', 'h_snr', 'k_snr', 'ph_qual', 'rd_flg', 'cc_flg', 'gal_contam', 'mp_flg',
]



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
    default_columns: list[str] = field(default_factory=list)  # e.g. Gaia core
    layout: str = "source_id"          # spatial | source_id
    order: int = 9                     # HEALPix order for spatial layout
    hdu: int | str = 0                 # FITS HDU
    fast_csv: bool = False             # comma-split fast path when safe
    schema_types: dict = field(default_factory=dict)
    schema_widths: dict = field(default_factory=dict)


BUILTIN_PROFILES: dict[str, Profile] = {
    "gaia_tier": Profile(
        name="gaia_tier", delimiter=",", header="first_row", glob="*.csv.gz",
        positions={"ra": "ra", "dec": "dec"}, id_key="source_id", sort_key="source_id",
        epoch={"mode": "global", "ref": "J2016.0"}, frame="ICRS",
        default_columns=list(GAIA_CORE_COLUMNS), layout="spatial", order=9),
    "gaia_dr3_source": Profile(
        name="gaia_dr3_source", delimiter=",", header="ecsv", glob="*.csv.gz",
        positions={"ra": "ra", "dec": "dec"}, id_key="source_id", sort_key="source_id",
        epoch={"mode": "global", "ref": "J2016.0"}, frame="ICRS",
        default_columns=list(GAIA_CORE_COLUMNS), layout="spatial", order=9,
        fast_csv=True),
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

    "allwise_psc": Profile(
        name="allwise_psc", delimiter="|", header="none",
        columns=list(ALLWISE_COLUMNS), glob="*.bz2",
        positions={"ra": "ra", "dec": "dec"},
        id_key="designation", sort_key="designation",
        epoch={"mode": "global", "ref": "J2010"}, frame="ICRS",
        layout="spatial", order=9),
    "allwise_nir": Profile(
        name="allwise_nir", delimiter="|", header="none",
        columns=list(ALLWISE_COLUMNS), glob="*.bz2",
        positions={"ra": "ra", "dec": "dec"},
        id_key="designation", sort_key="designation",
        epoch={"mode": "global", "ref": "J2010"}, frame="ICRS",
        default_columns=list(ALLWISE_NIR_COLUMNS), layout="spatial", order=9,
        schema_types={
            "designation": "str", "source_id": "str", "coadd_id": "str",
            "ra": "f8", "dec": "f8", "sigra": "f4", "sigdec": "f4",
            "sigradec": "f4", "glon": "f8", "glat": "f8", "elon": "f8",
            "elat": "f8", "wx": "f4", "wy": "f4", "cntr": "i8", "src": "i4",
            "w1mpro": "f4", "w1sigmpro": "f4", "w1snr": "f4", "w1rchi2": "f4",
            "w2mpro": "f4", "w2sigmpro": "f4", "w2snr": "f4", "w2rchi2": "f4",
            "w3mpro": "f4", "w3sigmpro": "f4", "w3snr": "f4", "w3rchi2": "f4",
            "w4mpro": "f4", "w4sigmpro": "f4", "w4snr": "f4", "w4rchi2": "f4",
            "ph_qual": "str", "cc_flags": "str", "ext_flg": "i2", "var_flg": "i2",
        },
        schema_widths={"designation": 20, "source_id": 28, "coadd_id": 20,
                       "ph_qual": 4, "cc_flags": 4}),
    "twomass_nir": Profile(
        name="twomass_nir", delimiter="|", header="external",
        header_file="twomass_psc_schema", header_kind="sql_schema", glob="psc_*.gz",
        positions={"ra": "ra", "dec": "decl"},
        id_key="designation", sort_key="designation",
        epoch={"mode": "global", "ref": "J2000"}, frame="ICRS",
        default_columns=list(TWOMASS_NIR_COLUMNS), layout="spatial", order=9,
        schema_types={
            "designation": "str", "ra": "f8", "decl": "f8",
            "j_m": "f4", "h_m": "f4", "k_m": "f4",
            "j_msigcom": "f4", "h_msigcom": "f4", "k_msigcom": "f4",
            "j_snr": "f4", "h_snr": "f4", "k_snr": "f4",
            "ph_qual": "str", "rd_flg": "str", "cc_flg": "str",
            "gal_contam": "i2", "mp_flg": "i2",
        },
        schema_widths={"designation": 17, "ph_qual": 3, "rd_flg": 3, "cc_flg": 3}),
}


DATASET_PROFILE = {
    "gaia_gdr3_gaia_source": "gaia_dr3_source",
    "gaia_gdr2_gaia_source": "gaia_tier",
    "tess_tic": "tess_tic",
    "twomass_psc": "twomass_psc",
    "allwise_nir": "allwise_nir",
    "twomass_nir": "twomass_nir",
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
def detect_source_format(path: Path) -> str:
    name = path.name.lower()
    if name.endswith((".csv", ".csv.gz", ".tsv", ".tsv.gz")) or \
       name.endswith((".csv.bz2", ".csv.xz")):
        return "csv"
    if name.endswith((".fits", ".fit", ".fts", ".fits.gz")):
        return "fits"
    if name.endswith(".ecsv"):
        return "ecsv"
    return "csv"


def _fits_module():
    try:
        from astropy.io import fits  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise ValueError("FITS input requires astropy (pip install astropy)") from exc
    return fits


def _fits_table(hdul, hdu: int | str = 0):
    """Return the requested table HDU, auto-finding the first BINTABLE for 0."""
    try:
        h = hdul[hdu]
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"HDU {hdu} not found") from exc
    if getattr(h, "columns", None) is not None and h.data is not None:
        return h
    if hdu == 0:
        for candidate in hdul:
            if getattr(candidate, "columns", None) is not None and candidate.data is not None:
                return candidate
    raise ValueError(f"HDU {hdu} has no table data")


def fits_columns(path: Path, hdu: int | str = 0) -> list[str]:
    fits = _fits_module()
    with fits.open(path, memmap=True) as hdul:
        h = _fits_table(hdul, hdu)
        names = list(h.columns.names)
        return [str(n).strip() for n in names]


def read_schema(path: Path, profile: Profile) -> tuple[list[str], dict[str, str]]:
    fmt = detect_source_format(path)
    if fmt == "fits":
        return fits_columns(path, profile.hdu), {}
    return read_header_columns(profile, path)


def resolve_sources(source: Path, profile: Profile, fmt: str | None = None) -> list[Path]:
    source = Path(source).expanduser()
    if source.is_file():
        return [source]
    if source.is_dir():
        pattern = profile.glob
        if fmt == "fits":
            pattern = "*.fits"
        files = sorted(p for p in source.glob(pattern) if p.is_file())
        if not files and fmt == "fits":
            files = sorted(p for p in source.glob("*.fit") if p.is_file())
        if not files:
            raise ValueError(f"no files matching '{pattern}' under {source}")
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


def _open_binary(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rb")
    if path.suffix == ".bz2":
        return bz2.open(path, "rb")
    if path.suffix == ".xz":
        return lzma.open(path, "rb")
    return open(path, "rb")


def iter_rows_fast(path: Path, profile: Profile, columns: list[str],
                   only: dict[str, int] | None = None, limit: int | None = None,
                   decode_indices: set[int] | None = None):
    """Fast comma-split path for Gaia ECSV/plain CSVs.

    GDR3 strings (designation/flags) are quoted but do not contain commas.
    If a line has a different field count (quoted comma), fall back to
    ``csv.reader`` for that line.  Values are returned as str just like
    ``iter_rows``.
    """
    with _open_binary(path) as fh:
        header = None
        for line in fh:
            if line.startswith(b"#"):
                continue
            if not line.strip():
                continue
            header = line.rstrip(b"\r\n").split(b",")
            break
        if header is None:
            raise ValueError(f"no header row found in {path}")
        if len(header) != len(columns):
            raise ValueError(f"header has {len(header)} columns, expected {len(columns)}")
        count = 0
        for line in fh:
            if line.startswith(b"#") or not line.strip():
                continue
            parts = line.rstrip(b"\r\n").split(b",")
            if len(parts) != len(columns):
                # quoted comma or malformed line: exact csv fallback
                parsed = next(csv.reader([line.decode("utf-8", "replace")]))
                selected = [parsed[i] if i < len(parsed) else "" for i in only.values()] \
                    if only is not None else list(parsed)
                yield selected
            else:
                selected = []
                for i in only.values():
                    v = parts[i].strip()
                    if len(v) >= 2 and v.startswith(b'"') and v.endswith(b'"'):
                        v = v[1:-1]
                    if decode_indices is None or i in decode_indices:
                        selected.append(v.decode("utf-8", "replace"))
                    else:
                        selected.append(v)
                yield selected
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


def _normalize_kind(kind: str) -> str:
    """Accept both schema-file and compact-profile shorthand dtypes."""
    mapping = {
        "f8": "float64", "f4": "float32", "f2": "float16",
        "i8": "int64", "i4": "int32", "i2": "int16", "i1": "int8",
    }
    return mapping.get(kind, kind)


def _numpy_dtype(columns: list[str], types: list[str], maxlens: list[int]) -> np.dtype:
    fields = []
    for name, kind, length in zip(columns, types, maxlens):
        if kind == "int64":
            fields.append((name, np.int64))
        elif kind in ("int8", "int16", "int32"):
            fields.append((name, np.dtype(kind)))
        elif kind in ("uint8", "uint16", "uint32", "uint64"):
            fields.append((name, np.dtype(kind)))
        elif kind == "float64":
            fields.append((name, np.float64))
        elif kind == "float32":
            fields.append((name, np.float32))
        elif kind == "bool":
            fields.append((name, np.bool_))
        else:
            fields.append((name, np.dtype(f"S{max(1, length)}")))
    return np.dtype(fields)


def _coerce(values, kind: str, width: int):
    # Gaia's null token is lowercase; avoid a .lower() call per field.
    nulls = ((b"", b"null", b"nan", b"na", b"\\n", b"\\N", b"nnnn", b"nnn", b"n")
             if values and isinstance(values[0], bytes) else NULL_TOKENS)
    if kind in ("int8", "int16", "int32", "int64"):
        # PyTables has no nullable ints.  Gaia uses null for some flag/int
        # columns; use -1 as the documented sentinel (astrotoys does the same).
        def _int_or_null(v):
            if v in nulls:
                return -1
            try:
                return int(v)
            except ValueError:
                text = v.decode("ascii", "ignore") if isinstance(v, bytes) else str(v)
                if set(text.lower()) <= set("0n"):
                    return -1
                raise
        return np.array([_int_or_null(v) for v in values], dtype=np.dtype(kind))
    if kind in ("uint8", "uint16", "uint32", "uint64"):
        def _uint_or_null(v):
            if v in nulls:
                return 0
            try:
                return int(v)
            except ValueError:
                text = v.decode("ascii", "ignore") if isinstance(v, bytes) else str(v)
                if set(text.lower()) <= set("0n"):
                    return 0
                raise
        return np.array([_uint_or_null(v) for v in values], dtype=np.dtype(kind))
    if kind in ("float32", "float64"):
        return np.array([np.nan if v in nulls else float(v) for v in values],
                        dtype=np.dtype(kind))
    if kind == "bool":
        return np.array([v.strip().lower() in (b"true", b"1", b"t", b"yes")
                         if isinstance(v, bytes) else
                         v.strip().lower() in ("true", "1", "t", "yes")
                         for v in values], dtype=bool)
    return np.array([v if isinstance(v, bytes) else v.encode("utf-8")
                     for v in values], dtype=f"S{width}")


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
    source_format: str = "csv"
    column_profile: str = "full"
    layout: str = "source_id"
    order: int = 9
    index_columns: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    jobs: int = 1
    schema_types: dict[str, str] | None = None
    schema_widths: dict[str, int] | None = None

    @property
    def mode(self) -> str:
        if self.region:
            return "trim"
        if self.column_profile == "custom":
            return "trim"
        if self.column_profile == "core":
            return "core"
        return "full"


def load_schema_file(path: Path) -> tuple[dict[str, str], dict[str, int]]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(raw, dict) and "dtype" in raw:
        raw = raw["dtype"]
    if isinstance(raw, dict) and "columns" in raw:
        raw = raw["columns"]
    items = raw.items() if isinstance(raw, dict) else raw
    types: dict[str, str] = {}
    widths: dict[str, int] = {}
    for name, spec in items:
        text = spec if isinstance(spec, str) else str(spec)
        text = text.strip()
        if text in ("str", "string", "unicode"):
            types[name] = "str"
            widths[name] = 30
        elif text in ("bool", "bool_", "?"):
            types[name] = "bool"
            widths[name] = 1
        elif text.startswith(("S", "U", "a")):
            digits = "".join(ch for ch in text[1:] if ch.isdigit())
            types[name] = "str"
            widths[name] = max(1, int(digits) if digits else 30)
        elif text.startswith(("i", "u")):
            digits = "".join(ch for ch in text[1:] if ch.isdigit())
            size = int(digits) if digits else 8
            if size not in (1, 2, 4, 8):
                raise ValueError(f"unsupported integer width for '{name}': {text}")
            types[name] = ("u" if text.startswith("u") else "") + f"int{size * 8}"
        elif text.startswith("f"):
            digits = "".join(ch for ch in text[1:] if ch.isdigit())
            size = int(digits) if digits else 8
            if size not in (2, 4, 8):
                raise ValueError(f"unsupported float width for '{name}': {text}")
            types[name] = f"float{size * 8}"
        else:
            raise ValueError(f"unsupported schema dtype for '{name}': {text}")
    return types, widths


def build_plan(source: Path | None, dataset_path: Path | None, app: Path,
               profile_spec: str | None, dataset_id: str | None,
               region_spec: str | None, attributes: str | None,
               limit: int | None, name: str | None,
               column_profile: str | None = None, layout: str | None = None,
               order: int | None = None, index: str | None = None,
               hdu: int | str | None = None, jobs: int = 1,
               schema: str | None = None) -> tuple[ConsolidatePlan | None, str]:
    dataset_id = dataset_id or None
    src = source or dataset_path
    try:
        profile = load_profile(profile_spec, dataset_id)
    except ValueError as exc:
        low = str(src).lower() if src else ""
        if profile_spec is None and "gaia" in low:
            profile = (BUILTIN_PROFILES["gaia_dr3_source"]
                       if "gdr3" in low and "gaia_source" in low
                       else BUILTIN_PROFILES["gaia_tier"])
        elif profile_spec is None and ("allwise" in low or "wise-allwise" in low):
            profile = BUILTIN_PROFILES["allwise_nir"]
        elif profile_spec is None and "2mass" in low:
            profile = BUILTIN_PROFILES["twomass_nir"]
        else:
            return None, str(exc)
    profile = copy.deepcopy(profile)
    if src is None:
        return None, "no source (give --from or an inventory dataset id)"
    src = Path(src).expanduser()
    if hdu is not None:
        profile.hdu = int(hdu) if isinstance(hdu, str) and hdu.strip().isdigit() else hdu
    try:
        source_files = resolve_sources(src, profile)
    except ValueError as exc:
        return None, str(exc)
    source_format = detect_source_format(source_files[0])
    if source_format not in ("csv", "fits"):
        return None, f"unsupported source format '{source_format}' (csv|fits)"
    if source_format == "fits" and len(source_files) != 1:
        return None, "FITS consolidate currently accepts one file at a time"
    try:
        columns, type_hints = read_schema(source_files[0], profile)
    except ValueError as exc:
        return None, str(exc)
    try:
        region = parse_region(region_spec)
    except ValueError as exc:
        return None, str(exc)
    if layout is None:
        layout = profile.layout
    if layout not in ("spatial", "source_id", "csr"):
        return None, f"unknown layout '{layout}' (spatial|source_id|csr)"
    if order is None:
        order = profile.order
    try:
        nside = hpx.order2nside(order)
    except ValueError as exc:
        return None, str(exc)
    if column_profile is None:
        column_profile = "core" if profile.default_columns else "full"
    if column_profile not in ("core", "full"):
        return None, f"unknown column profile '{column_profile}' (core|full)"
    attrs = [a.strip() for a in attributes.split(",") if a.strip()] if attributes else None
    if attrs:
        column_profile = "custom"
        marker = attrs
    elif column_profile == "core":
        marker = list(profile.default_columns)
    else:
        marker = []
    selected = [c for c in marker if c in columns]
    warnings = [f"requested column not in source: {c}" for c in marker if c not in columns]
    id_key = profile.id_key
    if not id_key or id_key not in columns:
        return None, f"required id column '{id_key}' not in source"
    for need in (profile.positions.get("ra"), profile.positions.get("dec")):
        if not need or need not in columns:
            return None, f"required position column '{need}' not in source"
    if layout == "spatial":
        for need in (profile.positions.get("ra"), profile.positions.get("dec")):
            if not need or need not in columns:
                return None, "spatial layout requires ra/dec columns"
    if not selected:
        selected = list(columns)
    if column_profile in ("core", "custom"):
        # Ensure positions are available for filtering/ipix, but keep the
        # user-visible column set as requested.
        for c in (profile.positions.get("ra"), profile.positions.get("dec")):
            if c and c not in selected:
                selected.append(c)
    if region and not (profile.positions.get("ra") in columns
                       and profile.positions.get("dec") in columns):
        return None, ("region filter requires position columns "
                      f"{profile.positions} present in the catalogue")
    if index is None:
        index_columns = ([id_key] if id_key == "source_id" else [])
        if "phot_g_mean_mag" in selected:
            index_columns.append("phot_g_mean_mag")
    else:
        index_columns = [c.strip() for c in index.split(",") if c.strip()]
        bad = [c for c in index_columns if c not in selected and c != "ipix"]
        if bad:
            return None, f"index columns not selected: {', '.join(bad)}"
    if jobs < 1:
        return None, "jobs must be >= 1"
    schema_types = schema_widths = None
    if schema:
        try:
            schema_types, schema_widths = load_schema_file(Path(schema).expanduser())
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            return None, f"bad schema: {exc}"
        missing = [c for c in selected if c not in schema_types]
        if missing:
            return None, f"schema lacks selected columns: {', '.join(missing)}"
    elif profile.schema_types:
        schema_types = {c: _normalize_kind(t)
                        for c, t in profile.schema_types.items() if c in selected}
        schema_widths = {c: profile.schema_widths.get(c, 30) for c in selected}
        missing = [c for c in selected if c not in schema_types]
        if missing:
            return None, f"profile schema lacks selected columns: {', '.join(missing)}"
    stem = name or dataset_id or (src.stem.split(".")[0] if src.is_file() else src.name)
    dest_dir = Path(app).expanduser() / "consolidated"
    return ConsolidatePlan(
        name=str(stem), source_files=source_files, columns=columns, profile=profile,
        dest_dir=dest_dir, dest_h5=dest_dir / f"{stem}.h5",
        dest_manifest=dest_dir / f"{stem}.manifest.json",
        region=region, attributes=(selected if column_profile in ("core", "custom") else None),
        limit=limit, type_hints=type_hints, source_format=source_format,
        column_profile=column_profile, layout=layout, order=order,
        index_columns=index_columns, warnings=warnings, jobs=int(jobs),
        schema_types=schema_types, schema_widths=schema_widths), ""


def _filters():
    """No compression: a consolidated table is an ephemeral working set.

    Compression only buys disk space and costs writer CPU; the workspace is
    regenerable and deleted after use, so throughput wins.
    """
    return None


def _index_filters():
    """Uncompressed CSI: build speed matters, index size does not."""
    return tables.Filters(complevel=0, complib="zlib")


def _source_columns(plan: ConsolidatePlan) -> list[str]:
    base = list(plan.attributes) if plan.attributes else list(plan.columns)
    for c in (plan.profile.positions.get("ra"), plan.profile.positions.get("dec")):
        if c and c not in base:
            base.append(c)
    return base


def _compute_ipix(ra, dec, order: int) -> np.ndarray:
    nside = hpx.order2nside(order)
    ra = np.asarray(ra, dtype=np.float64)
    dec = np.asarray(dec, dtype=np.float64)
    ipix = np.full(ra.shape, -1, dtype=np.int32)
    good = np.isfinite(ra) & np.isfinite(dec) & (dec >= -90.0) & (dec <= 90.0)
    if np.any(good):
        theta = np.radians(90.0 - dec[good])
        phi = np.radians(np.mod(ra[good], 360.0))
        ipix[good] = hpx.ang2pix_nest(nside, theta, phi).astype(np.int32)
    return ipix


def _make_text_array(block, dtype, source_cols, kinds, widths,
                     ra_col, dec_col, order) -> np.ndarray:
    array = np.empty(len(block), dtype=dtype)
    for i, col in enumerate(source_cols):
        values = [row[i] for row in block]
        array[col] = _coerce(values, kinds[col], widths[col])
    ra = array[ra_col].astype(np.float64, copy=False)
    dec = array[dec_col].astype(np.float64, copy=False)
    array["ipix"] = _compute_ipix(ra, dec, order)
    return array


def _append_text_block(table, block, source_cols, kinds, widths,
                       ra_col, dec_col, order) -> None:
    table.append(_make_text_array(block, table.dtype, source_cols, kinds,
                                  widths, ra_col, dec_col, order))


def _append_fits_block(table, chunk, source_cols, ra_col, dec_col, order) -> None:
    array = np.empty(len(chunk), dtype=table.dtype)
    for col in source_cols:
        values = chunk[col]
        if values.dtype.kind == "S":
            array[col] = values
        elif values.dtype.kind == "U":
            array[col] = np.char.encode(values, "utf-8")
        elif values.dtype.kind == "b":
            array[col] = values.astype(bool)
        elif values.dtype.kind in "iu":
            array[col] = values.astype(array.dtype[col], copy=False)
        elif values.dtype.kind == "f":
            array[col] = values.astype(array.dtype[col], copy=False)
        else:
            raise ValueError(f"unsupported FITS column '{col}' dtype {values.dtype}")
    ra = array[ra_col].astype(np.float64, copy=False)
    dec = array[dec_col].astype(np.float64, copy=False)
    array["ipix"] = _compute_ipix(ra, dec, order)
    table.append(array)


def _fits_dtype(data, columns: list[str]) -> np.dtype:
    fields = []
    for name in columns:
        if name not in data.dtype.names:
            raise ValueError(f"FITS column '{name}' not found")
        dt = np.dtype(data.dtype[name]).newbyteorder("=")
        if dt.shape:
            raise ValueError(f"FITS column '{name}' is not scalar (shape {dt.shape})")
        if dt.kind == "U":
            # Fixed-width bytes are more compact and PyTables-friendly.
            width = max(1, dt.itemsize // 4)
            dt = np.dtype(f"S{width}")
        if dt.kind not in ("b", "i", "u", "f", "S"):
            raise ValueError(f"unsupported FITS column '{name}' dtype {dt}")
        fields.append((name, dt))
    fields.append(("ipix", np.int32))
    return np.dtype(fields)


def _reader_worker(plan, source_cols, index, kinds, widths, ra_col, dec_col,
                   files, shm_name, slot_bytes, data_q, free_q, block_rows) -> None:
    """Parse files into final-dtype blocks and publish them via a shm ring.

    The writer receives only small metadata messages and does nothing but
    ``table.append(array_view)``; no array is pickled through a Queue.
    """
    shm = shared_memory.SharedMemory(name=shm_name)
    try:
        dtype = _numpy_dtype(source_cols, [kinds[c] for c in source_cols],
                             [widths.get(c, 1) for c in source_cols])
        dtype = np.dtype(list(dtype.descr) + [("ipix", np.int32)])
        samples: dict[str, list[str]] = {}
        shard_counts: dict[str, int] = {}
        rows_out = 0
        last_progress = 0
        prof = {k: 0.0 for k in ("parse", "build", "free_wait", "copy", "put", "body")}
        wall0 = time.perf_counter()

        def publish(block):
            nonlocal rows_out, last_progress
            if not block:
                return
            tb = time.perf_counter()
            arr = _make_text_array(block, dtype, source_cols, kinds, widths,
                                   ra_col, dec_col, plan.order)
            if PROFILE:
                prof["build"] += time.perf_counter() - tb
            tf = time.perf_counter()
            slot = free_q.get()
            if PROFILE:
                prof["free_wait"] += time.perf_counter() - tf
            try:
                off = slot * slot_bytes
                view = np.ndarray((arr.size,), dtype=dtype, buffer=shm.buf,
                                  offset=off)
                tc = time.perf_counter()
                view[:] = arr
                if PROFILE:
                    prof["copy"] += time.perf_counter() - tc
                tp = time.perf_counter()
                data_q.put(("block", slot, int(arr.size)))
                if PROFILE:
                    prof["put"] += time.perf_counter() - tp
            except BaseException:
                free_q.put(slot)
                raise
            rows_out += arr.size
            if rows_out - last_progress >= 500000:
                last_progress = rows_out
                data_q.put(("progress", rows_out))

        for path in files:
            block: list[list[str]] = []
            count = 0
            decode_idx = {i for c, i in index.items() if kinds[c] == "str"}
            use_fast = plan.profile.fast_csv and len(source_cols) >= 32
            it = (iter_rows_fast(path, plan.profile, plan.columns, only=index,
                                 decode_indices=decode_idx)
                  if use_fast
                  else iter_rows(path, plan.profile, plan.columns, only=index))
            while True:
                if PROFILE:
                    tp = time.perf_counter()
                try:
                    row = next(it)
                except StopIteration:
                    break
                if PROFILE:
                    prof["parse"] += time.perf_counter() - tp
                values = [v.strip() for v in row]
                if plan.region is not None:
                    ra_i, dec_i = source_cols.index(ra_col), source_cols.index(dec_col)
                    try:
                        ra_v, dec_v = float(values[ra_i]), float(values[dec_i])
                    except ValueError:
                        continue
                    if not region_mask(plan.region, np.array([ra_v]), np.array([dec_v]))[0]:
                        continue
                block.append(values)
                count += 1
                id_key = plan.profile.id_key
                if len(samples) < 3 and id_key in source_cols:
                    sid = values[source_cols.index(id_key)]
                    samples[str(sid)] = list(values)
                if len(block) >= block_rows:
                    publish(block)
                    block = []
            publish(block)
            shard_counts[path.name] = count
        if PROFILE:
            prof["wall"] = time.perf_counter() - wall0
            data_q.put(("profile", prof, len(files), rows_out))
        data_q.put(("sample", samples))
        data_q.put(("done", shard_counts))
    except BaseException:
        data_q.put(("error", traceback.format_exc()))
        try:
            data_q.put(("done", {}))
        except Exception:  # noqa: BLE001
            pass
    finally:
        shm.close()


def _run_csv_parallel(plan: ConsolidatePlan, tmp: Path, emit,
                      source_cols, parse_cols, kinds, widths) -> tuple:
    ra_col = plan.profile.positions["ra"]
    dec_col = plan.profile.positions["dec"]
    index = {c: plan.columns.index(c) for c in source_cols}
    workers = min(int(plan.jobs), len(plan.source_files))
    ctx = mp.get_context("spawn")
    dtype = _numpy_dtype(source_cols, [kinds[c] for c in source_cols],
                         [widths.get(c, 1) for c in source_cols])
    dtype = np.dtype(list(dtype.descr) + [("ipix", np.int32)])
    block_rows = 100000
    slots = max(4, workers + 2)
    slot_bytes = ((block_rows * dtype.itemsize + 63) // 64) * 64
    shm = shared_memory.SharedMemory(create=True, size=slots * slot_bytes)
    free_q = ctx.Queue()
    for i in range(slots):
        free_q.put(i)
    data_q = ctx.Queue()
    procs = []
    for i in range(workers):
        files = plan.source_files[i::workers]
        p = ctx.Process(target=_reader_worker,
                        args=(plan, source_cols, index, kinds, widths,
                              ra_col, dec_col, files, shm.name, slot_bytes,
                              data_q, free_q, block_rows))
        p.start()
        procs.append(p)
    rows_out = 0
    samples: dict[str, list[str]] = {}
    shard_counts: dict[str, int] = {}
    errors: list[str] = []
    profiles: list[tuple] = []
    done = 0
    ok = False
    wprof = {k: 0.0 for k in ("get_wait", "append", "free_put", "progress")}
    try:
        with tables.open_file(tmp, "w") as h5:
            table = h5.create_table("/", "table", dtype,
                                    title=f"consolidated {plan.name}",
                                    filters=_filters())
            while done < workers:
                tg = time.perf_counter()
                item = data_q.get()
                if PROFILE:
                    wprof["get_wait"] += time.perf_counter() - tg
                kind = item[0]
                if kind == "block":
                    slot, nrows = int(item[1]), int(item[2])
                    view = np.ndarray((nrows,), dtype=dtype, buffer=shm.buf,
                                      offset=slot * slot_bytes)
                    ta = time.perf_counter()
                    table.append(view)
                    if PROFILE:
                        wprof["append"] += time.perf_counter() - ta
                    rows_out += nrows
                    tf = time.perf_counter()
                    free_q.put(slot)
                    if PROFILE:
                        wprof["free_put"] += time.perf_counter() - tf
                elif kind == "profile":
                    profiles.append(item[1:])
                elif kind == "sample":
                    for sid, values in item[1].items():
                        samples.setdefault(sid, values)
                elif kind == "progress":
                    tp = time.perf_counter()
                    emit("progress", {"done": item[1], "written": rows_out})
                    if PROFILE:
                        wprof["progress"] += time.perf_counter() - tp
                elif kind == "error":
                    errors.append(item[1])
                elif kind == "done":
                    shard_counts.update(item[1])
                    done += 1
            table.flush()
        ok = True
    finally:
        if not ok:
            for p in procs:
                if p.is_alive():
                    p.terminate()
        for p in procs:
            p.join()
        free_q.close()
        data_q.close()
        shm.close()
        shm.unlink()
    if errors:
        raise RuntimeError("reader failure:\n" + "\n".join(errors))
    if PROFILE:
        emit("log", {"text": "profile " + json.dumps({
            "reader": profiles,
            "writer": {k: round(v, 3) for k, v in wprof.items()},
        }, ensure_ascii=False)})
    emit("log", {"text": f"written {rows_out} row(s) with {workers} reader(s) "
                         f"(shared-memory ring, {slots} slots)"})
    return source_cols, parse_cols, kinds, widths, samples, rows_out, rows_out, shard_counts


def _run_csv(plan: ConsolidatePlan, tmp: Path, emit) -> tuple[list[str], list[str], dict, dict, dict, int, int, dict]:
    source_cols = _source_columns(plan)
    index = {c: plan.columns.index(c) for c in source_cols}
    t_infer = time.time()
    if plan.schema_types is not None:
        types = [plan.schema_types[c] for c in source_cols]
        maxlens = [plan.schema_widths.get(c, 1) for c in source_cols]
        emit("log", {"text": "schema types supplied; skipping full type scan"})
    else:
        types, maxlens = infer_types(plan.source_files, plan.profile, plan.columns,
                                     index, plan.limit, emit, hints=plan.type_hints)
        emit("log", {"text": f"type scan: {time.time()-t_infer:.1f}s"})
    parse_cols = source_cols + ["ipix"]
    dtype = _numpy_dtype(source_cols, types, maxlens)
    dtype = np.dtype(list(dtype.descr) + [("ipix", np.int32)])
    kinds = {c: t for c, t in zip(source_cols, types)}
    widths = {c: max(1, ml) for c, ml in zip(source_cols, maxlens)}
    if plan.jobs > 1 and len(plan.source_files) == 1:
        emit("log", {"text": "jobs>1 ignored for a single CSV.gz (not seekable); "
                             "split the file or use multiple source files"})
    if plan.jobs > 1 and plan.limit is None and len(plan.source_files) > 1:
        return _run_csv_parallel(plan, tmp, emit, source_cols, parse_cols,
                                 kinds, widths)
    ra_col = plan.profile.positions["ra"]
    dec_col = plan.profile.positions["dec"]
    rows_in = rows_out = 0
    shard_counts: dict[str, int] = {}
    samples: dict[str, list[str]] = {}
    block: list[list[str]] = []
    block_rows = 20000
    with tables.open_file(tmp, "w") as h5:
        table = h5.create_table("/", "table", dtype,
                                title=f"consolidated {plan.name}",
                                filters=_filters())
        for path in plan.source_files:
            shard_count = 0
            for row in iter_rows(path, plan.profile, plan.columns, only=index,
                                 limit=(plan.limit - rows_in) if plan.limit else None):
                if plan.limit is not None and rows_in >= plan.limit:
                    break
                rows_in += 1
                values = [v.strip() for v in row]
                if plan.region is not None:
                    ra_i, dec_i = source_cols.index(ra_col), source_cols.index(dec_col)
                    try:
                        ra_v, dec_v = float(values[ra_i]), float(values[dec_i])
                    except ValueError:
                        continue
                    if not region_mask(plan.region, np.array([ra_v]), np.array([dec_v]))[0]:
                        continue
                block.append(values)
                if len(samples) < 3:
                    id_key = plan.profile.id_key
                    try:
                        sid = values[source_cols.index(id_key)]
                    except (ValueError, IndexError):
                        sid = None
                    if sid is not None:
                        if isinstance(sid, bytes):
                            sid = sid.decode("utf-8", "replace")
                        samples[str(sid)] = [
                            v.decode("utf-8", "replace") if isinstance(v, bytes) else v
                            for v in values]
                rows_out += 1
                shard_count += 1
                if len(block) >= block_rows:
                    _append_text_block(table, block, source_cols, kinds, widths,
                                       ra_col, dec_col, plan.order)
                    block = []
                if rows_in % 500000 == 0:
                    emit("progress", {"done": rows_in, "written": rows_out})
            shard_counts[path.name] = shard_count
            if plan.limit is not None and rows_in >= plan.limit:
                break
        if block:
            _append_text_block(table, block, source_cols, kinds, widths,
                               ra_col, dec_col, plan.order)
        emit("log", {"text": f"parsed/written {rows_out} row(s) of {rows_in} scanned "
                               f"in {time.time()-t_infer:.1f}s total"})
    return source_cols, parse_cols, kinds, widths, samples, rows_in, rows_out, shard_counts


def _run_fits(plan: ConsolidatePlan, tmp: Path, emit) -> tuple[list[str], list[str], dict, dict, dict, int, int, dict]:
    fits = _fits_module()
    source_cols = _source_columns(plan)
    ra_col = plan.profile.positions["ra"]
    dec_col = plan.profile.positions["dec"]
    rows_in = rows_out = 0
    shard_counts: dict[str, int] = {}
    samples: dict[str, list[str]] = {}
    with fits.open(plan.source_files[0], memmap=True) as hdul:
        hdu = _fits_table(hdul, plan.profile.hdu)
        data = hdu.data
        dtype = _fits_dtype(data, source_cols)
        parse_cols = source_cols + ["ipix"]
        kinds = {c: ("str" if dtype[c].kind == "S" else
                     "int64" if dtype[c].kind in "iu" else
                     "float64" if dtype[c].kind == "f" else "bool")
                 for c in source_cols}
        widths = {c: dtype[c].itemsize for c in source_cols if dtype[c].kind == "S"}
        with tables.open_file(tmp, "w") as h5:
            table = h5.create_table("/", "table", dtype,
                                    title=f"consolidated {plan.name}",
                                    filters=_filters(), expectedrows=len(data))
            step = 50000
            for start in range(0, len(data), step):
                stop = min(len(data), start + step)
                chunk = data[start:stop]
                # Convert to a plain structured array so field access works
                # for both FITS_rec and memmap-backed tables.
                plain = np.empty(len(chunk), dtype=[(c, data.dtype[c]) for c in source_cols])
                for c in source_cols:
                    plain[c] = chunk[c]
                # Apply region/limit before appending.
                if plan.region is not None:
                    ra = plain[ra_col].astype(np.float64)
                    dec = plain[dec_col].astype(np.float64)
                    keep = region_mask(plan.region, ra, dec)
                    plain = plain[keep]
                if plan.limit is not None:
                    remain = plan.limit - rows_in
                    if remain <= 0:
                        break
                    plain = plain[:remain]
                rows_in += len(plain)
                if len(plain) == 0:
                    continue
                _append_fits_block(table, plain, source_cols, ra_col, dec_col, plan.order)
                rows_out += len(plain)
                id_key = plan.profile.id_key
                if len(samples) < 3 and id_key in source_cols:
                    sid = plain[id_key][0]
                    samples[str(sid)] = [str(plain[c][0]) for c in source_cols]
                shard_counts[plan.source_files[0].name] = shard_counts.get(
                    plan.source_files[0].name, 0) + len(plain)
                emit("progress", {"done": rows_in, "written": rows_out})
                if plan.limit is not None and rows_in >= plan.limit:
                    break
    return source_cols, parse_cols, kinds, widths, samples, rows_in, rows_out, shard_counts


def _build_ipix_offsets(h5, table, order: int) -> np.ndarray:
    nside = hpx.order2nside(order)
    npix = hpx.nside2npix(nside)
    counts = np.zeros(npix, dtype=np.int64)
    step = 500000
    for start in range(0, table.nrows, step):
        chunk = table.read(start, min(table.nrows, start + step))
        values = np.asarray(chunk["ipix"], dtype=np.int64)
        values = values[values >= 0]
        if values.size:
            counts += np.bincount(values, minlength=npix)
    pixels = np.nonzero(counts)[0].astype(np.int32)
    offsets = np.empty(pixels.size + 1, dtype=np.int64)
    offsets[0] = 0
    np.cumsum(counts[pixels], out=offsets[1:])
    group = h5.create_group("/", "index", "query indexes")
    parr = h5.create_array(group, "ipix_pixels", pixels)
    arr = h5.create_array(group, "ipix_offsets", offsets)
    for a in (parr, arr):
        a.attrs.order = int(order)
        a.attrs.nside = int(nside)
        a.attrs.npix = int(npix)
        a.attrs.sparse = True
    return offsets


def _build_csr_index(h5, table, order: int) -> dict:
    """Unsorted table + per-pixel row-id CSR; avoids the full sort copy."""
    nside = hpx.order2nside(order)
    npix = hpx.nside2npix(nside)
    ipix = np.asarray(table.cols.ipix[:], dtype=np.int64)
    valid = ipix >= 0
    order_idx = np.argsort(ipix[valid], kind="stable")
    sorted_pix = ipix[valid][order_idx]
    counts = np.bincount(sorted_pix, minlength=npix)
    pixels = np.nonzero(counts)[0].astype(np.int32)
    offsets = np.empty(pixels.size + 1, dtype=np.int64)
    offsets[0] = 0
    np.cumsum(counts[pixels], out=offsets[1:])
    # row ids in the *table*, not in the valid subset
    rowids = np.nonzero(valid)[0][order_idx].astype(np.int64)
    group = h5.create_group("/", "index", "query indexes")
    for name, arr in (("ipix_pixels", pixels), ("ipix_offsets", offsets),
                      ("ipix_rowids", rowids)):
        a = h5.create_array(group, name, arr)
        a.attrs.order = int(order)
        a.attrs.nside = int(nside)
        a.attrs.npix = int(npix)
        a.attrs.csr = True
    return {"pixels": int(pixels.size), "rows": int(rowids.size)}


def _finalize(plan: ConsolidatePlan, tmp: Path, source_cols: list[str],
              parse_cols: list[str], kinds: dict, widths: dict,
              samples: dict, rows_in: int, rows_out: int,
              shard_counts: dict, started: float, emit) -> int:
    with tables.open_file(tmp, "a") as h5:
        table = h5.root.table
        if plan.layout == "spatial":
            t0 = time.time()
            table.cols.ipix.create_csindex()
            t_index = time.time()
            sorted_table = table.copy(h5.root, "table_sorted", sortby="ipix",
                                      checkCSI=True)
            t_copy = time.time()
            h5.remove_node("/table")
            sorted_table.move(h5.root, "table")
            table = h5.root.table
            emit("log", {"text": f"ipix CSI: {t_index-t0:.1f}s; "
                                 f"sort copy: {t_copy-t_index:.1f}s; "
                                 f"total: {time.time()-t0:.1f}s"})
            t_off = time.time()
            _build_ipix_offsets(h5, table, plan.order)
            emit("log", {"text": f"ipix offsets: {time.time()-t_off:.1f}s"})
        elif plan.layout == "csr":
            t0 = time.time()
            info = _build_csr_index(h5, table, plan.order)
            emit("log", {"text": f"csr index: {info['pixels']} pixels, "
                                 f"{info['rows']} rows, {time.time()-t0:.1f}s"})
        index_built = []
        for col in plan.index_columns:
            if col == "ipix" or col not in table.dtype.names:
                continue
            t0 = time.time()
            try:
                getattr(table.cols, col).create_csindex(filters=_index_filters())
                index_built.append(col)
                emit("log", {"text": f"CSI on {col}: {time.time()-t0:.1f}s"})
            except Exception as exc:  # noqa: BLE001 - report, keep table usable
                emit("log", {"text": f"CSI skipped on {col}: {type(exc).__name__}: {exc}"})
        table.attrs.columns = np.array([c.encode("utf-8") for c in parse_cols], dtype="S64")
        table.attrs.types = np.array([kinds.get(c, "int32").encode("utf-8")
                                      for c in parse_cols], dtype="S8")
        table.attrs.rows = int(rows_out)
        table.attrs.epoch = json.dumps(plan.profile.epoch, ensure_ascii=False)
        table.attrs.frame = plan.profile.frame
        table.attrs.sort_key = ("ipix" if plan.layout == "spatial"
                                else "csr" if plan.layout == "csr"
                                else (plan.profile.sort_key or ""))
        table.attrs.id_key = plan.profile.id_key or ""
        table.attrs.layout = plan.layout
        table.attrs.order = int(plan.order)
        table.attrs.nside = int(hpx.order2nside(plan.order))
        table.attrs.column_profile = plan.column_profile
        table.attrs.indexes = json.dumps(index_built)
        h5.root._v_attrs["consolidate"] = json.dumps({
            "kind": "consolidated", "name": plan.name, "mode": plan.mode,
            "profile": plan.profile.name, "created": now_iso(),
            "source_format": plan.source_format,
            "region": plan.region, "attributes": plan.attributes, "limit": plan.limit,
            "column_profile": plan.column_profile, "layout": plan.layout,
            "order": plan.order,
            # HDF5 attributes are capped at ~64 KiB; the full list lives in
            # the manifest, not in the object header.
            "source_count": len(plan.source_files),
            "source_sample": [p.name for p in plan.source_files[:8]],
        }, ensure_ascii=False)
    os.replace(tmp, plan.dest_h5)
    digest = sha256_file(plan.dest_h5)
    size = plan.dest_h5.stat().st_size
    emit("log", {"text": f"{plan.dest_h5.name}: {size/1e6:.1f} MB  sha256={digest[:16]}…"})
    qc = verify_samples(plan, source_cols, samples)
    manifest = {
        "generated_at": now_iso(),
        "kind": "consolidated",
        "mode": plan.mode,
        "name": plan.name,
        "workspace": str(plan.dest_dir.parent),
        "source": {
            "format": plan.source_format,
            "files": [str(p) for p in plan.source_files],
            "profile": plan.profile.name,
            "epoch": plan.profile.epoch, "frame": plan.profile.frame,
            "note": "master stays at the publication channel; this copy is regenerable",
        },
        "params": {"region": plan.region, "attributes": plan.attributes,
                   "limit": plan.limit, "column_profile": plan.column_profile,
                   "layout": plan.layout, "order": plan.order,
                   "index": plan.index_columns,
                   "warnings": plan.warnings},
        "table": {"file": plan.dest_h5.name, "node": "/table", "rows": rows_out,
                  "columns": parse_cols, "types": [kinds.get(c, "int32") for c in parse_cols],
                  "int_null_sentinel": -1,
                  "bytes": size, "sha256": digest, "layout": plan.layout,
                  "order": plan.order, "nside": int(hpx.order2nside(plan.order)),
                  "compression": "none",
                  "index": ("spatial:ipix_pixels/ipix_offsets + "
                            if plan.layout == "spatial" else
                            "csr:ipix_pixels/ipix_offsets/ipix_rowids + "
                            if plan.layout == "csr" else "")
                           + ",".join(index_built)},
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


def run_consolidate(plan: ConsolidatePlan, emit) -> int:
    plan.dest_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    tmp = plan.dest_h5.with_name(plan.dest_h5.name + ".tmp")
    try:
        if plan.source_format == "fits":
            source_cols, parse_cols, kinds, widths, samples, rows_in, rows_out, shards = \
                _run_fits(plan, tmp, emit)
        else:
            source_cols, parse_cols, kinds, widths, samples, rows_in, rows_out, shards = \
                _run_csv(plan, tmp, emit)
        return _finalize(plan, tmp, source_cols, parse_cols, kinds, widths,
                         samples, rows_in, rows_out, shards, started, emit)
    except BaseException:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def _row_values(row, cols):
    values = []
    for c in cols:
        v = row[c]
        if isinstance(v, bytes):
            v = v.decode("utf-8")
        values.append(v)
    return values


def verify_samples(plan: ConsolidatePlan, cols: list[str],
                   samples: dict) -> dict:
    """Compare sampled source rows against a fresh read of the consolidated table."""
    report = {"samples": 0, "matched": 0, "mismatches": []}
    if not samples:
        return report
    with tables.open_file(plan.dest_h5, "r") as h5:
        table = h5.get_node("/table")
        id_key = plan.profile.id_key
        for sid, expected in samples.items():
            if id_key in table.dtype.names:
                if table.dtype[id_key].kind in ("i", "u"):
                    got_rows = table.read_where(f"{id_key} == {int(sid)}")
                else:
                    got_rows = table.read_where(f"{id_key} == {sid!r}")
            else:
                continue
            if len(got_rows) == 0:
                report["mismatches"].append({"source_id": sid, "reason": "not found"})
                continue
            got = _row_values(got_rows[0], cols)
            report["samples"] += 1
            ok = True
            for j, col in enumerate(cols):
                a = got[j]
                b = expected[j]
                if isinstance(b, str):
                    if b.lower() in NULL_TOKENS:
                        if isinstance(a, (int, np.integer)):
                            ok = int(a) == -1
                        elif isinstance(a, (float, np.floating)):
                            ok = bool(np.isnan(a))
                        else:
                            text = a.decode("utf-8", "replace") if isinstance(a, bytes) else str(a)
                            ok = text.strip().lower() == b.strip().lower()
                    else:
                        try:
                            b_num = float(b)
                        except ValueError:
                            b_num = None
                        if b_num is not None and isinstance(a, (int, float, np.floating, np.integer)):
                            tol = 1e-6 if isinstance(a, np.floating) and a.dtype.itemsize <= 4 else 1e-9
                            if abs(float(a) - b_num) > tol * max(1.0, abs(b_num)):
                                ok = False
                        elif str(a) != b:
                            ok = False
                elif isinstance(a, (int, np.integer)):
                    if b.lower() in NULL_TOKENS:
                        if int(a) != -1:
                            ok = False
                    elif str(a) != str(b):
                        ok = False
                elif isinstance(a, (float, np.floating)):
                    if b.lower() in NULL_TOKENS:
                        ok = ok and bool(np.isnan(a))
                    else:
                        tol = 1e-6 if a.dtype.itemsize <= 4 else 1e-9
                        if abs(float(a) - float(b)) > tol * max(1.0, abs(float(b))):
                            ok = False
                elif str(a) != str(b):
                    ok = False
                if not ok:
                    report["mismatches"].append({"source_id": sid, "column": col})
                    break
            if ok:
                report["matched"] += 1
    return report


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()
