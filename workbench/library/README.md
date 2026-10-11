# OASIS 共享参考文献库

四角色共用的文献基础设施：统一登记、单一路径沉淀文献元数据、开放获取原文与全文解析结果。

- 检索工具：OpenAlex API（脚本 [`scripts/openalex.py`](scripts/openalex.py)，仅标准库）
- 全文解析：MinerU v4（本地文档库 + 本地模型，MPS 加速；watch 自动入库）

## 目录结构

```
library/
├── README.md          # 本文件：章程、工作流、规则
├── registry.md        # 文献登记册（唯一条目清单与状态）
├── bib/
│   ├── oasis.bib      # 自动生成（openalex.py bib --all），勿手工修改
│   └── manual.bib     # 手工登记条目（无 DOI 来源，如官方标准）
├── meta/              # OpenAlex 元数据缓存（<key>.json，自动保存）
├── pdf/               # 开放获取 PDF（<key>.pdf；已挂入 MinerU watch）
├── notes/             # MinerU 全文 Markdown（<key>.md）
├── scripts/
│   └── openalex.py    # search / get / bib 子命令
└── reading-lists/     # 四角色阅读清单：design / science / review / qm
```

## 核心规则

1. **命名**：文献 key 为 `<一作姓氏><年份><题名首词>`（小写字母数字，如 `duvert2017oifits`），
   同一 key 贯穿 `meta / pdf / notes / bib / registry`，引用一律使用 key。
2. **准入**：只收录**开放获取（OA）**PDF；非 OA 或出版社拦截的文献仅登记元数据与 DOI 链接。
3. **单一来源**：登记册、BibTeX、元数据、原文、解析文本互不复制；`oasis.bib` 由脚本再生（可重现），
   `manual.bib` 人工维护。
4. **溯源**：每条目保留 OpenAlex ID 与 DOI；手工条目在登记册中标注 `manual`。
5. **版本**：登记册与阅读清单变更递增版本号；由质量管理监督准入规则执行。

## 标准工作流（新增一条文献）

```bash
cd workbench/library

# 1) 检索（可加 --oa-only）
python3 scripts/openalex.py search "high contrast imaging space telescope" --limit 10 --oa-only

# 2) 取回登记：保存元数据 + 下载 OA PDF（arXiv 优先回退；出版社拦截自动跳过）
python3 scripts/openalex.py get doi:10.1051/0004-6361/202140366 --key quanz2022life --save --pdf

# 3) 再生 BibTeX
python3 scripts/openalex.py bib --all --out bib/oasis.bib

# 4) MinerU：单篇全文解析（→ notes/<key>.md）；或依赖 watch 自动入库
mineru parse pdf/quanz2022life.pdf -p all -o notes/quanz2022life.md

# 5) 更新 registry.md（人工评审后登记）
```

## MinerU 集成

- `pdf/` 目录已挂入 MinerU watch（label `oasis-library`），新增 PDF 自动入库解析；
  查看/移除：`mineru watch list` / `mineru watch remove <id>`。
- 文档库检索：`mineru search "<关键词>" -n 10`；按定位读取：`mineru read <locator>`；入库清单：`mineru list docs`。
- **注意**：MinerU 文档库是全局库（`~/.mineru/doclib.db`），含其他项目文献；
  本库文献以文件路径 `/Users/huo/Projects/oasis/workbench/library/pdf/` 区分。
- 基础 PDF 解析（无版面结构需求）亦可用 `pdftotext`（poppler 已安装）。

## 四角色职责

| 角色 | 对文献库的职责 | 阅读清单 |
|:---|:---|:---|
| 设计开发 | 维护格式/标准类文献（FITS、OIFITS、WCS、工具链）；设计中引用 key | [reading-lists/design.md](reading-lists/design.md) |
| 科学用户 | 领域文献策展（干涉测量、目标科学）；用例科学依据引用 key | [reading-lists/science.md](reading-lists/science.md) |
| 评审专家 | 以标准原文为评审基准；核查设计对标准的符合性 | [reading-lists/review.md](reading-lists/review.md) |
| 质量管理 | 监督登记完整性与准入规则执行；维护库治理记录 | [reading-lists/qm.md](reading-lists/qm.md) |

## 工具状态（2026-10-10 环境体检）

- **OpenAlex**：`api.openalex.org` 连通（HTTP 200，约 1.2s）；Crossref、arXiv API 均连通。
- **MinerU v4.0.7**（uv tool 安装）：本地模型 2.0G（MinerU-4 + MinerU2.5-Pro GGUF）；
  本地文档库 `~/.mineru/` 运行中；torch 2.14（Apple MPS 可用）；
  远程服务 mineru.net 匿名额度可用（≤200 页/文件、≤200 MiB，可选 `--remote`）。
- **网络**：huggingface.co 不可达（模型下载请走 ModelScope）；modelscope.cn 可达。
- 其他已装工具：`jq`、`pdftotext`（poppler）、`gs`、`sqlite3`、XeLaTeX/latexmk、PlantUML、pandoc、uv。
