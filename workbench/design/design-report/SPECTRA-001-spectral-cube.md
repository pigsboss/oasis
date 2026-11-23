# SPECTRA-001：GDR3 全量 343 点光谱立方开发任务书

- 编号：SPECTRA-001　版本：v0.1　日期：2026-11-24
- 目标：从已构建的全量 Gaia DR3 core/spatial PyTables 目录，生成 **nside=2048、343 点（336–1020 nm，2 nm）的逐像素光谱立方**。
- 关联：DSM-004（catalogue profiles）、SKY-001（HEALPix/天图）、`oasis_datasets.consolidate`、`hpxmap`。

## 1. 范围与假设

本任务先交付 **可复现的 T1 级推断立方**：

- 星表：`/mnt/data/huo/Datasets/Gaia/gdr3/consolidated/gaia_dr3_core_spatial.h5`
  - 1,811,709,771 行；core 14 列 + ipix；spatial order 9。
- 本机没有 XP 光谱表，也没有把 GSP-Phot 参数并入 core 表；
- 因此本阶段使用：
  - `BP-RP → Teff` 的 16 级经验映射；
  - 黑体 Planck 模板（336–1020 nm，343 点）；
  - 以 G 星等作为相对亮度权重；
  - **所有光谱标记为 `inferred_blackbody`，quality=D**。
- 输出为**相对通量**（G=6.5 参考），不是绝对辐射定标；
- 本机全量统计：**270,939,282 源缺 BP-RP**（15.0%，太阳型 fallback），
  **5,455,339 源缺 G**（0.30%，计入 count 但 flux=0）。
- 后续 XP / GSP-Phot 模板可复用同一立方接口，替换模型层。

## 2. 功能单元

| # | 单元 | 职责 |
|:--|:--|:--|
| 1 | `SpectralGrid` | 固定 343 点波长网格；单位、掩膜 |
| 2 | `BlackbodyTemplates` | BP-RP→Teff 网格；Planck 模板；600 nm 归一 |
| 3 | `TemplateIndex` | BP-RP→template index；NaN/越界回退 |
| 4 | `PixelMapper` | core `ipix(order9)` + RA/Dec→nside2048 child |
| 5 | `CubeAccumulator` | 按 parent 像素局部累加 `[16,T]` 权重；避免 1.8B×343 中间数组 |
| 6 | `CubeWriter` | PyTables EArray `/spectra/flux[npix,343]`；分块 append |
| 7 | `Provenance` | `/spectra/count`, `inferred_fraction`, `xp_fraction`, `quality` |
| 8 | `CLI/QA` | `oasis-datasets spectral-cube`；shape/count/sum/NaN 校验 |

## 3. 架构位置

```text
targets/data
  consolidate (已有)
  hpxmap (已有)
  spectral-cube (本任务)  <-- 目标层空间-光谱数据产品
        │ HDF5
        ▼
observables
  CIE / filter / reflectance
        ▼
payloads
  cubemap / equirectangular / HTML5
```

- 立方属于 **target 层数据段**；
- CIE/滤光/反射属于 observables，不在本任务；
- Web 纹理属于 payload，不在本任务。

## 4. HDF5 布局

```text
/spectra/wavelength    float32[343]        # 336..1020, 2 nm
/spectra/templates     float32[16,343]     # blackbody, 600 nm normalized
/spectra/teff          float32[16]
/spectra/flux          float32[npix,343]   # 逐像素 bincount 相对通量
/spectra/count         int64[npix]
/spectra/quality       uint8[npix]         # 4 = inferred_blackbody
/spectra/inferred_fraction float32[npix]   # 1.0
/spectra/xp_fraction   float32[npix]       # 0.0
```

## 5. 算法

1. 读 core 表块（`ipix`, `ra`, `dec`, `phot_g_mean_mag`, `bp_rp`）；
2. `parent = ipix`（order 9）；`child = ang2pix_nest(2048, ra, dec)`；
3. `tidx = digitize(BP_RP_GRID, bp_rp)`；NaN 用太阳型 fallback；
4. `w = 10^(-0.4*(G-6.5))`；
5. 表按 parent 有序；对每个 parent：
   - 局部 `weights[16,T] += w at (child offset, tidx)`；
   - `cube_block = weights @ templates` → `[16,343]`；
   - 追加到 EArray；同时累加 count；
6. 结束补齐空 parent 的零行，写 quality/inferred 数组和 meta。

## 6. 性能与规模

- nside=2048：npix=50,331,648；343×float32 = **68.9 GB**；
- 输入扫描约 1.8B 行；块 1–2M 行；
- 局部 `[16,16]` 权重，内存不随 npix 爆炸；
- 输出 HDF5 无压缩；磁盘 `/mnt/data` 4.4 TB 可用；
- 实测：单进程约 7 min（I/O/ang2pix 主导）；输出 69.9 GB。

## 7. 验收

- HDF5 存在；`/spectra/flux.shape == (50331648,343)`；
- `wavelength` 为 336..1020，343 点；
- `count.sum() == 1,811,709,771`（含缺 G 源；缺 G 源 flux=0）；
- flux 全 finite，无 NaN/Inf；
- 抽样像素 `sum(flux)` >0；与 count 一致；
- meta 明确 `inferred=true`、`model=blackbody_bp_rp`、`quality=D`、
  `missing_bp_rp=270939282`、`missing_g=5455339`；
- 生成 nside=2048 立方文件路径：
  `/mnt/data/huo/Datasets/Gaia/gdr3/spectral/gaia_dr3_spectral_n2048.h5`；
  实测 1,811,709,771 行、69.9 GB、count 和 1,811,709,771、flux 全 finite。

## 8. 风险

- 黑体忽略线 blanketing/金属丰度；颜色仅为 D 级；
- 没有 XP/GSP-Phot 时无法得到真实 343 光谱；
- 1.8B 全量推断仍是模型产品，不是观测产品；
- 后续应接入 XP/GSP-Phot 模板，保留相同立方接口和 provenance。
