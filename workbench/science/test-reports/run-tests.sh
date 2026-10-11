#!/usr/bin/env bash
# ============================================================
# P4 用例测试：正例（文档示例 + UC 样例经 JSON Schema）与负例（应被拒绝的构造）
# 用法：bash workbench/science/test-reports/run-tests.sh
# ============================================================
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 2

PASS=0; FAIL=0

echo '== 正例：文档示例 + UC 样例（7 对象）经 JSON Schema =='
if python3 workbench/design/tools/validate_yaml.py; then
  echo 'POSITIVE: PASS'
  PASS=$((PASS + 1))
else
  echo 'POSITIVE: FAIL'
  FAIL=$((FAIL + 1))
fi

echo
echo '== 负例：3 个应被拒绝的构造 =='
python3 - <<'PY'
import copy, json, pathlib, sys
import yaml
from jsonschema import Draft202012Validator

root = pathlib.Path('.').resolve()
schema = json.loads((root / 'docs/design/schemas/target-model-submission.schema.json').read_text(encoding='utf-8'))
v = Draft202012Validator(schema)

base4 = yaml.safe_load((root / 'workbench/science/use-cases/uc4_extinction_background.yaml').read_text(encoding='utf-8'))
base1 = yaml.safe_load((root / 'workbench/science/use-cases/uc1_binary.yaml').read_text(encoding='utf-8'))

cases = {}
c = copy.deepcopy(base4); del c['background']['spatial_model']
cases['N1 异向背景缺 spatial_model'] = c
c = copy.deepcopy(base1); del c['source']
cases['N2 缺 source（顶层必填）'] = c
c = copy.deepcopy(base1); c['source']['spectral_model']['parameters']['temperature'] = {'value': 'warm', 'unit': 'K'}
cases['N3 value 非数值'] = c

rc = 0
for name, obj in cases.items():
    errs = list(v.iter_errors(obj))
    if errs:
        print(f'REJECTED(ok)   {name} -> {errs[0].message[:70]}')
    else:
        rc = 1
        print(f'ACCEPTED(bad)  {name} -> 未按预期拒绝')
sys.exit(rc)
PY
if [ $? -eq 0 ]; then
  echo 'NEGATIVE: PASS（3/3 被拒绝）'
  PASS=$((PASS + 1))
else
  echo 'NEGATIVE: FAIL'
  FAIL=$((FAIL + 1))
fi

echo
printf '汇总：PASS=%d FAIL=%d\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
