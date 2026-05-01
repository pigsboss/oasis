# ADR 0005: 将 TargetModel 溯源字段命名为 provider

- **状态**：已接纳
- **日期**：2026-04-04
- **决策者**：OASIS 架构团队
- **涉及文档**：docs/design/targets_data_model.md, docs/design/targets.md, docs/diagrams/targets/classes.puml

## 背景

在目标层核心数据类型 `TargetModel` 的初始设计中，用于表示“模型由谁提供/来自何处”的字段被命名为 `source`。然而在天文学语境中，`source` 一词通常指代天体信号源（如点源、展源），且 `SourceModel` 恰为 `TargetModel` 的直接子类。这种命名重叠会在开发、接口设计及科学讨论中造成持续歧义：用户和开发者可能难以瞬间区分 `source` 是指模型的出处，还是模型所描述的天体物理源。

为避免概念混淆并保持语义清晰，需要为这一溯源字段选择更具区分度的名称。

## 决策

我们将 `TargetModel` 中用于描述模型提供者/出处的字段由 `source` 重命名为 `provider`。

`provider` 的值可为用户名、文献 DOI、算法名称、反演任务 ID 等字符串。若用户未显式提供，默认值为 `"user"`。

相应的：

- `TargetModel` 字段列表中的 `source` 全部替换为 `provider`。
- 概要设计文档、类图及其他引用了该字段的地方一并更新。
- 现有 ADR 001（TargetModel 基类字段设计）中若已涉及 `source` 需同步修正（当前 ADR 001 中已使用 `provider`，无需额外改动）。

## 理由

- `provider` 明确指向“提供者”，与物理源（source）彻底分离，消除了术语歧义。
- 该词简短、通用，能涵盖用户、文献、算法等各类来源，不局限学术引用。
- 与 OASIS 其他模块（如层次管理器）的语境相容，向上游追溯时易于理解。

## 影响

- **正面**：大大降低开发者与用户的认知成本；代码自文档化效果提升。
- **需同步更新**：
  - `docs/design/targets_data_model.md`（已完成）
  - `docs/design/targets.md` 第 4.1 节表格中 `TargetModel` 的字段行
  - `docs/diagrams/targets/classes.puml` 中 `TargetModel` 的属性声明
  - 未来所有 `TargetModel` 子类及测试数据中的字段名
- **数据兼容**：若已有序列化数据使用 `source` 键，需执行一次性迁移或提供读取时的回退机制。

## 考虑的替代方案

- **方案1：使用 `citation`**
  - 优点：强调学术引用，更具科学规范感。
  - 缺点：对非文献类来源（如用户、算法）不够直觉，可能误导使用方式。
  - **否决**：因为需要包容多种来源，`provider` 更通用。

- **方案2：拆分为 `source_type` 和 `source_value`**
  - 优点：结构化，可区分来源类型。
  - 缺点：额外复杂度，且仍保留 `source` 词根，未解决歧义。
  - **否决**：过度设计。
