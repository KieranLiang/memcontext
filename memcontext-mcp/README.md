# MemoryOS MCP 服务器部署指南

Memcontext MCP 服务器是一个基于 Model Context Protocol (MCP) 的智能记忆系统，为 Cursor 和 Claude Desktop 等编辑器提供记忆管理功能。

## 📋 目录

- [环境要求](#环境要求)
- [安装步骤](#安装步骤)
- [配置说明](#配置说明)
- [部署到不同平台](#部署到不同平台)
- [使用方法](#使用方法)
- [测试](#测试)
- [故障排除](#故障排除)

## 🔧 环境要求

### 必需环境

- **Python**: 3.8 或更高版本
- **操作系统**: Windows / macOS / Linux
- **内存**: 建议 4GB 以上（用于运行嵌入模型）

### Python 依赖

项目需要以下 Python 包（见 `requirements.txt`）：
- `mcp` - Model Context Protocol 服务器框架
- `sentence-transformers` - 文本嵌入模型
- `transformers` - Hugging Face 模型库
- `faiss-cpu` - 向量相似度搜索
- `FlagEmbedding` - BGE-M3 嵌入模型支持
- `openai` - OpenAI API 客户端
- 其他依赖见 `requirements.txt`

### Windows 额外要求

如果需要在 Windows 上编译某些 Python 包，可能需要：
- **Microsoft Visual C++ Build Tools**（可选，仅在安装需要编译的包时使用）

## 📦 安装步骤

### 1. 克隆或下载项目

```bash
cd memcontext-mcp
```

### 2. 创建 Python 虚拟环境（推荐）

```bash
# 使用 conda
conda create -n mcp python=3.10
conda activate mcp

# 或使用 venv
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 MemoryOS

编辑 `config.json` 文件，设置以下必需参数：

```json
{
  "user_id": "your_user_id",
  "openai_api_key": "your_api_key",
  "openai_base_url": "https://api.openai.com/v1",
  "data_storage_path": "./memcontext_data",
  "assistant_id": "memcontext_assistant",
  "short_term_capacity": 10,
  "mid_term_capacity": 2000,
  "embedding_model_name": "BAAI/bge-m3",
  "long_term_knowledge_capacity": 100,
  "retrieval_queue_capacity": 7,
  "mid_term_heat_threshold": 7.0,
  "mid_term_similarity_threshold": 0.6,
  "llm_model": "gpt-4o-mini"
}
```

**配置参数说明：**

- `user_id`: 用户唯一标识符
- `openai_api_key`: OpenAI API 密钥（或兼容 API 的密钥）
- `openai_base_url`: API 基础 URL（可选，默认 OpenAI）
- `data_storage_path`: 数据存储路径（相对或绝对路径）
- `assistant_id`: 助手标识符
- `short_term_capacity`: 短期记忆容量
- `mid_term_capacity`: 中期记忆容量
- `embedding_model_name`: 嵌入模型名称（支持 `BAAI/bge-m3`, `all-MiniLM-L6-v2` 等）
- `llm_model`: 使用的 LLM 模型名称

## 🚀 部署到不同平台

### 部署到 Cursor

1. **运行配置脚本**：

```bash
python setup_cursor.py
```

脚本会自动：
- 检测 Python 解释器路径
- 备份现有配置（如果存在）
- 更新 `~/.cursor/mcp.json` 配置文件

2. **重启 Cursor**：
   - 完全关闭 Cursor（不是最小化）
   - 重新启动 Cursor

3. **验证安装**：
   在 Cursor 的 AI 聊天中询问：
   ```
   请列出所有可用的 MCP 工具
   ```
   如果能看到 `add_memory`、`retrieve_memory`、`get_user_profile` 工具，说明配置成功。

### 部署到 Claude Desktop

1. **运行配置脚本**：

```bash
python setup_claude_desktop.py
```

脚本会自动：
- 检测操作系统类型
- 找到 Claude Desktop 配置文件位置：
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Linux: `~/.config/claude/claude_desktop_config.json`
- 备份现有配置
- 更新配置文件

2. **重启 Claude Desktop**：
   - 完全关闭 Claude Desktop
   - 重新启动

3. **验证安装**：
   在 Claude Desktop 中询问：
   ```
   请列出所有可用的 MCP 工具
   ```

## 💻 使用方法

### 在编辑器中使用

配置完成后，您可以在编辑器的 AI 聊天中直接使用以下工具：

#### 1. 添加记忆

```
请使用 add_memory 工具保存这条对话：
- user_input: 我在使用 Python 编程
- agent_response: Python 是一门很好的编程语言
```

或简单说：
```
请使用 MemoryOS 保存这条对话
```

#### 2. 检索记忆

```
请使用 retrieve_memory 工具查询：我使用什么编程语言？
```

或：
```
请从 MemoryOS 检索关于编程语言的记忆
```

#### 3. 获取用户画像

```
请使用 get_user_profile 工具获取我的用户画像
```

### 工具参数说明

#### `add_memory`
- `user_input` (必需): 用户的输入或问题
- `agent_response` (必需): 助手的回应
- `timestamp` (可选): 时间戳，格式：`YYYY-MM-DD HH:MM:SS`
- `meta_data` (可选): 元数据字典

#### `retrieve_memory`
- `query` (必需): 检索查询文本
- `relationship_with_user` (可选): 与用户的关系类型，默认 `"friend"`
- `style_hint` (可选): 回应风格提示
- `max_results` (可选): 最大结果数量，默认 `10`

#### `get_user_profile`
- `include_knowledge` (可选): 是否包含用户知识，默认 `True`
- `include_assistant_knowledge` (可选): 是否包含助手知识，默认 `False`

## 🧪 测试

### 运行测试脚本

```bash
python test_simple.py
```

测试脚本会验证：
1. MemoryOS 初始化
2. `add_memory` 工具功能
3. `retrieve_memory` 工具功能
4. `get_user_profile` 工具功能

### 手动测试 MCP 服务器

```bash
python server_new.py --config config.json
```

服务器会通过 stdio 与 MCP 客户端通信。

## 🔍 故障排除

### 问题 1: 工具不可用

**症状**: 在编辑器中看不到 MCP 工具

**解决方案**:
1. 确认已完全重启编辑器（不是最小化）
2. 检查配置文件路径是否正确
3. 检查 Python 路径是否正确
4. 查看编辑器日志中的错误信息

### 问题 2: 初始化失败

**症状**: 服务器启动时提示 MemoryOS 初始化失败

**解决方案**:
1. 检查 `config.json` 文件格式是否正确
2. 确认所有必需字段都已填写
3. 检查 `data_storage_path` 路径是否可写
4. 确认 API 密钥有效

### 问题 3: 路径问题

**症状**: 找不到配置文件或数据目录

**解决方案**:
1. 使用绝对路径而不是相对路径
2. Windows 路径使用正斜杠 `/` 或双反斜杠 `\\`
3. 检查路径中是否有特殊字符

### 问题 4: 依赖安装失败

**症状**: `pip install` 失败

**解决方案**:
1. 更新 pip: `pip install --upgrade pip`
2. 使用国内镜像源（如需要）:
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
3. Windows 上可能需要安装 Visual C++ Build Tools

### 问题 5: 嵌入模型下载慢

**症状**: 首次运行时下载模型很慢

**解决方案**:
1. 使用国内镜像或代理
2. 手动下载模型到本地，修改 `embedding_model_name` 为本地路径
3. 使用较小的模型（如 `all-MiniLM-L6-v2`）

## 📝 配置文件示例

### 完整配置示例

```json
{
  "user_id": "test_user_001",
  "openai_api_key": "your-api-key-here",
  "openai_base_url": "https://api.openai.com/v1",
  "data_storage_path": "./memcontext_data",
  "assistant_id": "memcontext_assistant",
  "short_term_capacity": 10,
  "mid_term_capacity": 2000,
  "embedding_model_name": "BAAI/bge-m3",
  "long_term_knowledge_capacity": 100,
  "retrieval_queue_capacity": 7,
  "mid_term_heat_threshold": 7.0,
  "mid_term_similarity_threshold": 0.6,
  "llm_model": "gpt-4o-mini"
}
```

### MCP 配置示例（自动生成）

**Cursor** (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "memcontext": {
      "command": "D:/anaconda3/envs/mcp/python.exe",
      "args": [
        "D:/project/memcontext-memcontext/memcontext-mcp/server_new.py",
        "--config",
        "D:/project/memcontext-memcontext/memcontext-mcp/config.json"
      ],
      "env": {}
    }
  }
}
```

**Claude Desktop** (`%APPDATA%\Claude\claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "memcontext": {
      "command": "D:/anaconda3/envs/mcp/python.exe",
      "args": [
        "D:/project/memcontext-memcontext/memcontext-mcp/server_new.py",
        "--config",
        "D:/project/memcontext-memcontext/memcontext-mcp/config.json"
      ],
      "env": {}
    }
  }
}
```

## 🔄 更新配置

如果需要更新配置：

1. **更新 MemoryOS 配置**：直接编辑 `config.json`
2. **更新 MCP 服务器路径**：重新运行对应的 `setup_*.py` 脚本

## 📚 相关资源

- MemoryOS 项目主页
- MCP 协议文档
- 支持的嵌入模型列表

## ⚠️ 注意事项

1. **API 密钥安全**：不要将包含 API 密钥的 `config.json` 提交到公共仓库
2. **数据备份**：定期备份 `memcontext_data` 目录
3. **路径格式**：Windows 路径建议使用正斜杠 `/` 以避免转义问题
4. **重启要求**：修改配置后必须重启编辑器才能生效

## 📞 支持

如遇到问题，请检查：
1. Python 版本是否符合要求
2. 所有依赖是否正确安装
3. 配置文件格式是否正确
4. 编辑器日志中的错误信息

---

**最后更新**: 2026-01-07

