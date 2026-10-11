#!/usr/bin/env bash
# ============================================================
# OASIS 验证总入口（完成契约 G-001 证据 E1–E9）
# 用法：bash workbench/design/verify.sh [--strict]
#   默认：尚未进入对应阶段、按计划未产出的检查项记 SKIP（不影响退出码）
#   --strict：禁止 SKIP——所有检查项必须 PASS（用于最终验收）
# 退出码：0 = 无 FAIL；1 = 存在 FAIL
# ============================================================
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 2

STRICT=0
[ "${1:-}" = "--strict" ] && STRICT=1

FAIL=0; SKIP=0; PASS=0
pass() { printf 'PASS  %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf 'FAIL  %s\n' "$1"; FAIL=$((FAIL + 1)); }
skip() {
  if [ "$STRICT" = 1 ]; then fail "$1（strict：不允许 SKIP）"; else printf 'SKIP  %s\n' "$1"; SKIP=$((SKIP + 1)); fi
}

echo "==== OASIS 验证（verify.sh）$( [ "$STRICT" = 1 ] && echo '· strict' ) ===="

echo '-- E2/E3 文档一致性与死链 --'
if python3 workbench/design/tools/check_docs.py; then pass "E2/E3 文档检查"; else fail "E2/E3 文档检查"; fi

echo '-- E4 YAML 示例与 Schema 校验 --'
if python3 workbench/design/tools/validate_yaml.py; then pass "E4 YAML Schema"; else fail "E4 YAML Schema"; fi

echo '-- E5 LaTeX 构建 --'
if (cd docs/overview-design && latexmk -xelatex -interaction=nonstopmode main.tex >/tmp/oasis_latexmk.log 2>&1) && [ -f docs/overview-design/main.pdf ]; then
  pass "E5 latexmk 构建 + main.pdf"
else
  fail "E5 latexmk 构建（日志：/tmp/oasis_latexmk.log）"
fi

echo '-- E6 文献引用 key --'
KEYS=$(grep -oE 'duvert2017oifits|fits_standard40|greisen2002wcs|astropy2022|quanz2022life|monnier2003optical|eisenhauer2023advances' docs/overview-design/main.tex | sort -u | wc -l | tr -d ' ')
if [ "$KEYS" -ge 4 ]; then pass "E6 文献库 key（$KEYS 个 >= 4）"; else fail "E6 文献库 key 不足（$KEYS）"; fi

echo '-- E7 ICN 台账归零 --'
if [ -f workbench/design/audit/issues.md ] && ! grep -q '| OPEN |' workbench/design/audit/issues.md; then
  pass "E7 ICN 台账 0 OPEN"
else
  fail "E7 ICN 台账仍有 OPEN 条目"
fi

echo '-- E8 门禁记录 --'
E8_OK=1
for f in RR-001 RR-002; do grep -q '通过' "workbench/review/review-reports/$f.md" 2>/dev/null || E8_OK=0; done
for f in GR-001 GR-002; do grep -q '准予' "workbench/qm/gate-records/$f.md" 2>/dev/null || E8_OK=0; done
if [ "$E8_OK" = 1 ]; then pass "E8 G1/G2 门禁记录（RR-001/002、GR-001/002）齐备且通过"; else fail "E8 门禁记录缺失或未通过"; fi

echo '-- E9 测试报告（P4 产物）--'
TV=workbench/science/test-reports/TV-001.md
if [ -f "$TV" ]; then
  E9_OK=1
  for i in 1 2 3 4 5; do grep -q "| UC-$i |" "$TV" || E9_OK=0; done
  grep -q '结论.*通过' "$TV" || E9_OK=0
  if [ "$E9_OK" = 1 ]; then
    pass "E9 TV-001 用例 UC-1..5 逐条在册且结论通过"
  else
    fail "E9 TV-001 缺用例行或结论非通过"
  fi
else
  skip "E9 TV-001 尚未产出（P4 阶段产物）"
fi

echo '================================'
printf '汇总：PASS=%d  FAIL=%d  SKIP=%d\n' "$PASS" "$FAIL" "$SKIP"
[ "$FAIL" = 0 ] || exit 1
exit 0
