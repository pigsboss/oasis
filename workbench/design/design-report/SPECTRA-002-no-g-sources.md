# SPECTRA-002：缺 G 源分类与有限数据光谱推断

- 日期：2026-11-24
- 数据：Gaia DR3 `gaia_source` 全量 152 列；1,811,709,771 行
- 关联：SPECTRA-001、`no_g_supp.h5`、`spectral-cube v2`

## 1. 结论

缺 G 不是“星等暂时为空”，而是**G 波段观测次数为 0**：

```text
phot_g_n_obs = 0
phot_g_mean_flux = NaN
```

这些源没有 Gaia G 流量，不能用 Gaia 内部数据恢复 G。它们不是完全无测光：

- 70.5% 有 RP；
- 29.5% 在 G/BP/RP 三个宽带内没有可用测光；
- XP continuous 仅 175 个，XP sampled 为 0；
- GSP-Phot Teff 仅 7,577 个；
- 分类概率很高，可判断恒星/QSO/星系。

## 2. 全量统计

```text
缺 G 总数        5,455,339 / 1,811,709,771 = 0.301%
phot_g_n_obs=0   5,455,339（全部）
RP 有效          3,848,128（70.5%）
BP 有效              5,309（0.10%）
无 G/RP/BP       1,602,051（29.4%）
```

按测光组：

| 组 | 数量 | 说明 |
|:--|--:|:--|
| `rp_only` | 3,847,979 | 有 RP，无 G/BP |
| `rp_bp` | 149 | 有 RP/BP，无 G（极少） |
| `bp_only` | 5,160 | 有 BP，无 G/RP |
| `no_phot` | 1,602,051 | G/BP/RP 均无 |

## 3. DSC 统计分类

使用 Gaia `classprob_dsc_combmod_*` 的三类概率取最大值：

| 类型 | 数量 | 占比 |
|:--|--:|--:|
| star | 4,800,154 | 87.99% |
| quasar | 33,560 | 0.62% |
| galaxy | 48,203 | 0.88% |
| unknown | 573,422 | 10.51% |

分类置信度：

| 类型 | 中位概率 | P90 |
|:--|--:|--:|
| star | 0.99948 | 0.999997 |
| quasar | 0.90623 | 0.99961 |
| galaxy | 0.98831 | 0.999999 |

分类 × 测光组：

| 类型 | RP-only | BP-only | 无宽带 |
|:--|--:|--:|--:|
| star | 3,673,420 | 4,531 | 1,122,086 |
| quasar | 14,131 | 137 | 19,291 |
| galaxy | 22,814 | 8 | 25,381 |

## 4. 有限数据光谱推断

### 4.1 有 RP（3.85M）

用统计/模板回退：

- star / binary / unknown：估计 `G-RP` 与 `BP-RP`，取黑体模板；
- quasar：蓝类模板（BP-RP≈0.3）；
- galaxy：红类模板（BP-RP≈0.8）；
- 以 RP 定标亮度；
- 标记 `quality=5`（RP-only stellar）或 `6`（class template）。

这是**统计推断**，不是实测光谱；颜色和亮度均可能偏差。

### 4.2 无 G/BP/RP（1.60M）

- 没有宽带测光，无法可靠确定视亮度；
- 当前立方仍计入 `count`，但 `flux=0`，`quality=7`；
- 需要 2MASS/AllWISE/Pan-STARRS/SDSS 等外部测光才有机会补亮度；
- 不应伪造光谱。

### 4.3 XP/AP 的作用

- 缺 G 源中没有 XP sampled；continuous 仅 175；
- GSP-Phot Teff 仅 7,577；
- 因此 XP/AP 对这批源帮助很小；XP 主要服务正常有 G/BP/RP 的源。

## 5. 立方更新

`spectral-cube` v2 使用 `no_g_supp.h5`：

```text
/spectra/count            总源数
/spectra/count_normal     G+BP-RP 正常黑体
/spectra/count_rp_only    RP-only 恒星回退
/spectra/count_class      QSO/galaxy 类模板
/spectra/count_no_phot    无宽带（零 flux）
/spectra/quality          4/5/6/7
```

输出：

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/gaia_dr3_spectral_n2048_v2.h5
```

验收要求：

- shape `(50,331,648, 343)`；
- count 和 1,811,709,771；
- flux finite；
- count_normal + count_rp_only + count_class + count_no_phot = count；
- quality 覆盖 4/5/6/7；
- meta 记录 `model=blackbody_bp_rp_v2` 和 `no_g_supp`。

## 6. 风险

- 分类概率是 Gaia DSC 模型输出，不是直接目标类型；
- RP-only 的 G/颜色是统计估计；
- 无宽带源没有可靠亮度，零 flux 是明确掩膜，不是观测为零；
- 后续应接入外部 NIR/光学测光，并把 `quality=7` 源单独处理。
