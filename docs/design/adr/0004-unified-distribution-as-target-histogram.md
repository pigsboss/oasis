# 统一分布表示为 TargetHistogram

- **状态**：已接受
- **日期**：2026-04-05
- **决策者**：OASIS 目标层设计团队
- **涉及文档**：docs/guides/targets.md, docs/diagrams/targets/classes.puml

## 背景
正演引擎的输出和反演引擎的输入均表现为多维亮度分布，具体形态有图像（空间直方图）、光谱（波长直方图）、光变曲线（时间直方图）甚至多维数据立方。在设计初期，曾考虑分别为每种类型创建单独的类（如 `Image`、`Spectrum`、`LightCurve`），但这将导致管道分支逻辑复杂，组件间传递的数据类型多样化，增加维护负担。我们需要一种统一的方式来处理这些分布，保持接口简洁和流程通用。

## 决策
引入 `TargetHistogram` 类型，作为目标区域亮度分布的统一容器。它包含：
- 一个多维数组 `data` 存储亮度值。
- 轴描述列表 `axes`，每个轴具有名称、单位、坐标向量及 WCS 信息（可选）。
- 物理单位 `units`，不确定性 `uncertainty`。
- 一个枚举 `histogram_type` 标识其维度语义（image, spectrum, light_curve, cube）。
- 引用关联的参数化模型（`source_model_ref`, `background_model_ref`, `transmission_model_ref`）。

无论是正演生成的结果，还是从观测数据解析得到的输入，都采用 `TargetHistogram` 表示。`Physics Engine` 和 `Parameter Estimator` 均以它为交互对象。FITS 序列化/反序列化组件负责将内存中的 `TargetHistogram` 转换为标准 FITS 多维 HDU。

## 理由
- **统一接口**：简化了管道设计，组件只需处理一种分布类型，无需根据不同维度编写条件分支。
- **自然映射**：天文数据通常以多维数组存储（如 FITS 文件），`TargetHistogram` 直接对应这种结构，序列化/反序列化更直接。
- **可扩展性**：未来增加新维度（如偏振、Stokes 参数）只需扩展轴描述和数组维度，不改变类型定义。
- **追溯性**：通过模型引用字段，可以反向关联产生这些分布的信号源、背景和透过率模型，支持反演参数更新。
- **消除重复**：避免了 `Image`/`Spectrum`/`LightCurve` 各自携带坐标、单位、不确定性等重复字段。

## 影响
- 类图中 `TargetHistogram` 取代了原先设想的多个分布类。
- 正演/反演内部接口（B、C）统一传递 `TargetHistogram` 内存对象。
- FITS/HDF5 I/O Manager 需要实现 `TargetHistogram` 与 FITS 多 HDUs 之间的双向映射。
- 反演输出的参数化模型实例可直接关联到输入数据的 `TargetHistogram`。

## 考虑的替代方案
- **方案1**：为每种分布类型创建单独类（`Image`, `Spectrum`, `LightCurve`）。
   - 优点：类型安全，各维度操作专用方法可优化。
   - 缺点：管道逻辑复杂，需大量 isinstance 检查；代码重复；难以统一处理多维数据立方。
- **方案2**：使用通用的 `xarray.DataArray` 或类似的标注数组。
   - 优点：功能强大，社区支持好。
   - 缺点：引入外部依赖，可能需要额外转换层；其元数据模型可能与 FITS/WCS 不完全匹配；增加学习成本。
- **方案3**：直接使用裸 `numpy.ndarray` + 元数据字典。
   - 优点：极简，无额外抽象开销。
   - 缺点：缺乏结构保证，易出错，约束不足，不利于代码理解和维护。
