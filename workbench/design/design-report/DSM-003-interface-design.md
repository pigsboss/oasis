# 接口设计：datasets 管理工具（DSM-003）

- 编号：DSM-003　版本：v1.0（**已审查通过**，2026-10-11；含配置工具增补）　编制：设计开发
- 依据：RA-001 v1.0、DSM-002（架构与机制）；本文为其**接口专篇**（配置文件族 + CLI + Web API）
- 审查范围：与 DSM-002 一并审查；§9 列出接口层的重点裁决点

## 1. 接口总览与通用约定

| 类 | 接口 | 形态 |
|:--|:--|:--|
| 配置族 | `inventory.yaml`、`review-log.jsonl`、`config.yaml`、`slices/<id>.yaml` | 人写/工具读写（UTF-8） |
| 运行态 | `tasks/<id>/{task.json, events.jsonl, out.log}`、产品 `manifest.json` | 工具读写 |
| 命令 | CLI 命令树（§6） | 终端 |
| 网络 | Web HTTP/JSON/SSE（§7） | 本机 127.0.0.1 |

通用约定：

- 路径支持 `~` 展开；时间一律 ISO 8601 UTC（`…Z`）；id 规范：`^[a-z0-9_]+$`；
- **严格校验**：未知字段报错；预留 `x-` 前缀字段为扩展位（前向兼容）；
- 每个文件携带版本字段；主版本不兼容变更需迁移脚本；
- 全部配置可 `validate` 校验（CLI 与 Web 同源）。

## 2. `~/.config/oasis/inventory.yaml`（清单，唯一管理作用域）

**清单纳入准则（2026-10-11 用户审定）**：只收**发布型 catalogue**——具有明确发布渠道
（机构/档案服务）的数据产品（本卷口径即：Gaia DR 系列、AllWISE、2MASS PSC、TESS TIC）；
**不纳入**：本地渲染件、公众传播媒体、测绘自采数据等非发布型资料；派生品不入清单（既有规则）。
（配套：SPICE **kernels 底座资产**亦不入本清单——以平行注册 `kernels.yaml` 管理，见 DSM-004 §6 裁决七。）

### 2.1 完整示例

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
    added: "2026-10-11"
    added_by: "owner"
    channels:
      - id: areca_local
        protocol: file
        path: "/Volumes/ArecaStudio/Datasets/Gaia/gdr3/gaia_source"
        checksum: {manifest: "_MD5SUM.txt", format: md5sum, content: auto}
        version_rule: {type: checksum_mtime}
      - id: esa_archive
        protocol: https
        url: "https://gea.esac.esa.int/archive/"
        version_rule: {type: last_modified}
    notes: "分片按 source_id 区间；npy 侧车需显式 dtype"
  - id: mpcorb
    title: "MPCORB 轨道根数"
    publisher: "Minor Planet Center"
    licence: {name: "MPC Copyright", url: "https://www.minorplanetcenter.net/iau/info/Copyright.html"}
    fmt: {type: "fixed-width text (gzip)", files: 1, size_hint: "~93.5 MB"}
    storage_pref: [macbook_ssd, zfs_nas]
    status: active
    channels:
      - id: mpc_https
        protocol: https
        url: "https://www.minorplanetcenter.net/iau/MPCORB/MPCORB.DAT.gz"
        version_rule: {type: last_modified}
proposals:
  - id: new_dataset_example
    title: "示例提案"
    publisher: "…"
    licence: {name: "…", url: "…"}
    channels:
      - {id: c1, protocol: https, url: "https://…", version_rule: {type: last_modified}}
    reason: "用户侧渲染需要 …"
    proposed_at: "2026-10-11T00:00:00Z"
    proposed_by: "owner"
```

### 2.2 dataset 字段表

| 字段 | 类型 | 必需 | 默认 | 约束 |
|:--|:--|:--|:--|:--|
| `id` | str | 是 | — | `^[a-z0-9_]+$`，全局唯一（含 proposals） |
| `title` | str | 是 | — | 非空 |
| `publisher` | str | 是 | — | 机构/个人 |
| `licence` | map | 是 | — | `{name: str≥1, url: str(URL)}`；`url` 为空串时**告警不报错**（迁移期待补） |
| `fmt` | map | 否 | — | `{type: str, files: int≥1, size_hint: str}` |
| `storage_pref` | list[str] | 否 | `[]` | 元素必须存在于 `config.storages[].id` |
| `status` | enum | 是 | `active` | `active` / `deprecated` |
| `added` / `added_by` | str | 否 | — | approve 时自动写入 |
| `channels` | list | 是 | — | 长度 ≥1（见 2.3） |
| `notes` | str | 否 | — | 描述性 |
| `x-*` | any | 否 | — | 扩展位（工具忽略） |

### 2.3 channel 字段表

公共：`id`（str，必填，条目内唯一）、`protocol`（enum：`file|https|ssh`，必填）、`notes`（可选）、
`checksum`（可选：`{manifest: str, format: auto|md5sum|sha256sum, content: auto|compressed|decompressed}`）、
`version_rule`（必填：`{type: last_modified|etag|checksum_mtime|release|none, value?: str}`）。

| protocol | 必填专有字段 | 说明 |
|:--|:--|:--|
| `file` | `path` (str) | 本机/本节点可见路径 |
| `https` | `url` (str, https) | 单文件端点或清单端点 |
| `ssh` | `host` (str)、`path` (str) | ssh 别名/主机 + 远端路径（rsync 可达） |

**优先级 = 列表顺序**（此前草案的 `priority` 字段取消）。

### 2.4 proposal 字段表

在 dataset 字段（除 `status`/`added*`）之外：`reason`（str，必填）、`proposed_at`（str，工具写入）、
`proposed_by`（str，工具写入）。approve 时：移入 `datasets`、置 `status=active`、写 `added/added_by`、追加 review-log。

### 2.5 校验规则（`inventory validate`）

| # | 规则 |
|:--|:--|
| V-01 | id 全局唯一；channel id 条目内唯一；id 匹配 `^[a-z0-9_]+$` |
| V-02 | `storage_pref ⊆ storages.ids`（跨文件校验） |
| V-03 | 每 dataset ≥1 channel；protocol 专有字段齐备；https 必须 `https://` |
| V-04 | `version_rule.type` 为枚举值；`release` 型须带 `value` |
| V-05 | 未知字段（非 `x-` 前缀）一律报错 |
| V-06 | proposals 与 datasets id 不冲突 |

告警（WARN，不阻断）：`licence.url` 为空；迁移生成的 `x-source-format` 等 `x-` 扩展字段不作校验。

## 3. `~/.config/oasis/review-log.jsonl`（v0.2 修订：通用审计流）

每行一个 JSON 对象（UTF-8，追加式；工具**只 append**）：

| 字段 | 类型 | 必需 | 说明 |
|:--|:--|:--|:--|
| `ts` | str | 是 | ISO 8601 UTC（工具写入） |
| `action` | enum | 是 | `propose` / `approve` / `reject` / `deprecate` / **`edit`** |
| `target` | str | 是 | 目标引用 `<kind>:<id>`，kind ∈ `dataset|storage|node|slice|config`（v0.2 由原 `dataset` 字段泛化） |
| `by` | str | 是 | 操作主体（单用户＝`owner`） |
| `note` | str | 否 | 审核意见/理由（`edit` 时填改动摘要） |

校验：`review-log validate` 逐行 JSON 解析；损坏报错且**不自动改写**。
（`edit` 记录由 Web 配置工具的受控写入产生，见 §10。）

## 4. `~/.config/oasis/config.yaml`（系统配置，正式化）

| 字段 | 类型 | 必需 | 说明 |
|:--|:--|:--|:--|
| `oasis_config_version` | str | 是 | 如 `"0.1"` |
| `store_root` | str(path) | 是 | 产品区根（默认 `~/oasis-catalog-store`） |
| `storages` | list | 是 | 见 §4.1 |
| `nodes` | list | 否 | 见 §4.2 |
| `datasets`（旧） | list | 否 | **deprecated**：迁移后仅供一个版本周期回退读取 |

### 4.1 storages 条目

| 字段 | 类型 | 必需 | 约束 |
|:--|:--|:--|:--|
| `id` | str | 是 | `^[a-z0-9_]+$`，唯一 |
| `class` | enum | 是 | `hot`/`scratch`/`archive`/`shared`/`portable` |
| `node` | str | 否 | 引用 `nodes[].id` |
| `access` | map | 是 | `protocol`（或 `protocols[]`：`file`/`smb`/`ssh+rsync`）+：`file` 需 `path`（**`class: portable` 除外**：挂载点非常驻，运行期经 `--to-path` 指认）；`smb`/`ssh+rsync` 需 `host`（`smb` 可附 `share`） |
| `io` / `role` / `notes` | str | 否 | 描述性 |

### 4.2 nodes 条目

`id`、`title`、`role`（描述）、`access: {protocol: local|ssh, alias?}`。

### 4.3 跨文件引用（与 inventory 联检）

`inventory.storage_pref ⊆ config.storages.ids`；`config.storages.node ⊆ config.nodes.ids`。

## 5. `~/.config/oasis/slices/<id>.yaml`（切片规格）

```yaml
id: gaia_t1
source: gaia_dr3                 # 必须为 inventory 清单内数据集
channel: areca_local             # 可选：优先渠道；缺省=按渠道顺序取首个可用
select:                          # 条件列表（AND）；空列表=全量
  - {column: phot_g_mean_mag, op: le, value: 6.0}
columns: [source_id, ra, dec, parallax, pmra, pmdec,
          phot_g_mean_mag, bp_rp, phot_bp_mean_mag, phot_rp_mean_mag]
output: {storage: raid0_scratch, path: "catalogs/gaia/t1", filename: "gaia_t1.csv.gz"}
determinism: {sort_by: source_id, gzip_mtime: 0}
qc: {sample: 8, source_trace: true}
execution: {parallel: 8, resume: true}
```

| 字段 | 类型 | 必需 | 默认 | 约束 |
|:--|:--|:--|:--|:--|
| `id` | str | 是 | — | 与文件名一致，唯一 |
| `source` | str | 是 | — | inventory 数据集 id |
| `channel` | str | 否 | 首个可用 | 该数据集 channel id |
| `select[]` | list[map] | 否 | `[]`（全量） | 见下表 |
| `columns` | list[str] | 是 | — | 非空；须为源列子集（源列以该渠道校验清单/表头为准） |
| `output` | map | 是 | — | `storage`（storages.id）或 `to_path`；`path` 相对 storage 根；`filename` 默认 `<id>.csv.gz` |
| `determinism` | map | 否 | 见默认 | `sort_by`（默认 `source_id`）、`gzip_mtime`（默认 0） |
| `qc` | map | 否 | `{sample: 8, source_trace: true}` | 抽样回源 |
| `execution` | map | 否 | `{parallel: 8, resume: true}` | 并行度、断点续跑 |

`select` 条目：`column`（str，必填）、`op`（enum：`le|lt|ge|gt|eq|ne|between|in`，必填）、
`value`（number / `[lo,hi]`（between）/ list（in））。

**确定性前提**：要求源按 `sort_by` 列分块有序（gdr3 满足）；若源无序，引擎需全局排序
（设计标注为限制，报错提示而非静默产出）。

**实现注记（v1.0 首验）**：① 输出的 `path` 相对 storage 根（如 `raid0_scratch` +
`catalogs/gaia/t1` → `/Volumes/DWB/catalogs/gaia/t1/`）；② 多成员 gzip 的表头由装配器以
独立首成员写入一次（数据块成员一律无表头），任意块选择的断点续跑拼接后 `zcat` 均为单表头；
③ `slice run --chunks M-N` 支持部分块运行（估算/测试），manifest 记 `partial: true` 与块区间；
④ 分块记账随暂存区（`dest 旁 .oasis-staging/<spec>/chunks.jsonl`，含 sha256 校验，跨任务可续），
任务目录留 `slice-chunks.jsonl` 副本。

### 5.1 高级导出增补（F-09 天区分片 / F-10 HDF5 切片；**待审查**）

**架构修订（用户方向，2026-10-11：固化优先）**：任一目录（任意格式）先**一次性固化为 HDF5 表**
（profile 驱动解析 → 复合表：列名齐备、chunked＋压缩、attrs 携 epoch/frame/provider/profile，
按 sort_key 建区间索引），此后**导出 = 天区条件 × 属性列表**（二维）→ HDF5 和/或 CSV.gz + manifest；
**固化产物跟随应用工作区**（哪个应用需要就放哪个工作区，不设全局 core 目录）。
本节 `in_cone/in_box` 与 `format: hdf5` 即在该链上实现；雏形实测：锥面条件直接可算、
T2（17.7 万行）全扫 0.12 s、区间索引点查 ~0.65 ms/次、固化 1.5 s/17.7 万行；
瓦片分片（healpix/native）保留为**输出组织选项**。**固化栈已定**（DSM-004 §6 裁决五，用户裁定：
应用侧固化＝PyTables；交付锚点＝CSV.gz；可移植 rendition＝h5py 维持现状）；**定位＝应用侧
consolidate**（FCP 语义；整目录整合 ／ 天区×属性裁剪整合 两档，见 DSM-004 §6 裁决六）；
锥面条件与区间索引**自研**（不引用外部小工具）。

**规格扩展**（§5 的向后兼容增量）：

```yaml
id: gaia_region_x
source: gaia_gdr3_gaia_source
select:
  - {column: phot_g_mean_mag, op: le, value: 15.0}
  - {op: in_cone, value: {ra: 280.0, dec: -25.0, radius: 2.0}}   # 或 in_box: {ra: [lo,hi], dec: [lo,hi]}
columns: [source_id, ra, dec, phot_g_mean_mag, bp_rp]
output:
  storage: raid0_scratch
  path: catalogs/gaia/region_x
  format: [csv.gz, hdf5]            # 默认 [csv.gz]；hdf5 为一等输出格式
  shard: {scheme: healpix, nside: 64}   # 可选；缺省不分片（none）
```

| 增量 | 语义 |
|:--|:--|
| `select` 空间算子 `in_cone`/`in_box` | 作用于 `ra/dec`（deg；表须含这两列）；锥含 `radius`，矩形含 `ra/dec` 区间 |
| `output.format` | `csv.gz`（canonical，字节可复现语义不变）与/或 `hdf5`（一等格式） |
| `output.shard` | `healpix`（RING；`nside` 默认 64≈0.92°）或 `none`；分片输出 `tile_<ipix>.{csv.gz,h5}`，manifest 增 `tiles` 数组（ipix/行数/bytes/sha256/边界） |
| HDF5 索引（F-10） | `/table` 复合数据集（既有 rendition 语义）＋ **区间索引**：每 chunk 的 `source_id` min/max 独立数据集，区间定位 O(log n)；行序与 CSV 一致；`track_times=False` 字节可复现 |

**引擎复用**：单遍扫描 ＋ per-chunk 并行 ＋ 断点续跑（M3 既有）；瓦片指派在 map 阶段完成
（每行由 `ra/dec` 直接算 ipix），装配阶段按瓦片有序拼接；QC 增补：**Σ瓦片行数=总行数**、
抽样点几何回验（点→瓦片号一致性）。CLI：`slice run` 支持上述字段；`hdf5` 命令升级为
带列选择/谓词/索引的导出路径（保留原转换语义）。

**实现注记（M5 首验，2026-10-11）**：`oasis-datasets consolidate` 已落地——内置 profile
（`gaia_tier` / `tess_tic` / `twomass_psc`；支持 YAML 自定义）；**表头源的类型注解**
（TIC bracket、2MASS SQL DDL）用于钉住列类型（首验即抓到 `ndet` 零填充字符串被数据推断
误判为 int——schema hint 修复，43/115 列被钉住）；产物 `<app>/consolidated/<name>.h5` +
manifest（来源/参数/行数/sha256/QC/partial 标记）；QC 抽样回读逐列比对（前 3 行）。
实测：Gaia T2 17.7 万行 5 s（含 CSI）；2MASS 单分片 30 万行 26 s；TIC 单片 20 万行 29 s；
应用侧锥面查询：T2 0.01 s、TIC 0.36 s（含属性子集）。

**默认建议（待审查确认）**：① 分片方案 **HEALPix-RING**（天文惯例；如需矩形网格可改）；
② hdf5 索引先做 `source_id` 每 chunk min/max（大表空间索引留待需要）；
③ 天区算子依赖表内 `ra/dec` 列——MPC 根数表无位置列，其对象的天区筛选需消费侧先做位置
传播后另行提出导出，不在本期。

## 6. CLI 命令树

| 命令 | 参数/选项 | 行为 | 退出码 |
|:--|:--|:--|:--|
| `list [ids...]` | — | 清单概览（含渠道健康摘要） | 0/1 |
| `inventory validate` | — | 校验（V-01…V-06 + 跨文件引用） | 0/2 |
| `propose <spec.yaml>` | — | 提交提案（写 proposals + review-log） | 0/2 |
| `review list` / `review approve|reject <id>` | `--note` | 单人审核（移入/驳回 + 留痕） | 0/1/2 |
| `probe <ids...>` | `--channel id` | 探测 + 版本确定（本次输出） | 0/1 |
| `storages` | `--json` | 文件系统视图（CLI 版） | 0/1 |
| `mirror <dataset>` | `--to <storage>` `--channel id` `--apply` | 远程→本地镜像（默认 dry-run 计划） | 0/1 |
| `sync <dataset 或产品>` | `--to <storage>` 或 `--to-path DIR` `--apply` | 本地跨设备同步（既有，扩展 ssh） | 0/1 |
| `slice list` / `slice run <ids...>` | `--chunks M-N` `--apply`（parallel 取自 spec.execution） | 切片导出（默认 dry-run 计划；组内共享 source 单遍扫描） | 0/1 |
| `tasks list|show|watch|cancel <id>` | `--follow` | 任务管理（watch=尾随事件） | 0/1 |
| `verify <refs...>` | `--sample N` `--full` | 校验清单/产品 sha256（既有） | 0/1/2 |
| `migrate-config` | — | 旧 `config.datasets` → `inventory.yaml` | 0/1/2 |
| `web` | `--port 8787` `--no-open` | 启动本机 Web（前台） | 0/1 |

兼容策略：`list/verify/sync` 保持既有语义；新命令一律"**默认 dry-run / 先计划后执行**"（只读命令除外）。

## 7. Web API（127.0.0.1，方案 A）

### 7.1 路由表

| 方法 | 路径 | 说明 |
|:--|:--|:--|
| GET | `/` `/inventory` `/storages` `/tasks` `/tasks/<id>` `/logs` | HTML 页面（htmx 片段） |
| GET | `/api/inventory` `/api/storages` `/api/tasks` `/api/tasks/<id>` | JSON 快照 |
| GET | `/api/events/<task_id>` | **SSE** 事件流（支持 `Last-Event-ID` 重放） |
| POST | `/api/actions/preview` | 入参 `{action, params}`；action ∈ `probe\|mirror\|sync\|slice\|edit.inventory\|edit.facilities\|edit.slice\|review.approve\|review.reject\|migrate` → 返回 `{plan, token, expires_at}`（表单编码时返回 HTML 片段：计划 + diff + Confirm 按钮） |
| POST | `/api/actions/execute` | 入参 `{token}` → 启动任务 → `{task_id}`；或执行受控写入（原子写+备份+审计） |
| POST | `/api/review` | 入参 `{op: approve\|reject, id, note, token（先经 preview 取得）}` → 与 CLI 同源留痕（实现注：受 §7.2 约束，review 同样走 preview→execute，token 绑定 op） |
| GET | `/static/*` | 静态资源（htmx 本地内置，sha256 记录） |

### 7.2 约束

- 仅绑定 `127.0.0.1`；无鉴权（单机单用户）；**所有变更动作必须 preview→execute**；
- `token`：一次性、绑定 params 哈希、TTL 10 分钟；
- SSE 事件 schema：`{seq, ts, task_id, type: state|progress|log|done|error, data}`；15s 心跳注释行；
  断线以 `Last-Event-ID` 从 `events.jsonl` 重放（与 CLI `tasks watch` 同源）。

## 8. 运行态与产品文件

- `task.json`：`{task_id, type, params, state, pid, created_at, started_at, ended_at, result, exit_code}`
  （state：`queued|running|done|failed|cancelled`）；
- `events.jsonl`：§7.2 事件对象逐行；
- `manifest.json` 扩展（向后兼容）：新可选头块
  `product: {kind: mirror|sync|slice, source_dataset, params, generated_by}`。

## 9. 接口层重点裁决点（请与 DSM-002 §7 一并裁）

1. **严格校验 + `x-` 扩展位**：未知字段报错（防隐性漂移），扩展须加 `x-` 前缀；
2. **优先级＝渠道列表顺序**（取消 `priority` 字段）；
3. **切片文件落 `~/.config/oasis/slices/`**，id=文件名，`select` op 集合如上；
4. **CLI/Web 一致性协议**：变更动作一律 preview→execute（Web 用一次性 token；CLI 用 dry-run 输出后 `--apply`）；
5. **任务/事件文件格式**（§8）作为 CLI 与 Web 的共同数据源。

## 10. 配置工具（Web 端配置编辑器，增补设计）

**定位**：把清单（datasets/channels/proposals）、存储与节点（storages/nodes）、切片规格（slices）
的编辑**表单化**——手写 YAML 从必须降为可选；**文件仍是唯一事实源**，GUI 是受控写入端。

### 10.1 通用机制

- **表单 ↔ YAML 双视图**：默认表单；"原始视图"只读预览实时生成的 YAML；"高级模式"允许直接编辑，
  保存前走同一**严格校验引擎**（与 CLI 同源）；
- **受控写入四步**：校验通过 → **diff 预览** → 一次性 token 确认 → **原子写（temp+rename）
  + 时间戳备份**（`.bak/<ts>`，保留最近 10 份）+ review-log 追加 `edit` 记录；
- **实时校验**：V-01…V-06 + 跨文件引用（`storage_pref`/`node` 下拉只列已登记项）；错误阻断保存；
- **并发防护**：打开时记录 mtime；保存前若 mtime 变化（如 CLI 同时改动）→ 提示重载，不覆盖；
- **导入/导出**：单条目 YAML 粘贴导入（propose 便捷通道）；整文件下载（备份/审阅）。

### 10.2 三个编辑页

| 页 | 路径 | 内容 |
|:--|:--|:--|
| 清单编辑器 | `/config/inventory` | dataset 表单 + **渠道子表**（协议切换字段：`file.path`/`https.url`/`ssh.host+path`；checksum 块；version_rule 下拉）；proposal 收件箱（同意/驳回+意见）；新增可选字段 **`fmt.columns_ref`**（列清单引用，如 `docs/references/gdr3_csv_header.txt`）→ 供切片编辑器的列下拉 |
| 存储与节点编辑器 | `/config/facilities` | storages/nodes 表单；与文件系统视图联动、**未注册设备一键"登记为存储"**（预填 path） |
| 切片编辑器 | `/config/slices` | source 下拉（清单内）→ 列多选（有 `columns_ref` 给建议列）→ 条件构造器（column/op/value）→ 输出（storage 下拉+path）→ determinism/qc/execution 默认折叠；保存到 `slices/<id>.yaml`；**"试跑"按钮**直接生成切片计划预览（复用 §7 preview 通道） |

### 10.3 迁移与审核

- 启动检测旧 `config.datasets` → 横幅"检测到旧配置，一键迁移"（先预览迁移结果，后写入 + 审计）；
- 准入/弃用仍走审核语义（propose/approve/reject/deprecate）；既有条目的**编辑**走 `edit` 审计，单人确认即可。

### 10.4 与 CLI 的关系

- 编辑以 Web 为主；CLI 保留 `inventory validate`、`migrate-config` 与（高级用户）直接编辑文件；
- 所有写入路径（Web/CLI/手工）最终受同一校验与审计约束。
