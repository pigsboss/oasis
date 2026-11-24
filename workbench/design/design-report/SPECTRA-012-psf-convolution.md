# SPECTRA-012：PNG 的光学 PSF 卷积

- 日期：2026-11-24
- 输入：`gaia_dr3_v4_cie_equirect_8192x4096_reinhard.png`（已 gray-world 校正）
- 模型：圆形孔径衍射 Airy PSF
- 默认镜头：50 mm f/1.8，550 nm
- 卷积域：linear-light sRGB
- 输出：

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/psf/
  gaia_dr3_v4_cie_equirect_8192x4096_psf_airy50f18.png
  ...json
```

## 关键数字

```text
PNG 像素尺度       158.203 arcsec/px
Airy FWHM          4.207 arcsec
Airy FWHM          0.02659 px
```

因此，在**当前全天空 8192×4096 图**上，真实 50mm f/1.8 镜头的 PSF 远小于一个像素。
卷积在物理上成立，但视觉上几乎不变；输出差异主要来自线性光往返和数值卷积。

## 工具

```bash
tools/psf_convolve.py \
  --png .../gaia_dr3_v4_cie_equirect_8192x4096_reinhard.png \
  --out .../psf/gaia_dr3_v4_cie_equirect_8192x4096_psf_airy50f18.png \
  --focal-mm 50 --f-number 1.8 --wavelength-nm 550
```

## 结论

- 全天空 PNG 的像素尺度远大于真实镜头 PSF；
- 要在图上看见镜头 PSF，需要：
  1. 提供具体镜头的处方/实测 PSF 和像元比例；
  2. 或改为高分辨率局部视场（例如 0.1″/px）；
  3. 或模拟一个 PSF FWHM 与显示像元相当的“显示 PSF”（不再是物理镜头）。
- 当前结果可作为“物理 PSF 已应用”的存档，但不应期待明显的星点变大。

## 限制

- 默认 Airy 是衍射极限圆孔，不包含具体镜头的像差、遮挡、离焦、色差；
- 只对 PNG 做卷积，TIFF 保持无 PSF 存档；
- 没有使用真实镜头的实测 PSF 核。
