# oasis_datasets —— 目标层 · 数据集管理工具

对**原始数据集**做三件事：**清单（list）→ 核验（verify）→ 放置（sync）**。
与 `oasis_catalog`（源表更新/交付 manifest）正交；共用 `~/.config/oasis/config.yaml`。

设计依据：`workbench/design/design-report/DSM-002-datasets-tool-design.md`（架构）、
`DSM-003-interface-design.md`（接口）；v0.1 能力见 DSM-001。

## 命令

```bash
tools/oasis-datasets list [ids...]                 # 清单概览（inventory 优先，含渠道健康摘要）
tools/oasis-datasets verify gaia_gdr3_gaia_source  # 抽检 8 个文件（默认）
tools/oasis-datasets verify tess_tic --sample 3    # 指定抽样数
tools/oasis-datasets verify twomass_psc --full     # 全量核验（慢）
tools/oasis-datasets sync tess_tic --to raid5_archive      # dry-run（默认）
tools/oasis-datasets sync tess_tic --to raid5_archive --apply
tools/oasis-datasets sync tess_tic --to zfs_nas --apply        # ssh 目标（host 用 storages/nodes 别名；自动远端 mkdir）
tools/oasis-datasets sync gaia_gdr3_gaia_source --to-path /tmp/mirror
tools/oasis-datasets mirror mpcorb --to raid0_scratch          # 远程→本地（并行分片+断点续传+manifest）
tools/oasis-datasets mirror mpcorb cometels --to raid0_scratch --apply
tools/oasis-datasets tasks list | tasks show <id> | tasks watch <id>
tools/oasis-datasets mpc parse [--raw PATH] [--dest DIR] [--apply]   # MPCORB.DAT.gz → 根数解析表 + manifest
tools/oasis-datasets hdf5 <csv.gz...> [--dest DIR] [--apply]          # CSV.gz → HDF5 rendition（可选格式；canonical 仍为 CSV.gz）
tools/refresh-delivery mpc|gaia|verify                                # UR-2026-1012 交付刷新（按需运行，自校）
tools/oasis-datasets kernels list|verify|fetch|send --app DIR        # SPICE 底座资产（注册/校验/取件/投送）
tools/oasis-datasets consolidate <catalogue|--from PATH> --app WORKSPACE [--profile P] \
    [--column-profile core|full] [--layout spatial|source_id] [--order N] \
    [--index source_id,phot_g_mean_mag] [--region cone:RA,DEC,R_DEG] \
    [--attributes A,B,C] [--limit N] [--apply]
                                                          # 应用侧整合（PyTables 工作集；core/spatial/CSI）
tools/oasis-datasets consolidate-select CATALOG.h5 --id ID | --cone RA,DEC,R | --box RA1,RA2,D1,D2 \
    [--where "phot_g_mean_mag < 18"] [--columns ...] [--format csv|fits|npy] --out FILE
                                                          # 从 consolidated 表按 ID/锥/盒/表达式选择
tools/oasis-datasets hpxmap CATALOG.h5 --nside 512 --quantity count \
    [--expr EXPR] [--weight-expr EXPR] [--unit UNIT] --out MAP.fits
                                                          # 源表 bincount -> NESTED HEALPix FITS
tools/oasis-datasets spectral-cube CATALOG.h5 --nside 2048 [--no-g-supp no_g_supp.h5] --out CUBE.h5
                                                          # 逐像素 343 点光谱立方（当前 blackbody/BP-RP，D 级推断）
tools/oasis-datasets crossmatch LEFT.h5 RIGHT.h5 --radius-arcsec 3 --out MATCHES.h5
                                                          # HDF5 源表空间最近邻交叉证认
tools/oasis-datasets probe [ids...] [--channel id] # 渠道连通性 + 版本确定（file/https/ssh）
tools/oasis-datasets storages [--json]             # 本机文件系统视图（挂载/未挂载/未登记）
tools/oasis-datasets web [--port 8787] [--no-open] # 本机 Web（127.0.0.1）：清单/存储/任务/审计 + 配置编辑器

# 切片导出（M3）：~/.config/oasis/slices/*.yaml；组内共享源单遍扫描；默认 dry-run
tools/oasis-datasets slice list                       # 规格 + 校验状态
tools/oasis-datasets slice run gaia_t1 gaia_t2 gaia_t3 --apply      # 全量三档
tools/oasis-datasets slice run gaia_t1 --chunks 0-99 --apply       # 部分块（估算/测试，manifest 标 partial）

# 清单生命周期（inventory.yaml + review-log.jsonl，单用户审核）
tools/oasis-datasets inventory validate            # V-01…V-06 + 跨文件引用校验
tools/oasis-datasets propose spec.yaml             # 清单外数据集提案（写 proposals + 审计流）
tools/oasis-datasets review list|approve|reject <id> [--note N]
tools/oasis-datasets migrate-config [--dry-run] [--force]   # 旧 config.datasets → inventory.yaml
```

**读取路径**：`list/verify/sync` 优先读 `inventory.yaml`，无清单时回退旧 `config.datasets`
（一个版本周期）；`oasis-catalog update` 仍读旧配置（store 布局在其中）。

## consolidate：Gaia 源表 → 可查询 HDF5

### 快速使用

```bash
# Gaia CSV.gz（自动识别 gaia profile）；默认 core + spatial + order 9
tools/oasis-datasets consolidate \
    --from /mnt/data/huo/Datasets/catalogs/gaia/t3/gaia_t3.csv.gz \
    --app /tmp/skyapp \
    --column-profile core --layout spatial --order 9 \
    --index source_id,phot_g_mean_mag --apply

# 锥查询 + 星等
tools/oasis-datasets consolidate-select /tmp/skyapp/consolidated/gaia_t3.h5 \
    --cone 83.822,-5.391,0.5 --where "phot_g_mean_mag < 18" \
    --columns source_id,ra,dec,phot_g_mean_mag --format csv --out orion.csv

# 多分片并行：--jobs N 只对多个 CSV 文件有效；单个 CSV.gz 不可 seek，会退化为单进程
# --schema 给出列 dtype，可完全跳过全表类型扫描
tools/oasis-datasets consolidate --from /tmp/t3shards --profile gaia_tier \
    --app /tmp/skyapp --column-profile core --layout spatial --order 9 \
    --jobs 8 --schema /tmp/t3_schema.json --apply

# 全量 Gaia DR3 官方 ECSV 分片：显式 gaia_dr3_source profile
# --schema 用 gdr3_csv_dtype 生成，保留 i1/i2/i4/f4/f8/S 精度
tools/oasis-datasets consolidate --from /mnt/data/huo/Datasets/Gaia/gdr3/gaia_source \
    --profile gaia_dr3_source --column-profile full --layout spatial --order 9 \
    --schema /tmp/gdr3_schema.json --jobs 16 --apply

# FITS 源表（需要 astropy；HDU 0 无表时自动找第一个 BINTABLE）
tools/oasis-datasets consolidate --from gaia.fits --app /tmp/skyapp --profile gaia_tier --apply
```

### HDF5 布局

```text
/table                  PyTables Table，按 ipix 排序（spatial）
  source_id, ra, dec, ipix, core columns ...
/index/ipix_pixels      int32[npix_used]   稀疏像素表
/index/ipix_offsets     int64[npix_used+1] 每个像素的行区间
/meta/*                 schema/source/index/manifest（attrs + manifest.json）
```

- **不压缩、不担心索引体积**：consolidate 是可再生工作集，用完删除；优先写吞吐与查询延迟；
- `source_id`、`phot_g_mean_mag` 建 **无压缩 CSI**；`ipix` 不建 CSI（排序 + 稀疏 offsets 已足够）；
- `--jobs N`：文件级并行 reader；共享内存 ring + 小消息队列；writer 只做
  `table.append(array_view)`，不做转换、不 pickle 数组；
- `--schema schema.json`：列 dtype 已知时跳过全表类型扫描；保留 `i1/i2/i4/f4/f8/S` 精确类型；
  无 schema 时回退全表推断；
- `null` 整数按 `-1` sentinel 写入（表 manifest 记 `int_null_sentinel`）；float 用 NaN；
- `core` 默认列：`source_id, ra, dec, ref_epoch, parallax, pmra, pmdec,
  phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag, bp_rp, ruwe,
  duplicated_source, phot_variable_flag`；源表缺列自动裁剪并记 warning；
- `--column-profile full` / `--attributes` 可写全列或自定义子集；
- `--layout source_id` 保留 ID 排序（无 ipix offsets），适合 ID 中心目录；
- `--layout csr`：**仅作 ingest/吞吐实验**；表不排序，额外写
  `ipix_pixels/ipix_offsets/ipix_rowids`；锥/盒是 row-id 随机读，**不是天区访问核心**；
  64 reader 下比 `spatial` 少 18–22 s sort/copy，但同一 1° 天区查询约 115–133 ms，
  `spatial` 仅 50–64 ms；核心仍用 `spatial`。
- `consolidate-select` 的 `--where` 是 PyTables 表达式（列名白名单校验）；
- FITS 输出需 astropy；系统 Python 无 astropy 时 CSV/NPY 仍可用。

### 源表交叉证认

```bash
tools/oasis-datasets crossmatch LEFT.h5 RIGHT.h5 \
    --radius-arcsec 3 --left-table /no_g --right-table /table \
    --left-id source_id --right-id source_id --out matches.h5
```

- 右表在单位球三维网格上建索引；
- 左表分块查询 27 个邻域 cell；
- 输出 `/matches`：`left_index, right_index, sep_arcsec, left_id, right_id`；
- 目前是 **HDF5 表到 HDF5 表**；AllWISE/2MASS 原始 bz2/固定宽度表还需要 NIR ingest adapter；
- 设计见 `SPECTRA-004-source-crossmatch.md`。

### 光谱立方（Phase 1）

```bash
tools/oasis-datasets spectral-cube \
    /mnt/data/huo/Datasets/Gaia/gdr3/consolidated/gaia_dr3_core_spatial.h5 \
    --nside 2048 --chunk 2000000 \
    --out /mnt/data/huo/Datasets/Gaia/gdr3/spectral/gaia_dr3_spectral_n2048.h5
```

当前实现（SPECTRA-001 T1）：

- 1.8B 源没有 XP/GSP-Phot 参数；使用 **BP-RP→Teff 16 级 + 黑体模板**；
- `/spectra/flux[npix,343]` 是逐像素源光谱 bincount；
- 所有像素 `inferred=true`、`quality=4 (inferred_blackbody)`、`xp_fraction=0`；
- 相对通量：`G=6.5` 参考、600 nm 归一；
- nside 2048：npix 50,331,648，343 点，float32 约 **68.9 GB**；
- 完整任务书：`workbench/design/design-report/SPECTRA-001-spectral-cube.md`。

输出布局：

```text
/spectra/wavelength       float32[343]
/spectra/templates        float32[16,343]
/spectra/teff             float32[16]
/spectra/flux             float32[npix,343]
/spectra/count            int64[npix]
/spectra/quality          uint8[npix]
/spectra/inferred_fraction float32[npix]
/spectra/xp_fraction      float32[npix]
```

### HEALPix bincount

```bash
# 源计数（使用 consolidate 的实际 ipix；nside <= 存储 order 时直接降采样）
tools/oasis-datasets hpxmap gaia.h5 --nside 512 --quantity count \
    --unit "sources/pixel" --out count_n512.fits

# 物理量：sum / mean / weighted_mean 由表达式定义
tools/oasis-datasets hpxmap gaia.h5 --nside 512 --quantity sum \
    --expr "3.3e6*10**(-0.4*phot_g_mean_mag)" \
    --unit "photon/s/cm2" --out g_flux_n512.fits

tools/oasis-datasets hpxmap gaia.h5 --nside 256 --quantity mean \
    --expr "bp_rp" --unit "mag" --out bp_rp_n256.fits

tools/oasis-datasets hpxmap gaia.h5 --nside 256 --quantity weighted_mean \
    --expr "bp_rp" --weight-expr "10**(-0.4*phot_g_mean_mag)" \
    --unit "mag" --out bp_rp_weighted_n256.fits
```

语义：

| quantity | 像素值 |
|:--|:--|
| `count` | 落入像素的源数 |
| `sum` | `expr` 的逐源值之和 |
| `mean` | `expr` 的算术平均（空像素为 0） |
| `weighted_mean` | `sum(expr*weight_expr) / sum(weight_expr)` |

- 目标 `nside` 粗于/等于存储 order 时用实际 `ipix` 右移，精确且快；
- 更细时用 RA/Dec → `ang2pix_nest`；
- 输出 NESTED、ICRS、float64 FITS BINTABLE；`PIXTYPE/ORDERING/NSIDE` 标准头，`healpy.read_map` 可读；
- FITS 头/JSON sidecar 记录 `QUANTITY/EXPR/WEIGHTEX/UNIT/NROWS`；
- 表达式使用表列名 + 常用 `np` 函数，本地 CLI 执行。

对照 AstroToys `table2hpx.py`：它固定 nside 4096，用 `source_id//2**35` 的 level-12 近似像素，并用 `gmag2photrate`；本工具支持任意 nside、实际 RA/Dec 精确像素、任意物理表达式。

测试（16 项）：

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
# 参考环境（含 astropy）：
PYTHONPATH=src /home/huo/Projects/distoptics/.venv/bin/python -m unittest discover -s tests -v
```

## 清单与审计（M1）

- `~/.config/oasis/inventory.yaml`：发布型数据集清单（渠道/许可证/存储偏好/版本规则）；
- `~/.config/oasis/review-log.jsonl`：追加式审计流（propose/approve/reject/deprecate/edit）；
- 受控写入：写前校验 → 原子替换（temp+rename）→ `.bak/` 保留 10 份；
- 规则：`x-` 前缀为扩展字段；`licence.url` 为空仅告警；变更动作 CLI 默认只读/预览。

## 校验清单：发现与语义校准

- **发现**：在源表路径及其一级子目录中自动寻找 `_MD5SUM.txt / MD5SUM.txt / md5sum.txt /
  *.md5.txt / *.md5sum.txt / *.sha256 / *.sha256sum`；
- **语义校准**（实测差异：Gaia=压缩流、TESS=解压流且清单名缺 `.gz`）：
  取清单前 12 条目中**最小实际文件**，按"压缩字节 / 解压流"各试算一次，命中者定语义；
  无法判定时默认压缩流。文件名解析允许自动补 `.gz/.bz2/.xz` 后缀。

## 安全规则（sync）

- **默认 dry-run**，`--apply` 才执行；**永不 `--delete`**（目标多余文件保留）；
- 只读源；目标只增；
- `--to <storage-id>`：目标 = `<storage.path>/oasis-datasets/<catalogue.path>`；
- `--to-path DIR`：目标 = `DIR/<catalogue.path>`（临时镜像/摆渡盘用）；
- ssh 目标（NAS 别名）待接线值补齐后加入（v0.2）。

## 状态

- v0.1：list / verify（抽样+全量，自动校准）/ sync（本机路径，dry-run 默认）；
- v0.2（M1 已交付）：inventory 清单 + 审核流 + 审计流 + migrate-config + probe + storages +
  inventory-first 读取切换；
- v0.2（M2 已交付）：本机 Web（127.0.0.1，htmx 本地内置）+ 任务/事件流（SSE）+ 审核收件箱 +
  受控写入引擎（preview→token→原子写+备份+审计）+ 三配置编辑器（清单/设施/切片）+ 未登记卷一键登记；
- v0.2（M3 已交付并首验）：切片导出引擎——组内共享源单遍扫描、per-chunk 多进程并行、多成员
  gzip 有序拼接（单表头 + mtime=0，字节级可复现）、抽样双向 QC（输出侧 + 回源侧）、断点续跑、
  manifest/CREDITS；**首例 Gaia T1/T2/T3 全量完成**：6,764 / 177,426 / 3,087,828 行
  （与官方 TAP 计数逐行一致），合计 236.5 MB，8 进程 ≈67 min；
- v0.2（M4 已交付）：远程→本地镜像（Range 并行分片 + `.part` 断点续传 + sha256 + 版本化落盘
  `<storage>/oasis-datasets/<id>/<version>/` + manifest）；sync 支持 ssh/ssh+rsync 目标
  （复用 storages/nodes 别名，远端自动 mkdir，dry-run 默认）；CLI `tasks list|show|watch`；
- v0.2（M4 后补，UR-OASIS-02 批次 2）：MPC 根数解析（`mpc parse`）——MPCORB.DAT.gz（定宽 202 列）
  → 20 列 `mpc_elements.csv.gz`（原始数值透传、`mtime=0` 字节可复现）+ 产品 manifest
  （逐行 epoch、frame=日心黄道 J2000、类别统计 v1）；全量 1,571,791 行/23 s；
- v0.2（M4 后补，rendition）：`hdf5` 命令——CSV.gz → `/table` 复合数据集（chunked+gzip、
  定宽串、`track_times=False` 字节可复现；回读校验）；交付物落 `~/Datasets/catalogs/`；
- v0.2（M5 首验，F-09/F-10 consolidate）：`consolidate`——profile 驱动任意格式 → PyTables
  工作集（列名齐备、无压缩、CSI、attrs 带 epoch/frame；manifest 记来源/参数/QC）；
  已验格式：Gaia 档（CSV+表头）／2MASS（pipe+SQL schema）／TIC（无表头+bracket 头）；
  锥面查询毫秒级；
- **v0.2（M5.1 consolidate core/spatial）**：Gaia 默认 `core`（14 列，按源表实际列裁剪）、
  `spatial` 布局（实际 HEALPix `ipix`，按 ipix 排序）；无压缩表 + 无压缩 CSI；
  稀疏 `/index/ipix_pixels` + `/index/ipix_offsets`；`consolidate-select` 支持
  ID/cone/box/where/columns/FITS/CSV/NPY；CSV+FITS（FITS 需 astropy）单文件；T1/T2/T3
  实测 6,764/177,426/3,087,828 行；T1 0.6 s/1.0 MB、T2 3.1 s/24.4 MB、
  单进程 T3 41 s/544 MB（无 schema）/ 24.6 s（schema）；4 分片×4 reader **10.2 s**，
  8 分片×8 reader **8.3 s**；T3 ID 查询 ~9 ms、1° 锥 ~67 ms（热缓存）、
  盒查询 ~11 ms、where 20 万行 ~2.0 s；
- **M5.2 astrotoys 对比**：GDR3 官方 4 个 ECSV 分片（1,812,532 行 × 152 列）：
  OASIS 4 reader + 纯 append writer + spatial/CSI **47.9 s / 2.4 GB 无压缩**；
  astrotoys 古法（4×`csv2npy` + `npy2table -c 5 -l blosc`）**49.9 s / 611 MB**；
  行数/QC 一致；OASIS 额外带 ipix 排序、稀疏 offsets、`source_id` CSI。
- **M5.3 64 分片 + 共享内存 ring**：官方 Gaia DR3 `gaia_source` 的 64 个 ECSV 分片，
  32,897,902 行；core 14 列；spatial + source_id/phot_g_mean_mag CSI；无压缩输出 7.35 GB：
  4/8/16/24/32/64 reader = **209.7 / 133.3 / 84.4 / 74.4 / 66.0 / 56.2 s**；
  64 reader 实际 CPU ~17 核；sort+offsets+CSI 固定 ~30 s。
  此前 `mp.Queue` 16 reader 为 86.9 s；共享内存 ring 只快 2–3%，主瓶颈在
  Python 解析/单 writer/串行 sort+CSI，而不是数组 IPC。
- **M5.5 64 reader 尾部**：`--index source_id`（不建 mag CSI）64 reader = **48.5 s**；
  其中 `ipix` CSI **10.6 s** + sort copy **8.2 s** + offsets 1.3 s + source_id CSI 5.5 s；
  parse/write 约 20 s。继续提升需要改排序/索引布局（例如 CSR row-id），而非加 reader。
- **M5.4 profiling（16 reader，64 分片，32.9M 行）**：
  - 每个 reader 的 wall ≈ 50 s：**parse 34.5 s + build/coerce 13.2 s**；
    shared-memory copy 0.06 s、free-slot wait <0.001 s、queue put <0.001 s；
  - writer：**等待 49.3 s、`table.append` 2.1 s**、free_slot put 0.007 s；
  - sort 18.6 s + offsets 1.4 s + CSI 12.0 s；
  - cProfile（498,386 行单分片）：`iter_rows` 9.1 s（gzip 2.5 s）、
    `_make_text_array` 5.1 s、`_coerce` 4.1 s、`ang2pix` 0.06 s；
  - 结论：ring 不是瓶颈；**parse 和 build（尤其 `_coerce`）是 reader 主成本，
    sort+CSI 是固定尾部**。
- **M5.6 CSR layout（吞吐优先）**：64 个 GDR3 ECSV 分片、32,897,902 行、core 14 列；
  `--layout csr --index source_id`：
  4/8/16/64 reader = **181.4 / 106.0 / 58.3 / 25.7 s**；
  实际 CPU约 **3.8 / 7.3 / 13.3 / 36.6 核**；输出 4.45 GB 无压缩 + 264 MB row-id；
  同条件 sorted `spatial` 64 reader 为 45.9 s（sort 18.8 + offsets 1.3 + CSI 5.5）。
  同一 424k 行天区：`spatial` 1° 锥 50–64 ms、盒 43 ms；
  CSR 1° 锥 **115–133 ms**、盒 119 ms；`source_id` 两者约 8–9 ms。
  CSR 适合“先快速落盘、后续再整理”，**不是天区查询核心**；`spatial` 仍是默认。
- **M5.7 天区访问（spatial 核心）**：64 个 GDR3 分片、32,897,902 行、core、
  `source_id` 索引；12/12/6 个落在源表中的随机中心，查询含 HDF5 open：
  - **1′**：中位 **8.6 ms**，P95 10.5 ms；中位 644 行（23–865）；
  - **1°**：中位 **116 ms**，P95 273 ms；中位 1,115,154 行（17,949–2,646,918）；
  - **10°**：中位 **275 ms**，P95 797 ms；中位 2,808,933 行（1,569,075–7,878,665）；
  - 结果均为精确 `ra/dec` 锥，spatial 连续区间读；1′ 主要受 fixed/open 开销影响，
    1°/10° 主要受该天区实际行数影响。数据在 page cache 中。
- **M5.12 通用交叉证认**：`crossmatch` HDF5 源表最近邻；
  单位球三维网格索引、3″ 半径、HDF5/CSV 输出；测试覆盖 brute-force 一致性。
- **M5.11 缺 G 源 v2**：`spectral-cube --no-g-supp no_g_supp.h5`；
  5,455,339 个缺 G 源中 3,848,128 有 RP，使用 RP-only 恒星回退或 QSO/星系模板；
  1,607,211 无 G/BP/RP，仅保留 count、flux=0、quality=7；v2 文件：
  `/mnt/data/huo/Datasets/Gaia/gdr3/spectral/gaia_dr3_spectral_n2048_v2.h5`；
  分析见 `SPECTRA-002-no-g-sources.md`。
- **M5.10 光谱立方 Phase 1**：`spectral-cube` 从 core/spatial 表流式生成逐像素 343 点立方；
  已生成 nside 2048、50,331,648 像素、343 点、**69.9 GB** float32：
  `/mnt/data/huo/Datasets/Gaia/gdr3/spectral/gaia_dr3_spectral_n2048.h5`；
  行数 1,811,709,771，count 和一致，flux 全 finite；当前无 XP/GSP-Phot，使用 BP-RP 黑体模板，
  全部标记 `inferred/quality=D`，`missing_bp_rp=270,939,282`、`missing_g=5,455,339`；
  任务书 `SPECTRA-001`。
- **M5.9 HEALPix bincount**：`hpxmap` 支持 count/sum/mean/weighted_mean、任意 nside、表达式定义物理量；
  全量 GDR3 `count` nside 512：25 MB FITS，和 = 1,811,709,771，51 s。
- **M5.8 全量 GDR3 core/spatial**：`/mnt/data/huo/Datasets/Gaia/gdr3/consolidated/gaia_dr3_core_spatial.h5`
  - 1,811,709,771 行 × core 14 列 + ipix；**404.7 GB**（377 GiB）；
  - 96 reader，**3867.7 s（64.5 min）**；QC 288/288；
  - `spatial`、order 9、`source_id` CSI（不建 mag CSI）；manifest 442 KB；
  - 全表锥查询（hierarchical candidate，非全像素扫描）：
    1′ **10 ms**、1° **21 ms**、10° **1.15–1.22 s**（该中心 975k 行）。
- v0.2（M5 后补，裁决七）：kernels 底座资产管理——`~/.config/oasis/kernels.yaml` ＋
  store `/Volumes/ArecaStudio/Datasets/SPICE Kernels/`（生态数据区命名约定）＋ `kernels`
  命令族（并行取件/校验/投送+manifest）；首件 de442／de440／naif0012／pck00011 已官方校验登记（de441 已取件，3.3 GB）；
- v0.2 计划（M5 候选）：Web 端 mirror/sync 动作与预览、Web 整文件下载与 fmt.columns_ref、
  多文件镜像（清单驱动）、ssh 目标的实测接线（saturn/enceladus 上线后）。
