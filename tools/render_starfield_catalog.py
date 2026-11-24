#!/usr/bin/env python3
"""Render magnitude-limited Gaia star layers from the full core table.

Stars are binned on a supersampled equirectangular grid, convolved with a
Gaussian display PSF, downsampled, then encoded with gamma 2.2.  No Reinhard.
"""
from __future__ import annotations

import argparse, json, time
from pathlib import Path

import numpy as np
import tables
from PIL import Image
from scipy.ndimage import gaussian_filter

from oasis_datasets.spectra import TEMPLATES, template_indices
from render_cube_cie import CMF, XYZ_TO_SRGB


def star_rgb_table():
    gains = np.array([0.80819, 1.02472, 1.27098], dtype=np.float32)
    xyz = TEMPLATES @ CMF
    rgb = np.maximum(xyz @ XYZ_TO_SRGB.T, 0.0) * gains
    y = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    return (rgb / np.maximum(y[:, None], 1e-9)).astype(np.float32)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--core", default="/mnt/data/huo/Datasets/Gaia/gdr3/consolidated/gaia_dr3_core_spatial.h5")
    ap.add_argument("--max-g", type=float, required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--width", type=int, default=8192)
    ap.add_argument("--height", type=int, default=4096)
    ap.add_argument("--supersample", type=int, default=2)
    ap.add_argument("--fwhm", type=float, default=3.0)
    ap.add_argument("--gamma", type=float, default=2.2)
    ap.add_argument("--exposure-percentile", type=float, default=99.9)
    ap.add_argument("--tone-mode", choices=["gamma", "reinhard"], default="gamma")
    ap.add_argument("--chunk", type=int, default=10_000_000)
    ap.add_argument("--stem", required=True)
    args = ap.parse_args(argv)
    ss = max(1, args.supersample)
    W, H = args.width * ss, args.height * ss
    colors = star_rgb_table()
    acc = np.zeros((H, W, 3), dtype=np.float32)
    n = 0
    t0 = time.time()
    with tables.open_file(args.core, "r") as h:
        t = h.root.table
        total = int(t.nrows)
        for start in range(0, total, args.chunk):
            stop = min(total, start + args.chunk)
            ra = np.asarray(t.read(start, stop, field="ra"), dtype=np.float64)
            dec = np.asarray(t.read(start, stop, field="dec"), dtype=np.float64)
            g = np.asarray(t.read(start, stop, field="phot_g_mean_mag"), dtype=np.float64)
            bprp = np.asarray(t.read(start, stop, field="bp_rp"), dtype=np.float64)
            m = np.isfinite(ra) & np.isfinite(dec) & np.isfinite(g) & (g <= args.max_g)
            if not np.any(m):
                continue
            ra = ra[m]; dec = dec[m]; g = g[m]; bprp = bprp[m]
            x = np.floor(ra / 360.0 * W).astype(np.int64)
            y = np.floor((90.0 - dec) / 180.0 * H).astype(np.int64)
            ok = (x >= 0) & (x < W) & (y >= 0) & (y < H)
            ra = ra[ok]; dec = dec[ok]; g = g[ok]; bprp = bprp[ok]
            x = x[ok]; y = y[ok]
            idx = y * W + x
            flux = np.power(10.0, -0.4 * (g - 6.5)).astype(np.float32)
            tidx, _ = template_indices(bprp)
            col = colors[tidx]
            for c in range(3):
                acc[..., c] += np.bincount(idx, weights=flux * col[:, c],
                                           minlength=W * H).reshape(H, W).astype(np.float32)
            n += ra.size
            if start % (args.chunk * 10) == 0:
                print(f"{stop}/{total} kept={n} {time.time()-t0:.0f}s", flush=True)
    print(f"stars kept={n}; blur", flush=True)
    sigma = (args.fwhm * ss) / 2.354820045
    for c in range(3):
        acc[..., c] = gaussian_filter(acc[..., c], sigma=sigma, mode="wrap")
    if ss > 1:
        acc = acc.reshape(args.height, ss, args.width, ss, 3).mean(axis=(1, 3))
    lum = acc @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    pos = lum[lum > 0]
    p = float(np.percentile(pos, args.exposure_percentile)) if pos.size else 1.0
    scale = 1.0 / max(p, 1e-9)
    if args.tone_mode == "reinhard":
        L = lum * scale
        Ld = L / (1.0 + L)
        ratio = np.divide(Ld, L, out=np.zeros_like(Ld), where=L > 0)
        rgb = acc * scale * ratio[..., None]
        out = np.power(np.clip(rgb, 0.0, 1.0), 1.0 / args.gamma)
    else:
        out = np.power(np.clip(acc * scale, 0.0, 1.0), 1.0 / args.gamma)
    u8 = np.round(out * 255.0).astype(np.uint8)
    dst = Path(args.out_dir).expanduser(); dst.mkdir(parents=True, exist_ok=True)
    tag = f"psf{args.fwhm:g}_{args.tone_mode}"
    png = dst / f"{args.stem}_{args.width}x{args.height}_{tag}.png"
    jpg = dst / f"{args.stem}_{args.width}x{args.height}_{tag}.jpg"
    im = Image.fromarray(u8, "RGB")
    im.save(png); im.save(jpg, quality=95, subsampling=0)
    (dst / f"{args.stem}_{args.width}x{args.height}_{tag}.json").write_text(json.dumps({
        "core": args.core, "max_g": args.max_g, "n_stars": int(n),
        "width": args.width, "height": args.height, "supersample": ss,
        "fwhm_pixels": args.fwhm, "gamma": args.gamma,
        "psf": "Gaussian display PSF", "tone_mapping": args.tone_mode,
        "exposure_percentile": args.exposure_percentile, "scale": scale,
        "png": str(png), "jpeg": str(jpg),
    }, indent=2))
    print("wrote", png, jpg, flush=True)


if __name__ == "__main__":
    main()
