# UR 清单 · 用户需求（oasis 源表管理）

> 提交方：深空任务建模仿真可视化（用户）｜日期 2026-10-12｜版本 v0.1｜对应提交函 `00_提交函.md`
> **字段口径参考**：Gaia 列名以官方 `gdr3_csv_header.txt`（`gaia_source` ECSV 头）为准；太阳系天体以 MPC 现行根数口径为准。

| # | 需求 | 理由 | 验收判据 |
|---|---|---|---|
| **UR-OASIS-01** | **源表覆盖·恒星**：Gaia DR3 `gaia_source` 的**分档子集**（T1 `G≤6`／T2 `G≤9`／T3 `G≤12`，可天区分片） | 星空生成器唯一输入；全量 ~1.8×10⁹ 行不可用 | 三档齐；行数与门限一致；可复现 |
| **UR-OASIS-02** | **源表覆盖·小天体**：MPC 轨道根数（`a,e,i,Ω,ω,M`〔或 `Tp`〕＋`epoch`＋`H`；类别 MBA／NEO／centaur／TNO） | 位置服务与"真实天体"插图 | 字段齐；`epoch` 明确；类别可筛 |
| **UR-OASIS-03** | **字段补充（恒星）**：`parallax`／`pmra`／`pmdec`／`phot_g_mean_mag`／`bp_rp`（或 `teff`）／`source_id` | 现 Target 模型只有 `ra/dec/distance`，无视差与测光，**星表进不来** | 字段在 Target 件中可携带 |
| **UR-OASIS-04** | **字段补充（通用）**：`epoch` 与 `frame` | 位置与自行的时标必须显式（现仅 ICRS 语义） | 每件含 epoch/frame |
| **UR-OASIS-05** | **`DynamicalModel`**（太阳系天体）：`epoch`＋轨道根数＋`H`；并支持**位置快照序列** | 现 T 层示例仅恒星/双星/系外行星/AGN/黄道光，**无太阳系天体** | 能表达某小行星在给定时刻的位置 |
| **UR-OASIS-06** | **派生量口径**：`distance = 1000/parallax`（mas→pc）；测光→`spectral_model` 的映射规则（或**保留原始字段**） | 消费端需稳定口径；测光**不得**入 `metadata`（其 schema 禁止） | 口径写入交付说明 |
| **UR-OASIS-07** | **交付形态**：**批量导出**（现契约"一星一文件"不可行）＋**manifest** ＋ 版本号 | 百万级恒星不可能一文件一星 | manifest 可逐条校验；批量目录约定 |
| **UR-OASIS-08** | **溯源与许可**：逐件登记 `provider`／DOI／许可条款（Gaia 条款、MPC 条款）并**随交付携带** | 用户入库须登记 credits | 交付含出处字段 |
| **UR-OASIS-09** | **导出消费约定**：目录结构＋命名＋版本；用户按 manifest 消费，**不改 schema** | 避免两端各自造格式 | 一条命令可导入并校验 |

## 用户验收判据（收到即验）

1. manifest 行数／门限／字段 与声明一致；
2. 抽样若干条，坐标与星等**可回溯**到官方源（Gaia Archive／MPC）；
3. `epoch`／`frame` 明确无缺；
4. 许可与出处可查；
5. **同版本重复交付可复现**（内容一致）。
