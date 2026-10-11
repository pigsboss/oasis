#!/usr/bin/env bash
# ============================================================
# 基线冻结：生成关键交付物与过程记录的 SHA-256 清单（BASELINE-MANIFEST.sha256）
# 用法：bash workbench/qm/baseline/freeze.sh [LABEL]   （LABEL 默认 BASELINE-002）
# 校验：shasum -a 256 -c workbench/qm/baseline/BASELINE-MANIFEST.sha256
# ============================================================
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 2

OUT=workbench/qm/baseline/BASELINE-MANIFEST.sha256
LABEL=${1:-BASELINE-002}
TODAY=$(date +%F)

{
  echo "# OASIS 基线清单 ${LABEL}（生成于 ${TODAY}；SHA-256）"
  echo "# 校验：shasum -a 256 -c workbench/qm/baseline/BASELINE-MANIFEST.sha256"
  for f in \
    README.md \
    docs/design/targets.md docs/design/targets_data_model.md docs/design/targets_interfaces.md \
    docs/design/adr/*.md docs/design/schemas/*.json \
    docs/diagrams/targets/*.puml docs/guides/CODING_STANDARDS.md \
    docs/overview-design/main.tex docs/overview-design/main.pdf docs/overview-design/refs.bib \
    docs/overview-design/chapters/*.tex \
    workbench/GOAL.md workbench/PLAN.md \
    workbench/design/audit/issues.md workbench/design/design-report/*.md \
    workbench/design/traceability/UR-trace.md workbench/design/verify.sh \
    workbench/design/tools/*.py \
    workbench/science/requirements/UR-catalog.md workbench/science/requirements/intake/UR-2026-1012/* workbench/science/use-cases/*.yaml \
    workbench/science/test-reports/TV-001.md workbench/science/test-reports/run-tests.sh \
    workbench/review/review-plans/*.md workbench/review/review-reports/*.md \
    workbench/qm/gate-records/*.md workbench/qm/audits/*.md workbench/qm/improvements/*.md \
    workbench/library/README.md workbench/library/registry.md workbench/library/bib/*.bib; do
    if [ -f "$f" ]; then
      shasum -a 256 "$f"
    fi
  done
} > "$OUT"

echo "写入：$OUT"
echo "条目数：$(grep -c '^[0-9a-f]' "$OUT")"
