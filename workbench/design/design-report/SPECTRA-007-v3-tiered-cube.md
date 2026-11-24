# SPECTRA-007：A–G tiered 343 点光谱立方 v3

- 日期：2026-11-24
- 输入：`gaia_dr3_core_spatial.h5`、`no_g_supp.h5`、`nir_supp.h5`
- 输出：`/mnt/data/huo/Datasets/Gaia/gdr3/spectral/gaia_dr3_spectral_n2048_v3.h5`
- 规模：50,331,648 × 343，67 GiB

## 规则

- A：XP sampled（本轮未接入，0）
- B：XP continuous（未接入，0）
- C：正常 G + BP-RP 黑体模板
- D：有限测光/NIR/黑体 fallback
- E：RP-only 或 NIR-only
- F：无测光但有分类，flux=0
- G：无测光无分类，flux=0

A/B 暂为 0；正常 G 源归 C。缺 G 源使用 `nir_supp.h5` 的 2MASS/AllWISE 匹配进入 D，
RP-only 无 NIR 进入 E，无测光按 class 进入 F/G。

## 实测 tier 计数

| tier | 源数 |
|:--|--:|
| A | 0 |
| B | 0 |
| C | 1,540,770,340 |
| D | 267,478,000 |
| E | 2,541,258 |
| F | 641,979 |
| G | 278,194 |
| 合计 | 1,811,709,771 |

## 图级 quality

```text
quality 0=A,1=B,2=C,3=D,4=E,5=F,6=G,255=空像素
```

像素计数：

```text
2: 34,743,132
3: 12,396,202
4:  1,487,791
5:    397,611
6:    227,928
255: 1,078,984
```

quality 取该像素**存在的最差 tier**；空像素为 255。

## 验证

```text
shape       (50,331,648,343)
count 和    1,811,709,771
tier 和     1,811,709,771
flux        all finite
wavelength  336..1020 nm, 343
```

产物约 67 GiB；v2 历史文件保留。

## 限制

- A/B=0：XP sampled 107 GB 已下载，但尚未按 source_id 接入立方；
- C 仍是黑体模板，不是 XP 实测；
- D 的 NIR-only/RP+NIR 模型是统计推断；
- F/G 的 flux=0，不能当作真实零通量；
- 像素 quality 是最差源等级，不反映通量加权质量。

## 下一步

1. 把 XP sampled 接入 A/B；
2. 用 XP 替换 C 中亮星的模板谱；
3. 用 NIR 颜色进一步细化 D；
4. 发布 tier-aware 真彩色/选择 API。
