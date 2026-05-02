# ADR 006: 为 BackgroundModel 增加空间各向异性支持

- **状态**：已提议
- **日期**：2026-04-10
- **决策者**：OASIS 架构团队
- **涉及文档**：docs/design/targets_data_model.md, docs/diagrams/targets/classes.puml

## 背景

目前 `BackgroundModel` 只能通过一个字符串字段 `region` 描述背景区域的范围（如 `"full_sky"`），但无法区分该区域内背景是否空间均匀（各向同性）或随方向变化（各向异性）。在真实天文场景中：

- 宇宙微波背景（CMB）在大尺度接近各向同性；
- 黄道光、银河系弥散辐射、仪器散射光等均展现显著的各向异性。

正演仿真时，物理引擎需要明确背景的空间变化性质以选择计算路径；反演时，空间分布参数同样需要被估计。因此，必须显式建模并暴露这一物理属性。

主要驱动力：
- **物理真实度**：异向性背景直接影响图像/光谱的可观测模型，缺失该建模将降低仿真科学性。
- **计算性能**：各向同性背景可简化为单一谱亮度乘立体角，各向异性则需逐像素采样，提前标识可优化调度。
- **接口完备性**：遵循“所有影响数值计算的物理参数必须放入类型化字段”的原则（ADR 001），空间变化特征不得隐藏在 `metadata` 或 `region` 字符串中。
- **可扩展性**：引入一个与 `SpectralModel` 对称的 `SpatialModel` 抽象基类，为未来的空间模型实现（多项式、HEALPix 查找表等）提供统一接口。

## 决策

我们决定在 `BackgroundModel` 中增加以下两个字段，并引入抽象基类 `SpatialModel`：

- `is_isotropic`（`bool`，可选，默认 `True`）：指示背景在 `region` 内是否空间均匀。默认值保证向后兼容现有模型。
- `spatial_model`（`Optional[SpatialModel]`，可选，默认 `None`）：当 `is_isotropic=False` 时必须提供，承载空间变化的具体实现。

同时，在 `targets_data_model.md` 中定义 `SpatialModel` 抽象基类的概要接口：

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `type` | `str` | 空间模型类型标识（如 `"polynomial"`, `"healpix_map"`） |
| `parameters` | `dict[str, ParameterValue]` | 模型参数，遵循 `{value, unit}` 模式 |
| `metadata` | `dict[str, Any]` | 附加描述信息，不影响计算 |

核心方法：`evaluate(coords: SkyCoord) -> Quantity`，返回给定坐标处的归一化或绝对亮度。

类图同步更新，在 `BackgroundModel` 中展示新属性，并关联到 `SpatialModel`。

## 理由

1. **最小侵入与向后兼容**：默认 `is_isotropic=True` 且 `spatial_model=None` 保持已有行为不变；仅当用户显式声明异向性时才需提供空间模型。
2. **物理参数显式化**：空间均匀性直接影响计算链路，必须作为类型化字段，符合 ADR 001 的约束。
3. **对称设计**：`SpatialModel` 在形式上与 `SpectralModel` 对称，降低学习和使用成本，也便于未来其他模型（如 `TransmissionModel`）复用。
4. **可检测的不变量**：通过 `is_isotropic` 与 `spatial_model` 的组合可以静态或动态检查完备性，物理引擎可据此优化执行路径。

## 影响

- **模型段**：`Physics Engine` 需读取 `is_isotropic` 标志，对异向性背景调用 `spatial_model.evaluate()` 进行逐像素合成；`Parameter Estimator` 需支持对 `spatial_model` 参数的反演。
- **接口段**：用户 YAML 输入可新增一个可选的 `spatial_model` 块，其结构类似于 `spectral_model`；输入验证器需检查 `is_isotropic` 与 `spatial_model` 的一致性。
- **数据段**：`SpatialModel` 的具体参数值（甚至查找表）需支持 FITS/HDF5 序列化，作为背景模型元数据的一部分。
- **文档与测试**：需为 `SpatialModel` 提供至少一个具体实现（如常数模型）作为基准，并编写单元测试验证布尔标志与空间模型的一致性和无效组合的处理。

## 考虑的替代方案

- **方案1：仅扩展 `region` 字符串语义**  
  例如 `region = "healpix_map:file.fits"` 或 `region = "polynomial(deg=2)"`.  
  - 优点：字段数量不增加。  
  - 缺点：类型不安全、解析脆弱、难以版本控制和 IDE 辅助；与模型段内存对象契约冲突。  
  - **否决**：因为违反显式物理参数原则，且与整体类型化设计不符。

- **方案2：在 `metadata` 中放置异向性标志**  
  - 优点：无需修改模型字段结构。  
  - 缺点：核心物理行为隐藏在非结构化字典中，违背 ADR 001；无法保证引擎能正确读取。  
  - **否决**：因为 `metadata` 被严格限定为不参与计算。

- **方案3：将空间模型完全分离为独立组件，外部绑定**  
  - 优点：`BackgroundModel` 保持最简。  
  - 缺点：破坏模型的自完备性，增加组合与反演追踪的复杂度；不利于序列化与缓存。  
  - **否决**：背景模型通常需要同时描述光谱和空间，内聚在一起更自然。
