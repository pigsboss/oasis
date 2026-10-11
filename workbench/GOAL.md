# 完成契约 G-001：OASIS 设计文档治理与概要设计交付

- 编号：G-001　版本：v1.0（已批准，2026-10-10）　日期：2026-10-10
- 编制：设计开发　审定：质量管理　依据：用户任务指令
- 关联：`PLAN.md`（v1.2）、四角色章程（`design|science|review|qm/CHARTER.md`）、文献库（`library/`）

## 1. 最终状态（完成定义）

全部满足方为完成：

1. **文档基线**：`docs/` 全部文档满足三准则——
   - 自洽：0 死链（全部交叉引用与约定路径可解析）、术语与字段名在文档间及文档—图之间一致（0 冲突）；
   - 准确：全部 YAML 示例通过对应 JSON Schema 校验；
   - 干净：目录结构规范、无临时/冗余产物、单一来源。
2. **ICN 台账归零**：`design/audit/issues.md` 无 OPEN 条目；A 级全部 CLOSED；
   B/C 级 CLOSED 或 WONTFIX（附理由）。
3. **LaTeX 概要设计**：`docs/overview-design/` 经 `latexmk -xelatex` 编译通过并产出 `main.pdf`；
   含 PLAN §9 约定的 10 章骨架；"引用文件"章节含 ≥4 个文献库 key 的 BibTeX 引用。
4. **门禁与过程记录**：
   - G1：方案设计评审结论"通过"，A 类意见全部闭环，`GR-001` 归档；
   - G2：测试报告评审结论"通过"，`GR-002` 归档；
   - TV 测试报告覆盖 UC-1…UC-5：每条用例有预期/实测对照；
     未覆盖项须显式声明、说明理由并经评审认可；
   - QM 的 QA 监督记录与 QI 改进台账存在且闭环。
5. **验证工件**：JSON Schema、YAML 用例样例、验证脚本 `design/verify.sh` 存在；
   脚本整体运行退出码 0。

## 2. 证据（如何证明——E1–E9 全部通过才算完成）

| # | 检查 | 命令 / 判据 | 通过标准 |
|:--|:--|:--|:--|
| E1 | 总验证 | `bash workbench/design/verify.sh` | 退出码 0，全项 PASS |
| E2 | 死链与引用 | verify.sh 内链接检查 | 0 死链 |
| E3 | 术语/字段一致性 | verify.sh 内对照检查 | 0 冲突 |
| E4 | YAML 示例 | verify.sh 内 Schema 校验 | 全部通过 |
| E5 | LaTeX 构建 | `latexmk -xelatex docs/overview-design/main.tex` | 退出码 0，`main.pdf` 存在 |
| E6 | 文献引用 | 对 `main.tex` 源文件 grep 文献库 key | ≥4 个 key |
| E7 | ICN 归零 | 台账中无 `OPEN` 状态条目 | 0 条 |
| E8 | 门禁记录 | `review/review-reports/RR-*.md` 结论=通过；`qm/gate-records/GR-*.md` 齐备 | 齐备且通过 |
| E9 | 测试报告 | `science/test-reports/TV-001.md` 用例逐条对照 | 全部通过（未覆盖项经评审认可） |

> E1–E4 的检查器随 P3 验证工件实现；检查器与 `verify.sh` 的存在性本身是完成条件之一。

## 3. 边界（不可逾越）

- 只允许修改：`docs/`、`workbench/`、根 `README.md`（确有需要时）；
- 不触碰：`docs/references/gdr3_csv_header.txt`、`.git/`、仓库外文件；
- 不实施 OASIS 正式软件系统开发（本目标范围为文档与设计交付；观测层/载荷层仅至接口级大纲）；
- 不伪造评审与测试结论：评审/验收由独立子代理（全新上下文）执行并留痕；
- 不删除或改写已归档的评审、质量与文献登记记录；文献库可按其规则正常增补；
- 不执行 `git commit / push`（除非用户另行指示）。

## 4. 循环（如何迭代）

1. 按 ICN 台账逐条闭环：修复 → 复核 → 关单；
2. 每轮修订后运行 `verify.sh`（P3 之前以临时检查代替），失败项立即回到修复；
3. 每阶段末由独立评审子代理执行评审：设计报告 → G1；测试报告 → G2；
4. QM 逐阶段审核并出具 GR / QA / QI 记录，无记录不流转。

## 5. 停止规则（诚实终止）

- 出现以下情况之一时，**记录并报告，不强行通过**：
  需用户决策的范围变更；外部条件阻塞（如工具链损坏、网络不可用）；
  同一阻塞连续 3 轮无法推进。
- 绝不把未经验证的条目标记为完成（含 E1–E9 中任何一项未通过时如实上报失败项与原因）。

## 6. 预算

- 默认不设预算：本目标自带明确终点与证据，达标即停、遇阻即报。
- 如需控制成本，可在批准时指定 token 预算。

## 7. 启动状态

- [x] 用户已批准（2026-10-10）；目标已启动（goal mode）。启动文字（已采用）：

  **objective**：按 `workbench/GOAL.md`（完成契约 G-001）完成 OASIS 设计文档治理与概要设计交付：
  `docs/` 文档基线自洽、准确、干净并经 ICN 台账闭环；LaTeX 概要设计编译产出 `main.pdf`；
  四角色门禁 G1/G2 与测试报告、验证工件齐备。

  **completionCriterion**：GOAL.md §2 证据表 E1–E9 全部通过（verify.sh 退出码 0；
  latexmk 编译成功且 `main.pdf` 存在；ICN 无 OPEN；RR/GR/TV 齐备且结论为通过）。
