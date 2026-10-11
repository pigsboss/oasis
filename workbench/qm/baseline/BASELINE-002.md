# 基线冻结记录 BASELINE-002

- 编号：BASELINE-002　版本：v1.0（2026-10-11）　主持：质量管理
- 取代：**BASELINE-001**（2026-10-10）
- 范围：完成契约 G-001 全部交付物与过程记录 **＋ C 循环增量**（MOTION-001 / ADR 0008/0009 / UR-2026-1012 受理件）
- 校验清单：`workbench/qm/baseline/BASELINE-MANIFEST.sha256`（**70 条**，SHA-256）
- 校验方法：`shasum -a 256 -c workbench/qm/baseline/BASELINE-MANIFEST.sha256`
- 重新生成：`bash workbench/qm/baseline/freeze.sh BASELINE-002`
- 冻结时刻终验：`bash workbench/design/verify.sh --strict` → **PASS=8 FAIL=0 SKIP=0**（退出码 0）

## 相对 BASELINE-001 的增量

- **设计契约**：ADR 0008（DynamicalModel）/0009（SourceModel 星表扩展）；`targets_data_model.md` §3.3/§3.4/§10；
  `targets.md` §3.3.1/§4.1/§4.3.1/§4.4.1；`targets_interfaces.md` §2.1.1；JSON Schema（`catalogue`/`dynamical`）；
  类图（DynamicalModel 等）；概要设计 ch04/ch06/ch09/ch10（`main.pdf` 重编译）；
- **样例与验证**：`uc6_dynamical.yaml`、`uc1` 增补星表字段；`verify.sh`（PlantUML 检查 + E8 扩展）；
  `check_docs.py`（E3-09/12/13）；`run-tests.sh`；`TV-001` v1.2；
- **过程记录**：`MOTION-001`（批准）、`RR-003`（复核）、`GR-003`（变更闭环）、UR 受理件 `intake/UR-2026-1012/`。

## 变更控制

冻结后任何受控文件的变更须：登记 QI/GR → 修改 → `verify.sh --strict` 回归 → 独立复核 → 重新冻结（BASELINE-00N）。
