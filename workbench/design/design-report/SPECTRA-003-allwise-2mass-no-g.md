# SPECTRA-003：AllWISE / 2MASS 对缺 G 源的可用性

- 日期：2026-11-24
- 本地数据：`/mnt/data/huo/Datasets/WISE`（48 个 AllWISE 分区）、`/mnt/data/huo/Datasets/2MASS`（92 个 PSC 文件）
- 关联：SPECTRA-002

## 1. 结论

**可用于补充一部分缺 G 源，但不能单独解决全部缺 G 源。**

在银河面附近一个测试天区（dec −1.50°…0.70°）抽取 5,000 个缺 G 源：

| 项目 | 数量 | 比例 |
|:--|--:|--:|
| 样本 | 5,000 | 100% |
| AllWISE 3″ 内匹配 | 1,006 | 20.1% |
| 2MASS 3″ 内匹配 | 1,659 | 33.2% |
| 任一 NIR 匹配 | **1,985** | **39.7%** |
| 无 NIR 匹配 | 3,015 | 60.3% |

按缺 G 子类：

| 子类 | 样本 | AllWISE | 2MASS | 任一 |
|:--|--:|--:|--:|--:|
| RP-only | 4,123 | 799 | 1,274 | **1,581（38.3%）** |
| 无 G/BP/RP | 876 | 206 | 385 | **403（46.0%）** |

2MASS 在这个天区比 AllWISE 覆盖更好；两者并集约 **40%**，但仍然有 **60% 没有 NIR 对应体**。

## 2. 数据与方法

- AllWISE：`wise-allwise-cat-part25.bz2`，dec −1.86°…0.75°，13,148,109 条；
  RA/Dec 取字段 2/3，W1/W2 取字段 17/21（1-based）。
- 2MASS：`psc_ace.gz`、`psc_baa.gz`，共 7,031,172 条；
  RA/Dec 取字段 1/2，J/H/K 取字段 7/11/15。
- 缺 G 样本来自 `no_g_supp.h5`；
- 最近邻匹配半径 **3″**，用球面角距；
- 测试天区为 Galactic plane 附近，不代表全天。

## 3. 解释

### 3.1 NIR 能提供什么

- J/H/K、W1/W2 光度；
- 近红外颜色（J−K、W1−W2）可约束 Teff、消光、星族；
- 对 RP-only 源，NIR 可帮助估计 G/颜色；
- 对无 G/BP/RP 源，NIR 至少给出一个 NIR SED，但**不能恢复 Gaia G 或 BP**。

### 3.2 NIR 不能提供什么

- 不能直接恢复 Gaia G 波段星等；
- 不能恢复 BP；
- 不能唯一确定光谱；
- 对 60% 无 NIR 对应的源完全无帮助。

### 3.3 建议的融合策略

1. 对 3.85M RP-only：优先用 RP + JHK/W1W2；
2. 对 1.60M 无 G/BP/RP：用 NIR 检测者建立 NIR-only 类模板，标记 `quality=6/7`；
3. NIR 无对应体：保持 `count>0, flux=0` 或掩膜；
4. 不应把 AllWISE/2MASS 匹配当作 Gaia G 的替代。

## 4. 局限

- 只测了一个 Galactic-plane 天区；全天覆盖率会随经纬度/消光变化；
- 3″ 匹配受星表分辨率、crowding、proper motion 影响；
- AllWISE/2MASS 星等极限远高于 Gaia RP 中位数（RP≈19.3）；
- 2MASS/AllWISE 的 NIR 颜色不能直接替代光学 CIE 颜色；
- 未对 5.45M 全量做最近邻；本报告是可行性抽样。

## 5. 结论与下一步

- **AllWISE + 2MASS 并集可补充约 40% 的本测试天区缺 G 源**；
- **不能解决全部无 G 源**；60% 仍需更深光学/近红外巡天（Pan-STARRS、DES、LSST 等）；
- 下一步：对全量 no-G 建 HEALPix 索引，做 AllWISE/2MASS 最近邻，生成 `nir_supp.h5`；
- 对 NIR 匹配源联合 RP/NIR 做统计光谱拟合，仍标 `inferred`。
