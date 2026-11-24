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
                        nir_supp: Path | str | None = None,
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
    nir_ids = nir_ok2 = nir_okw = None
    nir_j = nir_h = nir_k = nir_w1 = nir_w2 = None
    if nir_supp is not None and no_g_supp is None:
        raise ValueError("nir_supp requires no_g_supp")
    if nir_supp is not None:
        with tables.open_file(Path(nir_supp).expanduser(), "r") as nh:
            nt = nh.get_node("/nir_supp")
            nir_ids = np.asarray(nt.cols.source_id[:], dtype=np.int64)
            nir_ok2 = np.asarray(nt.cols.match_2mass[:], dtype=bool)
            nir_okw = np.asarray(nt.cols.match_wise[:], dtype=bool)
            nir_j = np.asarray(nt.cols.j_m[:], dtype=np.float64)
            nir_h = np.asarray(nt.cols.h_m[:], dtype=np.float64)
            nir_k = np.asarray(nt.cols.k_m[:], dtype=np.float64)
            nir_w1 = np.asarray(nt.cols.w1mpro[:], dtype=np.float64)
            nir_w2 = np.asarray(nt.cols.w2mpro[:], dtype=np.float64)
        no = np.argsort(nir_ids)
        nir_ids, nir_ok2, nir_okw = nir_ids[no], nir_ok2[no], nir_okw[no]
        nir_j, nir_h, nir_k = nir_j[no], nir_h[no], nir_k[no]
        nir_w1, nir_w2 = nir_w1[no], nir_w2[no]
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
            tier_counts = np.zeros((npix, 7), dtype=np.int32)
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
                              if (no_g_supp is not None or nir_supp is not None) else None)
                rp_mag = (np.asarray(table.read(start, stop, field="phot_rp_mean_mag"), dtype=np.float64)
                          if (no_g_supp is not None or nir_supp is not None) else None)
                good = (np.isfinite(ra) & np.isfinite(dec)
                        & (dec >= -90.0) & (dec <= 90.0))
                if not np.any(good):
                    continue
                ra = ra[good]
                dec = dec[good]
                gmag = gmag[good]
                bprp = bprp[good]
                if no_g_supp is not None or nir_supp is not None:
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
                # A=0 B=1 C=2 D=3 E=4 F=5 G=6 (A/B unused until XP is joined)
                qgroup = np.full(len(gmag), 6, dtype=np.uint8)
                # Normal Gaia G sources: C if BP-RP exists, else D.
                qgroup[gvalid & np.isfinite(bprp)] = 2
                qgroup[gvalid & ~np.isfinite(bprp)] = 3
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
                    nir_ok = np.zeros(len(sel), dtype=bool)
                    nj = np.full(len(sel), np.nan); nh = nj.copy(); nk = nj.copy()
                    nw1 = nj.copy(); nw2 = nj.copy()
                    if nir_supp is not None and len(sel):
                        npos = np.searchsorted(nir_ids, source_ids[sel])
                        nok = npos < nir_ids.size
                        npos2 = npos[nok]
                        nsel = np.flatnonzero(nok)
                        nfound = nir_ids[npos2] == source_ids[sel[nsel]]
                        nsel = nsel[nfound]; npos2 = npos2[nfound]
                        nir_ok[nsel] = nir_ok2[npos2] | nir_okw[npos2]
                        nj[nsel] = nir_j[npos2]; nh[nsel] = nir_h[npos2]; nk[nsel] = nir_k[npos2]
                        nw1[nsel] = nir_w1[npos2]; nw2[nsel] = nir_w2[npos2]
                    has_rp = np.isfinite(rp)
                    # D: NIR match (2MASS or AllWISE)
                    d = nir_ok
                    gd = np.full(len(sel), np.nan)
                    bd = np.full(len(sel), 0.8)
                    gd[has_rp] = rp[has_rp] + 0.6
                    no_rp = d & ~has_rp & np.isfinite(nj)
                    gd[no_rp] = nj[no_rp] + 0.9
                    no_rp2 = d & ~has_rp & ~np.isfinite(nj) & np.isfinite(nw1)
                    gd[no_rp2] = nw1[no_rp2] + 1.0
                    jk = d & np.isfinite(nj) & np.isfinite(nk)
                    bd[jk] = np.clip(0.4 + 1.2 * (nj[jk] - nk[jk]), -0.2, 3.5)
                    ww = d & ~jk & np.isfinite(nw1) & np.isfinite(nw2)
                    bd[ww] = np.clip(0.8 + 0.6 * (nw1[ww] - nw2[ww]), -0.5, 3.0)
                    qso = d & (codes == 1)
                    gal = d & (codes == 2)
                    bd[qso] = 0.3; bd[gal] = 0.8
                    okd = d & np.isfinite(gd)
                    g_eff[sel[okd]] = gd[okd]; bprp_eff[sel[okd]] = bd[okd]
                    qgroup[sel[okd]] = 3
                    # E: only RP
                    e = ~d & has_rp
                    g_eff[sel[e]] = rp[e] + 0.6
                    bprp_eff[sel[e]] = 0.8
                    qgroup[sel[e]] = 4
                    # F: no photometry but a class prior; G: nothing
                    f = ~d & ~has_rp & (codes >= 0)
                    qgroup[sel[f]] = 5
                    qgroup[sel[~d & ~has_rp & (codes < 0)]] = 6
                tidx, miss = template_indices(bprp_eff)
                missing_bprp += int(miss.sum())
                weights = np.zeros_like(g_eff, dtype=np.float32)
                wgood = np.isfinite(g_eff) & (qgroup <= 4)
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
                    local_group = np.zeros((children, 7), dtype=np.int32)
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
                        tier_counts[base:base + children] += local_group
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
                        local_group = np.zeros((children, 7), dtype=np.int32)
                    np.add.at(local, (offset[first:end], tidx[first:end]),
                              weights[first:end])
                    for q in range(7):
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
                tier_counts[base:base + children] += local_group
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
            dst.create_array(spectra, "tier_counts", tier_counts)
            # 0=A,1=B,2=C,3=D,4=E,5=F,6=G; worst tier per pixel.
            quality = (6 - np.argmax(tier_counts[:, ::-1], axis=1)).astype(np.uint8)
            quality[counts == 0] = 255  # empty pixel: no tier
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
                "model": ("blackbody_bp_rp_v3" if no_g_supp is not None
                          else "blackbody_bp_rp"),
                "quality": 2, "quality_name": "tiered_spectral_model",
                "tier_names": ["A", "B", "C", "D", "E", "F", "G"],
                "tier_map": {
                    "A": "xp_sampled", "B": "xp_continuous",
                    "C": "G+BP-RP multi-band/template",
                    "D": "limited photometry / NIR / blackbody fallback",
                    "E": "RP-only or NIR-only",
                    "F": "class prior, zero flux",
                    "G": "no photometry/no class, zero flux",
                },
                "no_g_supp": str(no_g_supp) if no_g_supp is not None else None,
                "nir_supp": str(nir_supp) if nir_supp is not None else None,
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
        model=("blackbody_bp_rp_v3" if no_g_supp is not None else "blackbody_bp_rp"),
        missing_bprp=missing_bprp, missing_g=missing_g)
