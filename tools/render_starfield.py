#!/usr/bin/env python3
"""Render a Gaia bright-star layer with an oversampled PSF.

The spectral cube is integrated at nside=2048 (~1.7 arcmin pixels); it cannot
contain individual stellar PSFs.  This tool renders T3 Gaia stars (G<=12)
as point sources with a display PSF, on a finer pixel grid.
"""
from __future__ import annotations

import argparse, json
from pathlib import Path

import numpy as np
import tables
from PIL import Image
from scipy.ndimage import gaussian_filter

from oasis_datasets.spectra import BP_RP_GRID, TEMPLATES, template_indices
from render_cube_cie import CMF, XYZ_TO_SRGB, srgb_encode


def star_rgb_table(gains):
    xyz = TEMPLATES @ CMF
    rgb = xyz @ XYZ_TO_SRGB.T
    rgb = np.maximum(rgb, 0.0) * gains
    # normalize each template to unit luminance
    y = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    rgb /= np.maximum(y[:, None], 1e-9)
    return rgb.astype(np.float32)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default="/mnt/data/huo/Datasets/catalogs/gaia/t3/gaia_t3.h5")
    ap.add_argument("--max-g", type=float, default=None)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--width", type=int, default=8192)
    ap.add_argument("--height", type=int, default=4096)
    ap.add_argument("--supersample", type=int, default=2)
    ap.add_argument("--fwhm", type=float, default=3.0)
    ap.add_argument("--gamma", type=float, default=2.2)
    ap.add_argument("--exposure-percentile", type=float, default=99.9)
    ap.add_argument("--stem", default="gaia_t3_starfield")
    args = ap.parse_args(argv)
    ss = max(1, args.supersample)
    W, H = args.width * ss, args.height * ss
    with tables.open_file(args.catalog, "r") as h:
        t = h.root.table
        ra = np.asarray(t.cols.ra[:], dtype=np.float64)
        dec = np.asarray(t.cols.dec[:], dtype=np.float64)
        g = np.asarray(t.cols.phot_g_mean_mag[:], dtype=np.float64)
        bprp = np.asarray(t.cols.bp_rp[:], dtype=np.float64)
    print(f"stars {ra.size}, render {W}x{H}, output {args.width}x{args.height}", flush=True)
    ok = np.isfinite(ra) & np.isfinite(dec) & np.isfinite(g)
    if args.max_g is not None:
        ok &= g <= args.max_g
    ra, dec, g, bprp = ra[ok], dec[ok], g[ok], bprp[ok]
    # display white balance matching the maps
    gains = np.array([0.80819, 1.02472, 1.27098], dtype=np.float32)
    colors = star_rgb_table(gains)
    tidx, _ = template_indices(bprp)
    col = colors[tidx]
    flux = np.power(10.0, -0.4 * (g - 6.5)).astype(np.float32)

    # bilinear subpixel splat
    x = (ra / 360.0 * W) - 0.5
    y = ((90.0 - dec) / 180.0 * H) - 0.5
    x0 = np.floor(x).astype(np.int64); y0 = np.floor(y).astype(np.int64)
    fx = (x - x0).astype(np.float32); fy = (y - y0).astype(np.float32)
    img = np.zeros((H, W, 3), dtype=np.float32)
    for dx, wy in ((0, 1-fy), (1, fy)):
        for dy, wx in ((0, 1-fx), (1, fx)):
            ix = x0 + dx; iy = y0 + dy
            m = (ix >= 0) & (ix < W) & (iy >= 0) & (iy < H)
            val = (flux[m] * wy[m] * wx[m])[:, None] * col[m]
            np.add.at(img, (iy[m], ix[m]), val)
    print("splat done; blur", flush=True)
    sigma = (args.fwhm * ss) / 2.354820045
    for c in range(3):
        img[..., c] = gaussian_filter(img[..., c], sigma=sigma, mode="wrap")
    if ss > 1:
        img = img.reshape(args.height, ss, args.width, ss, 3).mean(axis=(1, 3))
    print("blur/downsample done", flush=True)
    lum = img @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    pos = lum[lum > 0]
    p = float(np.percentile(pos, args.exposure_percentile)) if pos.size else 1.0
    scale = 1.0 / max(p, 1e-9)
    print(f"p{args.exposure_percentile}={p:.6g} scale={scale:.6g}", flush=True)
    out = np.power(np.clip(img * scale, 0.0, 1.0), 1.0 / args.gamma)
    u8 = np.round(out * 255.0).astype(np.uint8)
    dst = Path(args.out_dir).expanduser(); dst.mkdir(parents=True, exist_ok=True)
    png = dst / f"{args.stem}_{args.width}x{args.height}_psf{args.fwhm:g}.png"
    jpg = dst / f"{args.stem}_{args.width}x{args.height}_psf{args.fwhm:g}.jpg"
    im = Image.fromarray(u8, "RGB")
    im.save(png); im.save(jpg, quality=95, subsampling=0)
    meta = {"catalog": args.catalog, "n_stars": int(ra.size), "width": args.width,
            "height": args.height, "supersample": ss, "fwhm_pixels": args.fwhm,
            "gamma": args.gamma, "max_g": args.max_g, "psf": "Gaussian display PSF",
            "exposure_percentile": args.exposure_percentile, "scale": scale,
            "png": str(png), "jpeg": str(jpg)}
    (dst / f"{args.stem}_{args.width}x{args.height}_psf{args.fwhm:g}.json").write_text(json.dumps(meta, indent=2))
    print("wrote", png, jpg, flush=True)


if __name__ == "__main__":
    main()
