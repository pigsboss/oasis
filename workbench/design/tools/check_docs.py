#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify.sh 子检查：E2 仓库内路径引用 + E3 术语/字段一致性断言（只读）。"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]

MD_GLOBS = ["docs/**/*.md", "README.md"]
TOKEN = re.compile(r"(?:docs|workbench)/[A-Za-z0-9_./\-\u4e00-\u9fff]*[A-Za-z0-9_/\-\u4e00-\u9fff]")
SKIP_FRAG = ("{", "}", "*", "--", "…")
STRIP = "`'\".,;:)、，。；：》」”’"

ABSENT = [
    ("E3-01 target_name 无残留", ["docs/**/*.md"], r"target_name"),
    ("E3-02 无 true/false 字面量", ["docs/design/targets_interfaces.md"], r"true/false"),
    ("E3-03 无 'ADR 001' 悬空引用", ["docs/design/adr/*.md"], r"ADR 001"),
    ("E3-04 无 MCPC 残留", ["docs/**/*.md"], r"MCPC"),
    ("E3-05 无 UVCOORD 残留", ["docs/**/*.md"], r"UVCOORD"),
    ("E3-06 无 docs/guides/targets 旧路径", ["docs/**/*.md"], r"docs/guides/targets"),
    ("E3-07 无 '观测层' 术语残留", ["docs/**/*.md"], r"观测层"),
]

PRESENT = [
    ("E3-08 provider/version 可选口径（data_model）", "docs/design/targets_data_model.md", "| `provider` | `str` | 否"),
    ("E3-09 source 必选约束（interfaces）", "docs/design/targets_interfaces.md", "`source`：必选"),
    ("E3-10 §3.2.7 FITS 口径（targets）", "docs/design/targets.md", "FITS 主数据 + JSON/YAML 辅助文件"),
    ("E3-11 反演输入版本键（interfaces）", "docs/design/targets_interfaces.md", "`OASIS_OBS_INTF_VER` ：接口规范版本"),
]


def md_files():
    out = []
    for g in MD_GLOBS:
        out.extend(sorted(ROOT.glob(g)))
    return out


def link_check() -> int:
    bad = []
    for f in md_files():
        text = f.read_text(encoding="utf-8")
        for m in TOKEN.finditer(text):
            tok = m.group(0).rstrip(STRIP)
            if any(s in tok for s in SKIP_FRAG):
                continue
            if not (ROOT / tok).exists():
                line = text[: m.start()].count("\n") + 1
                bad.append(f"{f.relative_to(ROOT)}:{line}: {tok}")
    if bad:
        print("E2 失败：失效路径引用")
        for b in bad[:20]:
            print("   ", b)
        return 1
    print("E2 PASS：仓库内路径引用全部可解析")
    return 0


def grep(globs, pattern):
    hits = []
    rx = re.compile(pattern)
    for g in globs:
        for f in ROOT.glob(g):
            for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if rx.search(line):
                    hits.append(f"{f.relative_to(ROOT)}:{i}: {line.strip()[:90]}")
    return hits


def assert_checks() -> int:
    rc = 0
    for desc, globs, pat in ABSENT:
        hits = grep(globs, pat)
        if hits:
            rc = 1
            print(f"FAIL {desc}")
            for h in hits[:5]:
                print("   ", h)
        else:
            print(f"PASS {desc}")
    for desc, file, needle in PRESENT:
        p = ROOT / file
        if p.exists() and needle in p.read_text(encoding="utf-8"):
            print(f"PASS {desc}")
        else:
            rc = 1
            print(f"FAIL {desc}")
    return rc


def main() -> int:
    rc = link_check()
    rc |= assert_checks()
    return rc


if __name__ == "__main__":
    sys.exit(main())
