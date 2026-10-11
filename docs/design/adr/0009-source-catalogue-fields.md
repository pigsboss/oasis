# ADR 0009: SourceModel 增加 catalogue 块与 epoch/frame 字段

- **状态**：已接受（经 MOTION-001 审定批准，2026-10-11）
- **日期**：2026-10-11
- **决策者**：项目负责人（审定）；OASIS 设计开发（提出）
- **涉及文档**：docs/design/targets_data_model.md、docs/design/targets_interfaces.md、workbench/design/design-report/MOTION-001.md

## 背景

UR-2026-1012 中两条需求：
- UR-OASIS-03：恒星星表字段（`parallax`/`pmra`/`pmdec`/`phot_g_mean_mag`/`bp_rp`/`source_id`）
  需在 Target 件中可携带——现 `SourceModel` 仅 `coordinates(ra/dec/distance)` + `proper_motion`，
  "星表进不来"；
- UR-OASIS-04：`epoch`/`frame` 必须显式（现仅 ICRS 语义），且每件（含交付 manifest）携带。

## 决策

1. `SourceModel` 增加**可选** `catalogue` 子块（类型 `CatalogueEntry`）：
   - `catalog`（str，必填，如 `"gaia_dr3"`）、`source_id`（str，必填；Gaia int64 以十进制字符串保存）；
   - `parallax`/`phot_g_mean_mag`/`bp_rp`/`teff`（可选，均为 Quantity，原始值保真）；
2. `SourceModel` 增加**可选** `epoch`（默认 `"J2000"`）与 `frame`（默认 `"ICRS"`）类型化字段；
   交付 manifest 同步增加 `epoch`/`frame` 字段；
3. 随批准生效的口径条款：
   - Gaia `pmra`（已含 cos δ 因子）↔ `pm_ra_cosdec` **直接映射**，单位 mas/yr；
   - `distance = 1000 / parallax`（mas → pc）；视差 ≤ 0 时 `distance` 缺省、保留原始视差；
   - 测光 **不自动派生** `spectral_model`；保留原始测光，可选派生映射（如 `bp_rp`→`Teff`）
     须显式启用并标注 `derived`；
   - `epoch`/`frame` **禁入 `metadata`**（ADR 0007 一致性）；
   - `catalogue.catalog = "gaia_dr3"` 时 `epoch` 应显式写 `"J2016.0"`（由 Ingest 工具写入，模型层不做隐式推断）。

## 理由

- **原始值保真**：UR-OASIS-06 明确允许"保留原始字段"，类型化子块在保真的同时避免自由字典；
- **类型化原则**：若以原始列名字典透传，物理量将落入非结构化容器，违反 ADR 0007；类型化子块合规；
- **向后兼容**：全部字段可选，既有 YAML、样例与契约零破坏；
- **可扩展**：`catalog` 字段允许未来接入更多目录（2MASS/WISE/TESS）而不改结构。

## 影响

- `targets_data_model.md` §3.3/§3.4 更新（字段与不变量）；
- `targets_interfaces.md` §2.1.1 字段约束与示例更新；
- JSON Schema：`source_model` 增加 `catalogue`/`epoch`/`frame`；新增 `catalogue_entry` 定义；
- 用例样例 `uc1_binary.yaml` 增补星表示例字段；
- 口径条款写入设计文档与交付说明（随 C 循环的源表子系统设计细化）。

## 考虑的替代方案

- **方案1：原始列名自由字典透传** —— 违反 ADR 0007（物理量必须类型化），并破坏 Schema 校验能力；
  **否决**。
- **方案2：仅做测光→`spectral_model` 映射，不保留原始字段** —— 丢失原始值（UR-OASIS-06 要求保留）；
  **否决**。
- **方案3：将 `epoch`/`frame` 放入 `metadata`** —— 违反 ADR 0007 且不可校验；**否决**。
