# SPECTRA-004：源表交叉证认工具

- 日期：2026-11-24
- 层级：targets/data
- 目标：为 OASIS 源表提供通用空间最近邻交叉证认；首先服务 Gaia 缺 G 源与 AllWISE/2MASS 的融合。

## 1. 功能

```bash
oasis-datasets crossmatch LEFT.h5 RIGHT.h5 \
    --radius-arcsec 3 --out matches.h5
```

输入：

- 两个 HDF5 表；
- RA/Dec 列名可配置；
- 可选 ID 列。

输出：

```text
/matches
  left_index   int64
  right_index  int64
  sep_arcsec   float64
  left_id      可选
  right_id     可选
```

## 2. 算法

- 右表转单位球 Cartesian 坐标；
- 以 `radius` 为 cell 尺寸，建稀疏 3D cell index；
- 左表分块；每个源查询 27 个邻域 cell；
- 候选做精确球面角距；
- 取最近且 ≤ radius。

优点：

- 不依赖 HEALPix ordering；
- 不需要 KD-tree/scipy；
- 半径可配置；
- 适合 HDF5 表流式处理。

## 3. 当前限制

- 只接受 HDF5 表；AllWISE `.bz2`、2MASS 固定宽度 `.gz` 需要 ingest adapter；
- 当前为 one-to-nearest，尚未 one-to-many/one-to-one；
- 全量 AllWISE 747M / 2MASS 470M 建索引需要较大内存和预处理；
- 尚未把匹配结果写入 `nir_supp.h5`。

## 4. 与缺 G 源的关系

SPECTRA-003 抽样显示：

- AllWISE 20.1%；
- 2MASS 33.2%；
- 并集 39.7%（测试天区）。

交叉证认工具用于把这一抽样结果推广到全量 no-G 源：

```text
no_g_supp.h5 (5.45M)
    × AllWISE / 2MASS index
    → nir_supp.h5
    → v3 spectral cube
```

## 5. 验收

- 合成 400×2120 表，5″ 半径，120 个已知对应体全部找回；
- 与 brute-force 角距一致；
- HDF5/CSV 两种输出；
- 2 个单元测试通过。
