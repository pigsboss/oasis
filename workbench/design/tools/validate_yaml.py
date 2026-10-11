#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify.sh 子检查：E4 —— 文档 YAML 示例 + 用例样例的 JSON Schema 校验。"""
from __future__ import annotations

import json
import pathlib
import re
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "docs/design/schemas/target-model-submission.schema.json"

DOC_SOURCES = ["docs/design/targets.md", "docs/design/targets_interfaces.md"]
TEX_SOURCES = ["docs/overview-design/chapters/ch06_formats.tex"]
SAMPLE_GLOB = "workbench/science/use-cases/*.yaml"
BLOCK = re.compile(r"```yaml\n(.*?)```", re.S)
TEX_BLOCK = re.compile(r"\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}", re.S)


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    rc = 0
    n = 0

    def check(text: str, name: str) -> None:
        nonlocal rc, n
        n += 1
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as e:
            rc = 1
            print(f"FAIL {name}: YAML 解析失败: {str(e).splitlines()[0]}")
            return
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            rc = 1
            for e in errors[:4]:
                path = "/".join(map(str, e.path)) or "<root>"
                print(f"FAIL {name}: {path} -> {e.message[:140]}")
        else:
            print(f"PASS {name}")

    for src in DOC_SOURCES:
        text = (ROOT / src).read_text(encoding="utf-8")
        blocks = BLOCK.findall(text)
        if not blocks:
            rc = 1
            print(f"FAIL {src}: 未找到 yaml 代码块")
        for i, b in enumerate(blocks, 1):
            check(b, f"{src} 代码块{i}")

    for src in TEX_SOURCES:
        text = (ROOT / src).read_text(encoding="utf-8")
        for i, b in enumerate(TEX_BLOCK.findall(text), 1):
            if not b.lstrip().startswith("oasis_version"):
                continue
            check(b, f"{src} verbatim{i}")

    samples = sorted(ROOT.glob(SAMPLE_GLOB))
    if not samples:
        rc = 1
        print("FAIL 未找到用例样例 workbench/science/use-cases/*.yaml")
    for s in samples:
        check(s.read_text(encoding="utf-8"), s.relative_to(ROOT).as_posix())

    print(f"---- E4 小结：{n} 个对象校验{'全部通过' if rc == 0 else '存在失败'}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
