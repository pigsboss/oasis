# 文档问题台账（ICN）

- 编号：ICN-LEDGER　版本：v1.0（2026-10-10，P3 全量回归关闭完成）　编制：设计开发
- 等级：A 必须整改（6）｜B 应整改（19）｜C 可整改（8）
- 状态统计：**CLOSED 32 ｜ WONTFIX 1 ｜ FIXED 0 ｜ OPEN 0**
- 状态定义：OPEN / FIXED（已整改待复核）/ CLOSED（经复核）/ WONTFIX（附理由）

| ID | 位置 | 问题 | 类别 | 等级 | 状态 |
|:---|:---|:---|:---|:---|:---|
| ICN-001 | ADR 0002:6、0003:6、0004:6、ADR README:29/77、classes.puml:3 | 引用 `docs/guides/targets.md`（实际应为 `docs/design/targets.md`），共 6 处死链 | 干净 | B | CLOSED |
| ICN-002 | targets.md:217 vs §4.4.1:499-529；targets_interfaces.md:27/54 | YAML 顶层必填字段矛盾：§3.3.1 要求 `target_name`、`parameters`，而 §4.4.1 顶层字段清单、示例与接口文档均无此二字段 | 自洽 | A | CLOSED |
| ICN-003 | ADR 0005:24；ADR 0006:20/45/66 | 引用不存在的 "ADR 001（TargetModel 基类字段设计）"；该内容实际以"模板"名义存放于 `template.md` 且编号冲突（根源见 ICN-022） | 自洽 | B | CLOSED |
| ICN-004 | ADR README:11-14 | 示例目录列出不存在的文件名（如 `0002-use-target-histogram-for-distributions.md`） | 准确 | C | CLOSED |
| ICN-005 | ADR 0005:3-4、0006:3-4、ADR README | 状态与日期不一致：0006 已落实却标"已提议"；"已接纳" 与 "已接受" 混用；0005/0006 日期早于 ADR 机制建立（04-24）与提交时间 | 自洽 | B | CLOSED |
| ICN-006 | README、targets.md | "三层（TOP）" 与 "三段（V 型）" 术语相邻出现，层级概念易混 | 干净 | C | CLOSED |
| ICN-007 | README:44/52/54/58/61 vs targets*.md | 层间格式口径不一：README 称 OIFITS 2 为核心交换格式，目标层接口文档仅述 FITS+JSON，未见 OIFITS 对接映射 | 自洽 | A | CLOSED |
| ICN-008 | 仓库根 | 工程配套缺失：LICENSE、CI、贡献指南（设计阶段可接受，备案） | 干净 | C | WONTFIX |
| ICN-009 | targets.md、targets_interfaces.md | "FITS/HDF5" 双格式定位模糊：接口确定 FITS，但组件命名与诊断规范大量出现 HDF5，读者难辨实现边界 | 自洽 | B | CLOSED |
| ICN-010 | targets.md:520-527（§4.4.1 示例） | YAML 示例与数据模型不符：`spectral_model` 缺 `parameters` 包装（vs data_model §2.2）；`transmission` 块缺必填 `optical_depth`/`spectral_model`，且 `A_v` 非已声明参数（vs §5.3） | 自洽 | A | CLOSED |
| ICN-011 | targets_interfaces.md:29/32/36/38（§2.1.1） | 顶层结构示例 YAML 不可解析：`...` 被当作文档结束符、`true/false` 为字符串字面量（PyYAML 实测报错） | 自洽 | A | CLOSED |
| ICN-012 | data_model.md:22-23 vs interfaces.md:43-44 | `provider`/`version` 必填性与默认值口径矛盾（数据模型标"必需"并给默认值；接口标"可选"；`version` 默认 `0.1.0` 未见于数据模型） | 自洽 | B | CLOSED |
| ICN-013 | interfaces.md:179 vs §3.4:350-362 | `.error` 示例错误码 `OBS_001` 不符合 `E_{DOMAIN}_{CODE}` 格式，且码表无 `OBS` 域（存在语义重叠的 `E_DATA_002`） | 自洽 | B | CLOSED |
| ICN-014 | targets.md:534 vs interfaces.md:143-150 | 正演 FITS 必填关键字清单不一致：targets.md 仅列 5 个；interfaces.md 追加 `SRC_MODEL`/`BKG_MODEL`/`TRANS_MODEL`/`SPATIAL_TYP` | 自洽 | B | CLOSED |
| ICN-015 | interfaces.md:108 vs :327-334 | `ResultBundle.status` 示例值 `"success"` 不在 `TaskState` 枚举内（completed/failed/…） | 自洽 | B | CLOSED |
| ICN-016 | README:37-38、targets.md:536、interfaces.md:153-156/174 | 辅助文件清单与格式不一致：targets.md 称 CSV/TSV 处理指令，interfaces.md 为 `params.json`/`config.yaml`/`processing_log.txt`；README"反演=JSON"实际含 YAML | 自洽 | B | CLOSED |
| ICN-017 | interfaces.md:12/166-170；targets.md:250 | 反演输入包头关键字无版本类键（如 `OASIS_OBS_INTF_VER`），与"所有外部输入输出携带 oasis_version"及版本兼容校验要求冲突 | 自洽 | B | CLOSED |
| ICN-018 | components.puml:20-22 | `Observables Interface` 被画入 "Observables Layer" 包，与正文"数据段组件"归属矛盾；并致 `PE --> OI` 外观上直连观测量层 | 自洽 | A | CLOSED |
| ICN-019 | components.puml:56 | 数据服务横向箭头 `RP ..> FITSIO`，与接口 G"接口段→数据段（受控横向）"不符（端点应为数据段/结果仓库） | 自洽 | B | CLOSED |
| ICN-020 | activities.puml:32-35 vs targets.md:463/475 | 正演数据段步骤顺序颠倒：图示 FITS I/O 在 Observables Interface 之前，正文为 OI 接收→委派序列化 | 自洽 | B | CLOSED |
| ICN-021 | targets.md:429（§4.1） | `BackgroundModel` 行未同步 ADR 0006 的 `is_isotropic`/`spatial_model` 字段（全文无 SpatialModel 相关表述） | 自洽 | B | CLOSED |
| ICN-022 | adr/template.md:1-6 vs ADR README:21/52 | `template.md` 实为已填写的"ADR 001: TargetModel 基类字段设计"（编号冲突、模板失效）；应还原模板并归档为 ADR 0007 | 干净 | A | CLOSED |
| ICN-023 | ADR README:79 | 示例误引 "见 ADR-0001" 指代三段式架构（实际为 ADR 0002），且写法与命名规则不一致 | 准确 | B | CLOSED |
| ICN-024 | README:21 vs :23 | 总括"数据流 T → O → P"与载荷层行"载荷数据 → 观测量"方向表述矛盾 | 自洽 | B | CLOSED |
| ICN-025 | README:36/59 vs targets.md:222 | README 列"源表 (Catalogue) CSV/TSV"输入，规范明确"当前版本以 YAML 为确定接口"且未定义源表格式 | 自洽 | B | CLOSED |
| ICN-026 | README:46 | OIFITS 列名 `UVCOORD` 有误（标准为 `UCOORD`/`VCOORD`，见文献 `duvert2017oifits` OI_VIS/OI_VIS2 定义） | 准确 | B | CLOSED |
| ICN-027 | targets.md:103/361 vs ADR 0002:12 | 依赖方向表述含混："接口段只应对上"（§3.1）与接口 G 横向通道、ADR 0002 方向表述及 C/D/H 方向存在张力；"→"语义（数据流 vs 依赖）未统一 | 自洽 | B | CLOSED |
| ICN-028 | ADR 0001-0006、template | ADR 标题编号格式不统一：0001-0004 无前缀、0005 四位、0006 三位、template 三位 | 干净 | C | CLOSED |
| ICN-029 | interfaces.md:5/8/327 | "观测层"与"观测量层"术语混用（同文件 :135 又用"观测量层"） | 干净 | C | CLOSED |
| ICN-030 | CODING_STANDARDS.md:1 | 标题 "MCPC Coding Standards…" 与本项目（OASIS）无关且无出处 | 准确 | C | CLOSED |
| ICN-031 | classes.puml:18-19 | `SpectralModel` 类体为空，缺 `type`/`parameters`/`metadata`（与对称的 `SpatialModel` 不一致） | 自洽 | C | CLOSED |
| ICN-032 | classes.puml:68 | `BackgroundModel "0..1" --> "1" SpatialModel` 多重性方向写反（应为 `"1" --> "0..1"`） | 准确 | C | CLOSED |
| ICN-033 | targets_interfaces.md §2.1.1 示例 | 示例 source 缺数据模型约定义务的 `proper_motion`（P3 回归发现：JSON Schema 校验不通过；同日修复） | 准确 | B | CLOSED |

**审计方法与覆盖（P0 记录）**

- 三路独立只读审计：① 数据模型/接口一致性；② 架构/ADR/术语；③ 格式示例/死链/图语法。全部发现经人工抽查核验。
- 机械核查结果：PlantUML 1.2026.8 `-checkonly` 三个图文件全部通过；PyYAML 6.0.3 可用（ICN-011 实测报错）；
  除 ICN-001 六处外，仓库内无其他失效路径引用（GOAL/PLAN 中的 `overview-design/`、`verify.sh` 等为计划产出物，非死链）。
- 修正记录：ICN-002 行号 218 → 217；ICN-003 扩展覆盖 ADR 0006 三处引用。

**修订记录**

- 2026-10-10 v0.3（P1-A 批次）：ICN-002/003/010/011/018/019/022 置 FIXED。
- 2026-10-10 v0.4（P1-B/C 批次）：其余 24 项置 FIXED（死链、ADR 规范、FITS 口径、关键字清单、错误码、
  活动图步骤、README 数据流/源表/列名、依赖方向说明、类图与术语等）。
- 2026-10-10 v0.5（P1 复核关闭）：独立复核 6/6 A 级 PASS（详见 QA-001）；A 级 6 项 + ICN-003 置 CLOSED；
  ICN-008 置 WONTFIX（工程配套待代码化立项）。
- 2026-10-10 v0.6（P3 回归）：新增 ICN-033（§2.1.1 示例补 `proper_motion`）；`verify.sh` 首版运行
  PASS=6 / FAIL=0 / SKIP=1（E9 TV-001 为 P4 产物）。
- 2026-10-10 **v1.0（P3 回归关闭）**：24 项 FIXED 经 `bash workbench/design/verify.sh` 全量回归逐项通过
  （E2/E3 文档检查、E4 Schema 校验 7/7、E5 LaTeX 构建、E6 文献 key、E7 台账、E8 门禁记录），全部置 CLOSED。
  台账归零：OPEN 0 / FIXED 0。

> 结论：ICN 台账闭环完成（CLOSED 32、WONTFIX 1 附理由、OPEN 0）。后续回归统一由 `workbench/design/verify.sh` 执行。
