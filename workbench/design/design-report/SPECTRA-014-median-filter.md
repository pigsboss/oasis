# SPECTRA-014：PNG 的 median 滤波试验

- 日期：2026-11-24
- 输入：`gaia_dr3_v4_cie_equirect_8192x4096_gamma2.2_exposure4_blur1.png`
- 变换：对 RGB 三个通道分别做 median 3×3 / 5×5
- 输出目录：

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/median/
```

## 对比

| 版本 | 文件大小 | 平均 V | V p99.9 | V=255 | S=1 非黑 | 水平梯度均值 |
|:--|--:|--:|--:|--:|--:|--:|
| base | 71 MB | 38.39 | 227 | 34 | 9,362 | 15.72 |
| median 3×3 | 46 MB | 32.27 | 159 | 18 | 559 | 3.40 |
| median 5×5 | 36 MB | 31.38 | 154 | 0 | 193 | 1.62 |

- median 3×3 将水平梯度降到 **21.7%**；
- median 5×5 更平滑，但星点和银河细结构损失明显；
- 推荐 **3×3**。

## 文件

```text
gaia_dr3_v4_cie_equirect_8192x4096_gamma2.2_exposure4_median3.png/jpg
gaia_dr3_v4_cie_equirect_8192x4096_gamma2.2_exposure4_median5.png/jpg
```

## 说明

- median 应用于 **gamma 2.2 + exposure 4 + FWHM=1** 之后的 8-bit RGB；
- TIFF 不改；
- 如果采用 median 3×3，可再生成 Mollweide/cubemap/邮件版。
