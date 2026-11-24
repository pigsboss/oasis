#!/usr/bin/env python3
"""Mollweide all-sky true-colour sample from the v4 spectral cube.

CIE 1931 -> linear sRGB (D65), then Reinhard luminance tone mapping.
"""
from __future__ import annotations

import argparse, json
from pathlib import Path

import numpy as np
import tables
from PIL import Image
from scipy.ndimage import gaussian_filter

from oasis_datasets import hpx
from render_cube_cie import CMF, WHITE_D65, XYZ_TO_SRGB, srgb_encode, gray_world_balance


def mollweide_grid(width: int, height: int):
    """Return lon/lat degrees and inside-mask for a Mollweide image."""
    root2 = np.sqrt(2.0)
    x = (2.0 * (np.arange(width, dtype=np.float64) + 0.5) / width - 1.0) * 2.0 * root2
    y = (1.0 - 2.0 * (np.arange(height, dtype=np.float64) + 0.5) / height) * root2
    xx, yy = np.meshgrid(x, y)
    s = np.clip(yy / root2, -1.0, 1.0)
    theta = np.arcsin(s)
    cos_t = np.sqrt(np.maximum(0.0, 1.0 - s * s))
    lon = np.zeros_like(xx)
    good = cos_t > 1e-9
    lon[good] = xx[good] * np.pi / (2.0 * root2 * cos_t[good])
    lat = np.arcsin(np.clip((2.0 * theta + np.sin(2.0 * theta)) / np.pi, -1.0, 1.0))
    inside = good & (np.abs(lon) <= np.pi)
    return np.degrees(lon), np.degrees(lat), inside


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--width", type=int, default=4096)
    ap.add_argument("--height", type=int, default=2048)
    ap.add_argument("--tone-exposure", type=float, default=8.0)
    ap.add_argument("--fwhm", type=float, default=1.0)
    ap.add_argument("--white-balance", choices=["gray", "none"], default="gray")
    ap.add_argument("--stem", default="gaia_dr3_v4_cie_mollweide")
    args = ap.parse_args(argv)

    cube = Path(args.cube).expanduser()
    out = Path(args.out_dir).expanduser(); out.mkdir(parents=True, exist_ok=True)
    with tables.open_file(cube, "r") as h:
        flux = h.root.spectra.flux[:]
        nside = int(json.loads(h.root._v_attrs.consolidate)["nside"])
    lon, lat, inside = mollweide_grid(args.width, args.height)
    print(f"cube {flux.shape} nside={nside}; mollweide inside={inside.sum()}", flush=True)
    ipix = np.zeros(lon.shape, dtype=np.int64)
    th = np.radians(90.0 - lat[inside])
    ph = np.radians(np.mod(lon[inside], 360.0))
    ipix[inside] = np.asarray(hpx.ang2pix_nest(nside, th, ph), dtype=np.int64)

    xyz = np.zeros((args.height * args.width, 3), dtype=np.float32)
    flat = ipix.reshape(-1); mask = inside.reshape(-1)
    idx = np.flatnonzero(mask)
    for st in range(0, idx.size, 32 * args.width):
        en = min(idx.size, st + 32 * args.width)
        p = idx[st:en]
        xyz[p] = flux[flat[p]] @ CMF
        if (st // (32 * args.width)) % 16 == 0:
            print(f"  xyz {en}/{idx.size}", flush=True)
    del flux
    # absolute XYZ -> sRGB(D65); no second D65 division
    rgb = np.maximum(xyz @ XYZ_TO_SRGB.T, 0.0)
    Y = xyz[:, 1]
    gains = np.ones(3, dtype=np.float32)
    if args.white_balance == "gray":
        rgb, gains, _ref = gray_world_balance(rgb, Y, 50.0)
    Y = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    lum = Y[mask]
    p = float(np.percentile(lum[lum > 0], 99.9)) if np.any(lum > 0) else 1.0
    scale = 1.0 / max(p, 1e-12)
    print(f"p99.9={p:.6g} scale={scale:.6g}", flush=True)

    tone_scale = scale * args.tone_exposure
    L = Y * tone_scale
    Ld = L / (1.0 + L)
    ratio = np.divide(Ld, L, out=np.zeros_like(Ld), where=L > 0)
    tm = rgb * tone_scale * ratio[:, None]
    srgb = srgb_encode(tm).reshape(args.height, args.width, 3)
    if args.fwhm > 0:
        sigma = args.fwhm / 2.354820045
        srgb = gaussian_filter(srgb, sigma=(sigma, sigma, 0.0), mode="nearest")
    srgb[~inside] = 0.0
    u8 = np.round(srgb * 255.0).astype(np.uint8)
    png = out / f"{args.stem}_{args.width}x{args.height}_reinhard.png"
    jpg = out / f"{args.stem}_{args.width}x{args.height}_reinhard.jpg"
    img = Image.fromarray(u8, "RGB")
    img.save(png); img.save(jpg, quality=95, subsampling=0)
    meta = {"cube": str(cube), "projection": "mollweide", "nside": nside,
            "width": args.width, "height": args.height, "cie": "CIE 1931 2-degree analytic",
            "white": "D65", "scale": scale, "p99_9_luminance": p,
            "tone_exposure": args.tone_exposure, "fwhm_pixels": args.fwhm,
            "white_balance": args.white_balance,
            "white_balance_gains": gains.tolist(),
            "png": str(png), "jpeg": str(jpg)}
    (out / f"{args.stem}_{args.width}x{args.height}.json").write_text(json.dumps(meta, indent=2))
    print("wrote", png, jpg, flush=True)


if __name__ == "__main__":
    main()
