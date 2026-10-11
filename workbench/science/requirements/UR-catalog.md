# 科学需求集（UR Catalogue）

- 编号：UR-CAT-001　版本：v0.1（2026-10-10）　编制：科学用户　监督：质量管理
- 依据：用户任务指令；PLAN-001 §6 用例方向；共享文献库（`quanz2022life`、`monnier2003optical`、`eisenhauer2023advances`、`duvert2017oifits`、`fits_standard40`、`greisen2002wcs`、`astropy2022`）
- 范围：面向 OASIS 目标层当前设计阶段的科学需求；观测量层/载荷层需求待其设计立项后补充。
- 用途：P1/P2 设计输入与追溯基线（UR → 设计 → UC/TV）；G1 评审时核查设计对全部 UR 的覆盖。
- 优先级：M 必须 / S 应该 / C 可选。状态：全部 OPEN（待设计覆盖确认）。

| ID | 需求 | 优先级 | 设计落点 | 科学依据 | 关联用例 |
|:---|:---|:---|:---|:---|:---|
| UR-001 | 目标建模输入：以 YAML 提交「信号源＋背景＋透过率」参数化模型组合（`source` 必选，`background`/`transmission` 可选），支持层级继承与版本标识 | M | targets.md §4.4.1；interfaces §2.1.1 | 观测任务设计流程 | UC-1…5 |
| UR-002 | 参数扫描：`linspace`/`logspace`/`list` 三种网格定义，支撑观测策略与参数空间探索 | M | targets.md §3.3.1/§4.4.1；interfaces §2.1.1 | 观测规划 | UC-5 |
| UR-003 | 前向可观测输出：图像（2D/3D）、光谱、光变（偏振预留），由参数化模型直接生成 | M | targets.md §2.2/§4.1（TargetHistogram） | 观测模拟 | UC-1…4 |
| UR-004 | 单位与坐标语义：全部物理量带单位；坐标遵循天文标准（ICRS/SkyCoord）；距离、自行可表达 | M | data_model §2.2/§3 | astropy2022 | 全部 |
| UR-005 | 数据互操作：输出 FITS（WCS 完整＋关键头部元数据），可被 astropy 读取；观测层交换与 OIFITS 2 对齐 | M | targets.md §4.4.2；interfaces §2.2 | fits_standard40、greisen2002wcs、duvert2017oifits | UC-5 |
| UR-006 | 反演参数估计：MCMC / 嵌套采样 / 最大似然；输出拟合参数、后验摘要与不确定性 | M | targets.md §3.2.4/§4.3.2 | 模型参数约束方法 | UC-5 |
| UR-007 | 模型—数据一致性评估：χ²、残差、置信区间、AIC/BIC/贝叶斯因子与报告 | M | targets.md §3.2.4（Statistics Evaluator） | 统计推断惯例 | UC-1/3/5 |
| UR-008 | 背景各向异性建模：`is_isotropic=false` 时提供空间模型（多项式/查表等），支持黄道光类背景 | S | data_model §4/§9；ADR 0006 | 黄道光实测需求 | UC-4 |
| UR-009 | 消光/透过率建模：幂律消光与透过率曲线（表列或参数化）均可表达、可组合 | S | data_model §5 | 星际消光惯例 | UC-4 |
| UR-010 | 双星场景可用：点源/双星模型到可见度、闭合相位性质的链路可表达，支持观测设计 | M | 目标层模型侧 + 观测层接口对齐（观测层未立项） | monnier2003optical | UC-1 |
| UR-011 | 系外行星场景：凌星光变＋光谱组合模型可表达 | S | targets.md §2.2（光变/光谱） | 系外行星科学 | UC-2 |
| UR-012 | 任务级科学评估输入：支持 LIFE 类空间干涉任务探测良率评估所需的模型侧输入（目标 SED、背景/黄道光、透过率） | S | targets.md §1.1（需求二） | quanz2022life | UC-1/4 |
| UR-013 | 溯源：数据产品可追溯至输入模型与版本（MODEL_ID/version/溯源字段），支持结果复现 | M | data_model §6（`*_model_ref`）；targets.md §4.4.2 | 科学可重复性 | 全部 |
| UR-014 | 异步与大文件：任务异步化、哨兵就绪通知、大文件（GB 级）支持 | S | targets.md §3.3.1/§4.3.3 | 运维可靠性 | UC-5 |
| UR-015 | 错误与可用性：英文错误码/消息；任务状态可查询；结果可直接下载 | S | interfaces §3.3/§3.4 | 用户可用性 | 全部 |

**说明**

- UR-010/UR-012 的可见度/良率计算实际发生在观测量层；当前设计阶段以「模型侧输入可表达、层间接口对齐」为覆盖判据，观测量层详细需求待立项后补充。
- 需求变更须版本更新并附变更说明；G1 评审前需形成 UR→设计→UC/TV 追溯矩阵（`design/traceability/`）。
