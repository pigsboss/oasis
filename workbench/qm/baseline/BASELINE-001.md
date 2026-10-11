# 基线冻结记录 BASELINE-001

- 编号：BASELINE-001　版本：v1.0（2026-10-10）　主持：质量管理
- 范围：完成契约 G-001 的全部交付物与过程记录
- 校验清单：`workbench/qm/baseline/BASELINE-MANIFEST.sha256`（**59 条**，SHA-256）
- 校验方法：`shasum -a 256 -c workbench/qm/baseline/BASELINE-MANIFEST.sha256`
- 重新生成：`bash workbench/qm/baseline/freeze.sh`
- 冻结时刻终验：`bash workbench/design/verify.sh --strict` → **PASS=7 FAIL=0 SKIP=0**（退出码 0）

## 冻结内容概况

- **交付物（docs/）**：目标层设计基线 3 文档（targets / data_model / interfaces）；ADR 0001–0007 + README + 模板；
  设计图 3（PlantUML 源）；编码规范；JSON Schema；概要设计说明书（main.tex、ch01–ch10、refs.bib、main.pdf、figures）。
- **过程记录（workbench/）**：GOAL/PLAN；ICN 台账 v1.0；DR-001；TRACE-001；UR-CAT-001；用例样例 uc1–uc5；
  TV-001 v1.1；RP/RR/GR/QA/QI 记录；verify.sh 与检查工具；文献库登记册/BibTeX/脚本。

## 排除项

- LaTeX 构建中间产物（`.aux/.log/.fls/.fdb_latexmk/.xdv/.toc/.out/.bbl` 等）；
- 本记录、验收记录（QA-002）、冻结工具（freeze.sh）与清单自身——记录/生成冻结行为，不参与清单自引用；
- 文献库大体积内容（`pdf/`、`notes/`、`meta/`）按库规则独立管理。

## 变更控制

冻结后任何受控文件的变更须：登记 QI/GR → 修改 → 重跑 `verify.sh --strict` → 重新生成清单（`freeze.sh`）。
