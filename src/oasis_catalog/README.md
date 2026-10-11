# oasis_catalog —— 目标层 · 源表（Catalogue）子系统

配置驱动的源表管理工具：按系统配置（datasets 注册表）**清点数据集与源表、下载/刷新远程源表、
按 manifest 校验（sha256）**。

## 配置解析顺序

1. `--config <path>`；
2. 环境变量 `OASIS_CONFIG`；
3. **`~/.config/oasis/config.yaml`（推荐，系统级）**；
4. 仓库内 `catalogues.yaml`（回退示例）。

## 配置结构（datasets 注册表）

```yaml
oasis_config_version: "0.1"
store_root: "~/oasis-catalog-store"        # 本地源表仓库（更新输出）

datasets:
  - id: <str>                  # 唯一标识
    title: <str>
    kind: local_volume | remote | local_store
    access:                    # 如何访问
      # local_volume / local_store:
      protocol: file
      path: /Volumes/...       # 或 ~/...
      # remote:
      protocol: https
      base_url: "https://..."
      auth: none
    provider: <str>            # 可选，供其 catalogues 继承
    licence: <str>             # 可选
    catalogues:                # 包含哪些源表
      - id: <str>
        title: <str>
        # remote（可更新；update 使用）：
        url: <str>
        target_dir: catalogs/...     # store_root 下相对目录
        # local（只读；list 检查存在性）：
        path: <str>                  # 相对 access.path
        format: <str>
        size_hint: <str>
        notes: <str>
```

## 命令

```bash
tools/oasis-catalog list                    # 清点 datasets/catalogues 与本地状态
tools/oasis-catalog update                  # 更新全部远程源表（If-Modified-Since 跳过未变化）
tools/oasis-catalog update mpc              # 按 dataset id 更新
tools/oasis-catalog update mpcorb cometels  # 按 catalogue id 更新
tools/oasis-catalog update --force          # 丢弃本地副本重下（仍支持断点续传）
tools/oasis-catalog verify [ids...]         # 按 manifest 校验 sha256
```

运行输出为英文（CODING_STANDARDS §2.2）；注释与文档可为中文。

## 目录约定与 manifest（store_root 下）

```
catalogs/mpc/elements/
├── MPCORB.DAT.gz
├── CometEls.txt
└── manifest.json     # 头：generated_at + target_dir
                      # 行：id | path | bytes | sha256 | version | epoch | provider | licence | source_url
```

- 断点续传：中断后重跑 `update` 自 `.part` 续传；
- 快照口径：`version`/`epoch` 取端点 `Last-Modified`（C0-RECON-001）；数据文件内部历元原样保留；
- 交付协议：目录/命名/manifest 即用户侧"只认 manifest"的消费约定（HDF5 等 rendition 问题按 ADR 边界另行评估）。

## 状态

- v0.1：系统配置（datasets 注册表）+ MPC（mpcorb/cometels）实跑通过；Gaia 分档导出器（C2b）与
  catalogue 子系统设计文档待补（workbench/design/design-report/C0-RECON-001.md 为侦察依据）。
