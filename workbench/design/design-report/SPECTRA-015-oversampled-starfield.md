# SPECTRA-015：超采样恒星 PSF 渲染

- 日期：2026-11-25
- 问题：nside=2048 光谱立方是 **1.7′ 积分像元**，不是恒星点源；
  在 8192×4096 全天空图上逐像素最近邻采样，会把每个高流量立方像元显示为一个像素点，
  产生“宇宙线/砂粒”观感。
- 结论：对已有立方 PNG 再做 PSF/median 只是补救；正确做法是 **源级渲染**：
  恒星位置 + 流量 + PSF + 超采样像素网格。

## 本次样张

- 星表：Gaia T3，`G ≤ 12`，3,087,828 颗
- 位置：`ra/dec`
- 颜色：`BP-RP` → 黑体模板 → CIE 1931 → linear sRGB(D65)，gray-world 增益
- 流量：`10^-0.4(G-6.5)`
- PSF：Gaussian，FWHM=3 输出像素
- 超采样：2×（16384×8192 渲染，Gaussian FWHM=6，降采样到 8192×4096）
- 编码：线性曝光 + gamma 2.2，无 Reinhard
- 输出：

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_starfield/
  gaia_t3_8192x4096_psf3.png
  gaia_t3_8192x4096_psf3.jpg
  ...json
```

## 意义

- 恒星现在是 **over-sampled PSF**，FWHM≈3 px，不再是一像素宇宙线；
- 2× 超采样保证亚像素位置和 PSF 采样；
- T3 只有 G≤12 亮星，因此这是 **亮星层样张**，不是完整曝光；
- 完整图应把：
  1. 源级恒星层（更暗极限）
  2. 立方体的弥散背景（强模糊/去掉点源）
  合并。

## 工具

```bash
PYTHONPATH=src python tools/render_starfield.py \
  --catalog /mnt/data/huo/Datasets/catalogs/gaia/t3/gaia_t3.h5 \
  --out-dir /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_starfield \
  --width 8192 --height 4096 --supersample 2 --fwhm 3 \
  --gamma 2.2
```

## 后续

- 用完整 Gaia 亮星极限（例如 G≤15）扩展恒星层；
- 从立方体中只取平滑弥散背景，避免与恒星层双计；
- 或者直接改用 Gaia 源表 + XP/颜色模板做源级全天渲染。


## 亮星极限样张

| 版本 | 星数 | 文件 |
|:--|--:|:--|
| T1，G≤6 | 6,764 | `--catalog gaia_t1.h5` |
| T2，G≤9 | 177,426 | `gaia_t2_8192x4096_psf3.png/jpg` |
| G≤10 | 482,106 | `gaia_g10_8192x4096_psf3.png/jpg` |
| T3，G≤12 | 3,087,828 | `gaia_t3_8192x4096_psf3.png/jpg` |

T2 与 G≤10 都保留 FWHM=3 px 输出 PSF；T2 更适合干净的展示样张。
