# SPECTRA-009：v4 光谱立方的 CIE 天球映射

- 日期：2026-11-24
- 输入：`gaia_dr3_spectral_n2048_v4.h5`
- 投影：等距圆柱（equirectangular），8192 × 4096
- CIE：CIE 1931 2° 配色函数（Wyman 2013 解析近似）
- 白点：sRGB/D65（绝对 XYZ 直接进入 sRGB 矩阵，不再二次除 D65）
- 白平衡：gray-world（非黑区上半亮度中位数）
  增益 [0.80819, 1.02472, 1.27098]
- 输出：16-bit 线性 TIFF（无模糊）、Reinhard PNG/JPEG（高斯 FWHM=1 px）

## 1. 模型

对每个天球像素：

```text
L(λ)  ->  X = ∫ L x̄ dλ, Y = ∫ L ȳ dλ, Z = ∫ L z̄ dλ
XYZ   ->  linear sRGB（D65 白点）
```

立方体 343 个波长点（336–1020 nm，2 nm）直接与 CIE CMF 相乘。
每个输出像素通过 HEALPix nside=2048 最近邻采样立方体像元。

亮度归一：

```text
p99.9(Y) = 16.2173
linear exposure scale = 0.0616625
```

## 2. Tone mapping

Reinhard 作用于亮度，保留色度：

```text
Ld = L / (1 + L)
rgb_out = rgb_linear * (Ld / L)
```

再经 sRGB gamma。Tone exposure = 8。

## 3. 产物

目录：

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/
```

```text
gaia_dr3_v4_cie_equirect_8192x4096_16bit.tiff   106 MB
gaia_dr3_v4_cie_equirect_8192x4096_reinhard.png  73 MB
gaia_dr3_v4_cie_equirect_8192x4096_reinhard.jpg  36 MB
gaia_dr3_v4_cie_equirect_8192x4096.json
```

TIFF：`uint16`，RGB，线性光，按 p99.9 亮度裁剪到 16 bit；**不做高斯模糊**，作为 CIE 位图存档。
PNG/JPEG：8-bit sRGB，Reinhard tone-mapped，再做 **FWHM=1 px 高斯卷积**
（sigma=1/2.35482=0.4247 px），仅用于直接查看。

## 4. 工具

```bash
PYTHONPATH=src /home/huo/Projects/distoptics/.venv/bin/python \
  tools/render_cube_cie.py \
  --cube /mnt/data/huo/Datasets/Gaia/gdr3/spectral/gaia_dr3_spectral_n2048_v4.h5 \
  --out-dir /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie \
  --width 8192 --height 4096 --tone-exposure 8
```

## 5. 注意

- TIFF 是线性光曝光归一化，不是绝对辐射定标；
- 16-bit TIFF 对 p99.9 以上高光裁剪；
- CIE CMF 为解析近似，不是官方表格插值；
- 未做银河消光/前景去红化；
- 之前整体偏红来自把绝对 XYZ 又除了一次 D65 白点；已修正；
- 其后偏昏黄由积分光谱的整体色偏造成，现用 gray-world 线性 RGB 增益校正；
- 高斯只作用于 PNG/JPEG，不作用于 TIFF；
- 等距圆柱在两极有面积畸变；
- F/G 级源无可靠通量，在图中贡献为零；
- 当前未使用 XP continuous 的 B 级源。
