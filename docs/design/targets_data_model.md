# 目标层数据类型详细设计

## 1. TargetModel 基类

### 1.1 概述

`TargetModel` 是所有目标层模型的抽象基类，包括参数化模型（`SourceModel`、`BackgroundModel`、`TransmissionModel`）与可观测模型（`TargetHistogram`）。它承载模型实例的通用标识、溯源信息、版本控制及层级归属，为整个目标层提供统一的元数据模型与引用协议。

### 1.2 设计目标

- **唯一标识与可引用性**：每个模型实例拥有 OASIS 系统内稳定的逻辑标识，支持模型间的关联引用（如直方图追溯其源模型）。
- **溯源与科学可重复性**：明确记录模型的来源（用户、文献、算法或反演更新）与版本，支持结果复现与审计。
- **层级组织协作**：与 OASIS 五级模型层级（基础 → 主题 → 方向 → 任务 → 目标）协同，提供模型归属的定位信息。
- **可扩展性**：通过 `metadata` 字典携带无法归入标准字段的额外信息，避免核心接口膨胀。
- **生态兼容性**：字段类型优先采用 Python 标准类型与 Astropy 生态类型，确保与科学计算栈的互操作。

### 1.3 字段定义

| 字段名 | Python 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `name` | `str` | 是 | 模型实例的逻辑名称，在所属层级命名空间内唯一。 |
| `provider` | `str` | 是 | 模型提供者标识，可为用户名、文献 DOI、算法名称或反演任务 ID。若未提供，使用默认值 `"user"`。 |
| `version` | `str` | 是 | 语义化版本号，推荐 `MAJOR.MINOR.PATCH` 格式，支持预发布标识（如 `1.0.0-alpha`）。 |
| `metadata` | `dict[str, Any]` | 否 | 用户自定义扩展字典，用于存储附加描述信息。默认为空字典。禁止在此存放影响模型数值计算的物理参数。 |
| `hierarchy` | `Optional[HierarchyDescriptor]` | 否 | 模型在五级层级体系中的定位信息，由 `Hierarchy Manager` 在解析/注册时填充，初始为 `None`。 |

**辅助类型 `HierarchyDescriptor`**（后续由层级管理器详细定义，此处给出接口概要）：

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `theme` | `str` | 科学主题名称。 |
| `direction` | `Optional[str]` | 研究方向（可选）。 |
| `mission` | `Optional[str]` | 观测任务。 |
| `target` | `Optional[str]` | 具体目标标识。 |

### 1.4 约束与不变量

- `name` 必须为非空字符串，且在所属层级命名空间内保持唯一。
- `version` 应遵循语义化版本规范，便于版本比较与兼容性判断。
- `provider` 不可为空字符串。
- `metadata` 仅用于描述性信息，不得包含直接影响数值计算结果的物理参数（如温度、坐标等），此类参数必须作为具体子类的类型化字段定义。
- 模型实例应被视为**逻辑不可变**：创建后不应原地修改其核心字段值。如需变更，应创建新实例并递增版本号，以维护溯源链完整性。
- `hierarchy` 为 `None` 表示模型尚未注册到层级体系，仅在反序列化或初始构建阶段允许；模型进入处理流程前须由 `Hierarchy Manager` 完成补全。

---

## 2. SpectralModel 抽象基类

### 2.1 概述

`SpectralModel` 是所有光谱描述符的抽象基类，用于描述辐射源的光谱能量分布（SED）以及介质透过率曲线等。具体光谱类型（黑体、幂律、多温黑体、透过率曲线等）继承此类实现。它**不**继承自 `TargetModel`，而是作为 `SourceModel`、`BackgroundModel`、`TransmissionModel` 的组成部分使用。

### 2.2 字段定义

| 字段名 | Python 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `type` | `str` | 是 | 光谱类型标识符，例如 `"blackbody"`、`"power_law"`、`"multi_blackbody"`、`"transmission_curve"` 等。 |
| `parameters` | `dict[str, ParameterValue]` | 是 | 光谱参数字典，每个参数以 `{value, unit}` 形式表示。具体键值由子类规范定义。 |
| `metadata` | `dict[str, Any]` | 否 | 附加描述信息，不影响物理计算。默认为空字典。 |

**辅助类型 `ParameterValue`**：

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `value` | `float` | 参数数值。 |
| `unit` | `str` | 单位字符串，兼容天文标准单位制。 |

### 2.3 约束与不变量

- `type` 必须为非空字符串，且应匹配已注册的频谱子类。
- `parameters` 的键应与具体子类支持的参数名称一致。
- `metadata` 不得包含直接影响物理计算的参数。

### 2.4 子类示例（本文件仅列举，不完整）

- `BlackbodySpectralModel`：支持 `temperature`（温度）。
- `PowerLawSpectralModel`：支持 `alpha`（谱指数）、`reference_wavelength`（参考波长）。
- `MultiBlackbodySpectralModel`：支持 `temperatures`（多个温度列表）和 `weights`。
- `TransmissionCurveSpectralModel`：支持 `wavelength`（数组）和 `transmission`（数组），或参数化公式。

---

## 3. SourceModel 参数化模型

### 3.1 概述

`SourceModel` 表示目标区域中信号源的参数化模型，继承自 `TargetModel`。它描述了物理天体的位置、自行以及光谱特征。

### 3.2 继承字段

`SourceModel` 继承自 `TargetModel` 的所有字段：`name`、`provider`、`version`、`metadata`、`hierarchy`。

### 3.3 新增字段

| 字段名 | Python 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `coordinates` | `SkyCoord` (astropy) | 是 | 天体坐标，包含 RA、Dec 及可选的视向距离。 |
| `proper_motion` | `tuple[Quantity, Quantity]` | 是 | 自行，格式为 `(pm_ra_cosdec, pm_dec)`，单位通常为 `mas/yr`。 |
| `spectral_model` | `SpectralModel` | 是 | 描述光源光谱能量分布的模型。 |

### 3.4 约束与不变量

- `coordinates` 必须包含 RA 和 Dec；距离（distance）可选。
- `proper_motion` 的两个分量单位必须一致且允许空值（零自行）。
- `spectral_model` 不能为 `None`。

---

## 4. BackgroundModel 参数化模型

### 4.1 概述

`BackgroundModel` 表示目标区域中背景辐射的参数化模型，继承自 `TargetModel`。它描述了背景的空间分布范围以及光谱特征。

### 4.2 继承字段

同 `TargetModel`。

### 4.3 新增字段

| 字段名 | Python 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `region` | `str` | 是 | 背景区域描述字符串，例如 `"full_sky"` 或 `"annulus_10_20_arcsec"`。具体格式由实现定义。 |
| `spectral_model` | `SpectralModel` | 是 | 描述背景辐射光谱特征的模型。 |

### 4.4 约束与不变量

- `region` 必须为非空字符串。
- `spectral_model` 不能为 `None`。

---

## 5. TransmissionModel 参数化模型

### 5.1 概述

`TransmissionModel` 表示目标区域中介质对信号传输的透过率或消光模型，继承自 `TargetModel`。它描述了介质的吸收、散射等效应。

### 5.2 继承字段

同 `TargetModel`。

### 5.3 新增字段

| 字段名 | Python 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `optical_depth` | `Quantity` | 是 | 参考波长下的光学厚度（无量纲量或加单位，如 `{value: 0.3, unit: ""}`）。 |
| `transmission_curve` | `ndarray` | 否 | 传输曲线数组，通常为波长‑透过率对。若提供，优先于参数化模型；若为 `None`，则使用 `spectral_model` 计算。 |
| `spectral_model` | `SpectralModel` | 是 | 描述透过率随波长变化的模型，例如幂律消光、查表曲线等。 |

### 5.4 约束与不变量

- `optical_depth` 必须为非负值。
- `transmission_curve` 如果提供，应为形状 `(N,2)` 的数组，第一列为波长，第二列为透过率（0~1 之间）。
- `spectral_model` 不能为 `None`。

---

## 6. TargetHistogram 可观测模型

### 6.1 概述

`TargetHistogram` 表示目标区域亮度在空间、时间、波长维度上的离散分布（直方图），继承自 `TargetModel`。它是正演链路最终的输出载体，也是反演链路从观测数据提取的容器。

### 6.2 继承字段

同 `TargetModel`。

### 6.3 新增字段

| 字段名 | Python 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `data` | `ndarray` | 是 | 亮度分布数组（二维/三维/四维等）。 |
| `axes` | `list[AxisDescriptor]` | 是 | 每个维度的描述信息，长度与 `data.ndim` 一致。 |
| `units` | `Unit` (astropy) | 是 | 数据值的物理单位，例如 `"MJy/sr"`、`"photon/s/cm^2/arcsec^2"`。 |
| `uncertainty` | `ndarray` (可选) | 否 | 与 `data` 相同形状的误差数组，若为 `None` 表示仅提供名义值。 |
| `histogram_type` | `HistogramType` | 是 | 直方图类型枚举（详见第 7 节）。 |
| `source_model_ref` | `str` | 是 | 产生此直方图时使用的 `SourceModel` 的 `name`（溯源引用）。 |
| `background_model_ref` | `str` | 是 | 背景模型的 `name`，若无背景可用空字符串 `""`。 |
| `transmission_model_ref` | `str` | 是 | 透过率模型的 `name`，若无透过率可用空字符串 `""`。 |

### 6.4 约束与不变量

- `axes` 的长度必须等于 `data.ndim`。
- `uncertainty`（若提供）必须与 `data` 形状完全相同。
- `source_model_ref` 必须指向一个已注册的 `SourceModel` 实例的 `name`。
- 直方图类型应与其维度结构相符（例如 `spectrum` 应有且仅有一个波长轴）。

---

## 7. HistogramType 枚举

### 7.1 定义

`HistogramType` 是一个枚举类型，标识 `TargetHistogram` 的数据类别。

| 枚举值 | 说明 |
|:---|:---|
| `image` | 二维空间图像，轴为（y, x）或（dec, ra）。 |
| `spectrum` | 一维光谱，轴为波长/频率。 |
| `light_curve` | 一维光变曲线，轴为时间。 |
| `cube` | 三维/四维数据立方，例如（波长, y, x）或（时间, 波长, y, x）。 |

---

## 8. AxisDescriptor 辅助类型

### 8.1 概述

`AxisDescriptor` 描述 `TargetHistogram` 数据的一个维度，包括名称、单位、类型以及可选的坐标参考信息。

### 8.2 字段定义

| 字段名 | Python 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `name` | `str` | 是 | 坐标轴名称，例如 `"RA"`、`"Dec"`、`"wavelength"`、`"time"`。 |
| `unit` | `Unit` | 是 | 坐标轴单位的描述。 |
| `type` | `AxisType` | 是 | 轴类型枚举，见下文。 |
| `coordinate` | `Optional[WCSAxis]` | 否 | 与该轴关联的 WCS 信息（具体结构由数据段定义）。初始为 `None`。 |

**辅助枚举 `AxisType`**：

| 枚举值 | 说明 |
|:---|:---|
| `spatial` | 空间坐标（RA、Dec、像素等）。 |
| `spectral` | 光谱坐标（波长、频率、能量）。 |
| `temporal` | 时间坐标。 |
| `other` | 其他类型（如偏振、斯托克斯参数）。 |

### 8.3 约束与不变量

- `name` 应与目标层上层约定保持一致。
- `unit` 必须与 `type` 语义兼容（例如光谱轴不应使用时间单位）。
- `coordinate` 当 `type` 为 `spatial` 或 `spectral` 时建议提供。

---

> **注意**：`HierarchyDescriptor` 的定义已在 §1 中给出，此处不再重复。本章节涵盖了 target layer 所有核心数据类型，后续若需添加新辅助类型（如 `UncertaintyDescriptor`、`WCS` 详细描述等），可追加于本章之后。
