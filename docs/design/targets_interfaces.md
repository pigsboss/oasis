# 目标层接口设计

## 1. 概述

目标层接口遵循“段间内存对象契约”和“外部显式文件契约”的双重原则，确保内部组件松耦合、高性能，对外标准化、可审计。接口分为外部（面向用户、观测层、硬件）和内部（段间通信与支撑）两大类。

**设计原则**：
- **分段边界**：接口段只对用户/外部系统暴露，数据段只对观测层暴露，模型段不暴露对外接口。
- **类型安全**：所有跨段消息采用 Pydantic 模型，内置校验与序列化；物理量统一为 `{value, unit}` 结构。
- **零拷贝/低拷贝**：大数组通过共享内存视图句柄传递，避免冗余序列化。
- **异步解耦**：计算任务通过消息队列提交，资源状态通过发布-订阅事件流推送。
- **版本化与向前兼容**：所有外部输入输出携带 `oasis_version`，接口变更通过语义版本管理。
- **诊断与安全**：生产环境下禁用段间诊断导出，组件内部自检受路径隔离约束；所有异常返回英文错误码和消息。

## 2. 外部接口

### 2.1 用户交互接口

#### 2.1.1 YAML 参数化模型输入

用户通过 YAML 文件提交一组参数化模型，文件结构遵循 `targets.md §4.4.1` 的原始定义，并扩展支持 `SpatialModel`。

**顶层结构**：
```yaml
oasis_version: "1.0"
theme: "stellar"                 # 科学主题标识
source:                          # 可选，SourceModel 定义
  name: "..."
  ...
background:                      # 可选，BackgroundModel 定义
  name: "..."
  is_isotropic: true/false
  spatial_model:                 # 当 is_isotropic=false 时必填
    type: "polynomial"
    parameters:
      ...
transmission:                    # 可选，TransmissionModel 定义
  ...
```

**字段约束**（由 Input Validator 执行）：
- `name`：非空字符串，在同一个 YAML 文件内唯一（层级命名空间后期由 Hierarchy Manager 补充）。
- `provider`：可选，默认 `"user"`；若提供，不可为空。
- `version`：可选，默认 `"0.1.0"`，需符合语义版本格式。
- `is_isotropic`：可选，默认 `true`。若为 `false`，则必须提供 `spatial_model`。
- `spatial_model`：字典，必须包含 `type`（字符串）和 `parameters`（字典），可选 `metadata`。
- 所有物理量：必须为 `{value: <float>, unit: "<string>"}` 字典。
- 参数扫描：支持 `linspace`（start,stop,num）、`logspace`（start,stop,num）、`list`（数组），替换对应物理量的数值部分。

**输入验证器行为**：
- 使用 JSON Schema（衍生自 Pydantic 模型）验证结构完整性；非法节点返回精确行号提示。
- 不检查物理语义（如负温度、超光速自行），这部分留待模型段 Conflict Detector 处理。

#### 2.1.2 Python API

提供 Pythonic 的编程接口，允许用户以代码构建模型并提交任务。

**核心对象**：
- `TargetModelSubmission`：Pydantic 模型，包含 `oasis_version`、`theme`、`source`、`background`、`transmission` 等字段，每个字段为对应模型的参数集或对象。
- `AstropyIntegrationUtil`：工具函数，支持将 `astropy` 的 `SkyCoord`、`Quantity` 自动转换为内部 `{value, unit}` 格式，以及反向转换。

**提交方法**（示例）：
```python
def submit_forward(submission: TargetModelSubmission, 
                   mode: str = "sync",
                   scan_config: Optional[ScanConfig] = None) -> str:
    """返回 task_id"""
    ...

def submit_inverse(data_product_id: str,
                   prior_models: TargetModelSubmission,
                   method: str = "mcmc") -> str:
    """从现有数据产品反演，返回 task_id"""
    ...

def get_task_status(task_id: str) -> TaskStatus:
    """返回任务状态对象"""
    ...

def get_result(task_id: str) -> ResultBundle:
    """阻塞等待任务完成，返回结构化结果"""
    ...
```

**异步模式**：`mode="async"` 立即返回 `task_id`，用户通过 `get_task_status` 轮询或注册回调（未来扩展）。

#### 2.1.3 CLI 接口

命令行入口 `oasis` 子命令：

```bash
oasis submit forward <yaml_file> [--scan <scan_yaml>] [--async]
oasis submit inverse <product_id> --prior <yaml_file> [--method mcmc|nested]
oasis status <task_id>
oasis result <task_id> [--format json|yaml|md|pdf]
oasis download <task_id> [--output <dir>]
```

所有数据输出到标准输出或指定目录，日志和错误信息以英文输出到 stderr。

#### 2.1.4 用户输出报告

`Result Presenter` 生成统一的结构化输出 `ResultBundle`：

```json
{
  "task_id": "uuid",
  "status": "success",
  "mode": "forward",
  "output_products": {
    "target_histogram": { "id": "...", "fits_url": "..." },
    "auxiliary": [ ... ]
  },
  "fitted_models": {
    "source": { "name": "star_1", "parameters": { ... } },
    "background": null,
    "transmission": null
  },
  "statistics": {
    "log_likelihood": -120.5,
    "chi_sq": 0.98,
    "aic": 250.1
  },
  "diagnostics": {
    "posterior_plots": [ "plotly_fig_json", ... ],
    "residual_image": { "shape": [...], "dtype": "float32", "handle": "ur:/..." }
  },
  "messages": []
}
```

- 用户可直接从结果中下载 FITS 文件或图表。
- 统计诊断图表由 `Result Presenter` 生成，以 Plotly figure JSON 或静态图片链接形式返回。

### 2.2 观测量层交换接口

#### 2.2.1 正演输出（目标层 → observables）

`Observables Interface` 协调输出包生成，最终由 `FITS/HDF5 I/O Manager` 序列化。

**主 FITS 文件**：
- 第一 HDU：`TargetHistogram.data` 数组，配合 WCS 描述。
- 必填头关键字：
  - `OASIS_VER` ：目标层版本
  - `MODEL_ID` ：source_model 名称（或 UUID）
  - `TIMESTAMP` ：生成时间 ISO 8601
  - `TARGET_CLASS` ：`TargetHistogram` 类型枚举
  - `OASIS_OBS_INTF_VER` ：接口规范版本
  - `SRC_MODEL` / `BKG_MODEL` / `TRANS_MODEL` ：引用的模型名，若无则为空字符串。
  - `SPATIAL_TYP` ：若背景空间模型存在，记录其 type 字符串；否则为空。
- 图像/光谱 WCS 必须完备自洽；光变曲线包含时间轴描述。

**辅助文件包**（与主文件同目录）：
- `params.json` ：包含本次计算所用所有参数化模型的参数侧写（JSON 格式，纯数字+单位）。
- `config.yaml` ：观测配置摘要（如网格大小、积分时间等）。
- `processing_log.txt` ：计算过程元数据（英文日志摘要）。

**就绪通知**：所有文件写入完成后，在交换目录生成 `.forward_ready` 空哨兵文件。

#### 2.2.2 反演输入（observables → 目标层）

`Observables Interface` 监听交换目录，识别 `.inverse_ready` 哨兵。

**要求 observables 层提供的文件**：
- 主 FITS：科学数据产品，遵循与正演输出相同的数据结构，即 `TargetHistogram` 的存储形态。
- 头关键字要求：
  - `TASK_ID` ：对应任务 ID
  - `INSTRUMENT` ：仪器标识
  - `CALIB_VER` ：校准版本
  - `DATA_QUAL` ：数据质量标记（枚举：good, warning, bad）
- 辅助文件：
  - `noise_model.json` ：噪声模型参数
  - `instrument_response.json` ：仪器响应函数（可选）
  - `observation_config.yaml` ：观测配置（曝光时间、天顶点等）

**异常路径**：若 observables 层处理失败，放置 `.error` 文件，内容为 JSON：
```json
{
  "error_code": "OBS_001",
  "english_message": "Calibration failed due to missing dark frame",
  "timestamp": "2026-04-11T10:20:00Z"
}
```
目标层读取后向上传播，用户通过接口查看。

#### 2.2.3 数据获取哨兵协议

| 哨兵文件 | 放置方 | 含义 |
|:---|:---|:---|
| `.forward_ready` | 目标层 | 正演产物就绪，observables 层可消费 |
| `.inverse_ready` | observables 层 | 反演输入数据就绪 |
| `.error` | 任意方 | 处理失败，阻止后续自动流转 |

### 2.3 本地硬件接口

由 `Compute Runtime` 统一采集本地/集群资源状态，通过**发布-订阅**事件总线推送。

**监测内容**：
- **计算**：CPU/GPU 利用率，可用核心数，内存总量与可用量。
- **存储**：结果仓库目录的容量、可用空间、iops 估计值。
- **网络**：至 observables 层节点的延迟、包丢失率、带宽估计。

**资源状态对象 `ResourceStatus`**（Pydantic）：
```json
{
  "timestamp": "iso8601",
  "compute": {
    "cpu_available": 16,
    "gpu_available": 2,
    "memory_available_gb": 64
  },
  "storage": {
    "repo_capacity_tb": 10,
    "repo_available_gb": 500
  },
  "network": {
    "observable_node_latency_ms": 2.3,
    "bandwidth_mbps": 1000
  },
  "status": "healthy" | "degraded" | "critical"
}
```

**推送方式**：
- 事件主题：`oasis.resource.status`
- 接口段（User Interface）订阅该主题，用于向用户展示系统健康状态，或自动拒绝/降级新任务。

---

## 3. 内部接口

### 3.1 跨段内存对象契约

所有跨组件/跨段通信必须使用预定义的 Pydantic 模型，序列化边界为内存，不触及磁盘。

#### 3.1.1 核心数据模型

**`ParameterizedModelBundle`**（接口段 → 模型段）：
```python
class ParameterizedModelBundle(BaseModel):
    oasis_version: str
    theme: str
    source_models: List[SourceModelParams]
    background_models: List[BackgroundModelParams]
    transmission_models: List[TransmissionModelParams]
    hierarchy_override: Optional[HierarchyDescriptor] = None
```
其中各 `...Params` 模型为对应模型的参数描述，与 YAML 定义严格对应，物理量均用 `ValueUnit` 表示。

**`ObservableModelBundle`**（模型段 ↔ 数据段）：
```python
class ObservableModelBundle(BaseModel):
    task_id: str
    histogram: TargetHistogramParams   # 包含 data 的 ArrayHandle
    auxiliary: Dict[str, Any]
    provenance: ProvenanceMetadata
```

**`ComputeTaskRequest`**（模型段 → Compute Runtime）：
```python
class ComputeTaskRequest(BaseModel):
    task_id: str
    mode: Literal["forward", "inverse"]
    parameters_hash: str
    dependencies: List[str]  # 其他 task_id
    priority: int = 0
    payload_ref: str  # 指向共享内存中参数对象的标识符
```

**`ArrayHandle`**：
```python
class ArrayHandle(BaseModel):
    shm_id: str          # 跨进程共享内存标识
    shape: Tuple[int, ...]
    dtype: str
    strides: Tuple[int, ...]
    data_hash: str       # 可选，用于缓存命中
```

#### 3.1.2 共享内存协议

- **创建**：生产者（如 Physics Engine）调用 `SharedMemoryManager.create()` 创建区域，填充数据，生成 `ArrayHandle`，返回给调用方。
- **传递**：`ArrayHandle` 通过消息队列或直接函数参数发送给消费者。
- **映射**：消费者根据 `shm_id` 映射为 `np.ndarray` 视图，只读或可写（依约定）。
- **释放**：采用引用计数或超时机制清理，避免泄漏；`ArrayHandle` 提供 `close()` 方法。

### 3.2 管道接口详述

#### 3.2.1 输入管道（接口段 → 模型段）

- **载体**：`ParameterizedModelBundle` 对象，通过函数调用传递。
- **附加上下文**：任务元数据 `TaskMetadata`，包含 `mode`（forward/inverse）、`precision`（high/standard/low）、`user_callback`（可选）。
- **协议**：同步调用，接口段等待模型段返回 `task_id` 即表示提交成功；后续通过任务状态通道跟踪。

#### 3.2.2 正演管道（模型段 → 数据段）

- **接口**：`data_segment.store_observable(bundle: ObservableModelBundle) -> None`。
- `ObservableModelBundle` 中的 `histogram.data` 以 `ArrayHandle` 提供，数据段直接映射写入 FITS，无需复制整个数组。
- 数据段写入完成后，在交换目录生成哨兵。

#### 3.2.3 反演管道（数据段 → 模型段）

- **接口**：数据段解析完成后调用模型段的 `model_segment.on_inverse_data(bundle: ObservableModelBundle)`。
- 异步模式，数据段从观测层获取数据后主动推送。

#### 3.2.4 结果管道（模型段 → 接口段）

- **载体**：`ResultBundle` 对象（如 §2.1.4 定义），通过回调或消息队列发回。
- 包含拟合模型、统计量、诊断图表引用。图表数据可以 `ArrayHandle` 或 base64 编码的 JSON 传递。

#### 3.2.5 计算支撑接口（模型段 ↔ Compute Runtime）

- **任务提交**：`compute_runtime.submit(request: ComputeTaskRequest)`。
- **任务完成通知**：Compute Runtime 处理完成后，调用模型段注册的回调 `on_task_complete(task_id, result_handles)`。
- **缓存查询**：`compute_runtime.lookup_cache(param_hash) -> Optional[ArrayHandle]`。

#### 3.2.6 数据服务接口（接口段 → 数据段，横向）

- 受控访问端点：`data_service.get_product_status(task_id) -> Dict[str, ProductStatus]`
- `get_download_stream(task_id, product_type) -> Iterator[bytes]`
- 实现为本地 Unix Domain Socket，接口段不直接访问文件系统。

### 3.3 任务状态模型与事件

**任务状态枚举**：
```python
class TaskState(str, Enum):
    QUEUED = "queued"
    RESOURCE_WAIT = "resource_wait"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
```

**状态通知**：`TaskStatusEvent` 通过事件总线发布到主题 `oasis.task.{task_id}`，携带消息：
```json
{
  "task_id": "...",
  "old_state": "queued",
  "new_state": "running",
  "timestamp": "...",
  "message": "Starting physics simulation"
}
```
接口段订阅该主题，以驱动用户界面刷新。

### 3.4 错误码与异常传递

统一错误码格式 `E_{DOMAIN}_{CODE}`，英文摘要。

| 错误码 | 说明 |
|:---|:---|
| `E_INPUT_001` | YAML syntax error |
| `E_INPUT_002` | Missing required field |
| `E_INPUT_003` | Invalid unit string |
| `E_COMPUTE_001` | Insufficient memory |
| `E_COMPUTE_002` | Parameter out of physical bounds |
| `E_COMPUTE_003` | Simulation diverged |
| `E_DATA_001` | FITS header incompatible |
| `E_DATA_002` | .error sentinel received from observables |
| `E_COMM_001` | Observatory node unreachable |

模型段或数据段抛出异常时，必须包含错误码和英文消息，由 Result Presenter 封装进 `ResultBundle` 并呈现。

---

## 4. 接口版本策略

- 外部接口（YAML schema, FITS 头关键字）通过 `oasis_version` 标识。
- 内部 Pydantic 模型通过类版本字段 `model_version` 管理变迁；当发生不可向后兼容的修改时，递增主版本，并保留旧版本解析器至少一个版本周期。
- 发布-订阅主题命名中携带主版本，如 `oasis.v1.resource.status`，以支持多版本共存。

---

## 5. 诊断与开发支持

- **段间诊断导出**：开发模式下，可将 `ObservableModelBundle` 和 `ParameterizedModelBundle` 导出为 JSON（元数据）和 HDF5（数组）文件，路径由环境变量 `OASIS_DIAG_DIR` 指定，需确保各组件输出文件不冲突。
- **组件内部日志**：统一使用 `logging` 模块，英文格式化，`DEBUG` 级别包含完整 Trace；生产环境日志默认 INFO 或 WARNING。
- **性能计时**：接口段、模型段主要路径记录耗时标签，支持诊断延迟瓶颈。

---

## 6. 与现有设计的一致性

- 所有涉及 `SpatialModel` 的 YAML 输入和 API 参数均需兼容 ADR 006 的字段定义。
- `TargetHistogram` 的引用字段 `source_model_ref` 等，在正演输出时由模型段填充到 FITS 头部。
- `HierarchyDescriptor` 在用户输入时可省略，由层级管理器在模型段内部补全；API 返回的模型中会携带完整层级信息。

---

> 本文档作为目标层接口的权威参考，后续代码实现、测试用例以及外部集成均以此为准。任何接口变更必须同步更新此文档并通过架构讨论。
