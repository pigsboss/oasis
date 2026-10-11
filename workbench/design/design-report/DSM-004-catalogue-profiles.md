# DSM-004 目录画像与共性属性（M5 设计输入）

- 编号：DSM-004　版本：v0.1（供审查）　日期：2026-10-11　编制：设计开发
- 依据：用户要求"整理各类 catalogue 的共性属性"（2026-10-11）；服务目标：F-09 天区分片导出、F-10 HDF5 切片导出
- 方法：对本机在册数据集逐一实测（分片命名、表头形态、列族、校验清单、排序/分片键），不含推测

## 1. 属性分面（本研究采用的口径）

| 面 | 内容 |
|:--|:--|
| A 标识归属 | 稳定 ID、provider、licence（+URL） |
| B 版本时效 | version 语义（release tag / Last-Modified 快照）、epoch 语义（列 / 版本级 / 逐行）、更新节奏 |
| C 几何参考 | 角位置列（名称、单位、frame、历元） |
| D 主键粒度 | 主键列；一行=一对象 |
| E 物理量族 | 天测（ra/dec/视差）、运动（pm）、测光（星等）、刻画（Teff/类型等）、轨道根数 |
| F 形态布局 | 原生分片方案、容器/压缩、表头形态、分隔符 |
| G 规模排序 | 行数、分片数、排序键、覆盖 |
| H 质量校验 | 官方校验清单、摘要语义、说明/schema 文件 |
| I 用途定位 | 渲染 / 位置服务 / 模板 等 |

## 2. 逐目录速览（实测）

| 目录 | 主键 | 位置列 | 原生分片 | 形态 | 排序/分片键 | 官方校验 | 更新 | 量级 |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| Gaia DR3 `gaia_source` | `source_id` int64 | `ra/dec`（ICRS，`ref_epoch`=2016.0） | **3,386 片（source_id 区间）** | ECSV：`#` YAML 元数据块＋CSV 表头（~140 列） | source_id 升序 | `_MD5SUM.txt` | 静态发布 | ~702 GB |
| Gaia DR2 `gaia_source` | `source_id` int64 | `ra/dec`（ICRS，`ref_epoch`=2015.5） | **61,234 片（source_id 区间）** | CSV.gz 表头行（无 `#` 块） | source_id 升序 | `MD5SUM.txt` | 静态发布 | ~552 GB |
| TESS TIC v8 | `ID`（int） | `ra/dec`（J2000 近似）＋`pmRA/pmDEC` | **90 片（赤纬带，2° 步进）** | CSV.gz **无表头**（表头另附 `header.csv`＋列说明） | 赤纬带；片内按 ID | `md5sum.txt`（＋CTL） | 静态发布 | ~415 GB |
| WISE AllWISE | `designation`（Jhhmmss±ddmmss） | `ra/dec`（内部定序，bar 分隔） | **48 片（赤纬区间）** | ascii **bar 分隔、无表头** | 赤纬区间 | `*.bz2.md5.txt`（＋sizes） | 静态发布 | 747,634,026 行 / ~340 GB |
| 2MASS PSC | `designation`（hhmmss±ddmmss） | ra/dec（内部定序） | **92 片（天区码 aaa…bbi，沿赤纬推进）**＋scn/xsc | 定序 **pipe 分隔、无表头**；本地有 schema 文本 | 天区码 | 本地**无**官方清单（urls 有） | 静态发布 | ~41 GB |
| SEDs 模板库 | 模板名/类型 | **无角位置** | 单一 `tar.gz` | 46,124 个 `ascii.gz` 谱文件 | 目录分类 | 无 | 静态 | 6.7 GB |
| MPC `mpcorb` / `cometels` | packed `designation` | **无 ra/dec**（轨道根数） | 单文件 | 定宽文本（gz / txt） | 编号序 | 无（自算 sha256） | **日更** | 1,571,791 行 / 93.5 MB |
| 【派生】`gaia_t1/t2/t3` | `source_id` | `ra/dec`（ICRS，J2016.0） | 无（单件 + 分档） | CSV.gz（10 列，表头行）＋HDF5 rendition | source_id 升序 | manifest sha256 | 按需重导 | ≤236 MB |
| 【派生】`mpc_elements` | packed `designation` | **无**（根数＋逐行 epoch） | 无 | CSV.gz（20 列）＋HDF5 rendition | 原文件序 | manifest sha256 | 随 MPC | 93 MB |

## 3. 共性属性（分三级）

**① 全体共性（8/8）**
1. 有稳定**主键**（int64 ID / designation / 模板名）；
2. 有**归属三元组**：provider、licence（+URL）、版本语义；
3. 以**行式对象**组织，一行=一实体（对象或模板）；
4. 有（官方或自算的）**完整性校验**入口，且与**说明类文件**（README/schema/列说明）同封装；
5. 发布形态为**静态快照**或**可检测的滚动快照**（Last-Modified）。

**② 对象型星表共性（Gaia×2 / TIC / WISE / 2MASS / MPC）**
1. **"定位二选一"齐备**：五张位置星表全部含 ra/dec；MPC 以轨道根数定位（含逐行 epoch）；
2. 至少一族**测光量**（或根数+绝对星等 H），可做门限筛选；
3. **原生分片**普遍存在——要么按主键区间（Gaia），要么按赤纬/天区（TIC/WISE/2MASS）；
4. 历元语义可声明（列 / 版本级 / 逐行）。

**③ 例外（设计需显式容纳）**
- SEDs 模板库：**非对象型**——无位置、无天区语义、无分片（tar 内按类型分目录）；
- MPC：无 ra/dec（其"天区筛选"需先做位置传播）；
- 2MASS：本地无官方校验清单（urls 可回源）；WISE/2MASS 无表头，列序由 schema 决定。

## 4. 差异要点（对导出设计关键）

| 维度 | 现状差异 | 设计含义 |
|:--|:--|:--|
| 位置列 | `ra/dec`（Gaia/TIC）／内部定序（WISE/2MASS）／无（MPC、SEDs） | 需要**列映射（profile）**而非硬编码列名 |
| 原生分片 | source_id 区间（Gaia×2）／赤纬带（TIC 2°、WISE 48、2MASS 天区码） | 天区导出可做**原生分片透传**（选片免全扫）；Gaia 只能全扫 |
| 排序键 | source_id／ID／designation／packed designation | HDF5 **索引键=排序键**，随 profile 声明 |
| epoch | 列（ref_epoch 2016.0/2015.5）／版本级（TIC/WISE/2MASS 合并历元≈J2000）／逐行（MPC） | manifest 的 epoch/frame 应随 profile 一般化（Gaia 交付已实践） |
| 表头形态 | ECSV 元数据块／CSV 头行／独立 header 文件／无表头 | 解析入口需按 profile 取列名 |
| 更新节奏 | 静态（多数）／日更（MPC） | 导出物 manifest 记录快照来源即可 |
| 校验 | 官方 md5（Gaia/TESS/WISE）／无（2MASS/MPC） | verify 能力按"官方优先、自算兜底" |

## 5. 对 M5 设计的直接含义（建议）

1. **profile 作为一等配置**：建议在 inventory `fmt` 增可选 `profile` 块——
   `positions: [ra, dec]`、`id_key`、`sort_key`、`native_shard: none|id_range|dec_band|sky_code`、
   `epoch: {mode: column|global|per_row, ref?}`、`delimiter/header`——导出算子一律读 profile；
2. **天区算子分层**：小表全扫；大表借原生分片（TIC/WISE/2MASS 选片；Gaia 全扫 3,386 片 ≈ 分钟级）；
3. **分片输出两种模式**：`healpix`（重分片）与 `native`（顺原生分片切割透传）；
4. **HDF5 索引键=排序键**；天区查询在 ≤ 百万行规模全扫即可，更大表再上空间索引；
5. epoch/frame 随 profile 写入 manifest（把 Gaia 交付的做法一般化）。

## 6. 结论与设计裁决（据用户分析，2026-10-11）

**裁决一：目标层不做跨目录"合并/融合"导出。** 理由（由 §3/§4 证据支持）：
- **共性稀薄 → 信息衰减**：可合并列集近似只有 {主键、ra/dec、单一测光量、版本/许可}；合并表必然落入
  两难——"宽而空"（超集模式，绝大多数列为 NULL）或"窄而残"（交集模式，丢列：WISE 定序无表头、
  TIC 刻画列、MPC 逐行 epoch 均不可无损承载）；
- **交叉证认代价高**：确定同一源在不同目录的 ID 需位置交叉（含历元/自行传播、误差椭球、N×N 规模）
  或依赖官方交叉表；本地文件多数**不含**跨目录 ID 列（例外：TIC 内嵌 `GAIA`/`TWOMASS`/`ALLWISE` 列）。

**裁决二：联合价值的正解 = "同域平行切片"（co-spatial parallel slicing）。** 不做融合，而是
一次条件（天区/门限/列选择）应用到多个目录，各自按**原生 schema** 出片，随同一组 manifest
（共享选择几何与 epoch/frame 标注）——消费侧按需自行 join；需要交叉证认时，优先用目录内嵌 ID
（如 TIC），否则走官方 cross-match 服务，**不在目标层自造**。

**边界**：交叉证认、跨目录合并、天体位置传播均不属目标层职责；如同一目录内嵌 ID 缺失且消费侧
确有交叉需求，按"另行立项"处理。

*（拟纳入 M5 范围：`同域平行切片`——多 source、同 region 参数的组导出；对 F-09 的小扩展，待用户审定。）*

**裁决三（用户方向，2026-10-11）：固化优先（solidify-first）。**
任一目录（任意格式）先**一次性固化为 HDF5 表**（profile 驱动解析 → 复合表：列名齐备、
chunked＋压缩、attrs 携 epoch/frame/provider/profile），此后**导出即"天区条件 × 属性列表"二维查询**；
原型实测（Gaia T2，177,426 行；验证栈 PyTables）：固化 1.5 s / 11.9 MB；区间索引 0.2 s；
锥面 2°×5 属性 0.12 s；矩形条件 0.12 s。分片输出（healpix 重分片 / native 透传）保留为
**输出组织选项**，不再是核心路径。

- F-09/F-10 含义收敛：F-10 的 HDF5 由"可选 rendition"升级为**固化中间态**（导出的一等输入）；
  F-09 的天区维度 = 固化表上的条件查询（锥面可用解析式或格子化列）。

**裁决四（用户，2026-10-11）：固化产物跟随应用工作区。**
不设全局 core 目录；固化/导出产物物化到**发起应用的工作区**（哪个应用需要就放哪个），
manifest 记录来源（catalogue/快照）与用途；重生成按需，生命周期归该应用。

**裁决五（2026-10-11 定稿：用户裁定）。应用侧 catalogue 固化采用 PyTables。**
定位上，固化产物是**应用工作区内、可再生的工作副本**（非档案母本）——PyTables 的
`read_where`／CSI／表语义恰好服务应用侧的"天区×属性"查询与切片；"层维护风险"在这一
定位下不构成问题：母本永远是 CSV.gz／原始件，固化可随时重建（实测 17.7 万行 1.5 s）。
**分级（最终）**：交付锚点＝CSV.gz；可移植 rendition＝通用 HDF5（h5py，维持现状）；
应用侧固化＝PyTables（条件表达式、CSI、blosc）。**不引用 `~/Projects/tabio`**。

**附：既往项目扫描佐证（2026-10-11，`~/Projects` 全扫）**：纯 h5py＝`multistagecophasing`、`oasis`；
纯 PyTables＝`astrotoys`、`neosurvey`、`cosmos`、`pymath`；混合＝`hassdas`、`hxmtevmva`、`pimms`、
`tabio`、`_archives/syndd`（其中"数据产品封装用 h5py、分析内核用 PyTables"的分工反复出现）；
`primer` 为假阳性（自带 LaTeX 表格模块）。全仓无 C/C++ `hdf5`、无 `HDF5.jl`、无 pandas `to_hdf`、
无 netCDF4/xarray 通道。

**裁决六（用户，2026-10-11）：定位定名 = "Consolidate（整合）"，语义对标 Final Cut Pro。**

- **长期支持责任在 dataset 的发布渠道**（上游档案/服务）；本层**零档案责任**——本地一切
  HDF5/CSV 都是从渠道可重建的工作态；manifest 记 source channel + version/epoch，
  保证**可重建、可校验**；
- 应用侧唯一硬指标 = **性能**（查询/切片）；技术栈因此选 PyTables（裁决五）；
- **consolidate 两档**：
  ① **整目录整合**（默认）：catalogue → 应用工作区 PyTables（列名齐备、CSI、blosc），
     供该应用反复查询；② **裁剪整合**（给"天区 × 属性"参数）：仅收拢选定子集——
     即 F-09/F-10 的导出用例，两种表述合并为同一机制；
- 对标关系：master＝发布渠道；project＝应用；consolidate＝应用工作区内的自足工作集
  （可删、可重建；母本不受触碰）。

**裁决七（用户，2026-10-11）：生态两平面与 kernels 归属。**

- 生态命名：**深空探测与空间科学任务的数字孪生底座**；其中 **OASIS＝资产/供应平面**
  （datasets 源表 ＋ kernels 底座），**multistagecophasing＝仿真/设计平面**（应用侧消费）；
- **kernels 的管理与供应归 OASIS**（注册/取件/校验/投送）；**消费规范归各应用**
  （MCPC ADR-001 继续有效）；副本"跟随应用工作区"（MCPC 的 `spice_kernels/` 即首个应用副本样板）；
- 存储面（用户，2026-10-11）：**`Datasets` 目录 ≠ source catalogue**——它按"来源/类别"命名收纳
  各类数据资产（Gaia／TESS／WISE／2MASS／ESO Public／GDR2 Products／GPS Data／…）；
  **kernels store 亦收纳于其中**：`/Volumes/ArecaStudio/Datasets/SPICE Kernels/<category>/`；
  清单语义不变（inventory＝发布型 catalogue；kernels＝平行注册）；
- 实现（已交付）：`~/.config/oasis/kernels.yaml`（平行注册）＋ store
  `/Volumes/ArecaStudio/Datasets/SPICE Kernels/<category>/` ＋ CLI `kernels list|verify|fetch|send --app`
  （并行 Range＋续传复用 mirror；`--proxy` 支持）；`send` 产出 `<app>/spice_kernels/oasis-manifest.json`；
- 首件登记与验证：**de442**、**de440**（对 JPL `aa_checksums.txt` 官方 md5 逐位一致）、**naif0012**、
  **pck00011**（对 NAIF 现行文件重下载比对一致）；**de441**（3.3 GB）已取件并登记 sha256；
- 网络注记：JPL/NAIF 文件下载在本网络需 `HTTPS_PROXY=http://127.0.0.1:7897`
  （实测：主站 200、Horizons API、DE/SPICE 目录与取件均通；`ssd-api` 直连可达）。
