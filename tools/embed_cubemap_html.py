#!/usr/bin/env python3
"""Embed six cubemap JPEGs as data URIs in the standalone viewer."""
from __future__ import annotations

import argparse
import base64
import re
from pathlib import Path

FACES = ["px", "nx", "py", "ny", "pz", "nz"]
TARGETS = ["TEXTURE_CUBE_MAP_POSITIVE_X", "TEXTURE_CUBE_MAP_NEGATIVE_X",
           "TEXTURE_CUBE_MAP_POSITIVE_Y", "TEXTURE_CUBE_MAP_NEGATIVE_Y",
           "TEXTURE_CUBE_MAP_POSITIVE_Z", "TEXTURE_CUBE_MAP_NEGATIVE_Z"]


def data_uri(path: Path) -> str:
    raw = path.read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(raw).decode("ascii")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--faces", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    template = Path(args.template).read_text(encoding="utf-8")
    face_dir = Path(args.faces)
    lines = []
    for name, target in zip(FACES, TARGETS):
        lines.append(f'    ["{data_uri(face_dir / (name + ".jpg"))}", gl.{target}],')
    block = "  const faces = [\n" + "\n".join(lines) + "\n  ];"
    template, n = re.subn(r"  const faces = \[.*?\n  \];", block, template,
                          count=1, flags=re.S)
    if n != 1:
        raise SystemExit("could not find faces array in template")
    template = template.replace("OASIS spectral cube v4 · CIE 1931",
                                "EMAIL EDITION · six faces embedded · CIE 1931")
    template = template.replace('请用本地 HTTP 服务打开此目录。',
                                '请用现代浏览器打开此单文件 HTML。')
    out = Path(args.out)
    out.write_text(template, encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
