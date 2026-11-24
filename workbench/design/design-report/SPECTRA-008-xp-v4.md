# SPECTRA-008：接入 XP sampled 的 v4 343 点光谱立方

- 日期：2026-11-24
- 输入：`gaia_dr3_core_spatial.h5`、`no_g_supp.h5`、`nir_supp.h5`、`xp_supp.h5`
- 输出：
  - `xp_supp.h5`
  - `gaia_dr3_spectral_n2048_v4.h5`
- 立方：50,331,648 × 343，约 67 GiB

## 1. XP 补充表

XP sampled 3386 个 ECSV 文件，107 GB（114,428,151,566 bytes），本机：

```text
/mnt/data/huo/Datasets/Gaia/gdr3/xp_sampled_mean_spectrum
```

并行构建：

```bash
tools/build_xp_supp.py \
  --xp-dir /mnt/data/huo/Datasets/Gaia/gdr3/xp_sampled_mean_spectrum \
  --core .../gaia_dr3_core_spatial.h5 \
  --out .../xp_supp.h5 \
  --nside 2048 --jobs 16
```

产物：

```text
XP 源        34,467,653
非空像素     18,933,725
文件         25 GB
```

归一：

- XP 绝对通量除以 600 nm 通量，保留谱形；
- 以 `10^-0.4(G_est-6.5)` 加权；
- `G_est` 由 XP source_id 对 core 表 G 抽样标定，ZP=-26.308283；
- 每个源最多一个 XP 谱，按 HEALPix nside=2048 累加到像素。

## 2. v4 接入方式

- 若源在 `xp_supp` 的 source_id 集合中：tier=A，**不叠加 C 级黑体模板**；
- XP 像素和通过 dense `xp_dense[npix,343]` 在父像素 flush 时加入；
- 其余源仍按 C/D/E/F/G 规则；
- 保留 `tier_counts`、`xp_fraction`、`inferred_fraction`、`quality`。

## 3. 全量 tier 计数

| tier | 源数 |
|:--|--:|
| A | 34,467,653 |
| B | 0 |
| C | 1,506,302,687 |
| D | 267,478,000 |
| E | 2,541,258 |
| F | 641,979 |
| G | 278,194 |
| 合计 | 1,811,709,771 |

## 4. 图级 quality

```text
0=A, 1=B, 2=C, 3=D, 4=E, 5=F, 6=G, 255=空像素
```

像素计数：

```text
0:     151,857
2:  34,591,275
3:  12,396,202
4:   1,487,791
5:     397,611
6:     227,928
255: 1,078,984
```

A-only 像素 151,857；含 A 的像素会按最差 tier 抬高 quality。

## 5. 验证

```text
shape       (50,331,648,343)
count 和    1,811,709,771
tier 和     1,811,709,771
flux        all finite
A           34,467,653
xp_pixels   18,933,725
```

## 6. 限制

- XP 绝对通量到相对通量的归一依赖 600 nm 与 G 零点标定，属于近似；
- XP 采样源未做 per-source 误差传播；
- 未接入 XP continuous，B 仍为 0；
- A 源不叠加 C 模板，但 XP 谱与 Gaia G 标定存在系统差；
- F/G 的 flux=0 不是物理零通量。

## 7. 产物

```text
/mnt/data/huo/Datasets/Gaia/gdr3/xp_supp.h5
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/gaia_dr3_spectral_n2048_v4.h5
```

v4 为当前推荐立方；v3 保留为无 XP 历史版本。
