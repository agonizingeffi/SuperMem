# SuperMem

SuperMem 是面向大语言模型与智能体的记忆管理项目，提供记忆写入、检索、摘要和离线更新能力。可直接调用已部署的 HTTP 服务，也可在本地使用 Python 包或 MCP 服务。

项目仓库：https://github.com/agonizingeffi/SuperMem

## 已部署接口

| 功能 | 方法 | 地址 |
| --- | --- | --- |
| 写入记忆（Add） | POST | `https://supermem.021130.xyz/add` |
| 检索记忆（Search） | POST | `https://supermem.021130.xyz/search` |
| 健康检查（Health） | GET | `https://supermem.021130.xyz/health` |

Add 和 Search 均使用 JSON 请求体，需设置 `Content-Type: application/json`，无需 API Key。请求字段需符合部署服务的接口约定。

健康检查：

```bash
curl https://supermem.021130.xyz/health
```

### 运行与并发限制

- 已部署服务采用单进程运行。
- SQLite 持久化保存原文，Qdrant 保存派生索引。
- Add 成功返回后，新增内容即可检索。
- 相同 `request_id` 且请求内容一致的 Add 请求支持幂等重试。
- Add 支持最多 16 个并发调用；调用方应将同时进行的 Add 请求控制在 16 个以内。

## 本地安装

Python 包要求 Python 3.10 或 3.11。建议在独立虚拟环境中安装。

```bash
git clone https://github.com/agonizingeffi/SuperMem.git
cd SuperMem
python -m venv .venv
```

激活虚拟环境后安装项目：

```bash
python -m pip install -e .
```

Windows PowerShell 激活命令为 `.\.venv\Scripts\Activate.ps1`；Linux/macOS 为 `source .venv/bin/activate`。

使用本地模型、GPU 或独立评测工具时，还需满足对应组件的环境要求。

## Python 使用示例

先编辑 `mcp/example.json`，配置模型服务、模型路径、嵌入维度及存储路径，再运行以下代码。已部署 HTTP 接口无需 API Key；本地模型配置中的鉴权信息取决于所选模型服务。

```python
import json
from pathlib import Path

from supermem.memory.supermem import SuperMemory

config = json.loads(Path("mcp/example.json").read_text(encoding="utf-8"))
memory = SuperMemory.from_config(config)

memory.add_memory(
    messages=[
        {
            "role": "user",
            "content": "我喜欢喝不加糖的拿铁。",
            "time_stamp": "2026-10-12T09:00:00",
        }
    ],
    force_segment=True,
    force_extract=True,
)

results = memory.retrieve("我喜欢喝什么咖啡？", limit=5)
for result in results:
    print(result)
```

主要方法：

| 方法 | 用途 |
| --- | --- |
| `SuperMemory.from_config(config)` | 根据配置初始化记忆系统 |
| `add_memory(messages=...)` | 写入对话记忆 |
| `retrieve(query, limit=...)` | 检索相关记忆 |
| `summarize(...)` | 生成记忆摘要 |
| `construct_update_queue_all_entries()` | 构建离线更新队列 |
| `offline_update_all_entries(...)` | 执行离线记忆更新 |

## MCP 服务

安装 MCP 可选依赖：

```bash
python -m pip install -e ".[mcp]"
```

使用标准输入输出方式启动：

```bash
python mcp/server.py --config mcp/example.json
```

使用 HTTP 方式启动，默认读取 `mcp/example.json`：

```bash
fastmcp run mcp/server.py:mcp --transport http --port 8000
```

MCP HTTP 地址为 `http://127.0.0.1:8000/mcp`。

## 项目结构

```text
SuperMem/
├── src/supermem/       # Python 包、配置、记忆管理与评测工具
├── mcp/                # MCP 服务与配置示例
├── examples/           # 本地使用示例
├── experiments/        # 数据集评测与实验脚本
├── dataset/            # 数据集目录
├── tests/              # 测试
└── pyproject.toml      # 包元数据与依赖配置
```

## 评测与工具说明

- [LongMemEval 使用说明](experiments/longmemeval/readme.md)
- [LoCoMo 使用说明](experiments/locomo/readme.md)
- [记忆评测工具说明](src/supermem/memory_toolkits/readme.md)

运行前请按对应说明配置数据路径、模型服务和输出目录。不要将真实 API Key 或本地凭据提交到仓库。
