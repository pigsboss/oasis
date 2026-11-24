"""Generic spatial cross-match between two HDF5 source tables.

The right-hand catalogue is indexed on a sparse 3-D unit-sphere cell grid;
the left catalogue is streamed in chunks and queries the 27 neighbouring
cells.  This is deliberately independent of HEALPix ordering and works for
any table with RA/Dec columns.  It is the target-layer primitive intended
for Gaia <-> AllWISE/2MASS and other source-table joins.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import tables

from . import hpx

__all__ = ["CrossMatchResult", "GridIndex", "crossmatch_tables"]


def _unit_vectors(ra_deg, dec_deg):
    ra = np.radians(np.asarray(ra_deg, dtype=np.float64))
    dec = np.radians(np.asarray(dec_deg, dtype=np.float64))
    cd = np.cos(dec)
    return np.cos(ra) * cd, np.sin(ra) * cd, np.sin(dec)


def _cell_keys(x, y, z, cell_rad: float) -> tuple[np.ndarray, int]:
    scale = 1.0 / float(cell_rad)
    ix = np.floor((x + 1.0) * scale).astype(np.int64)
    iy = np.floor((y + 1.0) * scale).astype(np.int64)
    iz = np.floor((z + 1.0) * scale).astype(np.int64)
    ncell = int(np.floor(2.0 * scale)) + 1
    # For the intended arcsecond-to-arcminute radii the cube fits int64.
    key = (ix * ncell + iy) * ncell + iz
    return key, ncell


@dataclass
class GridIndex:
    keys: np.ndarray
    ra: np.ndarray
    dec: np.ndarray
    ids: np.ndarray | None
    ncell: int
    cell_rad: float


@dataclass
class CrossMatchResult:
    path: str
    left_rows: int
    right_rows: int
    matches: int
    radius_arcsec: float
    mode: str = "nearest"


def _read_catalog(path: Path | str, node: str, ra_col: str, dec_col: str,
                  id_col: str | None):
    with tables.open_file(Path(path).expanduser(), "r") as h5:
        t = h5.get_node(node)
        ra = np.asarray(t.cols._f_col(ra_col)[:], dtype=np.float64)
        dec = np.asarray(t.cols._f_col(dec_col)[:], dtype=np.float64)
        ids = (np.asarray(t.cols._f_col(id_col)[:]) if id_col else None)
    if ra.shape != dec.shape:
        raise ValueError("RA/Dec length mismatch")
    return ra, dec, ids


def build_grid_index(path: Path | str, node: str = "/table",
                     ra_col: str = "ra", dec_col: str = "dec",
                     id_col: str | None = None,
                     radius_arcsec: float = 3.0) -> GridIndex:
    """Index the right-hand catalogue on a unit-sphere cell grid."""
    ra, dec, ids = _read_catalog(path, node, ra_col, dec_col, id_col)
    good = np.isfinite(ra) & np.isfinite(dec)
    ra, dec = ra[good], dec[good]
    if ids is not None:
        ids = ids[good]
    radius_rad = float(radius_arcsec) * np.pi / (180.0 * 3600.0)
    cell = max(radius_rad * 1.01, 1e-8)
    x, y, z = _unit_vectors(ra, dec)
    keys, ncell = _cell_keys(x, y, z, cell)
    order = np.argsort(keys, kind="mergesort")
    return GridIndex(keys=keys[order], ra=ra[order], dec=dec[order],
                     ids=(ids[order] if ids is not None else None),
                     ncell=ncell, cell_rad=cell)


def _query_candidates(index: GridIndex, x: float, y: float, z: float) -> tuple[np.ndarray, np.ndarray]:
    cell = index.cell_rad
    scale = 1.0 / cell
    ix = int(np.floor((x + 1.0) * scale))
    iy = int(np.floor((y + 1.0) * scale))
    iz = int(np.floor((z + 1.0) * scale))
    chunks = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                a, b, c = ix + dx, iy + dy, iz + dz
                if min(a, b, c) < 0:
                    continue
                k = (a * index.ncell + b) * index.ncell + c
                lo = int(np.searchsorted(index.keys, k, side="left"))
                hi = int(np.searchsorted(index.keys, k, side="right"))
                if hi > lo:
                    chunks.append(np.arange(lo, hi, dtype=np.int64))
    if not chunks:
        return (np.empty(0, dtype=np.int64), np.empty(0), np.empty(0))
    cand = np.concatenate(chunks)
    return cand, index.ra[cand], index.dec[cand]


def crossmatch_tables(left: Path | str, right: Path | str,
                      out: Path | str, radius_arcsec: float = 3.0,
                      left_node: str = "/table", right_node: str = "/table",
                      left_ra: str = "ra", left_dec: str = "dec",
                      right_ra: str = "ra", right_dec: str = "dec",
                      left_id: str | None = None, right_id: str | None = None,
                      chunk_rows: int = 200_000,
                      fmt: str = "hdf5") -> CrossMatchResult:
    """Nearest-neighbour cross-match; one row per left source."""
    right_index = build_grid_index(right, right_node, right_ra, right_dec,
                                   right_id, radius_arcsec)
    radius = float(radius_arcsec)
    left_ra_arr, left_dec_arr, left_ids = _read_catalog(
        left, left_node, left_ra, left_dec, left_id)
    left_rows = left_ra_arr.size
    out = Path(out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "csv":
        return _write_csv_matches(out, left_ra_arr, left_dec_arr, left_ids,
                                  right_index, radius, chunk_rows)
    dtype = [("left_index", "i8"), ("right_index", "i8"),
             ("sep_arcsec", "f8")]
    if left_ids is not None:
        dtype.append(("left_id", left_ids.dtype))
    if right_index.ids is not None:
        dtype.append(("right_id", right_index.ids.dtype))
    matches = []
    for start in range(0, left_rows, chunk_rows):
        stop = min(left_rows, start + chunk_rows)
        for i in range(start, stop):
            if not (np.isfinite(left_ra_arr[i]) and np.isfinite(left_dec_arr[i])):
                continue
            x, y, z = _unit_vectors(left_ra_arr[i:i + 1], left_dec_arr[i:i + 1])
            cand, cra, cdec = _query_candidates(right_index, float(x[0]), float(y[0]), float(z[0]))
            if cand.size == 0:
                continue
            sep = hpx.angular_distance_deg(left_ra_arr[i], left_dec_arr[i], cra, cdec) * 3600.0
            j = int(np.argmin(sep))
            if sep[j] <= radius:
                matches.append((i, int(cand[j]), float(sep[j])))
    with tables.open_file(out, "w") as h5:
        if matches:
            arr = np.zeros(len(matches), dtype=np.dtype(dtype))
            for n, (li, ri, sep) in enumerate(matches):
                arr[n]["left_index"] = li
                arr[n]["right_index"] = ri
                arr[n]["sep_arcsec"] = sep
                if left_ids is not None:
                    arr[n]["left_id"] = left_ids[li]
                if right_index.ids is not None:
                    arr[n]["right_id"] = right_index.ids[ri]
            h5.create_table("/", "matches", arr, title="nearest spatial matches")
        else:
            h5.create_table("/", "matches", np.empty(0, dtype=np.dtype(dtype)))
        h5.root._v_attrs.match = json.dumps({
            "left": str(left), "right": str(right), "radius_arcsec": radius,
            "left_rows": int(left_rows), "right_rows": int(right_index.keys.size),
            "matches": len(matches), "mode": "nearest",
            "cell_rad": right_index.cell_rad,
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }, ensure_ascii=False)
    return CrossMatchResult(str(out), int(left_rows), int(right_index.keys.size),
                            len(matches), radius)


def _write_csv_matches(out: Path, left_ra, left_dec, left_ids,
                       right_index: GridIndex, radius: float,
                       chunk_rows: int) -> CrossMatchResult:
    rows = []
    for i in range(len(left_ra)):
        if not (np.isfinite(left_ra[i]) and np.isfinite(left_dec[i])):
            continue
        x, y, z = _unit_vectors(left_ra[i:i + 1], left_dec[i:i + 1])
        cand, cra, cdec = _query_candidates(right_index, float(x[0]), float(y[0]), float(z[0]))
        if not cand.size:
            continue
        sep = hpx.angular_distance_deg(left_ra[i], left_dec[i], cra, cdec) * 3600.0
        j = int(np.argmin(sep))
        if sep[j] <= radius:
            rows.append((i, int(cand[j]), float(sep[j])))
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["left_index", "right_index", "sep_arcsec"])
        w.writerows(rows)
    return CrossMatchResult(str(out), len(left_ra), int(right_index.keys.size),
                            len(rows), radius)
