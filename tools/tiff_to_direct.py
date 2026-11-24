#!/usr/bin/env python3
"""Make direct-view PNG/JPEG from the 16-bit linear CIE TIFF.

No Reinhard: linear TIFF values -> gamma encoding -> optional FWHM Gaussian.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image
from scipy.ndimage import gaussian_filter


def encode(x: np.ndarray, gamma: float) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    if gamma == 0:
        return x
    return np.power(x, 1.0 / gamma)


def mollweide_grid(width: int, height: int):
    root2 = np.sqrt(2.0)
    x = (2.0 * (np.arange(width) + 0.5) / width - 1.0) * 2.0 * root2
    y = (1.0 - 2.0 * (np.arange(height) + 0.5) / height) * root2
    xx, yy = np.meshgrid(x, y)
    s = np.clip(yy / root2, -1, 1)
    theta = np.arcsin(s)
    cos_t = np.sqrt(np.maximum(0.0, 1.0 - s * s))
    lon = np.zeros_like(xx)
    good = cos_t > 1e-9
    lon[good] = xx[good] * np.pi / (2.0 * root2 * cos_t[good])
    lat = np.arcsin(np.clip((2.0 * theta + np.sin(2.0 * theta)) / np.pi, -1, 1))
    inside = good & (np.abs(lon) <= np.pi)
    return np.degrees(lon), np.degrees(lat), inside


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiff", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--stem", required=True)
    ap.add_argument("--projection", choices=["equirect", "mollweide"], default="equirect")
    ap.add_argument("--width", type=int, default=0)
    ap.add_argument("--height", type=int, default=0)
    ap.add_argument("--gamma", type=float, default=2.2)
    ap.add_argument("--exposure", type=float, default=1.0)
    ap.add_argument("--fwhm", type=float, default=1.0)
    args = ap.parse_args(argv)

    lin = tifffile.imread(args.tiff).astype(np.float32) / 65535.0
    if lin.ndim != 3 or lin.shape[2] != 3:
        raise SystemExit("expected RGB TIFF")
    h, w = lin.shape[:2]
    inside = None
    if args.projection == "mollweide":
        out_w = args.width or 4096
        out_h = args.height or 2048
        lon, lat, inside = mollweide_grid(out_w, out_h)
        u = np.mod((lon / 360.0 * w).astype(np.int64), w)
        v = np.clip(((90.0 - lat) / 180.0 * h).astype(np.int64), 0, h - 1)
        img = lin[v, u]
        img[~inside] = 0.0
    else:
        img = lin
        out_h, out_w = h, w
    img = encode(img * args.exposure, args.gamma)
    if args.fwhm > 0:
        sigma = args.fwhm / 2.354820045
        img = gaussian_filter(img, sigma=(sigma, sigma, 0.0), mode="nearest")
    u8 = np.round(np.clip(img, 0, 1) * 255.0).astype(np.uint8)
    out = Path(args.out_dir).expanduser(); out.mkdir(parents=True, exist_ok=True)
    tag = f"gamma{args.gamma:g}_exposure{args.exposure:g}_blur{args.fwhm:g}"
    png = out / f"{args.stem}_{out_w}x{out_h}_{tag}.png"
    jpg = out / f"{args.stem}_{out_w}x{out_h}_{tag}.jpg"
    im = Image.fromarray(u8, "RGB")
    im.save(png); im.save(jpg, quality=95, subsampling=0)
    meta = {"tiff": str(args.tiff), "projection": args.projection,
            "width": out_w, "height": out_h, "gamma": args.gamma,
            "exposure": args.exposure, "fwhm_pixels": args.fwhm,
            "tone_mapping": "none (gamma direct, linear exposure only)",
            "png": str(png), "jpeg": str(jpg)}
    (out / f"{args.stem}_{out_w}x{out_h}_{tag}.json").write_text(
        json.dumps(meta, indent=2))
    print("wrote", png, jpg)


if __name__ == "__main__":
    main()
