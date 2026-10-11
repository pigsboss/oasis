# 交付回执 · 底座资产（SPICE kernels）

**致**：行星探测工程 › 专题工作区 › 深空任务建模仿真可视化（用户）
**发**：oasis 源表管理（MEAYIN-OASIS）　**日期**：2026-10-11
**对应**：底座资产（SPICE kernels）管理与供应（F-11，用户审定 2026-10-11）；生态两平面裁决
（OASIS＝资产/供应平面：datasets 源表 ＋ kernels 底座；multistagecophasing＝仿真/设计平面）
**性质**：供应就绪与首件核验说明（资产为准文件；消费端只认 manifest；消费规范（加载顺序/ET）归贵方 ADR-001）

---

## 一、供应内容与位置

位置（store，按类别收纳）：**`/Volumes/ArecaStudio/Datasets/SPICE Kernels/<类别>/`**
注册表（平行注册，不进 datasets 清单）：`~/.config/oasis/kernels.yaml`

| id | 类别 | 文件 | 字节 | sha256（前 16） | 官方核验 |
|:--|:--|:--|--:|:--|:--|
| de440 | spk | `spk/de440.bsp` | 119,799,808 | `a4ce9bf9b3282bec` | 对 JPL `aa_checksums.txt` 官方 md5 **逐位一致** |
| de442 | spk | `spk/de442.bsp` | 119,771,136 | `8d5001fab315eeff` | 同上 |
| de441 | spk | `spk/de441.bsp` | 3,307,878,400 | `9a824e6a8ce3d39f` | 取件完成＋sha256 登记（JPL 官方清单覆盖为分卷版，本件为整文件版） |
| naif0012 | lsk | `lsk/naif0012.tls` | 5,257 | `678e32bdb5a74411` | 与 NAIF 现行文件重下载比对一致 |
| pck00011 | pck | `pck/pck00011.tpc` | 131,226 | `3dff7b1dbeceaa01` | 同上 |

- de440 即贵方现役主历表；de441 覆盖 −13200→+17191（长时段历表，已入库备用）。

## 二、贵方现役一致性核验（收到即验）

对贵方工作区 `multistagecophasing/spice_kernels/` 现役四件做了独立核验——与 OASIS 官方核验副本
**sha256 逐位一致**，无需任何迁移：

| 贵方件 | 与 store 比对 |
|:--|:--|
| `spk/planets/de440.bsp` | 一致 |
| `spk/planets/de442.bsp` | 一致 |
| `lsk/naif0012.tls`（含同内容别名 `latest_leapseconds.tls`） | 一致 |
| `pck/pck00011.tpc` | 一致 |

核验方法：双侧 `shasum -a 256` 比对（2026-10-11）；同值即同字节。

## 三、核验与取用（一条命令）

```bash
tools/oasis-datasets kernels list                    # 注册表现状（含官方核验状态）
tools/oasis-datasets kernels verify                   # store 逐件重算 sha256
tools/oasis-datasets kernels verify <APP_DIR>         # 校验应用副本（读取 oasis-manifest.json）
tools/oasis-datasets kernels send de440 de442 de441 naif0012 pck00011 --app <APP_DIR> [--apply]
    # 投送：<APP_DIR>/spice_kernels/<类别>/ ＋ oasis-manifest.json
    #（本次未主动写入贵方工作区；按需投送）
```

投送产物随 `oasis-manifest.json`（id/path/bytes/sha256/source_url/coverage），
消费方式与 datasets 交付同约定——**只认 manifest**。

## 四、边界与约定

- **长期支持责任在上游**（JPL／NAIF）；本层**零档案责任**——store 可从渠道重建（`kernels fetch`），
  副本跟随应用工作区（贵方 `spice_kernels/` 即首个样板）；
- **消费规范归贵方**（加载顺序 LSK→PCK→SPK→FK/IK/CK、ET 使用范围——贵方 ADR-001）；本层不另立约定；
- 增补其他条目或新版本（贵方在用的 earth 高精度 PCK、月球 PA／地球 ITRF 等辅助件），按需提出即登记/取件。

## 五、关联

- 贵方 UR-2026-1012 批次 1+2 交付回执（星表侧）：`~/Datasets/catalogs/回执_UR-2026-1012.md`（内容不变，仍有效）。

## 六、异议与签收

核验不通过或需增补条目，请以书面（投放或回执）指明。未收到异议即视为本供应说明送达无误。
