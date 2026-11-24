#!/usr/bin/env python3
"""Build a sparse per-pixel XP supplement from Gaia XP sampled spectra.

Two phases:
  1. parallel per-file parsing -> parts/*.npz (small, file-local pixel sums)
  2. merge parts -> sparse /pixels arrays + /source_id

XP flux is absolute W m^-2 nm^-1.  Each source spectrum is divided by its
600 nm flux and scaled by 10^-0.4 (G_est - 6.5), where G_est is calibrated
from a few hundred XP source IDs against the core table's Gaia G.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import multiprocessing as mp
import os
import time
from pathlib import Path

import numpy as np
import tables

from oasis_datasets import hpx
from oasis_datasets.spectra import WAVELENGTH

N_WAVE = 343
I600 = 132


def _iter_file(path: Path):
    with gzip.open(path, "rt", errors="replace", newline="") as f:
        for line in f:
            if line.startswith("#"):
                continue
            if line.lstrip().lower().startswith("source_id"):
                break
        else:
            return
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 6:
                continue
            try:
                sid = int(row[0]); ra = float(row[2]); dec = float(row[3])
                flux = np.fromstring(row[4].strip().strip("[]"),
                                     sep=",", dtype=np.float32)
            except Exception:
                continue
            if flux.size == N_WAVE and np.isfinite(ra) and np.isfinite(dec):
                yield sid, ra, dec, flux


def _calibrate(core: Path, rows, sample: int = 200) -> float:
    vals = []
    with tables.open_file(core, "r") as h:
        t = h.root.table
        for sid, ra, dec, flux in rows:
            ref = float(np.nanmedian(flux[I600 - 4:I600 + 5]))
            if not np.isfinite(ref) or ref <= 0:
                continue
            got = t.read_where(f"source_id == {sid}")
            if len(got) == 0:
                continue
            vals.append(float(got["phot_g_mean_mag"][0]) + 2.5 * np.log10(ref))
            if len(vals) >= sample:
                break
    if not vals:
        raise RuntimeError("cannot calibrate XP zero point from core table")
    return float(np.median(vals))


def _part(args) -> tuple[str, int, int]:
    path_str, part_dir, zp, nside = args
    path = Path(path_str)
    part = Path(part_dir) / (path.stem + ".npz")
    if part.exists():
        try:
            z = np.load(part)
            return str(part), int(z["pix"].size), 0
        except Exception:
            pass
    pixs = []; fluxes = []; ids = []; bad = 0
    npix = hpx.nside2npix(nside)
    for sid, ra, dec, flux in _iter_file(path):
        ref = float(np.nanmedian(flux[I600 - 4:I600 + 5]))
        if not np.isfinite(ref) or ref <= 0:
            bad += 1; continue
        theta = np.radians(90.0 - dec)
        phi = np.radians(np.mod(ra, 360.0))
        pix = int(hpx.ang2pix_nest(nside, theta, phi))
        if pix < 0 or pix >= npix:
            bad += 1; continue
        shape = flux / ref
        shape = np.where(np.isfinite(shape), np.maximum(shape, 0.0), 0.0)
        g_est = -2.5 * np.log10(ref) + zp
        weight = float(10.0 ** (-0.4 * (g_est - 6.5)))
        pixs.append(pix); fluxes.append(shape.astype(np.float32) * weight); ids.append(sid)
    if pixs:
        np.savez(part, pix=np.asarray(pixs, dtype=np.int32),
                 flux=np.stack(fluxes).astype(np.float32),
                 ids=np.asarray(ids, dtype=np.int64))
    else:
        np.savez(part, pix=np.empty(0, np.int32), flux=np.empty((0, N_WAVE), np.float32),
                 ids=np.empty(0, np.int64))
    return str(part), len(pixs), bad


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--xp-dir", required=True)
    ap.add_argument("--core", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--nside", type=int, default=2048)
    ap.add_argument("--jobs", type=int, default=16)
    ap.add_argument("--parts", default=None)
    ap.add_argument("--limit-files", type=int, default=0)
    args = ap.parse_args(argv)

    xp_dir = Path(args.xp_dir).expanduser()
    files = sorted(xp_dir.glob("XpSampledMeanSpectrum_*.csv.gz"))
    if args.limit_files:
        files = files[:args.limit_files]
    if not files:
        raise SystemExit("no XP files")
    parts = Path(args.parts).expanduser() if args.parts else Path(args.out).with_suffix(".parts")
    parts.mkdir(parents=True, exist_ok=True)

    zp = _calibrate(Path(args.core).expanduser(), _iter_file(files[0]))
    print(f"calibrated ZP={zp:.6f}", flush=True)
    t0 = time.time()
    ok = bad = 0
    with mp.Pool(args.jobs) as pool:
        for i, (part, n, b) in enumerate(pool.imap_unordered(
                _part, [(str(p), str(parts), zp, args.nside) for p in files])):
            ok += n; bad += b
            if i % 100 == 0 or i + 1 == len(files):
                print(f"{i+1}/{len(files)} rows={ok} bad={bad} {time.time()-t0:.0f}s", flush=True)

    # merge
    print("merging parts", flush=True)
    pix_parts = []; flux_parts = []; id_parts = []
    for i, part in enumerate(sorted(parts.glob("*.npz"))):
        z = np.load(part)
        if z["pix"].size:
            pix_parts.append(z["pix"]); flux_parts.append(z["flux"]); id_parts.append(z["ids"])
    pix = np.concatenate(pix_parts)
    flux = np.concatenate(flux_parts)
    ids = np.concatenate(id_parts)
    order = np.argsort(pix, kind="stable")
    pix = pix[order]; flux = flux[order]
    uniq, start = np.unique(pix, return_index=True)
    counts = np.diff(np.append(start, pix.size)).astype(np.int32)
    summed = np.add.reduceat(flux, start, axis=0).astype(np.float32)
    ids = np.unique(ids)

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    with tables.open_file(out, "w") as h:
        grp = h.create_group("/", "pixels")
        h.create_array(grp, "pix", uniq.astype(np.int32))
        h.create_array(grp, "count", counts)
        h.create_earray(grp, "xp_flux", atom=tables.Float32Atom(),
                        shape=(0, N_WAVE), chunkshape=(4096, N_WAVE), filters=None)
        for st in range(0, uniq.size, 4096):
            grp.xp_flux.append(summed[st:st + 4096])
        h.create_array(h.root, "source_id", ids)
        h.root._v_attrs.meta = json.dumps({
            "nside": args.nside, "npix": int(hpx.nside2npix(args.nside)),
            "n_flux_pixels": int(uniq.size), "n_xp_sources": int(ids.size),
            "n_rows": int(ok), "bad_rows": int(bad), "zp": zp, "i600": I600,
            "files": len(files), "jobs": args.jobs,
            "units": "relative flux, G=6.5 reference, 600 nm normalized",
        }, ensure_ascii=False)
    print(f"wrote {out}: {uniq.size} pixels, {ids.size} sources, {ok} rows", flush=True)


if __name__ == "__main__":
    main()
