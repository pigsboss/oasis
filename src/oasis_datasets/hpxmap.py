"""Bincount a consolidated catalogue onto a HEALPix map.

Unlike AstroToys ``table2hpx.py`` (fixed nside 4096 and the level-12
``source_id`` formula), this uses the actual stored HEALPix pixels when the
target resolution is coarser than or equal to the store order, and exact
RA/Dec when it is finer.  The pixel value is user-defined via a small
expression, so the same command can emit source counts, summed flux,
magnitude-derived relative flux, mean colour, or a weighted mean.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import tables

from . import hpx

__all__ = ["MapResult", "build_map", "write_healpix_fits", "write_npy_map"]

FUNCS = {
    "np": np,
    "abs": np.abs,
    "log": np.log,
    "log10": np.log10,
    "exp": np.exp,
    "sqrt": np.sqrt,
    "power": np.power,
    "where": np.where,
    "isfinite": np.isfinite,
    "nan_to_num": np.nan_to_num,
    "minimum": np.minimum,
    "maximum": np.maximum,
}


@dataclass
class MapResult:
    values: np.ndarray
    meta: dict

    @property
    def nside(self) -> int:
        return int(self.meta["nside"])


def _expr_columns(expr: str, columns) -> list[str]:
    names = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr or ""))
    return [c for c in columns if c in names]


def _eval(expr: str, arrays: dict[str, np.ndarray]):
    env = dict(FUNCS)
    env.update(arrays)
    return eval(expr, {"__builtins__": {}}, env)  # noqa: S307 - local CLI expression


def _pixels(table, chunk: dict, source_order: int, target_order: int,
            nside: int) -> np.ndarray:
    if "ipix" in chunk and target_order <= source_order:
        shift = 2 * (source_order - target_order)
        return (np.asarray(chunk["ipix"], dtype=np.int64) >> shift)
    if "ra" not in chunk or "dec" not in chunk:
        raise ValueError("RA/Dec are required when target nside is finer than the store")
    ra = np.asarray(chunk["ra"], dtype=np.float64)
    dec = np.asarray(chunk["dec"], dtype=np.float64)
    pix = np.full(ra.shape, -1, dtype=np.int64)
    good = np.isfinite(ra) & np.isfinite(dec) & (dec >= -90.0) & (dec <= 90.0)
    if np.any(good):
        theta = np.radians(90.0 - dec[good])
        phi = np.radians(np.mod(ra[good], 360.0))
        pix[good] = hpx.ang2pix_nest(nside, theta, phi).astype(np.int64)
    return pix


def build_map(path: Path | str, nside: int, quantity: str = "count",
              expr: str | None = None, weight_expr: str | None = None,
              unit: str | None = None, label: str | None = None,
              chunk_rows: int = 1_000_000, limit: int | None = None,
              progress=None) -> MapResult:
    """Bincount a consolidated table into a NESTED HEALPix map."""
    nside = int(nside)
    order = hpx.nside2order(nside)
    npix = hpx.nside2npix(nside)
    quantity = quantity.lower()
    if quantity not in ("count", "sum", "mean", "weighted_mean"):
        raise ValueError("quantity must be count|sum|mean|weighted_mean")
    if quantity != "count" and not expr:
        raise ValueError(f"quantity={quantity} requires an expression")
    if quantity == "weighted_mean" and not weight_expr:
        raise ValueError("weighted_mean requires --weight-expr")
    path = Path(path).expanduser()
    with tables.open_file(path, "r") as h5:
        table = h5.get_node("/table")
        source_order = int(table.attrs.order or 0)
        if source_order <= 0:
            source_order = 9  # consolidated default
        target_order = order
        need_expr = _expr_columns(expr or "", table.dtype.names)
        need_weight = _expr_columns(weight_expr or "", table.dtype.names)
        needed = set(need_expr) | set(need_weight)
        if target_order <= source_order and "ipix" in table.dtype.names:
            needed.add("ipix")
        else:
            needed.update(("ra", "dec"))
        missing = [c for c in needed if c not in table.dtype.names]
        if missing:
            raise ValueError(f"columns not in table: {', '.join(sorted(missing))}")
        nrows = int(table.nrows)
        if limit is not None:
            nrows = min(nrows, int(limit))
        total = np.zeros(npix, dtype=np.float64)
        count = np.zeros(npix, dtype=np.float64) if quantity in ("mean", "weighted_mean") else None
        weight_total = np.zeros(npix, dtype=np.float64) if quantity == "weighted_mean" else None
        step = max(1, int(chunk_rows))
        done = 0
        for start in range(0, nrows, step):
            stop = min(nrows, start + step)
            chunk = {c: table.read(start, stop, field=c) for c in needed}
            pix = _pixels(table, chunk, source_order, target_order, nside)
            arrays = {c: chunk[c] for c in need_expr + need_weight}
            if quantity == "count":
                weights = np.ones(stop - start, dtype=np.float64)
                good = pix >= 0
            else:
                values = np.asarray(_eval(expr, arrays), dtype=np.float64)
                good = (pix >= 0) & np.isfinite(values)
                if quantity == "weighted_mean":
                    weights = np.asarray(_eval(weight_expr, arrays), dtype=np.float64)
                    good &= np.isfinite(weights)
                    total += np.bincount(pix[good], weights=(values * weights)[good],
                                         minlength=npix)
                    weight_total += np.bincount(pix[good], weights=weights[good],
                                                minlength=npix)
                elif quantity == "mean":
                    weights = values
                    count += np.bincount(pix[good], minlength=npix).astype(np.float64)
                    total += np.bincount(pix[good], weights=values[good], minlength=npix)
                else:  # sum
                    weights = values
            if quantity in ("count", "sum"):
                total += np.bincount(pix[good], weights=weights[good], minlength=npix)
            done += stop - start
            if progress:
                progress(done, nrows)
        if quantity == "mean":
            values_out = np.divide(total, count, out=np.zeros_like(total),
                                   where=count > 0)
        elif quantity == "weighted_mean":
            values_out = np.divide(total, weight_total, out=np.zeros_like(total),
                                   where=weight_total != 0)
        else:
            values_out = total
    meta = {
        "source": str(path), "table": "/table", "rows": int(nrows),
        "nside": nside, "order": order, "npix": npix, "nest": True,
        "coord": "C", "quantity": quantity, "expr": expr,
        "weight_expr": weight_expr, "unit": unit or "count",
        "label": label or quantity, "pixel_source": (
            f"ipix>>{2*(source_order-order)}" if target_order <= source_order
            else "ra/dec ang2pix"),
        "source_order": source_order,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return MapResult(values=values_out, meta=meta)


def _fmt_value(value) -> str:
    if isinstance(value, bool):
        return "T" if value else "F"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.10G}"
    return "'" + str(value).replace("'", "''") + "'"


def _card(key: str, value=None, comment: str | None = None) -> str:
    key = key.upper()[:8]
    if key in ("COMMENT", "HISTORY") and value is not None:
        return f"{key:<8} {str(value)}"[:80].ljust(80)
    if value is None:
        card = f"{key:<8}"
    else:
        card = f"{key:<8}= {_fmt_value(value):>20}"
    if comment:
        card += f" / {comment}"
    return card[:80].ljust(80)


def _header_bytes(cards: list[str]) -> bytes:
    cards = [c.ljust(80)[:80] for c in cards] + ["END".ljust(80)]
    cards += [" " * 80] * ((-len(cards)) % 36)
    return "".join(cards).encode("ascii")


def _pad(data: bytes) -> bytes:
    return data + b"\x00" * ((-len(data)) % 2880)


def write_healpix_fits(path: Path | str, result: MapResult) -> Path:
    values = np.asarray(result.values, dtype=np.float64)
    meta = result.meta
    primary = [_card("SIMPLE", True, "conforms to FITS standard"),
               _card("BITPIX", 8, "no primary data"),
               _card("NAXIS", 0, "no primary data"),
               _card("EXTEND", True)]
    ext = [
        _card("XTENSION", "BINTABLE", "binary table extension"),
        _card("BITPIX", 8, "8-bit bytes"),
        _card("NAXIS", 2, "2-dimensional binary table"),
        _card("NAXIS1", 8, "bytes per row"),
        _card("NAXIS2", values.size, "number of rows"),
        _card("PCOUNT", 0, "no heap"),
        _card("GCOUNT", 1, "one data group"),
        _card("TFIELDS", 1, "one column"),
        _card("TTYPE1", "SIGNAL", "HEALPix value"),
        _card("TFORM1", "D", "64-bit floating point"),
        _card("TUNIT1", meta.get("unit", "count")[:68]),
        _card("EXTNAME", "HEALPIX", "HEALPix map"),
        _card("PIXTYPE", "HEALPIX", "HEALPix pixelisation"),
        _card("ORDERING", "NESTED", "NESTED pixel ordering"),
        _card("NSIDE", meta["nside"], "HEALPix resolution"),
        _card("ORDER", meta["order"], "nside=2^order"),
        _card("COORDSYS", "C", "celestial coordinates"),
        _card("RADESYS", "ICRS", "ICRS reference frame"),
        _card("FIRSTPIX", 0, "first pixel"),
        _card("LASTPIX", values.size - 1, "last pixel"),
        _card("INDXSCHM", "IMPLICIT", "implicit indexing"),
        _card("OBJECT", meta.get("label", "map")[:68], "map label"),
        _card("QUANTITY", meta["quantity"], "bincount quantity"),
        _card("BUNIT", meta.get("unit", "count")[:68], "physical unit"),
        _card("NROWS", meta["rows"], "rows processed"),
        _card("SOURCE", Path(meta["source"]).name[:68], "input table"),
        _card("HISTORY", "oasis-datasets hpxmap"),
    ]
    if meta.get("expr"):
        ext.append(_card("EXPR", meta["expr"][:68], "value expression"))
    if meta.get("weight_expr"):
        ext.append(_card("WEIGHTEX", meta["weight_expr"][:68], "weight expression"))
    payload = (_header_bytes(primary) + _header_bytes(ext)
               + _pad(values.astype(">f8").tobytes(order="C")))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path


def write_npy_map(path: Path | str, result: MapResult) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(path, result.values)
    path.with_suffix(path.suffix + ".json").write_text(
        json.dumps(result.meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
