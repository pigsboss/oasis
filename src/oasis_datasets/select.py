"""Select from a consolidated PyTables catalogue.

The consolidated table is sorted by HEALPix ``ipix`` and carries a sparse
``ipix_pixels``/``ipix_offsets`` index plus CSI indexes on selected columns
(``source_id``, ``phot_g_mean_mag``).  This module exposes ID, cone, box and
PyTables-expression selection without loading the whole catalogue.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import tables
from numpy.lib.recfunctions import repack_fields

from . import hpx

__all__ = ["Selection", "ConsolidatedCatalog", "select"]


@dataclass
class Selection:
    arrays: np.ndarray
    meta: dict

    def __len__(self) -> int:
        return int(self.arrays.size)

    def to_npy(self, path: Path | str) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.save(path, self.arrays)
        return path

    def to_csv(self, path: Path | str, null: str = "null") -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        cols = list(self.arrays.dtype.names or ())
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(cols)
            for row in self.arrays:
                values = []
                for c in cols:
                    v = row[c]
                    if isinstance(v, bytes):
                        v = v.decode("utf-8", "replace")
                    elif isinstance(v, np.floating):
                        v = null if np.isnan(v) else repr(float(v))
                    elif isinstance(v, np.integer):
                        v = str(int(v))
                    elif isinstance(v, np.bool_):
                        v = "true" if v else "false"
                    values.append(v)
                writer.writerow(values)
        return path

    def to_fits(self, path: Path | str) -> Path:
        try:
            from astropy.io import fits  # type: ignore
        except Exception as exc:  # noqa: BLE001
            raise ValueError("FITS output requires astropy (pip install astropy)") from exc
        cols = []
        for name in self.arrays.dtype.names or ():
            arr = self.arrays[name]
            dt = arr.dtype
            if dt.kind == "S":
                fmt = f"A{dt.itemsize}"
            elif dt.kind == "b":
                fmt = "L"
            elif dt.kind == "i":
                fmt = {1: "B", 2: "I", 4: "J", 8: "K"}[dt.itemsize]
            elif dt.kind == "u":
                fmt = {1: "B", 2: "I", 4: "J", 8: "K"}[dt.itemsize]
            elif dt.kind == "f":
                fmt = {4: "E", 8: "D"}[dt.itemsize]
            else:
                raise ValueError(f"unsupported column '{name}' dtype {dt}")
            cols.append(fits.Column(name=name, format=fmt, array=arr))
        hdu = fits.BinTableHDU.from_columns(cols)
        for k, v in self.meta.items():
            if isinstance(v, (str, int, float, bool)):
                hdu.header[f"HIERARCH SKY_{k.upper()}"] = v
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fits.HDUList([fits.PrimaryHDU(), hdu]).writeto(path, overwrite=True)
        return path


def _columns_condition(where: str, columns: tuple[str, ...]) -> str:
    """Validate identifiers in a PyTables condition against table columns."""
    if not where:
        return ""
    tokens = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", where))
    allowed = set(columns) | {"and", "or", "not", "in", "True", "False"}
    bad = sorted(t for t in tokens if t not in allowed)
    if bad:
        raise ValueError(f"unknown identifier(s) in --where: {', '.join(bad)}")
    return where


def _box_ra_ranges(ra1: float, ra2: float) -> list[tuple[float, float]]:
    ra1, ra2 = ra1 % 360.0, ra2 % 360.0
    if ra1 <= ra2:
        return [(ra1, ra2)]
    return [(ra1, 360.0), (0.0, ra2)]


class ConsolidatedCatalog:
    def __init__(self, path: Path | str):
        self.path = Path(path).expanduser()
        if not self.path.is_file():
            raise FileNotFoundError(self.path)
        with tables.open_file(self.path, "r") as h5:
            table = h5.get_node("/table")
            self.columns = tuple(table.dtype.names or ())
            self.rows = int(table.nrows)
            self.layout = str(table.attrs.layout or "source_id")
            self.order = int(table.attrs.order or 9)
            self.nside = int(table.attrs.nside or hpx.order2nside(self.order))
            self.attrs = {k: table.attrs[k] for k in table.attrs._v_attrnames
                          if not k.startswith("_")}
            self.meta = {}
            try:
                self.meta = json.loads(h5.root._v_attrs["consolidate"])
            except Exception:  # noqa: BLE001
                pass
            self.pixels = np.array(h5.root.index.ipix_pixels[:]) \
                if "/index/ipix_pixels" in h5 else None
            self.offsets = np.array(h5.root.index.ipix_offsets[:]) \
                if "/index/ipix_offsets" in h5 else None
            self.rowids = np.array(h5.root.index.ipix_rowids[:]) \
                if "/index/ipix_rowids" in h5 else None
            self._pix_ra = None
            self._pix_dec = None

    def __enter__(self) -> "ConsolidatedCatalog":
        return self

    def __exit__(self, *exc) -> None:
        return None

    def _pixel_centers(self):
        if self._pix_ra is None:
            if self.pixels is None:
                self._pix_ra = np.array([], dtype=np.float64)
                self._pix_dec = np.array([], dtype=np.float64)
            else:
                theta, phi = hpx.pix2ang_nest(self.nside, self.pixels)
                self._pix_ra = np.degrees(phi)
                self._pix_dec = 90.0 - np.degrees(theta)
        return self._pix_ra, self._pix_dec

    def _cone_pixels(self, cone) -> np.ndarray:
        ra, dec, radius = cone
        if self.pixels is None:
            raise ValueError("cone selection requires layout=spatial")
        cand = hpx.query_disc_candidates(self.nside, ra, dec, radius,
                                         pixels=self.pixels)
        if cand.size == 0:
            return np.array([], dtype=np.int64)
        pos = np.searchsorted(self.pixels, cand)
        ok = pos < self.pixels.size
        pos = pos[ok]
        cand = cand[ok]
        return pos[self.pixels[pos] == cand]

    def _box_pixels(self, box) -> np.ndarray:
        ra1, ra2, d1, d2 = box
        if self.pixels is None:
            raise ValueError("box selection requires layout=spatial")
        pra, pdec = self._pixel_centers()
        margin = hpx.max_tile_radius_deg(self.nside)
        dec_ok = (pdec >= d1 - margin) & (pdec <= d2 + margin)
        ra_ok = np.zeros(pra.size, dtype=bool)
        for lo, hi in _box_ra_ranges(ra1, ra2):
            ra_ok |= (pra >= lo - margin) & (pra <= hi + margin)
        return np.where(dec_ok & ra_ok)[0]

    def _read_ranges(self, table, positions, where: str,
                     exact, limit: int | None) -> np.ndarray:
        if positions.size == 0:
            return np.empty(0, dtype=table.dtype)
        starts = self.offsets[positions]
        stops = self.offsets[positions + 1]
        out = []
        total = 0
        if self.rowids is not None:
            pieces = [self.rowids[s:e] for s, e in zip(starts, stops) if e > s]
            if not pieces:
                return np.empty(0, dtype=table.dtype)
            rows = np.concatenate(pieces)
            if where:
                allowed = np.asarray(table.get_where_list(where), dtype=np.int64)
                rows = rows[np.isin(rows, allowed)] if allowed.size else rows[:0]
            if rows.size:
                block = table.read_coordinates(rows)
                if exact is not None:
                    block = block[exact(block)]
                out.append(block)
                total = block.size
            return out[0][:limit] if out and limit is not None else (out[0] if out else np.empty(0, dtype=table.dtype))
        for start, stop in zip(starts, stops):
            if stop <= start:
                continue
            if where:
                block = table.read_where(where, start=int(start), stop=int(stop))
            else:
                block = table.read(start=int(start), stop=int(stop))
            if exact is not None:
                block = block[exact(block)]
            if block.size:
                out.append(block)
                total += block.size
                if limit is not None and total >= limit:
                    break
        if not out:
            return np.empty(0, dtype=table.dtype)
        result = np.concatenate(out)
        return result[:limit] if limit is not None else result

    def select(self, ids=None, cone=None, box=None, where: str = "",
               columns=None, limit: int | None = None) -> Selection:
        where = _columns_condition(where, self.columns) if where else ""
        selected = list(columns) if columns else list(self.columns)
        missing = [c for c in selected if c not in self.columns]
        if missing:
            raise ValueError(f"columns not in catalogue: {', '.join(missing)}")
        with tables.open_file(self.path, "r") as h5:
            table = h5.get_node("/table")
            table_dtype = table.dtype
            if ids:
                clauses = [f"source_id == {int(i)}" for i in ids]
                cond = " | ".join(f"({c})" for c in clauses)
                if where:
                    cond = f"({cond}) & ({where})"
                rows = table.read_where(cond)
                if limit is not None:
                    rows = rows[:limit]
            elif cone is not None:
                positions = self._cone_pixels(cone)
                ra, dec, radius = cone

                def exact(block):
                    sep = hpx.angular_distance_deg(
                        ra, dec, block["ra"].astype(np.float64),
                        block["dec"].astype(np.float64))
                    return sep <= radius

                rows = self._read_ranges(table, positions, where, exact, limit)
            elif box is not None:
                positions = self._box_pixels(box)
                ra1, ra2, d1, d2 = box

                def exact(block):
                    ra = block["ra"].astype(np.float64) % 360.0
                    dec = block["dec"].astype(np.float64)
                    ok = (dec >= d1) & (dec <= d2)
                    if ra1 % 360.0 <= ra2 % 360.0:
                        ok &= (ra >= ra1 % 360.0) & (ra <= ra2 % 360.0)
                    else:
                        ok &= (ra >= ra1 % 360.0) | (ra <= ra2 % 360.0)
                    return ok

                rows = self._read_ranges(table, positions, where, exact, limit)
            else:
                rows = table.read_where(where) if where else table[:]
                if limit is not None:
                    rows = rows[:limit]
        if rows.size == 0:
            arrays = np.empty(0, dtype=[(c, table_dtype[c]) for c in selected])
        else:
            arrays = repack_fields(rows[selected]) if selected != list(rows.dtype.names) else rows
        meta = {
            "file": str(self.path), "rows": int(arrays.size),
            "columns": selected, "layout": self.layout, "order": self.order,
            "ids": [int(i) for i in ids] if ids else None,
            "cone": list(cone) if cone else None,
            "box": list(box) if box else None,
            "where": where or None,
        }
        return Selection(arrays=arrays, meta=meta)


def select(path: Path | str, **kwargs) -> Selection:
    return ConsolidatedCatalog(path).select(**kwargs)
