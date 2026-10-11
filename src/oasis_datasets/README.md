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
    [--region cone:RA,DEC,R_DEG] [--attributes A,B,C] [--limit N] [--apply]
                                                          # 应用侧整合（PyTables 工作集；两档：整目录/天区×属性裁剪）
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
  工作集（列名齐备、blosc、CSI、attrs 带 epoch/frame；manifest 记来源/参数/QC）；
  已验格式：Gaia 档（CSV+表头）／2MASS（pipe+SQL schema）／TIC（无表头+bracket 头）；
  锥面查询毫秒级；
- v0.2（M5 后补，裁决七）：kernels 底座资产管理——`~/.config/oasis/kernels.yaml` ＋
  store `/Volumes/ArecaStudio/Datasets/SPICE Kernels/`（生态数据区命名约定）＋ `kernels`
  命令族（并行取件/校验/投送+manifest）；首件 de442／naif0012／pck00011 已官方校验登记（de441 未取）；
- v0.2 计划（M5 候选）：Web 端 mirror/sync 动作与预览、Web 整文件下载与 fmt.columns_ref、
  多文件镜像（清单驱动）、ssh 目标的实测接线（saturn/enceladus 上线后）。
