# 文献登记册（Registry）

- 版本：v0.2（2026-10-10，初版；全部存量条目 notes 全文解析完成）　维护：设计开发；监督：质量管理（登记完整性与准入规则）
- 状态：meta（`meta/<key>.json`）｜pdf（`pdf/<key>.pdf`）｜notes（`notes/<key>.md` 全文解析）
- 引用约定：一律使用 key；BibTeX 见 `bib/oasis.bib`（自动生成）与 `bib/manual.bib`（手工）

| Key | 标题 | 一作 | 年 | 来源 | DOI | OA | 本地 | 主要角色 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `duvert2017oifits` | OIFITS 2: the 2nd version of the data exchange standard for optical interferometry | Duvert, Young & Hummel | 2016 | A&A 597, A8 | 10.1051/0004-6361/201526405 | bronze | meta✓ pdf✓ notes✓ | 设计·科学·评审 |
| `fits_standard40` | Definition of the Flexible Image Transport System (FITS), Version 4.0（manual） | IAU FITS Working Group | 2016 | fits.gsfc.nasa.gov | — | 官方公开 | pdf✓ notes✓ | 设计·评审·科学 |
| `pence2010fits` | Definition of the Flexible Image Transport System (FITS), version 3.0 | Pence et al. | 2010 | A&A 524, A42 | 10.1051/0004-6361/201015362 | closed | meta✓ pdf✗ | 设计·评审 |
| `greisen2002wcs` | Representations of world coordinates in FITS | Greisen & Calabretta | 2002 | A&A 395, 1061 | 10.1051/0004-6361:20021326 | bronze | meta✓ pdf✓ notes✓ | 设计·评审 |
| `astropy2022` | The Astropy Project: Sustaining and Growing a Community-oriented Open-source Project… (v5.0) | Astropy Collaboration | 2022 | ApJ 935, 167 | 10.3847/1538-4357/ac7c74 | gold (CC-BY) | meta✓ pdf✓ notes✓ | 设计 |
| `quanz2022life` | Large Interferometer For Exoplanets (LIFE) | Quanz et al. | 2022 | A&A 664, A21 | 10.1051/0004-6361/202140366 | gold (CC-BY) | meta✓ pdf✓ notes✓ | 科学·设计 |
| `monnier2003optical` | Optical interferometry in astronomy | Monnier | 2003 | Rep. Prog. Phys. 66, 789 | 10.1088/0034-4885/66/5/203 | bronze | meta✓ pdf✓ notes✓ | 科学·评审 |
| `eisenhauer2023advances` | Advances in Optical/Infrared Interferometry | Eisenhauer et al. | 2023 | ARA&A 61, 237 | 10.1146/annurev-astro-121622-045019 | hybrid (CC-BY) | meta✓ pdf✗（出版社拦截，待补） | 科学·评审 |

**备注**

- `duvert2017oifits` 年份以 OpenAlex 为准（2016 在线；期刊卷 597 于 2017 年 1 月出版）。
- `fits_standard40` 为手工登记（`bib/manual.bib`）：FITS 官方标准 4.0（2016-07-22 更新），
  用于替代 closed 的 `pence2010fits` 正文；正文 PDF 已获取并入库。
- `eisenhauer2023advances` 为 CC-BY 但 annualreviews.org 拒绝脚本下载（HTTP 403）；
  登记元数据保留，正文待人工获取后补入。
- 准入规则：只收录开放获取 PDF；closed / 出版社拦截的条目仅登记元数据与 DOI。
