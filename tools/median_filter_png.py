#!/usr/bin/env python3
"""Apply a median filter to an 8-bit RGB PNG/JPEG."""
from __future__ import annotations

import argparse, json, os
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import median_filter


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--size", type=int, default=3)
    ap.add_argument("--stem", default=None)
    args = ap.parse_args(argv)
    src = Path(args.png).expanduser()
    a = np.asarray(Image.open(src).convert("RGB"))
    out = np.empty_like(a)
    for c in range(3):
        out[..., c] = median_filter(a[..., c], size=args.size, mode="nearest")
    dst_dir = Path(args.out_dir).expanduser(); dst_dir.mkdir(parents=True, exist_ok=True)
    stem = args.stem or src.stem
    png = dst_dir / f"{stem}_median{args.size}.png"
    jpg = dst_dir / f"{stem}_median{args.size}.jpg"
    im = Image.fromarray(out, "RGB")
    im.save(png)
    im.save(jpg, quality=95, subsampling=0)
    meta = {"input": str(src), "size": args.size, "png": str(png), "jpeg": str(jpg)}
    (dst_dir / f"{stem}_median{args.size}.json").write_text(json.dumps(meta, indent=2))
    print("wrote", png, jpg)


if __name__ == "__main__":
    main()
