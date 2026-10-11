# 设计：datasets 数据集管理工具（DSM-001）

- 编号：DSM-001　版本：v0.1（2026-10-11）　编制：设计开发
- 服务目标：UR-2026-1012 的 UR-OASIS-07/08/09（交付形态/溯源/消费约定）在**原始数据集**侧的对应件
- 关系：与 `oasis_catalog`（源表更新与交付 manifest）正交——本工具管"原始数据集"本身

## 1. 目标与三件事

| 动作 | 命令 | 说明 |
|:--|:--|:--|
| 清单 | `list` | 数据集/源表所在存储层、路径存在性、**校验清单就绪度**（发现到的 MD5/SHA 清单） |
| 核验 | `verify` | 按官方校验清单**抽检（默认 8 个文件）**或全检（`--full`），支持"压缩流/解压流"两种哈希语义 |
| 放置 | `sync` | rsync 将数据集（源表级粒度）复制到目标存储层；**默认 dry-run，`--apply` 才执行**；永不 `--delete` |

## 2. 核验语义（2026-10-11 实测定案）

| 数据集 | 清单文件 | 语义（实测） |
|:--|:--|:--|
| Gaia gdr3 | `gaia_source/_MD5SUM.txt`（3387 行） | **压缩流 md5**（直接命中） |
| Gaia gdr2 / gdr1 | `gaia_source/MD5SUM.txt`、`{csv,fits,votable}/MD5SUM.txt` | 同族，默认按压缩流 |
| TESS | `md5sum.txt`（90 行，**清单名不含 .gz**） | **解压流 md5**（实测 `gunzip 流 md5 ≡ 清单值`） |
| WISE | `wise-allwise-cat.bz2.md5.txt`（+ sizes） | 压缩流 md5 |
| 2MASS / SEDs | 无官方清单 | `verify` 报 "no manifest"（退出码 2） |

**自动校准**：清单发现（`_MD5SUM.txt / MD5SUM.txt / md5sum.txt / *.md5.txt / *.sha256…`，深度 1–2）
＋ 语义校准（在清单前 12 个条目中取**最小实际文件**分别按压缩流/解压流试算一次，哪边命中定哪边；
无法判定时默认压缩流）。零配置即可覆盖上表全部形态。

## 3. 配置与目录

- 复用 `~/.config/oasis/config.yaml`（datasets/storages/nodes）与 `oasis_catalog.config` 加载器；
- `sync --to <storage-id>` 目标约定：`<storage.path>/oasis-datasets/<catalogue.path>`；
- `sync --to-path DIR` 目标约定：`DIR/<catalogue.path>`（便于临时/测试与摆渡盘）。

## 4. 安全与边界

- 源只读；目标只增不删（无 `--delete`）；dry-run 为默认，`--apply` 明示执行；
- 不搬运远端未挂载资源（v0.1 仅本机可见路径；ssh 目标待"四个接线值"后加）；
- 不做清理/删除/改写任何数据集；不管理派生源表（归 `oasis-catalog`）。

## 5. 借鉴来源

- `toolbox/external_storage_tools`：外置盘"激活/映射"概念（本工具先做"放置"子集）；
- `toolbox/verify-local-repo.py`：**gzip 透明校验**与缺失清单输出（本工具校准器的直接来源）；
- `toolbox/pfetch.py`：清单驱动的并行/重试（v0.2 移植为多文件并行同步）。

## 6. 后续（v0.2+）

- ssh+rsync 目标（storage.nodes 别名就绪后）；并行多文件同步（pfetch 模式）；
- 声明显式覆盖（config 中 catalogue 级 `checksum:` 块，含 `content: compressed|decompressed` 与 `parallel: N`）；
- 与 C3 先导交付联动：`sync --to usb --apply` 作为摆渡通道。
