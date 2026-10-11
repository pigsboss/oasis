# 动议 MOTION-001：Target 模型承载星表字段与太阳系天体（UR-OASIS-03/04/05）

- 编号：MOTION-001　版本：v0.1（提请审定）　日期：2026-10-11
- 提出人：设计开发　审定人：项目负责人（用户侧代表）
- 关联：UR-2026-1012 提交包（UR-OASIS-03/04/05）、基线 BASELINE-001（冻结中）、C 循环计划
- 性质：**触及已冻结目标层设计的变更动议**——批准后方可进入 C1 设计修订（含独立复核与基线更新）

## 一、背景

UR-2026-1012 中有 3 条"模型承载"类需求在现设计中无处安放：

1. **UR-OASIS-03**：恒星星表字段（`parallax`/`pmra`/`pmdec`/`phot_g_mean_mag`/`bp_rp`/`source_id`）——
   `SourceModel` 现仅 `coordinates(ra/dec/distance)` + `proper_motion`，**星表进不来**；
2. **UR-OASIS-04**：`epoch`/`frame` 必须显式——现仅 ICRS 语义，无时标字段；
3. **UR-OASIS-05**：太阳系天体（轨道根数＋`H`＋位置快照）无对应类型——现类型均面向恒星/星系/系外行星/AGN/背景。

## 二、动议内容（三项设计变更）

### 变更一：`SourceModel` 增加可选 `catalogue` 块（UR-03）

保持原始值保真，采用**类型化**子块（不引入自由字典，遵守 ADR 0007）：

| 字段 | 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `catalog` | str | 是（块内） | 来源目录标识，如 `"gaia_dr3"` |
| `source_id` | str | 是（块内） | 目录内唯一 ID（Gaia int64 以十进制字符串保存，兼容 MPC 编号/名称） |
| `parallax` | Quantity | 否 | 三角视差（典型 mas） |
| `phot_g_mean_mag` | Quantity | 否 | G 波段平均星等（命名沿 Gaia 官方列语义） |
| `bp_rp` | Quantity | 否 | 颜色指数 |
| `teff` | Quantity | 否 | 有效温度（若目录直接给温，优先于 `bp_rp` 派生） |

示例：
```yaml
source:
  name: "gaia_5853498713190525696"
  coordinates:
    ra: {value: 83.633, unit: "deg"}
    dec: {value: 22.014, unit: "deg"}
  proper_motion:
    pm_ra_cosdec: {value: 34.5, unit: "mas/yr"}
    pm_dec: {value: -12.3, unit: "mas/yr"}
  catalogue:
    catalog: "gaia_dr3"
    source_id: "5853498713190525696"
    parallax: {value: 15.2, unit: "mas"}
    phot_g_mean_mag: {value: 5.71, unit: "mag"}
    bp_rp: {value: 1.02, unit: "mag"}
  spectral_model:
    type: "blackbody"
    parameters:
      temperature: {value: 5778, unit: "K"}
```

### 变更二：`SourceModel` 增加 `epoch`/`frame` 类型化字段（UR-04）

- `epoch`（可选，默认 `"J2000"`；Gaia 来源须显式写 `"J2016.0"`）；
- `frame`（可选，默认 `"ICRS"`）；
- 交付 manifest 同步增加 `epoch`/`frame` 字段（满足"每件携带"）；
- 二者**不得**进入 `metadata`（ADR 0007 一致性）。

### 变更三：新增 `DynamicalModel` 类型（UR-05）→ 拟立 ADR 0008

- 继承 `TargetModel`，与 `SourceModel` 平级；
- 字段：

| 字段 | 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `epoch` | str/Quantity | 是 | 根数历元（JD/TDB，MPC 口径） |
| `elements` | `OrbitalElements` | 是 | `a, e, i, Ω, ω` + `M` 或 `Tp`（二选一） |
| `H` | Quantity | 是 | 绝对星等（mag） |
| `frame` | str | 否 | 默认日心黄道 J2000；例外（如重心系 NEO）显式声明 |
| `category` | enum | 否 | MBA / NEO / centaur / TNO |
| `spectral_model` | `SpectralModel` | 否 | 有 SED 时的可选补充 |
| `position_snapshots` | list | 否 | 给定时刻的位置序列（时间＋位置）；**生成**属物理引擎职责，本次仅模型承载 |

- 角度单位 `deg`；轨道传播/位置计算列实现阶段；MPC 解析器在该阶段对齐本节口径。

## 三、备选方案与否决理由

| 变更 | 备选方案 | 结论 |
|:---|:---|:---|
| 03 | 原始列名自由字典透传 | 违反 ADR 0007"物理量必须类型化"，**否决** |
| 03 | 仅做测光→SED 映射，不保留原始值 | 丢失原始字段（UR-06 明确要求保留），**否决** |
| 03 | 采用的方案 | 类型化 `catalogue` 块 + 文档化映射，保留原始值 |
| 04 | 放入 `metadata` | 违反 ADR 0007，**否决** |
| 04 | 仅全局默认、不设字段 | 不满足"显式"，**否决** |
| 05 | 塞入 `SourceModel`（虚构自行表达运动） | 语义错误，**否决** |
| 05 | 仅文件层处理、不进模型 | 不满足"能表达某小行星在给定时刻的位置"，**否决** |

## 四、口径条款（随批准生效，写入设计文档）

1. Gaia `pmra`（已含 cos δ 因子）↔ `pm_ra_cosdec` **直接映射**；单位 mas/yr；
2. `distance = 1000 / parallax`（mas → pc）；视差 ≤ 0 时 `distance` 缺省并保留原始视差；
3. 测光→`spectral_model` **不自动派生**；保留原始测光；可选派生映射（如 `bp_rp`→`Teff`）须显式启用并标注 `derived`；
4. `DynamicalModel` 默认日心黄道 J2000；元素与历元**原样保留** MPC 口径；
5. `epoch`/`frame` 为类型化字段，禁入 `metadata`。

## 五、影响面

| 工件 | 变更 |
|:---|:---|
| `docs/design/targets_data_model.md` | `SourceModel` 字段更新；新增 `DynamicalModel` 章节 |
| `docs/design/targets.md` §4.1 | 数据类型表更新/新增行 |
| `docs/design/targets_interfaces.md` | YAML 输入示例与字段约束更新 |
| `docs/design/schemas/target-model-submission.schema.json` | 新字段与 `DynamicalModel` 定义 |
| `docs/diagrams/targets/classes.puml` | 新类与关系 |
| 用例样例 | 新增 `uc6_dynamical.yaml`；`uc1` 增星表示例字段 |
| 概要设计说明书 | ch4 数据结构更新（重编译） |
| ADR | 新增 **0008**（DynamicalModel）、**0009**（SourceModel 星表扩展） |
| 验证/基线 | `verify.sh` 断言扩展＋全量回归；登记 GR-003；基线 → BASELINE-002 |

## 六、兼容性与边界

- **全部新字段可选** → 既有 YAML、用例样例、契约零破坏（以 `verify.sh --strict` 回归保证）；
- 不改变：TOP 架构、三段契约、FITS 层间格式、五级层级、OIFITS 口径；
- 风险：`M` vs `Tp` 两种根数表达在实现阶段需与 MPC 解析器对齐——口径条款已预先固定。

## 七、审定请求

请择一回复：

- **批准 MOTION-001**（三项变更＋口径条款），进入 C1 设计修订；
- 批准但附修改意见（请指明条款）；
- 暂缓或驳回（请说明原因）。

批准后的执行路径：C1 设计修订（ADR 0008/0009＋Schema＋样例）→ 独立复核（门禁）→ `verify.sh --strict` 回归 → 更新基线（BASELINE-002）。
