# Gaia DR3 源表光谱信息分级（A–G）

- 版本：v1.0
- 日期：2026-11-24
- 适用范围：OASIS targets 层 Gaia DR3 源表、consolidate 产品、光谱立方与真彩色产品
- 关联：ADR-0009、DSM-004、SPECTRA-001～006

## 1. 目的

Gaia DR3 源表的光谱信息不是单一等级：同一张 `gaia_source` 中，有的源有 XP 实测谱，
有的只有 G/BP/RP 多波段测光，有的缺 G 但仍有 RP 或外部 NIR 测光，还有的只有分类先验甚至没有任何测光。

OASIS 必须用**互斥、可追溯的等级**描述“这个源的光谱是怎么来的”，禁止把所有源都当作同一种
`spectral_model`，也禁止对无测光源伪造通量。

## 2. A–G 分级

| 等级 | 数据条件 | 推荐光谱 | 通量锚点 | 可信度 |
|:--|:--|:--|:--|:--|
| **A** | 有实测 `xp_sampled` 343 点 | 直接用实测谱 | XP 外部标定 | 最高 |
| **B** | 有 `xp_continuous` 110 系数，无 sampled | GaiaXPy 重建 343 点 | XP 外部标定 | 高 |
| **C** | 有 ≥3 个独立波段，含光学（典型 G+BP+RP） | 模板/合成谱拟合 | G 或组合通量 | 中高 |
| **D** | 有 1–2 个波段 + 颜色/Teff 约束（典型 RP + NIR，或 G + 一个颜色） | 模板或等效黑体 + 经验颜色 | RP/NIR/G | 中低 |
| **E** | 只有单波段（RP-only 或 NIR-only） | RP-only / NIR-only 类模板 | 该单波段 | 低 |
| **F** | 无测光，但有 DSC 分类概率 | class prior 光谱形状 | **无可靠通量** | 很低 |
| **G** | 无测光、无分类 | 不生成光谱 | 无 | 掩膜 |

### 关键边界

- **等效黑体不是等级**；它是 C/D 级中的一种 fallback 模型；
- **F 级不得进入通量立方**：没有测光就没有可靠视亮度，只保留 count/分类先验；
- **G 级直接 mask**；
- A/B 是实测/实测重建；C/D/E 是模型推断；F/G 是分类/无信息；
- 单波段 RP-only 与单波段 NIR-only 都归 E，但 `spectral_source` 必须区分
  `rp_only` / `nir_only`。

## 3. 判定决策树

```text
has_xp_sampled
  → A

else has_xp_continuous
  → B

else n_optical_bands >= 3 或 (G + BP + RP)
  → C

else (RP + NIR) 或 (G + 一个颜色) 或 (Teff + 通量锚点)
  → D

else 只有 RP，或只有 NIR（JHK/W1W2）
  → E

else 无测光但 classprob 有效
  → F

else
  → G
```

判定必须按源逐一进行，不能用一个目录级标签覆盖整张表。

## 4. 缺 G 源的映射

Gaia DR3 全量 1,811,709,771 源中，缺 G 源 **5,455,339（0.301%）**；
它们 `phot_g_n_obs=0`、`phot_g_mean_flux=NaN`，不是“平均星等暂时为空”。

### 4.1 测光子类

| 子类 | 数量 | 判定 |
|:--|--:|:--|
| 有 RP，无 G/BP | 3,847,979 | RP-only → D/E |
| 有 RP/BP，无 G | 149 | D |
| 有 BP，无 G/RP | 5,160 | E/D |
| 无 G/BP/RP | 1,602,051 | 依 NIR/分类 → D/E/F/G |

### 4.2 与 AllWISE/2MASS 联合后

| 子类 | 数量 | 等级 |
|:--|--:|:--|
| RP + NIR | 1,306,795 | D |
| RP，无 NIR | 2,541,184 | E |
| 无 G/BP/RP + NIR | 686,110 | D/E |
| 无 G/BP/RP，无 NIR | 约 915,941 | F（有分类）/ G（无分类） |

全量 NIR 并集覆盖 **1,993,910 / 5,455,339 = 36.55%**；
其中 **738,863** 个源同时被 2MASS 与 AllWISE 证认。

### 4.3 分类的作用

DSC `classprob_dsc_combmod_*` 只决定“可能是什么”，不提供通量：

- galaxy 类 NIR 匹配率约 96.3%；
- quasar 约 67.6%；
- star 约 36.0%；
- unknown 约 34.0%。

分类可用于选模板/先验，但不能把 F 级提升为有通量的光谱。

## 5. 源级字段

建议在 consolidated 表或 side table 中记录：

```text
spectral_tier        A|B|C|D|E|F|G
spectral_source      xp_sampled|xp_continuous|template|blackbody|rp_only|nir_only|class_prior|none
spectral_model       BT-Settl/PHOENIX/MARCS/blackbody/QSO/galaxy/...
inferred             bool
n_bands              int
flux_anchor          G|RP|JHK|W1W2|none
xp_fraction          float
class_code           DSC argmax（star/quasar/galaxy/unknown）
class_prob           DSC 最大概率
nir_2mass / nir_wise bool
sep_2mass / sep_wise arcsec
```

`A/B` 的 `inferred` 为 false（或 `measured_reconstructed`）；
`C/D/E` 为 true；`F/G` 不进入通量产品。

## 6. 图级字段

对 HEALPix 光谱立方：

```text
/spectra/tier_counts      int64[npix, 7]  # A..G
/spectra/xp_fraction      float32[npix]
/spectra/inferred_fraction float32[npix]
/spectra/quality          uint8[npix]     # 映射见下
/spectra/count_*          int64[npix]
```

像素 `quality` 取该像素中**最差**的源等级（G 最差），或按通量加权另存质量层；
两者必须明确，不可混用。

v3 已采用 A–G 数值码：

```text
0=A, 1=B, 2=C, 3=D, 4=E, 5=F, 6=G
255 = 空像素
```

v3 全量统计：

```text
A          0
B          0
C  1,540,770,340
D    267,478,000
E      2,541,258
F        641,979
G        278,194
合计 1,811,709,771
```

A/B 为 0：本轮 v3 尚未把 XP sampled 表接入立方；正常 G 源归 C，
缺 G 源按 NIR/RP/分类归 D/E/F/G。

## 7. 与现有产品的对应

| 产品 | 说明 |
|:--|:--|
| `gaia_dr3_core_spatial.h5` | 1.811B 行 core 14 列 |
| `no_g_supp.h5` | 5.45M 缺 G 源 flags/class/RP |
| `nir_supp.h5` | 5.45M 源 + 2MASS JHK + AllWISE W1–W4 + 匹配质量 |
| `gaia_dr3_spectral_n2048_v3.h5` | v3 A–G tiered；tier_counts + quality；67 GiB |
| `gaia_dr3_spectral_n2048_v2.h5` | v2 数值 quality 4/5/6/7（历史产品） |
| XP sampled 镜像 | 107 GB，3386/3386 MD5 OK |
| XP summary 镜像 | 9.2 GB，3386/3386 MD5 OK |

## 8. 硬性约束

1. **不许**把 F 级（无测光）源以单位通量写入光谱立方；
2. **不许**把等效黑体作为 A/B 实测谱；
3. **必须**记录 `spectral_tier`、`spectral_source`、`inferred`；
4. **必须**传播 `xp_fraction` 和 NIR 匹配质量；
5. **A/B** 可直接用于真彩色；C/D/E 是模型颜色；F/G 不得当作正常颜色；
6. **D/E** 的模型必须标注模板/黑体及参数来源；
7. 像素级质量与源级分级必须可追溯。

## 9. 实施顺序

1. 为 consolidated/side table 增加 A–G 字段；
2. 对 5.45M 缺 G 源按本文决策树打标；
3. 更新 v3 立方的 `tier_counts`/`quality`；
4. 对 A/B 源用 XP 实测谱替换黑体；
5. 对 D/E 源使用 NIR/RP 模板；
6. F/G 保持 count/mask，不赋 flux。
