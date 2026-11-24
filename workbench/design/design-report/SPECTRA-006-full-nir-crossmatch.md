# SPECTRA-006：缺 G 源全量 AllWISE/2MASS 交叉证认

- 日期：2026-11-24
- 输入：
  - `no_g_supp.h5`：5,455,339 个缺 G 源
  - `2MASS.h5`：470,992,970 行 compact
  - `WISE.h5`：747,634,026 行 compact
- 方法：3″ 最近邻，单位球 3D cell 索引，向量化查询
- 输出：`no_g_2mass_matches.h5`、`no_g_wise_matches.h5`、`nir_supp.h5`

## 1. 全量结果

| 项目 | 数量 | 占 5.45M |
|:--|--:|--:|
| 2MASS 匹配 | 1,748,833 | 32.06% |
| AllWISE 匹配 | 983,940 | 18.03% |
| **并集** | **1,993,910** | **36.55%** |
| 两表都匹配 | 738,863 | 13.54% |
| 仅 2MASS | 1,009,970 | 18.51% |
| 仅 AllWISE | 245,077 | 4.49% |
| 两者都无 | 3,461,429 | 63.45% |

## 2. 按缺 G 子类

| 子类 | 样本 | 2MASS | WISE | 并集 |
|:--|--:|--:|--:|--:|
| RP-only | 3,847,979 | 1,090,358（28.3%） | 661,882（17.2%） | **1,306,795（34.0%）** |
| 无 G/BP/RP | 1,602,051 | 657,632（41.0%） | 321,383（20.1%） | **686,110（42.8%）** |

## 3. 按 DSC 分类

| 类型 | 样本 | 2MASS | WISE | 并集 |
|:--|--:|--:|--:|--:|
| star | 4,800,154 | 1,499,303（31.2%） | 841,802（17.5%） | 1,729,681（36.0%） |
| quasar | 33,560 | 21,851（65.1%） | 13,356（39.8%） | 22,690（67.6%） |
| galaxy | 48,203 | 46,114（95.7%） | 36,720（76.2%） | 46,416（96.3%） |
| unknown | 573,422 | 181,565（31.7%） | 92,062（16.1%） | 195,123（34.0%） |

## 4. 匹配质量

| 匹配 | 中位 separation | P95 |
|:--|--:|--:|
| 2MASS | 1.52″ | 2.87″ |
| AllWISE | 1.55″ | 2.87″ |
| 两表均匹配 | 1.59″ | 2.84″ |

NIR 颜色中位数：

```text
2MASS J-H = 0.766
2MASS H-K = 0.300
AllWISE W1-W2 = -0.116
```

## 5. 产物

```text
/mnt/data/huo/Datasets/Gaia/gdr3/consolidated/no_g_2mass_matches.h5
/mnt/data/huo/Datasets/Gaia/gdr3/consolidated/no_g_wise_matches.h5
/mnt/data/huo/Datasets/Gaia/gdr3/consolidated/nir_supp.h5
```

`nir_supp.h5` 约 513 MB，5,455,339 行，含：

```text
source_id, ra, dec, rp_mag, class_code, class_prob,
match_2mass, sep_2mass, j_m, h_m, k_m, j_msigcom, h_msigcom, k_msigcom,
match_wise, sep_wise, w1mpro, w2mpro, w3mpro, w4mpro, w1sigmpro, w2sigmpro
```

## 6. 结论

- 全量并集覆盖 **36.55%**，与抽样研究（约 40%）一致；
- 2MASS 覆盖明显好于 AllWISE；
- **738,863 个源在两张独立 NIR 星表中都有对应体**，可做交叉验证；
- 无 G/BP/RP 子类的 NIR 并集覆盖率反而更高（42.8%），说明这些源很多是 NIR 亮的拥挤/特殊源；
- galaxy 类匹配率 **96.3%**，quasar 67.6%，恒星 36.0%；
- 仍有 **63.45%** 无 3″ NIR 对应体，需要更深巡天或保持 mask。

## 7. 注意

- 3″ 半径在银道面高密度区存在偶然匹配；
- 2MASS/AllWISE 位置和历元不同，未做 proper-motion 修正；
- DSC classprob 是统计分类，不是真实标签；
- NIR 只能提供 JHK/W1W2，不能恢复 Gaia G/BP；
- 下一阶段应把 `nir_supp.h5` 接入光谱推断，更新 v3 立方。
