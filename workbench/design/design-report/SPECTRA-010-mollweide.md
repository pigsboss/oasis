# SPECTRA-010：v4 光谱立方的 Mollweide 真彩色样张

- 日期：2026-11-24
- 输入：`gaia_dr3_spectral_n2048_v4.h5`
- 投影：Mollweide（椭圆全天空）
- 尺寸：4096 × 2048
- CIE：CIE 1931 2°，D65
- 输出：Reinhard 映射后的 PNG/JPEG，高斯 FWHM=1 px

## 结果

```text
p99.9(Y) = 16.2402
linear scale = 0.0615755
Tone exposure = 8
inside pixels = 6,588,416
```

色彩：绝对 XYZ 直接进入 sRGB(D65) 矩阵；不再二次除 D65。
直接查看格式做 FWHM=1 px 高斯卷积（sigma=0.4247 px）。

产物：

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie_mollweide/
  gaia_dr3_v4_cie_mollweide_4096x2048_reinhard.png   17 MB
  gaia_dr3_v4_cie_mollweide_4096x2048_reinhard.jpg  7.2 MB
  gaia_dr3_v4_cie_mollweide_4096x2048.json
```

## 工具

```bash
PYTHONPATH=src:tools /home/huo/Projects/distoptics/.venv/bin/python \
  tools/render_cube_mollweide.py \
  --cube /mnt/data/huo/Datasets/Gaia/gdr3/spectral/gaia_dr3_spectral_n2048_v4.h5 \
  --out-dir /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie_mollweide \
  --width 4096 --height 2048 --tone-exposure 8
```

## 说明

- 真彩色由 CIE XYZ → linear sRGB(D65) 得到；
- Reinhard 只作用于亮度，保留色度；
- 椭圆外为黑色；
- 未做消光改正；
- F/G 源通量为零。
