"""Build a per-pixel 343-point HEALPix spectral cube from consolidate.

Phase-1 model: Gaia core sources without XP are assigned a blackbody
template from a BP-RP -> Teff grid; the per-pixel cube is the sum of the
source spectra (relative flux, G=6.5 reference, 600 nm normalized).  Every
pixel is explicitly provenance-tagged as inferred.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import tables

from . import hpx

__all__ = [
    "WAVELENGTH", "BP_RP_GRID", "TEFF_GRID", "TEMPLATES",
    "SpectralCubeResult", "blackbody_templates", "template_indices",
    "build_spectral_cube",
]

WAVELENGTH = np.arange(336.0, 1020.0 + 0.1, 2.0, dtype=np.float32)
BP_RP_GRID = np.array([
    -0.50, -0.25, 0.00, 0.30, 0.60, 0.90, 1.20, 1.50,
    1.80, 2.10, 2.40, 2.70, 3.00, 3.40, 3.80, 4.40,
], dtype=np.float32)
TEFF_GRID = np.array([
    15000., 11000., 9000., 7500., 6400., 5600., 5000., 4500.,
    4050., 3700., 3400., 3150., 2950., 2700., 2450., 2200.,
], dtype=np.float32)

# physical constants (SI)
_H = 6.62607015e-34
_C = 2.99792458e8
_KB = 1.380649e-23


def blackbody_templates(wavelength: np.ndarray = WAVELENGTH,
                        teff: np.ndarray = TEFF_GRID) -> np.ndarray:
    """Planck spectra normalized at 600 nm; shape (n_teff, n_wave)."""
    lam = np.asarray(wavelength, dtype=np.float64) * 1e-9
    out = np.empty((len(teff), len(lam)), dtype=np.float32)
    for i, t in enumerate(teff):
        x = _H * _C / (lam * _KB * float(t))
        # exp overflow is harmless for the very blue Rayleigh-Jeans tail
        b = 1.0 / (lam ** 5 * (np.expm1(x)))
        ref = np.interp(600e-9, lam, b)
        out[i] = (b / ref).astype(np.float32)
    return out


TEMPLATES = blackbody_templates()

# Gaia DSC classprob_dsc_combmod_* argmax codes.
NO_G_CLASS_NAMES = ("star", "quasar", "galaxy", "whitedwarf", "binarystar")
# class -> (estimated BP-RP, estimated G-RP, quality group)
# group 1 = RP-only stellar fallback, group 2 = class template.
NO_G_CLASS_MODEL = {
    0: (0.80, 0.60, 1),   # star
    4: (0.80, 0.60, 1),   # binary star
    1: (0.30, 0.30, 2),   # quasar
    2: (0.80, 0.50, 2),   # galaxy
    3: (0.00, 0.00, 2),   # white dwarf
}


def template_indices(bp_rp: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Map BP-RP to template index; returns (indices, missing_mask)."""
    bp_rp = np.asarray(bp_rp, dtype=np.float64)
    missing = ~np.isfinite(bp_rp)
    safe = np.where(missing, 0.7, bp_rp)  # solar-ish fallback
    idx = np.searchsorted(BP_RP_GRID.astype(np.float64), safe, side="right") - 1
    idx = np.clip(idx, 0, len(BP_RP_GRID) - 1).astype(np.int64)
    return idx, missing


@dataclass
class SpectralCubeResult:
    path: str
    rows: int
    nside: int
    npix: int
    nwave: int
    inferred: bool = True
    model: str = "blackbody_bp_rp"
    quality: int = 4
    missing_bprp: int = 0
    missing_g: int = 0


def _flush_pending(flux, pending: list[np.ndarray]) -> None:
    if pending:
        flux.append(np.concatenate(pending, axis=0))
        pending.clear()


def build_spectral_cube(path: Path | str, out: Path | str, nside: int = 2048,
                        chunk_rows: int = 1_000_000,
                        buffer_parents: int = 4096,
                        no_g_supp: Path | str | None = None,
                        progress=None) -> SpectralCubeResult:
    """Stream a consolidated spatial table into a per-pixel spectral cube.

    The source table must be spatial/ipix sorted; each target parent group is
    accumulated in a tiny [children, n_templates] array, so no 1.8B x 343
    intermediate is materialized.
    """
    nside = int(nside)
    target_order = hpx.nside2order(nside)
    npix = hpx.nside2npix(nside)
    nwave = WAVELENGTH.size
    templates = TEMPLATES
    ntemp = templates.shape[0]
    source = Path(path).expanduser()
    out = Path(out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise FileExistsError(f"output exists: {out}")

    supp_ids = supp_code = supp_rp = None
    if no_g_supp is not None:
        with tables.open_file(Path(no_g_supp).expanduser(), "r") as sh:
            st = sh.get_node("/no_g")
            supp_ids = np.asarray(st.cols.source_id[:], dtype=np.int64)
            supp_code = np.asarray(st.cols.class_code[:], dtype=np.int8)
            supp_rp = np.asarray(st.cols.rp_mag[:], dtype=np.float64)
        order = np.argsort(supp_ids)
        supp_ids = supp_ids[order]
        supp_code = supp_code[order]
        supp_rp = supp_rp[order]

    with tables.open_file(source, "r") as src:
        table = src.get_node("/table")
        source_order = int(table.attrs.order or 9)
        if target_order < source_order:
            raise ValueError("target nside must be >= source order")
        children = 4 ** (target_order - source_order)
        nrows = int(table.nrows)

        with tables.open_file(out, "w") as dst:
            spectra = dst.create_group("/", "spectra")
            flux = dst.create_earray(
                spectra, "flux", atom=tables.Float32Atom(),
                shape=(0, nwave), chunkshape=(8192, nwave), filters=None)
            counts = np.zeros(npix, dtype=np.int64)
            count_normal = np.zeros(npix, dtype=np.int64)
            count_rp_only = np.zeros(npix, dtype=np.int64)
            count_class = np.zeros(npix, dtype=np.int64)
            count_no_phot = np.zeros(npix, dtype=np.int64)
            missing_bprp = 0
            missing_g = 0
            processed = 0
            current_parent = -1
            local = None
            local_group = None
            next_parent = 0
            pending: list[np.ndarray] = []
            pending_rows = 0
            step = max(1, int(chunk_rows))
            for start in range(0, nrows, step):
                stop = min(nrows, start + step)
                ra = np.asarray(table.read(start, stop, field="ra"), dtype=np.float64)
                dec = np.asarray(table.read(start, stop, field="dec"), dtype=np.float64)
                gmag = np.asarray(table.read(start, stop, field="phot_g_mean_mag"), dtype=np.float64)
                bprp = np.asarray(table.read(start, stop, field="bp_rp"), dtype=np.float64)
                source_ids = (np.asarray(table.read(start, stop, field="source_id"), dtype=np.int64)
                              if no_g_supp is not None else None)
                rp_mag = (np.asarray(table.read(start, stop, field="phot_rp_mean_mag"), dtype=np.float64)
                          if no_g_supp is not None else None)
                good = (np.isfinite(ra) & np.isfinite(dec)
                        & (dec >= -90.0) & (dec <= 90.0))
                if not np.any(good):
                    continue
                ra = ra[good]
                dec = dec[good]
                gmag = gmag[good]
                bprp = bprp[good]
                if no_g_supp is not None:
                    source_ids = source_ids[good]
                    rp_mag = rp_mag[good]
                child = hpx.ang2pix_nest(
                    nside, np.radians(90.0 - dec), np.radians(np.mod(ra, 360.0)))
                child = np.asarray(child, dtype=np.int64)
                parent = child // children
                offset = child - parent * children
                gvalid = np.isfinite(gmag)
                missing_g += int((~gvalid).sum())
                g_eff = gmag.copy()
                bprp_eff = bprp.copy()
                qgroup = np.zeros(len(gmag), dtype=np.uint8)  # 0 normal
                if no_g_supp is not None and np.any(~gvalid):
                    idx = np.flatnonzero(~gvalid)
                    pos = np.searchsorted(supp_ids, source_ids[idx])
                    ok = pos < supp_ids.size
                    pos = pos[ok]
                    sel = idx[ok]
                    found = supp_ids[pos] == source_ids[sel]
                    sel = sel[found]
                    codes = supp_code[pos[found]]
                    rp = rp_mag[sel].copy()
                    rp_side = supp_rp[pos[found]]
                    rp[~np.isfinite(rp)] = rp_side[~np.isfinite(rp)]
                    has_rp = np.isfinite(rp)
                    for cls, (bprp_v, dgrp, q) in NO_G_CLASS_MODEL.items():
                        m = has_rp & (codes == cls)
                        if np.any(m):
                            bprp_eff[sel[m]] = bprp_v
                            g_eff[sel[m]] = rp[m] + dgrp
                            qgroup[sel[m]] = q
                    m = has_rp & (codes == -1)
                    if np.any(m):
                        bprp_eff[sel[m]] = 0.80
                        g_eff[sel[m]] = rp[m] + 0.60
                        qgroup[sel[m]] = 1
                    # no RP at all, or no supplement row
                    qgroup[idx] = np.where(qgroup[idx] == 0, 3, qgroup[idx])
                tidx, miss = template_indices(bprp_eff)
                missing_bprp += int(miss.sum())
                weights = np.zeros_like(g_eff, dtype=np.float32)
                wgood = np.isfinite(g_eff) & (qgroup != 3)
                weights[wgood] = np.power(
                    10.0, -0.4 * (g_eff[wgood] - 6.5)).astype(np.float32)
                # parent is non-decreasing because the source table is ipix-sorted
                if current_parent < 0:
                    current_parent = int(parent[0])
                    if current_parent > 0:
                        gap = current_parent * children
                        pending.append(np.zeros((gap, nwave), dtype=np.float32))
                        pending_rows += gap
                    local = np.zeros((children, ntemp), dtype=np.float32)
                    local_group = np.zeros((children, 4), dtype=np.int64)
                changes = np.flatnonzero(parent[1:] != parent[:-1]) + 1
                first = 0
                for end in np.r_[changes, len(parent)]:
                    p = int(parent[first])
                    if p != current_parent:
                        if p < current_parent:
                            raise ValueError("source table is not spatial/ipix sorted")
                        # flush the finished parent
                        base = current_parent * children
                        spec = local @ templates
                        pending.append(np.asarray(spec, dtype=np.float32))
                        counts[base:base + children] += local_group.sum(axis=1)
                        count_normal[base:base + children] += local_group[:, 0]
                        count_rp_only[base:base + children] += local_group[:, 1]
                        count_class[base:base + children] += local_group[:, 2]
                        count_no_phot[base:base + children] += local_group[:, 3]
                        pending_rows += children
                        next_parent = current_parent + 1
                        if pending_rows >= buffer_parents * children:
                            _flush_pending(flux, pending)
                            pending_rows = 0
                        # gap parents: keep row order and zero-fill
                        if p > next_parent:
                            gap = (p - next_parent) * children
                            pending.append(np.zeros((gap, nwave), dtype=np.float32))
                            pending_rows += gap
                            if pending_rows >= buffer_parents * children:
                                _flush_pending(flux, pending)
                                pending_rows = 0
                            next_parent = p
                        current_parent = p
                        local = np.zeros((children, ntemp), dtype=np.float32)
                        local_group = np.zeros((children, 4), dtype=np.int64)
                    np.add.at(local, (offset[first:end], tidx[first:end]),
                              weights[first:end])
                    for q in range(4):
                        m = qgroup[first:end] == q
                        if np.any(m):
                            local_group[:, q] += np.bincount(
                                offset[first:end][m], minlength=children)
                    first = end
                processed += len(parent)
                if progress:
                    progress(processed, nrows)
            # final parent
            if current_parent >= 0:
                base = current_parent * children
                spec = local @ templates
                pending.append(np.asarray(spec, dtype=np.float32))
                counts[base:base + children] += local_group.sum(axis=1)
                count_normal[base:base + children] += local_group[:, 0]
                count_rp_only[base:base + children] += local_group[:, 1]
                count_class[base:base + children] += local_group[:, 2]
                count_no_phot[base:base + children] += local_group[:, 3]
                pending_rows += children
                next_parent = current_parent + 1
            _flush_pending(flux, pending)
            if flux.nrows < npix:
                remaining = npix - flux.nrows
                for start in range(0, remaining, 8192):
                    n = min(8192, remaining - start)
                    flux.append(np.zeros((n, nwave), dtype=np.float32))
            # small metadata arrays
            dst.create_array(spectra, "wavelength", WAVELENGTH)
            dst.create_array(spectra, "templates", templates)
            dst.create_array(spectra, "teff", TEFF_GRID)
            dst.create_array(spectra, "count", counts)
            dst.create_array(spectra, "count_normal", count_normal)
            dst.create_array(spectra, "count_rp_only", count_rp_only)
            dst.create_array(spectra, "count_class", count_class)
            dst.create_array(spectra, "count_no_phot", count_no_phot)
            quality = np.full(npix, 4, dtype=np.uint8)
            quality[count_rp_only > 0] = 5
            quality[count_class > 0] = 6
            quality[count_no_phot > 0] = 7
            dst.create_array(spectra, "quality", quality)
            dst.create_array(spectra, "inferred_fraction",
                             np.ones(npix, dtype=np.float32))
            dst.create_array(spectra, "xp_fraction",
                             np.zeros(npix, dtype=np.float32))
            meta = {
                "kind": "spectral_cube", "nside": nside, "order": target_order,
                "npix": npix, "nwave": nwave, "wave_min": float(WAVELENGTH[0]),
                "wave_max": float(WAVELENGTH[-1]), "wave_step": 2.0,
                "source_order": source_order, "children": children,
                "rows": processed, "missing_bp_rp": missing_bprp,
                "missing_g": missing_g,
                "note_missing_g": ("RP-only/class templates used when available; "
                                   "no-broadband sources count but zero flux"),
                "inferred": True,
                "model": ("blackbody_bp_rp_v2" if no_g_supp is not None
                          else "blackbody_bp_rp"),
                "quality": 4, "quality_name": "inferred_blackbody",
                "quality_groups": {
                    "4": "G+BP-RP blackbody",
                    "5": "RP-only stellar fallback",
                    "6": "class-template fallback",
                    "7": "no broadband photometry (zero flux)",
                },
                "no_g_supp": str(no_g_supp) if no_g_supp is not None else None,
                "xp_fraction": 0.0,
                "bunit": "relative flux (G=6.5 reference, 600 nm normalized)",
                "source": str(source), "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "note": "BP-RP -> Teff blackbody templates; not measured XP spectra",
            }
            dst.root._v_attrs.consolidate = json.dumps(meta, ensure_ascii=False)
            dst.create_array(dst.root, "meta",
                             np.frombuffer(json.dumps(meta, ensure_ascii=False).encode(),
                                           dtype=np.uint8))
    return SpectralCubeResult(
        str(out), processed, nside, npix, nwave,
        model=("blackbody_bp_rp_v2" if no_g_supp is not None else "blackbody_bp_rp"),
        missing_bprp=missing_bprp, missing_g=missing_g)
