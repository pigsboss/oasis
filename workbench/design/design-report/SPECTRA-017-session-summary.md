# SPECTRA-017：源表固化、交叉证认、光谱填充与 CIE 成像会话总结

- 日期：2026-11-25
- 范围：OASIS `oasis_datasets` 的 Gaia 源表处理、外部 NIR 星表、343 点光谱立方、简单成像装置/人眼 CIE 模拟
- 结论：形成一条可复现链路
  **源表 consolidate → 跨表交叉证认 → A–G 光谱信息分级 → 343 点立方 → PSF/CIE/显示映射 → cubemap HTML5 查看器**

---

## 1. 总体设计

### 1.1 数据分层

```text
原始源表（Gaia ECSV / AllWISE bz2 / 2MASS gz）
        ↓ consolidate（profile + schema + QC + manifest）
PyTables 固化表（CSR 或 spatial）
        ↓ crossmatch（3D 单位球网格 + 向量化最近邻）
匹配表 / nir_supp.h5
        ↓ A–G tier 分配 + 光谱模型填充
343 点光谱立方（HEALPix nside=2048）
        ↓ CIE 1931 + PSF + tone/encode
全天图 / Mollweide / cubemap / HTML5 查看器
```

### 1.2 关键原则

1. **源表先固化**，不在每次渲染时重解析 CSV；
2. **全量和紧凑两种 profile**，NIR 交叉证认优先 compact；
3. **ID 不硬编码为 `source_id`**，由 profile 的 `id_key` 决定；
4. **无测光源不得伪造通量**；
5. **TIFF 作为线性 CIE 位图存档，不参与显示 tone mapping**；
6. **直接查看格式才做显示 gamma、blur、PSF、Reinhard**；
7. **立方体像元不是恒星点源**，恒星 PSF 必须源级渲染。

---

## 2. 源表 consolidate

### 2.1 Gaia DR3

- 全量 `gaia_source`：1,811,709,771 行；
- 固化核心表：`gaia_dr3_core_spatial.h5`，377 GB；
- 核心 14 列，spatial/ipix 排序，`source_id` CSI；
- 另有 `no_g_supp.h5`：5,455,339 个缺 G 源，含 flags、DSC 分类、RP。

### 2.2 AllWISE / 2MASS

新增 profile：

| profile | 模式 | 列数 |
|:--|:--|--:|
| `allwise_psc` | 全量 | 298 |
| `allwise_nir` | compact | 36 |
| `twomass_psc` | 全量 | 60 |
| `twomass_nir` | compact | 17 |

实际 compact 产品：

| 表 | 行数 | 列 | 行宽 | 文件 |
|:--|--:|--:|--:|--:|
| 2MASS | 470,992,970 | 18（含 ipix） | 86 B | 42 GB |
| AllWISE | 747,634,026 | 37（含 ipix） | 228 B | 165–176 GB |

2MASS QC 96/96 通过；NIR 字符串 ID 后续改为跳过全表 QC 扫描。

### 2.3 本阶段修复

- compact profile 的 `f8/f4/i8/i4` 简写被误当字符串；
- AllWISE/2MASS null token：`\N`、`nnnn`、`0nnn`、`11nn`；
- AllWISE 数值 flag 的 `11nn` 等；
- NIR 字符串 ID 的全表 QC 扫描；
- 这些修复保证了 compact 表为数值列，而不是 `S30` 字符串。

---

## 3. 跨源表交叉证认

### 3.1 引擎

`oasis_datasets.crossmatch`：

- 右表构建单位球 3D 网格索引；
- 27 邻域 cell；
- 左表分块、27 邻域向量化 `searchsorted`；
- 精确角距最近邻；
- 输出 `left_index/right_index/right_table_index/sep_arcsec/left_id/right_id`；
- 保留右表原始行号，便于后续读 NIR 测光。

### 3.2 缺 G 源全量结果

| 项目 | 数量 | 占比 |
|:--|--:|--:|
| 缺 G 源 | 5,455,339 | 100% |
| 2MASS 匹配 | 1,748,833 | 32.06% |
| AllWISE 匹配 | 983,940 | 18.03% |
| **并集** | **1,993,910** | **36.55%** |
| 两表都匹配 | 738,863 | 13.54% |
| 两者都无 | 3,461,429 | 63.45% |

按子类：

| 子类 | 样本 | 2MASS | AllWISE | 并集 |
|:--|--:|--:|--:|--:|
| RP-only | 3,847,979 | 28.3% | 17.2% | 34.0% |
| 无 G/BP/RP | 1,602,051 | 41.0% | 20.1% | 42.8% |

匹配中位分离 1.52–1.59″，P95 2.84–2.87″。

### 3.3 产物

```text
no_g_2mass_matches.h5                 96 MB
no_g_wise_matches.h5                  57 MB
nir_supp.h5                          490 MB
```

`nir_supp.h5`：5,455,339 行，含 2MASS JHK、AllWISE W1–W4、匹配标志与分离。

---

## 4. 光谱信息分级与填充

### 4.1 A–G 分级

| 等级 | 数据条件 | 光谱来源 |
|:--|:--|:--|
| A | XP sampled 343 点 | 实测 XP |
| B | XP continuous | 重建 XP |
| C | ≥3 波段（G+BP+RP） | 黑体/模板 |
| D | 有限测光 + NIR/颜色 | 模板/黑体 fallback |
| E | 单波段 RP/NIR | RP-only/NIR-only |
| F | 无测光，有分类 | class prior，无可靠通量 |
| G | 无测光无分类 | mask/零通量 |

关键边界：

- **等效黑体不是独立等级**，只是 C/D fallback；
- F 级不能进入可靠通量产品；
- G 级只保留 mask；
- 决策树按源逐一判定。

### 4.2 v3 / v4 立方

| 版本 | 形状 | 大小 | 说明 |
|:--|:--|--:|:--|
| v3 | 50,331,648 × 343 | 67 GB | A/B=0，C/D/E/F/G |
| v4 | 50,331,648 × 343 | 67 GB | 接入 XP sampled |

v4 tier 计数：

```text
A     34,467,653
B              0
C  1,506,302,687
D    267,478,000
E      2,541,258
F        641,979
G        278,194
合计 1,811,709,771
```

v4 增加：

- `tier_counts[npix,7]`
- `quality`：0=A … 6=G，255=空像素
- `xp_fraction`
- `inferred_fraction`

XP 补充表：

```text
xp_supp.h5
源         34,467,653
非空像素   18,933,725
大小       25 GB
```

### 4.3 填充模型

- 正常 G + BP-RP → 黑体模板（C）；
- 缺 G + NIR/RP → 模板/黑体 fallback（D）；
- RP-only → E；
- 无测光 + DSC 分类 → F（零通量）；
- 无信息 → G（掩膜）。

**注意**：这里的“光谱类型推断”是测光/分类驱动的模板填充，不是机器学习光谱分类。

---

## 5. 343 点光谱立方

### 5.1 规格

```text
波长      336–1020 nm，2 nm，343 点
天区      HEALPix nside=2048
像素      50,331,648
源        1,811,709,771
```

### 5.2 构造

- 按 spatial/ipix 流式读取 Gaia core 表；
- 逐父像素聚合同一 HEALPix 子像素的源；
- A 源直接使用 XP 谱，并禁止叠加 C 模板；
- C/D/E 用模板；
- F/G 权重为零；
- 每像素输出 343 点相对光谱；
- 同时记录 tier/quality/provenance。

### 5.3 用途

- 简单成像装置/相机的**光谱积分输入**；
- CIE 人眼颜色计算；
- 全天图/局部视场渲染；
- 不是单颗恒星的星表级 PSF 模型。

---

## 6. 简单成像装置与 CIE 人类视觉模拟

### 6.1 颜色模型

- CIE 1931 2° 配色函数（Wyman 2013 解析近似）；
- XYZ → linear sRGB(D65)；
- gray-world 白平衡：线性增益约

```text
R 0.80819
G 1.02472
B 1.27098
```

- 直接查看格式：gamma 2.2 + exposure 4（线性曝光，不是 tone mapping）；
- 可选 Reinhard：亮度 `Ld = L/(1+L)`，保留色度。

### 6.2 显示/存档分离

- **TIFF**：16-bit 线性 RGB，**无 blur**，作为 CIE 位图存档；
- **PNG/JPEG**：gamma/Reinhard + FWHM=1 px Gaussian，仅用于直接查看；
- cubemap 各面在自身分辨率再做 FWHM=1 px；
- 这避免了把显示处理写进科学存档。

### 6.3 PSF 与采样

- 光学 PSF：Airy 圆孔，默认 50 mm f/1.8、550 nm；
- 全天空 8192×4096 像素尺度约 158″/px；
- 50 mm f/1.8 Airy FWHM ≈ 4.2″ = 0.027 px；
- 因此**真实镜头 PSF 在全天空图上物理上不可见**；
- 恒星 PSF 必须靠**源级渲染**：T2/T3/全量星表 + 2× 超采样 + Gaussian FWHM=3 px。

### 6.4 源级星场

| 图层 | 星数 |
|:--|--:|
| T2，G≤9 | 177,426 |
| G≤10 | 482,106 |
| T3，G≤12 | 3,087,828 |
| G≤15 | 36,909,365 |
| G≤18 | 304,942,094 |
| 全量（有 G） | 1,806,254,432 |

- 2× 超采样：16384×8192 → 8192×4096；
- PSF FWHM=3 px；
- BP-RP → 黑体模板 → CIE；
- 全量图因源密度极高，银河面接近连续背景。

### 6.5 输出

- 等距圆柱 8192×4096；
- Mollweide 4096×2048；
- 银道坐标全天图，中心 l=0、b=0 正对银心；
- 4096×4096×6 cubemap；
- HTML5 WebGL 查看器（旋转、缩放、触摸、全屏）；
- 邮件版单文件 HTML（低分辨率，base64 六面内嵌）。

---

## 7. 测试与验证

### 7.1 自动测试

```text
PYTHONPATH=src python3 -m unittest discover -s tests
Ran 18 tests
OK (skipped=1)
```

覆盖：

- consolidate profile/schema、compact 输出；
- crossmatch 暴力一致性、CSV 输出；
- NIR compact 构造；
- 343 点立方形状、模板值、provenance；
- 数据/索引/选择。

### 7.2 手工验收

| 项目 | 验收 |
|:--|:--|
| 2MASS compact | 470,992,970 行，86 B/row，QC 96/96 |
| AllWISE compact | 747,634,026 行，228 B/row |
| 缺 G NIR 并集 | 1,993,910 / 5,455,339 |
| XP 补充 | 34,467,653 源，18,933,725 像素 |
| v4 tier 总和 | 1,811,709,771 |
| v4 flux | 全部 finite |
| 全量星层 | 1,806,254,432 有 G 源 |
| cubemap | 6 × 4096，银心在 +X 面中心 |
| HTML5 | HTTP 200，六面加载 |

### 7.3 本阶段发现并修复的问题

| 问题 | 修复 |
|:--|:--|
| compact schema 简写被当字符串 | dtype 归一化 |
| NIR null token `\N`、`nnnn`、`0nnn`、`11nn` | null 处理 |
| NIR 字符串 ID 全表 QC 扫描 | 跳过 NIR 全表 QC |
| crossmatch 缺右表原始行号 | 增加 `right_table_index` |
| CIE 二次除 D65 导致偏红 | 移除二次白点除法 |
| 整体偏黄 | gray-world 线性 RGB 增益 |
| 直接查看过曝 | exposure 8 → 4；实测无饱和裁切 |
| Reinhard 全量广播错误 | `ratio[..., None]` |
| 立方体单像素颗粒 | 源级超采样 + PSF |
| Mollweide 负经度采样错误 | 经度 `mod 360` |

---

## 8. 设计结论

1. **固化层**已能覆盖 Gaia、AllWISE、2MASS，支持全量与 compact；
2. **交叉证认**已验证缺 G 源 NIR 覆盖约 36.55%，两表共同证认 738,863；
3. **A–G 分级**能明确区分实测、模板、单波段、分类先验和掩膜；
4. **v4 立方**已接入 XP，A 级 3,446 万源，B 仍为 0；
5. **简单成像模拟**的正确分工是：
   - 立方体/源表提供光谱；
   - 源级 PSF + 超采样提供恒星形态；
   - CIE 1931 + sRGB 提供颜色；
   - TIFF 存档与显示 tone/encode 分离；
6. 对全天空 158″/px 图像，真实镜头 PSF 是亚像素的；颗粒感来自立方体像元/点源采样，不是镜头 PSF；
7. 全量星表渲染已接近连续背景，展示应使用 T2/G≤15 或分层合成。

---

## 9. 产物索引

```text
/mnt/data/huo/Datasets/Gaia/gdr3/consolidated/
  gaia_dr3_core_spatial.h5
  no_g_supp.h5
  nir_supp.h5
  no_g_2mass_matches.h5
  no_g_wise_matches.h5

/mnt/data/huo/Datasets/catalogs/nir/consolidated/
  2MASS.h5
  WISE.h5

/mnt/data/huo/Datasets/Gaia/gdr3/spectral/
  gaia_dr3_spectral_n2048_v3.h5
  gaia_dr3_spectral_n2048_v4.h5
  xp_supp.h5

/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/
  ..._16bit.tiff
  ..._gamma2.2_exposure4_blur1.png/jpg
  cubemap_v4/
  cubemap_v4/galactic_4096/

/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_galactic/
  gaia_full_galactic_8192x4096_psf3_reinhard.png/jpg

/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_starfield/
  gaia_t2_...
  gaia_g10_...
  gaia_g15_...
  gaia_g18_...
  gaia_full_...
```

---

## 10. 仍然存在的限制

- B 级仍为 0：XP continuous 未接入；
- 全量星层不包含 5,455,339 个缺 G 源；
- F/G 级零通量不是物理零通量；
- 没有银河消光/大气/仪器响应；
- CIE CMF 为解析近似，不是官方表格；
- gray-world 是显示白平衡，不是物理色度；
- 人类视觉模型未包含瞳孔、Stiles–Crawford、眼像差、明暗适应；
- 简单望远镜/相机目前用 Gaussian display PSF，未用具体镜头处方；
- 全量星场源密度极高，单星不可辨，需要分层合成或局部视场。
