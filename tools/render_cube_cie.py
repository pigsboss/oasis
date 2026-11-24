#!/usr/bin/env python3
"""Render a HEALPix spectral cube to CIE 1931 XYZ/sRGB sky maps.

Outputs:
  * 16-bit RGB TIFF, equirectangular, linear-light (exposure-normalized)
  * 8-bit sRGB PNG/JPEG after Reinhard luminance tone mapping

The CIE 1931 2-degree colour matching functions use the analytic Wyman et al.
(2013) approximation, adequate for visual sky maps.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import tables
from PIL import Image
import tifffile

from oasis_datasets import hpx
from oasis_datasets.spectra import WAVELENGTH


def cie_xyz_cmf(wavelength_nm: np.ndarray) -> np.ndarray:
    """Approximate CIE 1931 2-degree xbar/ybar/zbar at given wavelengths."""
    w = np.asarray(wavelength_nm, dtype=np.float64)
    def gauss(w, mu, s1, s2):
        s = np.where(w < mu, s1, s2)
        t = (w - mu) * s
        return np.exp(-0.5 * t * t)
    x = (0.362 * gauss(w, 442.0, 0.0624, 0.0374)
         + 1.056 * gauss(w, 599.8, 0.0264, 0.0323)
         - 0.065 * gauss(w, 501.1, 0.0490, 0.0382))
    y = (0.821 * gauss(w, 568.8, 0.0213, 0.0247)
         + 0.286 * gauss(w, 530.9, 0.0613, 0.0322))
    z = (1.217 * gauss(w, 437.0, 0.0845, 0.0278)
         + 0.681 * gauss(w, 459.0, 0.0385, 0.0725))
    return np.stack([x, y, z], axis=1).astype(np.float32)


CMF = cie_xyz_cmf(WAVELENGTH)
WHITE_D65 = np.array([0.95047, 1.0, 1.08883], dtype=np.float32)
XYZ_TO_SRGB = np.array([
    [3.2406, -1.5372, -0.4986],
    [-0.9689, 1.8758, 0.0415],
    [0.0557, -0.2040, 1.0570],
], dtype=np.float32)


def srgb_encode(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, 12.92 * x,
                    1.055 * np.power(x, 1.0 / 2.4) - 0.055)


def build_map(cube: Path, width: int, height: int, chunk_rows: int = 32):
    with tables.open_file(cube, "r") as h:
        s = h.root.spectra
        # use the stored nside from metadata if possible
        try:
            nside = int(json.loads(h.root._v_attrs.consolidate)["nside"])
        except Exception:
            pass
        flux = s.flux[:]  # (npix,343) float32
    npix, nwave = flux.shape
    nside = int(round(np.sqrt(npix / 12.0)))
    print(f"cube {flux.shape} nside={nside}", flush=True)

    # equirectangular pixel centres
    lon = (np.arange(width, dtype=np.float64) + 0.5) * (360.0 / width)
    lat = 90.0 - (np.arange(height, dtype=np.float64) + 0.5) * (180.0 / height)
    lon_grid, lat_grid = np.meshgrid(lon, lat)
    theta = np.radians(90.0 - lat_grid)
    phi = np.radians(np.mod(lon_grid, 360.0))
    ipix = np.asarray(hpx.ang2pix_nest(nside, theta, phi), dtype=np.int64)
    print(f"map {width}x{height}, ipix unique={np.unique(ipix).size}", flush=True)

    # CIE XYZ per map pixel, chunked to bound temporary memory
    xyz = np.empty((height * width, 3), dtype=np.float32)
    flat_ipix = ipix.reshape(-1)
    for st in range(0, flat_ipix.size, chunk_rows * width):
        en = min(flat_ipix.size, st + chunk_rows * width)
        spec = flux[flat_ipix[st:en]]
        xyz[st:en] = spec @ CMF
        if (st // (chunk_rows * width)) % 16 == 0:
            print(f"  xyz {en}/{flat_ipix.size}", flush=True)
    del flux
    # normalize to D65 white and convert to linear sRGB
    xyz /= WHITE_D65
    rgb = xyz @ XYZ_TO_SRGB.T
    rgb = np.maximum(rgb, 0.0)
    Y = xyz[:, 1]
    lum = np.maximum(Y, 0.0)
    valid = lum > 0
    p = float(np.percentile(lum[valid], 99.9)) if np.any(valid) else 1.0
    scale = 1.0 / max(p, 1e-12)
    print(f"luminance p99.9={p:.6g} scale={scale:.6g}", flush=True)
    return rgb, Y, scale, nside, width, height


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--width", type=int, default=8192)
    ap.add_argument("--height", type=int, default=4096)
    ap.add_argument("--chunk-rows", type=int, default=32)
    ap.add_argument("--tone-exposure", type=float, default=8.0)
    ap.add_argument("--stem", default="gaia_dr3_v4_cie_equirect")
    args = ap.parse_args(argv)

    cube = Path(args.cube).expanduser()
    out = Path(args.out_dir).expanduser(); out.mkdir(parents=True, exist_ok=True)
    rgb, Y, scale, nside, width, height = build_map(
        cube, args.width, args.height, args.chunk_rows)

    # 16-bit linear TIFF
    linear = np.clip(rgb * scale, 0.0, 1.0)
    u16 = np.round(linear * 65535.0).astype(np.uint16).reshape(height, width, 3)
    tif_path = out / f"{args.stem}_{width}x{height}_16bit.tiff"
    tifffile.imwrite(
        tif_path, u16, photometric="rgb", compression="zlib",
        metadata={"description": (
            "Gaia DR3 v4 343-point spectral cube; CIE 1931 2deg; "
            f"linear-light exposure scale={scale:.9g}; "
            f"HEALPix nside={nside}; equirectangular")},
    )
    print("wrote", tif_path, flush=True)

    # Reinhard on luminance, preserving chromaticity
    tone_scale = scale * float(args.tone_exposure)
    L = Y * tone_scale
    Ld = L / (1.0 + L)
    ratio = np.divide(Ld, L, out=np.zeros_like(Ld), where=L > 0)
    tm = rgb * tone_scale * ratio[:, None]
    srgb = srgb_encode(tm).reshape(height, width, 3)
    u8 = np.round(srgb * 255.0).astype(np.uint8)
    png_path = out / f"{args.stem}_{width}x{height}_reinhard.png"
    jpg_path = out / f"{args.stem}_{width}x{height}_reinhard.jpg"
    img = Image.fromarray(u8, "RGB")
    img.save(png_path)
    img.save(jpg_path, quality=95, subsampling=0)
    meta = {
        "cube": str(cube), "nside": nside, "width": width, "height": height,
        "projection": "equirectangular", "cie": "CIE 1931 2-degree analytic",
        "white": "D65", "scale": scale, "p99_9_luminance": float(1.0/scale),
        "tone_exposure": float(args.tone_exposure),
        "tiff": str(tif_path), "png": str(png_path), "jpeg": str(jpg_path),
    }
    (out / f"{args.stem}_{width}x{height}.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8")
    print("wrote", png_path, jpg_path, flush=True)


if __name__ == "__main__":
    main()
