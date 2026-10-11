# ADR 0008: 新增 DynamicalModel 承载太阳系天体

- **状态**：已接受（经 MOTION-001 审定批准，2026-10-11）
- **日期**：2026-10-11
- **决策者**：项目负责人（审定）；OASIS 设计开发（提出）
- **涉及文档**：docs/design/targets_data_model.md、docs/design/targets.md、docs/design/targets_interfaces.md、workbench/design/design-report/MOTION-001.md

## 背景

UR-2026-1012 的 UR-OASIS-05 要求：能够表达太阳系天体（小行星、彗星等）——给定历元与轨道根数，
表达其在指定时刻的位置（并支持位置快照序列）。现 `TargetModel` 类型族（`SourceModel`/`BackgroundModel`/
`TransmissionModel`/`TargetHistogram`）均面向恒星/星系/系外行星/AGN/背景，无动力学定义的目标类型；
用户侧"天体位置服务"与"真实天体背景"渲染均被此缺口阻塞。

## 决策

新增 `TargetModel` 子类 **`DynamicalModel`**，与 `SourceModel` 平级：

- 字段：`epoch`（必填，根数历元，MPC 口径）、`elements`（`a`/`e`/`i`/`raan`/`argp` + `M` 或 `Tp` 二选一）、
  `H`（绝对星等）、`frame`（默认日心黄道 J2000）、`category`（可选：MBA/NEO/centaur/TNO）、
  `spectral_model`（可选）、`position_snapshots`（可选位置快照序列：`{time, x, y, z}`，
  观测变体 `{time, ra, dec, distance}`）；
- YAML 顶层新增 `dynamical` 键；顶层必填规则改为「`source` 与 `dynamical` 至少其一」；
- **位置计算（轨道传播）属物理引擎实现阶段职责**；本 ADR 仅定义模型承载与口径，
  实现阶段需以 MPC 解析器对齐 `M`/`Tp` 两种表达。

## 理由

- **满足需求且语义正确**：以轨道根数定义位置与自行的语义不可用 `SourceModel` 表达，独立类型避免语义污染；
- **口径保真**：元素与历元原样保留 MPC 口径（与 UR-OASIS-06"保留原始字段"一致）；
- **类型化**：全部字段为类型化定义，符合 ADR 0007 原则（物理量禁入 `metadata`）；
- **与既有层级兼容**：继承 `TargetModel`，纳入五级层级与命名空间管理；正演/反演引擎按类型分派。

## 影响

- `targets_data_model.md` 新增第 10 章（字段、`OrbitalElements` 辅助类型、不变量）；
- `targets.md` §4.1 数据类型表新增行；§3.3.1 顶层必填字段口径更新；
- `targets_interfaces.md` §2.1.1 字段约束与示例更新；
- JSON Schema 新增 `dynamical` 顶层键与 `OrbitalElements`/`dynamical_model` 定义；
- 类图新增 `DynamicalModel`/`OrbitalElements`；用例样例新增 `uc6_dynamical.yaml`；
- 概要设计说明书第 4 章数据结构与第 9 章用例表更新（重编译）。

## 考虑的替代方案

- **方案1：塞入 `SourceModel`（虚构自行表达运动）** —— 动力学语义无法表达，反演/正演分派错误；
  **否决**。
- **方案2：仅文件层处理、不进 Target 模型** —— 不满足"能表达某小行星在给定时刻的位置"；
  **否决**。
- **方案3：沿用 `TargetHistogram` 承载位置序列** —— 直方图容器语义为亮度分布，非天体定义；
  **否决**。
