# SPECTRA-013：TIFF 颜色 + gamma 直出 + FWHM=1 blur

- 日期：2026-11-24
- 输入：`gaia_dr3_v4_cie_equirect_8192x4096_16bit.tiff`
- 色彩：直接使用 TIFF 的 gray-world balanced linear RGB
- Tone mapping：**无 Reinhard**
- 显示编码：gamma 2.2
- 曝光：线性 exposure=8（仅曝光，不压缩动态范围）
- 模糊：gamma 后 FWHM=1 px（sigma=0.4247 px）
- 输出：PNG/JPEG

## 处理链

```text
uint16 TIFF / 65535
  -> linear RGB * exposure
  -> gamma 2.2
  -> Gaussian FWHM=1 px
  -> 8-bit sRGB PNG/JPEG
```

TIFF 本身不做 blur，仍作为 CIE 位图存档。

## 产物

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/
  gaia_dr3_v4_cie_equirect_8192x4096_16bit.tiff
  gaia_dr3_v4_cie_equirect_8192x4096_gamma2.2_exposure8_blur1.png
  gaia_dr3_v4_cie_equirect_8192x4096_gamma2.2_exposure8_blur1.jpg
```

Mollweide：

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie_mollweide/
  gaia_dr3_v4_cie_mollweide_4096x2048_gamma2.2_exposure8_blur1.png
  gaia_dr3_v4_cie_mollweide_4096x2048_gamma2.2_exposure8_blur1.jpg
```

Cubemap / 邮件版：

```text
cubemap_v4/        6 × 2048
cubemap_email_1024/gaia_dr3_skyviewer_email.html
```

单文件邮件版约 **3.5 MB**。

## 说明

- **Reinhard 已移除**；没有 `_reinhard` 文件；
- `exposure=8` 只是线性曝光，不是 tone mapping；
- 如果直接 `exposure=1`，图像会非常暗；
- 颜色来自 TIFF 的 gray-world balanced linear RGB；
- TIFF 是 16-bit 无模糊存档；
- Mollweide 直接从该 TIFF 重投影，不再走 Reinhard。

## 工具

```bash
python tools/tiff_to_direct.py \
  --tiff .../gaia_dr3_v4_cie_equirect_8192x4096_16bit.tiff \
  --out-dir .../maps_cie \
  --stem gaia_dr3_v4_cie_equirect \
  --projection equirect --gamma 2.2 --exposure 8 --fwhm 1
```

```bash
python tools/tiff_to_direct.py \
  --tiff .../gaia_dr3_v4_cie_equirect_8192x4096_16bit.tiff \
  --out-dir .../maps_cie_mollweide \
  --stem gaia_dr3_v4_cie_mollweide \
  --projection mollweide --width 4096 --height 2048 \
  --gamma 2.2 --exposure 8 --fwhm 1
```
