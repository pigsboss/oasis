#!/usr/bin/env python3
"""Convolve an sRGB PNG with a physically parameterized optical PSF.

Default model: diffraction-limited circular aperture (Airy), 50 mm f/1.8,
550 nm, with the pixel scale taken from an equirectangular map metadata or
explicitly supplied.  The convolution is done in linear-light RGB.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import convolve
from scipy.special import j1


def srgb_to_linear(x):
    x = x.astype(np.float32) / 255.0
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(x):
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, 12.92 * x,
                    1.055 * np.power(x, 1.0 / 2.4) - 0.055)


def airy_kernel(pixel_arcsec: float, focal_mm: float, f_number: float,
                wavelength_nm: float, size: int, ss: int = 8):
    lam = wavelength_nm * 1e-9
    D = (focal_mm * 1e-3) / f_number
    pix_rad = pixel_arcsec * math.pi / (180.0 * 3600.0)
    # integrate each output pixel over ss x ss subpixels
    subs = (np.arange(size * ss, dtype=np.float64) + 0.5) / ss - size / 2.0
    yy, xx = np.meshgrid(subs, subs, indexing="ij")
    theta = np.hypot(xx, yy) * pix_rad
    x = np.pi * D * np.sin(theta) / lam
    with np.errstate(divide="ignore", invalid="ignore"):
        amp = np.where(x > 1e-12, (2.0 * j1(x) / x) ** 2, 1.0)
    amp = amp.reshape(size, ss, size, ss).sum(axis=(1, 3))
    amp /= amp.sum()
    return amp.astype(np.float32)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--focal-mm", type=float, default=50.0)
    ap.add_argument("--f-number", type=float, default=1.8)
    ap.add_argument("--wavelength-nm", type=float, default=550.0)
    ap.add_argument("--pixel-arcsec", type=float, default=None,
                    help="default: 360*3600/width for equirectangular input")
    ap.add_argument("--kernel-size", type=int, default=7)
    args = ap.parse_args(argv)

    src = Path(args.png).expanduser()
    im = Image.open(src).convert("RGB")
    a = np.asarray(im)
    h, w = a.shape[:2]
    pixel_arcsec = args.pixel_arcsec
    if pixel_arcsec is None:
        pixel_arcsec = 360.0 * 3600.0 / w
    psf = airy_kernel(pixel_arcsec, args.focal_mm, args.f_number,
                      args.wavelength_nm, args.kernel_size)
    fwhm_arcsec = 1.03 * args.wavelength_nm * 1e-9 * args.f_number / (args.focal_mm * 1e-3) * 206264.806
    fwhm_px = fwhm_arcsec / pixel_arcsec
    print(f"pixel_scale={pixel_arcsec:.6g} arcsec/px  PSF_FWHM={fwhm_arcsec:.4g} arcsec = {fwhm_px:.6g} px")
    lin = srgb_to_linear(a)
    out = np.empty_like(lin)
    for c in range(3):
        out[..., c] = convolve(lin[..., c], psf, mode="nearest")
    rgb = np.round(linear_to_srgb(out) * 255.0).astype(np.uint8)
    dst = Path(args.out).expanduser(); dst.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgb, "RGB").save(dst)
    meta = {
        "input": str(src), "output": str(dst), "model": "Airy circular aperture",
        "focal_mm": args.focal_mm, "f_number": args.f_number,
        "wavelength_nm": args.wavelength_nm, "pixel_arcsec": pixel_arcsec,
        "psf_fwhm_arcsec": fwhm_arcsec, "psf_fwhm_px": fwhm_px,
        "kernel_size": args.kernel_size, "note": "linear-light convolution",
    }
    Path(str(dst) + ".json").write_text(json.dumps(meta, indent=2))
    print("wrote", dst)


if __name__ == "__main__":
    main()
