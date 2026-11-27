# SPECTRA-019：源级超采样 CIE 全天图

- 日期：2026-11-27
- 输入：`gaia_dr3_core_spatial.h5`
- 坐标：ICRS
- 恒星：1,806,254,432（有 G）
- 超采样：2×，16384×8192
- 输出：8192×4096
- PSF：Gaussian，FWHM=3 px
- 色彩：BP-RP → 黑体模板 → CIE 1931 2° → linear sRGB(D65)
- 白平衡：gray-world
- Tone：Reinhard luminance
- 编码：gamma 2.2

## 输出

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie_sourcelevel/
  gaia_cie_source_icrs_8192x4096_psf3_reinhard.png
  gaia_cie_source_icrs_8192x4096_psf3_reinhard.jpg
  gaia_cie_source_icrs_8192x4096_psf3_reinhard.json
```

## 说明

- 这是**源级**渲染，不是 nside=2048 立方像元渲染；
- 恒星按源位置、G 和 BP-RP 单独注入，再经超采样和 PSF；
- 与之前的 full Reinhard 星场参数相同，因此像素结果一致；
- 5,455,339 个缺 G 源仍未加入该层；
- v5 的 B 级已包含在有 G 的 1,806,254,432 颗中，但源级颜色仍用 BP-RP，不是逐源 XP。

## 32k × 16k / 10-bit

```text
输出        32768×16384
超采样      2×，65536×32768
PSF         Gaussian FWHM=3 px
Tone        Reinhard luminance
位深        10 bit/通道，3 通道
容器        16-bit TIFF/PNG，数值量化为 10 bit
坐标        Galactic，银心在画面中央
```

文件：

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie_32k/
  gaia_cie_galactic_32k_32768x16384_psf3_reinhard_10bit.tiff
  gaia_cie_galactic_32k_32768x16384_psf3_reinhard_10bit.png
  gaia_cie_galactic_32k_32768x16384_psf3_reinhard.jpg
  gaia_cie_galactic_32k_32768x16384_psf3_reinhard_10bit.json
```
