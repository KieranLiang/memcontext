# Memcontext MCP 服务器部署指南

Memcontext MCP 服务器是一个基于 Model Context Protocol (MCP) 的智能记忆系统，为 Cursor、Claude Desktop、Claude Code CLI 和 OpenCode 等编辑器提供记忆管理功能。

## ⚡ 快速开始

如果您想快速体验 Memcontext，可以按照以下步骤操作：

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **配置 `config.json`**：
   - 设置您的 `user_id` 和 `openai_api_key`
   - 其他参数可以使用默认值

3. **部署到编辑器**：
   - **Cursor**: 运行 `python setup_cursor.py`
   - **Claude Desktop**: 运行 `python setup_claude_desktop.py`
   - **Claude Code CLI**: 运行 `python setup_claude_code.py`
   - **OpenCode**: 运行 `python setup_opencode.py`

4. **重启编辑器并开始使用**：
   - 重启后，AI 助手会自动使用记忆系统
   - 或者手动使用：`请使用 Memcontext 保存这条对话`

详细说明请继续阅读下面的章节。

## 📋 目录

- [快速开始](#快速开始)
- [环境要求](#环境要求)
- [安装步骤](#安装步骤)
- [配置说明](#配置说明)
- [部署到不同平台](#部署到不同平台)
- [使用方法](#使用方法)
- [记忆系统架构：短中长记忆详解](#记忆系统架构短中长记忆详解)
- [自动记忆管理 (Skill)](#自动记忆管理-skill)
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

### 4. 配置 Memcontext

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

- `user_id`: 用户唯一标识符（必需）
- `openai_api_key`: OpenAI API 密钥（或兼容 API 的密钥，必需）
- `openai_base_url`: API 基础 URL（可选，默认 `https://api.openai.com/v1`）
- `data_storage_path`: 数据存储路径（相对或绝对路径，建议使用绝对路径）
- `assistant_id`: 助手标识符（可选，默认 `memcontext_assistant`）
- `short_term_capacity`: 短期记忆容量（默认 10，存储最近的对话对）
- `mid_term_capacity`: 中期记忆容量（默认 2000，存储历史对话页面）
- `embedding_model_name`: 嵌入模型名称（支持 `BAAI/bge-m3`, `all-MiniLM-L6-v2` 等）
- `long_term_knowledge_capacity`: 长期知识库容量（默认 100，存储用户和助手的知识条目）
- `retrieval_queue_capacity`: 检索队列容量（默认 7，控制检索时的上下文数量）
- `mid_term_heat_threshold`: 中期记忆热度阈值（默认 7.0，用于判断记忆的重要性）
- `mid_term_similarity_threshold`: 中期记忆相似度阈值（默认 0.6，用于去重和合并）
- `llm_model`: 使用的 LLM 模型名称（默认 `gpt-4o-mini`，用于知识提取和总结）

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

### 部署到 Claude Code CLI

**重要说明**：Claude Code CLI 和 Claude Desktop 使用**不同的配置文件**：
- Claude Desktop 使用：`%APPDATA%\Claude\claude_desktop_config.json`（Windows）
- Claude Code CLI 使用：`~/.claude.json`，且 MCP 配置是**按项目存储**的

因此，配置 `claude_desktop_config.json` **不会影响** Claude Code CLI。必须使用专门的配置脚本。

1. **运行配置脚本**：

```bash
python setup_claude_code.py
```

脚本会：
- 检测 Claude Code CLI 是否已安装
- 检测 Python 解释器路径
- **交互式询问配置范围 (scope)**：
  - `local` - 仅当前项目可用
  - `project` - 项目共享
  - `user` - 用户全局可用（跨所有项目，存储在 ~/.claude.json）
- 使用 `claude mcp add` 命令添加 MCP 服务器

2. **验证安装**：
   在 Claude Code CLI 中使用：
   ```
   claude mcp list
   ```
   或者直接在对话中询问：
   ```
   请列出所有可用的 MCP 工具
   ```
   如果能看到 `add_memory`、`retrieve_memory`、`get_user_profile` 工具，说明配置成功。

3. **测试 MCP 工具**：
   在 Claude Code 中测试：
   ```
   请使用 Memcontext 添加一条记忆：我在 Claude Code 中使用 Python
   ```

**注意**：
- 如果选择 `local` scope，配置仅对当前项目有效
- 如果选择 `project` scope，配置存储在项目根目录的 `.mcp.json` 文件中，项目成员可以共享
- 如果选择 `user` scope，配置对所有项目都有效
- 使用 `claude mcp list` 查看所有配置的服务器
- 使用 `claude mcp remove memcontext -s <scope>` 移除指定 scope 的服务器

### 部署到 OpenCode

OpenCode 是通过 npm 全局安装的编辑器。配置步骤：

1. **确保 OpenCode 已安装**：
   ```bash
   npm install -g opencode-ai
   ```

2. **运行配置脚本**：
   ```bash
   python setup_opencode.py
   ```

   脚本会自动：
   - 检测 OpenCode 是否通过 npm 全局安装
   - 自动查找或创建配置文件（**始终使用标准位置**）：
     - **Windows**: `C:\Users\<用户名>\.config\opencode\opencode.json`
     - **macOS/Linux**: `~/.config/opencode/opencode.json`
   - 备份现有配置（如果存在）
   - 更新或创建 MCP 服务器配置

3. **重启 OpenCode**：
   - 完全关闭 OpenCode（不是最小化或重新加载窗口）
   - 重新启动 OpenCode

4. **验证安装**：
   在 OpenCode 的 AI 聊天中询问：
   ```
   请列出所有可用的 MCP 工具
   ```
   如果能看到以下工具，说明配置成功：
   - `add_memory` - 添加记忆
   - `retrieve_memory` - 检索记忆
   - `get_user_profile` - 获取用户画像
   - `update_user_profile` - 更新用户画像
   - `add_user_knowledge` - 添加用户知识

**重要提示**：
- OpenCode 配置文件名称是 `opencode.json`（**不带点**，不是 `.opencode.json`）
- **配置文件标准位置**（脚本会始终写入此位置）：
  - **Windows**: `C:\Users\<用户名>\.config\opencode\opencode.json`
  - **macOS/Linux**: `~/.config/opencode/opencode.json`
- 如果脚本发现旧位置的配置文件（如用户目录下的 `opencode.json`），会提示您，但仍会在标准位置创建新配置
- 建议将旧配置迁移到标准位置
- OpenCode 支持全局配置和项目级配置
- 项目级配置文件位于项目根目录（`opencode.json` 或 `opencode.jsonc`）
- 项目级配置会覆盖全局配置

**故障排除**：
- 如果 OpenCode 无法识别 MCP 工具，请检查：
  1. 配置文件位置是否正确（标准位置：`.config/opencode/opencode.json`）
  2. 配置文件名称是否正确（`opencode.json`，不带点）
  3. 配置文件格式是否正确（`command` 必须是数组）
  4. 是否完全重启了 OpenCode（不是重新加载）
  5. 查看 OpenCode 的日志文件查找错误信息

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
请使用 Memcontext 保存这条对话
```

#### 2. 检索记忆

```
请使用 retrieve_memory 工具查询：我使用什么编程语言？
```

或：
```
请从 Memcontext 检索关于编程语言的记忆
```

#### 3. 获取用户画像

```
请使用 get_user_profile 工具获取我的用户画像
```

### 使用场景示例

#### 场景 1: 保存项目信息
```
用户: 我正在开发一个 Python Web 应用，使用 Flask 框架
AI: [自动保存] 已记录您的项目信息
```

#### 场景 2: 记住用户偏好
```
用户: 我不喜欢吃香菜
AI: [自动保存] 已记录您的饮食偏好
```

#### 场景 3: 检索历史对话
```
用户: 我之前提到过什么项目？
AI: [自动检索] 根据记忆，您之前提到正在开发一个 Python Web 应用...
```

#### 场景 4: 获取用户画像
```
用户: 总结一下我的信息
AI: [调用 get_user_profile] 根据您的记忆，您是一位 Python 开发者...
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


## 🤖 自动记忆管理 (Skill)

为了让 AI 助手能够**自动**使用记忆系统（无需用户显式调用工具），我们提供了一个 Skill 定义文件。

### 什么是 Skill？

`SKILL.md` 文件定义了 "Memory Manager (Memcontext Auto-Pilot)" 技能，它指导 AI 助手：
- **自动检索**历史记忆（在回答前）
- **自动保存**重要信息（在回答后）
- 让对话具备连续性，而不是每次都是新开始

### 如何使用 Skill？

1. **在 Cursor 中使用**：
   - 将 `SKILL.md` 文件的内容复制到 Cursor 的自定义指令（Custom Instructions）中
   - 或者在对话中引用该文件：`@SKILL.md`

2. **在 Claude Desktop 中使用**：
   - 将 `SKILL.md` 的内容添加到 Claude Desktop 的系统提示词中
   - 或者作为对话上下文引用

3. **在 Claude Code CLI中使用**：
   - **方法一（推荐）**：手动复制到技能目录
     
     将 `skills/memory_manager` 目录复制到 Claude Code 的技能目录：
     ```bash
     # Windows (PowerShell)
     $CLAUDE_SKILLS = "$env:USERPROFILE\.claude\skills"
     New-Item -ItemType Directory -Path $CLAUDE_SKILLS -Force | Out-Null
     Copy-Item -Path "memcontext-mcp\skills\memory_manager" -Destination "$CLAUDE_SKILLS\memory_manager" -Recurse -Force
     
     # macOS/Linux
     CLAUDE_SKILLS="$HOME/.claude/skills"
     mkdir -p "$CLAUDE_SKILLS"
     cp -r memcontext-mcp/skills/memory_manager "$CLAUDE_SKILLS/memory_manager"
     ```
     
     然后在 Claude Code 中使用 `/reload-skills` 命令重新加载技能，或者重启 Claude Code。
   
   - **方法二**：在对话中临时引用（不推荐，每次都需要引用）
     ```
     @skills/memory_manager/SKILL.md 请按照这个技能定义来工作
     ```
     
   > **注意**：技能目录位于 `%USERPROFILE%\.claude`（Windows）或 `~/.claude`（macOS/Linux），`SKILL.md` 文件必须在 `memory_manager` 子目录中。

4. **在 OpenCode 中使用**：
   
   **推荐方式**：将 `SKILL.md` 放在 OpenCode 的 skill 目录下 memory_manager目录中
   - `opencode.json` 位置：`C:\Users\<用户名>\.config\opencode\opencode.json`
   - `SKILL.md` 位置：`C:\Users\<用户名>\.config\opencode\skill\memory_manager\SKILL.md`（Windows）
   - 或 `~/.config/opencode/skill/memory_manager/SKILL.md`（macOS/Linux）
   
   **其他方式**：
   - 如果 `SKILL.md` 在项目目录中，直接 `@SKILL.md` 即可
   - 如果 `SKILL.md` 在其他位置，使用完整路径：`@d:/Users/memcontext-dev/memcontext-mcp/SKILL.md`
   - 在 OpenCode 的 AI 聊天中直接引用：
     ```
     @SKILL.md 请按照这个技能定义来工作
     ```
   
   **说明**：
   - `opencode.json` 配置文件位于标准位置（Windows: `C:\Users\<用户名>\.config\opencode\opencode.json`）
   - OpenCode 会自动读取全局配置文件，**不需要在对话中引用**
   - 只需要引用 `SKILL.md` 文件即可启用自动记忆管理
   - 将 `SKILL.md` 放在 `.config/opencode/skill/memory_manager/` 目录下，便于统一管理，且 OpenCode 可以轻松访问

5. **工作流程**：
   Skill 定义了 "查-回-存" 三步法：
   - **Step 1**: 自动检索相关记忆
   - **Step 2**: 结合记忆生成回答
   - **Step 3**: 自动保存有价值的信息

详细说明请查看 [SKILL.md](./SKILL.md) 文件。

## 🧪 测试

### 运行测试脚本

```bash
python test_simple.py
```

测试脚本会验证：
1. Memcontext 初始化
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

**症状**: 服务器启动时提示 Memcontext 初始化失败

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

### 问题 6: 记忆检索不准确

**症状**: 检索到的记忆与查询不相关

**解决方案**:
1. 检查 `embedding_model_name` 是否正确
2. 调整 `mid_term_similarity_threshold` 参数（降低值可提高召回率）
3. 确保记忆已正确保存（检查 `memcontext_data` 目录）

### 问题 7: 数据目录权限问题

**症状**: 无法写入数据目录

**解决方案**:
1. 检查 `data_storage_path` 目录是否存在
2. 确保目录有写入权限
3. 使用绝对路径而不是相对路径

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

> ⚠️ **安全提示**: 请勿将包含真实 API 密钥的配置文件提交到公共代码仓库。建议使用环境变量或配置文件排除在版本控制之外。

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

> 💡 **提示**: 上述路径为示例，实际使用时配置脚本会自动检测并设置正确的路径。

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

> 💡 **提示**: 上述路径为示例，实际使用时配置脚本会自动检测并设置正确的路径。

**OpenCode** (Windows: `C:\Users\<用户名>\.config\opencode\opencode.json`, macOS/Linux: `~/.config/opencode/opencode.json`):
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "memcontext": {
      "type": "local",
      "command": [
        "D:/anaconda3/python.exe",
        "D:/file/memcontext-dev/memcontext-mcp/server_new.py",
        "--config",
        "D:/file/memcontext-dev/memcontext-mcp/config.json"
      ],
      "enabled": true
    }
  }
}
```

> 💡 **提示**: 
> - 上述路径为示例，实际使用时运行 `python setup_opencode.py` 会自动检测并设置正确的路径
> - 配置文件名称必须是 `opencode.json`（**不带点**），不是 `.opencode.json`
> - **配置文件标准位置**（脚本会始终写入此位置）：
>   - Windows: `C:\Users\<用户名>\.config\opencode\opencode.json`
>   - macOS/Linux: `~/.config/opencode/opencode.json`
> - 如果发现旧位置的配置文件，脚本会提示，但仍会在标准位置创建新配置
> - OpenCode 也支持在项目根目录创建 `opencode.json` 进行项目级配置
> - 项目级配置会覆盖全局配置

## 🔄 更新配置

如果需要更新配置：

1. **更新 Memcontext 配置**：直接编辑 `config.json`
2. **更新 MCP 服务器路径**：重新运行对应的 `setup_*.py` 脚本

## 📚 相关资源

- Memcontext 项目主页
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

**最后更新**: 2026-01-14
