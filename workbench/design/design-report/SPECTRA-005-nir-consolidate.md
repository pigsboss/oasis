# SPECTRA-005：AllWISE / 2MASS consolidate

- 日期：2026-11-24
- 层级：targets/data
- 目标：把 AllWISE、2MASS 源表固化为 PyTables，支持全量与紧凑两种模式。

## 1. profiles

| profile | 数据 | 默认 |
|:--|:--|:--|
| `allwise_psc` | AllWISE，298 列 | 全量 |
| `allwise_nir` | AllWISE compact | 36 列 |
| `twomass_psc` | 2MASS PSC，60 列 | 全量 |
| `twomass_nir` | 2MASS compact | 17 列 |

### AllWISE compact

```text
designation, ra, dec, sigra, sigdec, sigradec, glon, glat, elon, elat,
wx, wy, cntr, source_id, coadd_id, src,
w1mpro, w1sigmpro, w1snr, w1rchi2,
w2mpro, w2sigmpro, w2snr, w2rchi2,
w3mpro, w3sigmpro, w3snr, w3rchi2,
w4mpro, w4sigmpro, w4snr, w4rchi2,
ph_qual, cc_flags, ext_flg, var_flg
```

### 2MASS compact

```text
designation, ra, decl, j_m, h_m, k_m,
j_msigcom, h_msigcom, k_msigcom, j_snr, h_snr, k_snr,
ph_qual, rd_flg, cc_flg, gal_contam, mp_flg
```

## 2. 使用

```bash
tools/oasis-datasets consolidate --from /mnt/data/huo/Datasets/WISE \
  --profile allwise_nir --app /mnt/data/huo/Datasets/catalogs/nir \
  --column-profile core --layout spatial --order 9 --jobs 48 --apply

tools/oasis-datasets consolidate --from /mnt/data/huo/Datasets/2MASS \
  --profile twomass_nir --app /mnt/data/huo/Datasets/catalogs/nir \
  --column-profile core --layout spatial --order 9 --jobs 32 --apply
```

全量：

```bash
--profile allwise_psc --column-profile full
--profile twomass_psc --column-profile full
```

## 3. 实现

- AllWISE 的 298 列来自官方 `wise-allwise-cat-schema.txt`；
- 2MASS 复用 `twomass_psc_schema`；
- compact profile 内置类型/宽度，跳过全表类型扫描；
- generic `id_key` 不再强制 `source_id`；
- `ipix` + spatial sort 仍由 consolidate 生成；
- QC 使用 `designation` 作为键（字符串）；
- 交叉证认可直接消费 `/table`。

## 4. 验证

- 合成 AllWISE compact：3 行，`designation/ra/dec/W1..W4` 正确；
- 合成 2MASS compact：3 行，`designation/ra/decl/J/H/K` 正确；
- QC 通过；
- 2 个单元测试。

## 5. 注意

- 全量 AllWISE 约 365 GB 压缩、747M 行，解析和 spatial sort 耗时长；
- 全量 2MASS 约 42 GB 压缩、470M 行；
- full profile 需要大磁盘和长运行时间；
- compact 是缺 G 源交叉证认的优先产品。
