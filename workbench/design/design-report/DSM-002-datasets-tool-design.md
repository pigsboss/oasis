# 设计：datasets 管理工具（DSM-002）

- 编号：DSM-002　版本：v1.0（**已审查通过**，2026-10-11；进入开发 M1）　编制：设计开发
- 依据：RA-001 v1.0（验收通过）；取代并扩展 DSM-001（v0.1 工具设计）
- 审查说明：§7 列出 7 个**设计决策点**，请在审查时逐条裁决；其余为实现细节。
- 接口详设（配置文件族逐字段规范 + CLI 命令树 + Web API）见 `DSM-003-interface-design.md`，**与本文同属本次设计审查包**。

## 1. 架构总览

```
        ┌──────────── 单一事实源（磁盘）────────────┐
        │ ~/.config/oasis/  inventory.yaml          │ 清单（唯一作用域）
        │                   review-log.jsonl        │ 审核记录（追加式）
        │                   config.yaml             │ storages / nodes / store_root
        │ ~/.local/state/oasis/tasks/<id>/…         │ 运行态：task.json/events.jsonl/out.log
        └───────────────────────────────────────────┘
                              ▲ 读写
   ┌────────────── 内核 kernel（src/oasis_datasets）──────────────┐
   │ inventory · probe · mirror · sync · slice_export · storage_view · tasks │
   └──────────────────────────────────────────────────────────────┘
            ▲ 薄适配层                          ▲ 薄适配层
   CLI（tools/oasis-datasets）        Web（stdlib ThreadingHTTPServer + htmx + SSE）
```

原则：**CLI 与 Web 共用内核**；**长任务在子进程执行**（UI 重启不丢任务）；一切状态落盘。

## 2. 数据模型（三份文件）

### 2.1 清单 `~/.config/oasis/inventory.yaml`（唯一作用域）

```yaml
inventory_version: "0.1"
datasets:
  - id: gaia_dr3
    title: "Gaia DR3 gaia_source"
    publisher: "ESA / Gaia DPAC"
    licence: {name: "Gaia data licence", url: "https://www.cosmos.esa.int/web/gaia-users/credits"}
    fmt: {type: "ecsv.gz", files: 3386, size_hint: "~700 GB"}
    storage_pref: [raid5_archive, zfs_nas]
    status: active
    channels:
      - {id: areca_local, protocol: file, path: "/Volumes/ArecaStudio/Datasets/Gaia/gdr3/gaia_source",
         checksum: {manifest: "_MD5SUM.txt", format: md5sum, content: auto},
         version_rule: checksum_mtime}
      - {id: esa_archive, protocol: https, url: "https://gea.esac.esa.int/archive/…", priority: 2}
proposals: []        # 待审提案（清单外新数据集）
```

- 每条目 ≥1 channel；`checksum` 与 `version_rule` 驱动探测/校验/镜像；
- **派生品不入清单**（裁决①）；清单仅收纳发布型数据集。

### 2.2 审核记录 `~/.config/oasis/review-log.jsonl`（追加式）

`{ts, action: propose|approve|reject|deprecate, dataset, by, note}` —— 工具只 append；逐行 JSON 校验。

### 2.3 运行态与产品记账

- 任务：`~/.local/state/oasis/tasks/<task_id>/`：`task.json`（type/params/state/pid/时间戳/result）、
  `events.jsonl`（SSE 数据源）、`out.log`；
- 产品：沿用 `manifest.json` 协议 + 新可选头块
  `product: {kind: mirror|sync|slice, source_dataset, params, generated_by}`（向后兼容）。

## 3. 关键机制

### 3.1 渠道探测与版本确定（probe.py）

| 协议 | 探针 |
|:--|:--|
| https | HEAD/Range 0-0（状态/延迟/Range 支持）+ 可选小样本带宽 |
| file | 存在性/可读性/容量 |
| ssh | `ssh -o BatchMode=yes host true` + `rsync --version` |

版本规则：`last_modified`（HTTP）/`etag`/`checksum_mtime`（校验清单 mtime，如 gdr3）/`release`（人工字段）。
输出结构化 JSON → CLI 表格 + Web 徽章。

### 3.2 远程镜像（mirror.py）

- 单文件：`oasis-datasets mirror <ids...> --to <storage>`（默认 dry-run 计划：HEAD 探测 + 目的路径）；
  下载按 `Accept-Ranges` 且 ≥8MB 时 N 路 Range 并行分片，`.partN` 断点续传（服务端忽略
  Range 时自动重下该片），未知长度单流兜底；
- **多文件**（如 gdr3 3386 块）：以官方校验清单为文件列表，逐文件下载 + 校验
  （复用 `checksums.py` 的语义校准）；**并行 N workers（pfetch 模式：池+重试）**；
  增量：远端版本未变 → 全跳过（M5 候选，当前首批为单文件场景）；
- 目标版式：`<storage.path>/oasis-datasets/<dataset_id>/<version>/`（version 来自 Last-Modified，
  形如 `20261010T135037Z`）；完成后 sha256 + 产品 manifest（商店协议 + `product` 头块）；
- 实测：MPCORB 93.5MB @ 16.7MB/s（8 路），sha256 与独立商店副本一致；部分预置分片续跑后字节一致。

### 3.3 本地存储设备间同步（sync.py 扩展）

- 本机 rsync（v0.1 既有）+ **ssh 目标**（storages/nodes 别名，`host:path` 传输；远端先
  `ssh mkdir -p`（老 rsync 无 `--mkpath`），dry-run 不触远端写）；
- 安全：dry-run 默认、`--apply`、永不 `--delete`。

### 3.4 切片导出（slice_export.py）

声明式规格（YAML 片段，落 `~/.config/oasis/slices/`）：

```yaml
id: gaia_t1
source: gaia_dr3
filter: {column: phot_g_mean_mag, op: le, value: 6.0}
columns: [source_id, ra, dec, parallax, pmra, pmdec, phot_g_mean_mag, bp_rp, phot_bp_mean_mag, phot_rp_mean_mag]
output: {storage: raid0_scratch, path: "catalogs/gaia/t1"}
determinism: {sort_by: source_id, gzip_mtime: 0}
```

- 引擎：**per-chunk 并行 map**（解析→过滤→写 per-chunk 临时 CSV.gz，mtime=0）
  → 按 chunk 序号**有序拼接**（多成员 gzip；表头以独立首成员写入一次，`gzip -d` 兼容，
  字节级确定性）→ 计数 QC + 抽样回源（记录来源 chunk+行号）+ manifest + CREDITS.txt；
- 断点续跑：per-chunk 完成记账（暂存区 `chunks.jsonl` 含 sha256 校验，跨任务可续；
  任务目录留副本），中断续跑跳过已完成块；`--chunks M-N` 支持部分块运行（manifest 记 partial）；
- 三档共享**单遍扫描**（一次解析，按门限分流）。

### 3.5 文件系统视图（storage_view.py，追加需求）

- 数据源：`/Volumes` 枚举 + `os.path.ismount` + `shutil.disk_usage` + 可写性检查；
  外部设备状态补充 `diskutil list`（区分**未接入**）；
- 状态机（每行）：**已挂载**（路径存在且为挂载点）/ **已接入未挂载**（diskutil 可见、无挂载点）/
  **未接入**（配置有、两处皆无）/ **未注册**（/Volumes 有、配置无，提示可 propose）；
- 列：状态徽章、容量/已用/可用、读写权限、已知产品存在性（`oasis-datasets/<dataset_id>/`）；
- ssh 目标（NAS）：显示"未探测/在线/离线"，**按需按钮触发**（不自动 ping）；
- 入口：CLI `storages` 子命令 + Web `/storages` 页（SSE 刷新）。

### 3.6 任务引擎（tasks.py）

- 长任务**子进程**执行（`python -m oasis_datasets._runner <task.json>`）；父进程仅启动与监视；
- 事件流 `events.jsonl` 追加；CLI `tasks watch` 与 Web SSE **同源**；
- 任务类型：probe / mirror / sync / slice；均记录参数、状态、结果与退出码。

### 3.7 Web（web/，栈已确认：方案 A）

- 后端：`ThreadingHTTPServer`（JSON 端点 + SSE + 静态文件）；模板用 `string.Template` 片段（零依赖）；
- 前端：htmx **本地内置**（开发时一次性 vendor，记录 sha256）；原生 JS 少量；
- 页面：`/` 概览（渠道健康/版本/运行中任务）、`/inventory`（清单+审核收件箱）、
  `/storages`（文件系统视图）、`/tasks`（任务卡+日志尾随）、`/logs`；
- 安全：仅绑定 127.0.0.1；变更动作一律 **dry-run 预览 → 一次性确认令牌** 执行；审计留痕与 CLI 同源。

### 3.8 配置迁移（设计决策点①）

- 新模型：`inventory.yaml`（清单）与 `config.yaml`（storages/nodes/store_root）分家；
- 迁移映射：现 `config.datasets` 的 areca 6 条 + mpc → inventory；`oasis_store` **移出清单**
  （它是产品区，不是发布型数据集）；
- 迁移时 `storage_pref` 取候选序 ∩ `config.storages[].id`（本地：`[raid5_archive, zfs_nas]`；
  远程：`[macbook_ssd, zfs_nas]`），保证 V-02 通过；
- 兼容：工具优先读 inventory，缺省回退旧 `config.datasets`（一个版本周期）；
  提供 `oasis-datasets migrate-config` 一次性迁移并生成审核记录。

### 3.9 MPC 根数解析（mpcorb.py，UR-OASIS-02 批次 2）

- `oasis-datasets mpc parse [--raw|--dest|--limit|--apply]`：`MPCORB.DAT.gz`（定宽 202 列，
  列位经实测核对）→ `mpc_elements.csv.gz`（20 列：`designation, readable, H, G, epoch, M,
  argp, node, incl, e, n, a, q, U, category, n_obs, n_opp, arc, rms, last_obs`）；
- 原始数值透传、行序=文件序、gzip `mtime=0` → 字节级可复现（实测重跑 sha256 一致）；
- `epoch`：packed（`K2669`）转 ISO（`2026-06-09`），**逐行**（少数陈年对象保留旧历元）；
  `designation` 为 MPC packed（≥100000 用字母制，如 `D4340`=Pluto）；
- 类别规则 v1（消费端可在 a/e/q 上自筛）：NEO `q<1.3` / TNO `a>30.1` /
  Centaur `5.5<a<30.1` / MBA `2.0≤a≤3.2` / other（含木星特洛伊 `a≈5.2`）；
- 产品 manifest：逐行 epoch 语义、`epoch_range`、`frame=heliocentric ecliptic J2000`、
  类别统计、抽样回源 QC；实测 1,571,791 行 / 23 s；
- CSV 产物的**可选 HDF5 rendition**：`oasis-datasets hdf5 <csv.gz>`（`/table` 复合数据集、
  65536 行分块 + gzip、定宽 UTF-8 串、`track_times=False` 字节可复现、回读校验；
  交付侧以 manifest `renditions` 数组登记；canonical 仍为 CSV.gz）。

## 4. 实施分期（v0.2 修订：Web 配置工具提前）

| 期 | 内容 | 验收映射 |
|:--|:--|:--|
| M1 | 内核+清单+`migrate-config`（从既有配置**零手写**生成初始清单）+validate+probe+`storages` 视图（CLI） | A-01/02/03/09 |
| M2 | **Web 基础 + 配置工具**（清单/存储/切片三编辑器 + 审核收件箱 + 文件系统视图页） | A-07（部分） |
| M3 | 切片导出：Gaia T1/T2/T3（含 Web 计划预览与任务卡） | A-06 |
| M4 | 镜像（多文件并行）+ ssh 同步 + Web 任务监控/日志完善 | A-04/05 |
| M5 | **应用侧 consolidate**：整目录整合（PyTables 工作集＋CSI）／天区×属性裁剪整合（＋可选 HealPix 瓦片分片） | F-09/F-10 |

- 修订理由（用户设计审查意见）：配置文件复杂度过高 → **配置工具先于任务功能落地**；
- 配置工具设计详见 `DSM-003 §10`；
- M5 修订（用户提出，2026-10-11）：天区分片导出与 HDF5 切片导出为**目标层高级功能**，
  设计增补见 `DSM-003 §5.1`（待审查）。

## 5. 测试计划（映射）

- 单元：checksums 校准（既有）、probe 解析、inventory 校验/审核状态机、slice 过滤器与排序确定性；
- 集成：Gaia 三档实跑（断点续跑演练：中断一次再续）；gdr3 单块镜像演练；ssh 目标到 NAS 演练；
- 验收：A-01…A-09 逐条记录（TV 报告）。

## 6. 风险

| 风险 | 缓解 |
|:--|:--|
| gdr3 全量镜像 700 GB 耗时 | 增量+并行；优先单块演练；夜间调度（mini） |
| 多成员 gzip 兼容性 | 标准 gzip 支持多成员；测试 `gzip -t`/`zcat`/`gunzip` 全链路 |
| htmx vendoring 需一次外网下载 | 下载后 sha256 入库；备选：内置最小 JS 替代 |
| inventory 迁移一次性成本 | migrate-config 脚本 + 回退读旧配置一个版本周期 |
| 长任务子进程管理 | 状态落盘 + PID 记录；`tasks` 命令可列出/清理孤儿任务 |

## 7. 设计决策点（请审查时逐条裁决）

1. **清单独立文件 + 迁移方案**（3.8）：inventory.yaml 与 config.yaml 分家，oasis_store 移出清单；
2. **确定性实现**（3.4）：per-chunk 临时 gz + 有序拼接（多成员 gzip）vs 单写压缩；
3. **任务模型**（3.6）：子进程 + 文件事件流；
4. **模板选型**（3.7）：`string.Template`（零依赖）vs Jinja（多一依赖）；
5. **分期顺序**（4）：M1→M4 如上，Web 是否提前；
6. **镜像目标版式**（3.2）：`oasis-datasets/<dataset_id>/<version>/`；
7. **审核记录**（2.2）：JSONL 追加式格式。
