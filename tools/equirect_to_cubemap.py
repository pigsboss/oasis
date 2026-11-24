#!/usr/bin/env python3
"""Convert an equirectangular sky map to six WebGL cube-map faces.

World convention: x=cos(dec)cos(ra), y=sin(dec), z=cos(dec)sin(ra).
Faces use the standard OpenGL/WebGL cube-map direction mapping and are
written with the image top at t=1 (the viewer sets UNPACK_FLIP_Y_WEBGL).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def face_dirs(n: int, face: str):
    # s,t in [-1,1], t=+1 at the top row
    t = (1.0 - 2.0 * (np.arange(n, dtype=np.float32) + 0.5) / n)[:, None]
    s = (-1.0 + 2.0 * (np.arange(n, dtype=np.float32) + 0.5) / n)[None, :]
    s = np.broadcast_to(s, (n, n)); t = np.broadcast_to(t, (n, n))
    if face == "+x":
        x, y, z = np.ones_like(s), -t, -s
    elif face == "-x":
        x, y, z = -np.ones_like(s), -t, s
    elif face == "+y":
        x, y, z = s, np.ones_like(s), t
    elif face == "-y":
        x, y, z = s, -np.ones_like(s), -t
    elif face == "+z":
        x, y, z = s, -t, np.ones_like(s)
    elif face == "-z":
        x, y, z = -s, -t, -np.ones_like(s)
    else:
        raise ValueError(face)
    # normalize
    inv = 1.0 / np.sqrt(x * x + y * y + z * z)
    return x * inv, y * inv, z * inv


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--equirect", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--size", type=int, default=2048)
    ap.add_argument("--quality", type=int, default=92)
    args = ap.parse_args(argv)
    src = Image.open(args.equirect).convert("RGB")
    a = np.asarray(src)
    h, w = a.shape[:2]
    print(f"equirect {w}x{h} -> cube {args.size}")
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    for face in ("+x", "-x", "+y", "-y", "+z", "-z"):
        x, y, z = face_dirs(args.size, face)
        lon = np.degrees(np.arctan2(z, x)) % 360.0
        lat = np.degrees(np.arcsin(np.clip(y, -1.0, 1.0)))
        u = np.clip((lon / 360.0 * w).astype(np.int64), 0, w - 1)
        v = np.clip(((90.0 - lat) / 180.0 * h).astype(np.int64), 0, h - 1)
        rgb = a[v, u]
        # Naming: px, nx, py, ny, pz, nz
        name = {"+x": "px", "-x": "nx", "+y": "py", "-y": "ny",
                "+z": "pz", "-z": "nz"}[face] + ".jpg"
        Image.fromarray(rgb).save(out / name, quality=args.quality,
                                  subsampling=0, optimize=True)
        print("wrote", out / name)
    print("done", out)


if __name__ == "__main__":
    main()
