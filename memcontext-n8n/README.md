# n8n 记忆管理服务 - 超详细部署指南

> 🎯 专为完全零基础小白设计的超详细教程，每个步骤都有详细说明和验证方法

## 📋 目录

### 快速开始（使用脚本）
- [快速开始 - 使用脚本快速上手](#快速开始---使用脚本快速上手)

### 基础部分
- [什么是这个服务？](#什么是这个服务)
- [架构说明：服务是如何运行的？](#架构说明服务是如何运行的)
- [前置要求检查清单](#前置要求检查清单)

### 部署步骤（按顺序执行）
- [第一步：下载代码](#第一步下载代码)
- [第二步：安装 Python 依赖](#第二步安装-python-依赖)
- [第三步：配置文件](#第三步配置文件)
- [第四步：启动服务](#第四步启动服务)
- [第五步：在 n8n 平台安装插件](#第五步在-n8n-平台安装插件)
- [第六步：在 n8n 中创建工作流](#第六步在-n8n-中创建工作流)

### 参考文档
- [工作流程图解](#工作流程图解)
- [完整测试流程](#完整测试流程)

### 问题排查
- [常见问题详细排查](#常见问题详细排查)

### 进阶
- [进阶使用](#进阶使用)

---

## 快速开始 - 使用脚本快速上手

> ⚡ **适用于已经了解基本操作的用户**  
> 如果你想快速开始，可以使用以下脚本自动完成大部分步骤。  
> 如果是第一次使用，建议按照后面的详细步骤操作。

### 🚀 快速开始步骤

#### 步骤 1：前置检查（必需）

确保你已经安装了：
- ✅ Python 3.8+
- ✅ pip
- ✅ FFmpeg（用于视频处理）
- ✅ Docker Desktop（如果需要使用 Docker 运行 n8n）

**检查方法**：
```bash
python --version
pip --version
ffmpeg -version
docker --version
```

#### 步骤 2：安装依赖（一次性）

在**项目根目录**执行：
```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 memcontext 包
pip install -e .

# 安装 memcontext-n8n 依赖
pip install -r memcontext-n8n/requirements.txt
```

#### 步骤 3：创建 .env 文件（必需）

**重要**：需要在**两个位置**创建 `.env` 文件

在**项目根目录**执行：
```bash
# 切换到项目根目录
cd D:\project\memcontext-memcontext

# 创建根目录的 .env 文件
type nul > .env

# 复制到 memcontext 目录
copy .env memcontext\.env

# 验证创建成功
dir .env
dir memcontext\.env
```

**编辑 .env 文件**（使用记事本或任何编辑器）：

在**两个位置**的 `.env` 文件中都添加以下内容：
```env
# ============================================
# Memcontext-n8n API Key 配置（必需）
# ============================================
# 用于访问 memcontext-n8n 服务的 API Key
# 可以设置任意字符串，建议使用随机字符串
# 多个 Key 用逗号分隔
N8N_API_KEYS=your-secret-key-here

# ============================================
# n8n API Key 配置（可选）
# ============================================
# 用于调用 n8n API 的 Key（如果 n8n 需要 API Key 认证）
# 如果不需要，可以删除这一行
N8N_API_KEY=your-n8n-api-key-here

# ============================================
# LLM 配置（必需）
# ============================================
# LLM API Key
LLM_API_KEY=sk-your-llm-api-key-here

# LLM API 地址
# OpenAI: https://api.openai.com/v1
# 火山引擎: https://ark.cn-beijing.volces.com/api/v3
LLM_BASE_URL=https://api.openai.com/v1

# LLM 模型名称
# OpenAI: gpt-4, gpt-3.5-turbo, gpt-4-turbo-preview
# 火山引擎: ep-20241208200000-xxxxx
LLM_MODEL=gpt-4

# ============================================
# Embedding 模型配置（可选）
# ============================================
# 用于文本向量化
# OpenAI: text-embedding-3-small, text-embedding-3-large
# 如果不设置，会使用默认值
EMBEDDING_MODEL=text-embedding-3-small

# ============================================
# SiliconFlow 配置（可选）
# ============================================
# 用于视频/音频转录
# 如果不需要视频/音频功能，可以删除这一行
SILICONFLOW_API_KEY=your-siliconflow-api-key-here
```

**注意**：
- 将 `your-secret-key-here` 替换为你自己的 Memcontext-n8n API Key（可以是任意字符串，建议使用随机字符串）
- 将 `your-n8n-api-key-here` 替换为你的 n8n API Key（如果 n8n 需要 API Key 认证）
- 将 `sk-your-llm-api-key-here` 替换为你的 LLM API Key（例如 OpenAI 的 sk-... 格式）
- 根据你使用的 LLM 服务，修改 `LLM_BASE_URL` 和 `LLM_MODEL`
- 两个 `.env` 文件内容应该完全相同

#### 步骤 4：启动记忆服务

**打开第一个命令行窗口**：

```bash
# 进入 memcontext-n8n 目录
cd memcontext-n8n

# 启动服务
python app.py
```

**看到以下输出说明启动成功**：
```
 * Running on http://127.0.0.1:5019
```

**重要**：**保持这个窗口打开**，不要关闭！

#### 步骤 5：启动 n8n（使用 Docker 脚本）

**打开第二个命令行窗口**：

```bash
# 进入 memcontext-n8n 目录
cd memcontext-n8n

# 运行 Docker 启动脚本
docker-run-n8n.bat
```

**脚本会自动**：
- ✅ 检查 Docker 状态
- ✅ 检查端口是否被占用
- ✅ 启动 n8n Docker 容器
- ✅ 挂载本地目录

**等待脚本执行完成**，然后访问：`http://localhost:5678`

**默认登录**：
- 用户名：`admin`
- 密码：`admin`

#### 步骤 6：创建工作流（使用脚本）

**打开第三个命令行窗口**：

```bash
# 进入 memcontext-n8n 目录
cd memcontext-n8n

# 运行工作流创建脚本
create_video_workflow.bat
```

**脚本会自动**：
- ✅ 创建工作流
- ✅ 配置所有节点
- ✅ 激活工作流

**执行完成后**，你会看到工作流 URL，例如：
```
Workflow URL: http://localhost:5678/workflow/123
```

#### 步骤 7：测试工作流

1. **打开浏览器**，访问：`http://localhost:5678`
2. **登录 n8n**（用户名：`admin`，密码：`admin`）
3. **找到工作流**："Video Upload and Retrieval Workflow"
4. **打开工作流**，点击 "When clicking test" 节点
5. **点击右上角的 "Execute Workflow" 按钮**
6. **等待执行完成**（视频处理可能需要几分钟）
7. **查看结果**：在 "Format Output" 节点查看执行结果

### 📝 快速开始命令总结

**在一个新的命令行窗口中，按顺序执行**：

```bash
# ============================================
# 1. 切换到项目根目录
# ============================================
cd D:\project\memcontext-memcontext

# ============================================
# 2. 安装依赖（仅第一次需要）
# ============================================
pip install -r requirements.txt
pip install -e .
pip install -r memcontext-n8n/requirements.txt

# ============================================
# 3. 创建 .env 文件（仅第一次需要）
# ============================================
type nul > .env
copy .env memcontext\.env
# 然后手动编辑两个 .env 文件，填入配置

# ============================================
# 4. 启动记忆服务（窗口1，保持打开）
# ============================================
cd memcontext-n8n
python app.py

# ============================================
# 5. 启动 n8n（窗口2，保持打开）
# ============================================
# 在另一个命令行窗口执行：
cd memcontext-n8n
docker-run-n8n.bat

# ============================================
# 6. 创建工作流（窗口3，执行一次即可）
# ============================================
# 在另一个命令行窗口执行：
cd memcontext-n8n
create_video_workflow.bat

# ============================================
# 7. 测试工作流
# ============================================
# 在浏览器访问：http://localhost:5678
# 登录后找到 "Video Upload and Retrieval Workflow"
# 执行工作流测试
```

### ⚠️ 常见问题

**Q: 脚本执行失败？**

A: 请检查：
1. 是否在正确的目录执行脚本
2. Python 和 pip 是否已安装
3. `.env` 文件是否在两个位置都存在
4. Docker Desktop 是否正在运行（如果使用 Docker）

**Q: 服务启动失败？**

A: 请检查：
1. 端口 5019 是否被占用
2. `.env` 文件配置是否正确
3. Python 依赖是否已安装

**Q: n8n 无法访问？**

A: 请检查：
1. Docker Desktop 是否正在运行
2. 端口 5678 是否被占用
3. 是否等待容器完全启动

**更多问题**：请查看后面的 [常见问题详细排查](#常见问题详细排查) 章节

---

## 什么是这个服务？

这是一个**记忆管理 API 服务**，可以：

- ✅ **记住对话**：保存用户和 AI 的对话内容，下次可以回忆起来
- ✅ **智能检索**：根据问题自动查找相关记忆，生成个性化回复
- ✅ **视频处理**：上传视频，自动提取内容并建立记忆
- ✅ **多模态支持**：支持文本、视频、音频、图片等多种格式

**简单来说**：让你的 n8n 工作流拥有"记忆"功能，可以记住历史对话和内容。

**工作流程示意**：
```
用户提问 → n8n 工作流 → 记忆服务 → 查找相关记忆 → 生成个性化回复 → 返回给用户
```

---

## 架构说明：服务是如何运行的？

### 运行架构

**简单说明**：这是一个记忆管理 API 服务，运行在你的本地机器上，n8n 工作流通过 HTTP 请求调用它。

#### 1. memcontext-n8n/app.py 服务

**运行位置**：你的本地机器上，监听端口 5019

**功能**：
- 提供记忆管理 API 接口
- 处理记忆的添加、检索、更新
- 支持视频、音频等多媒体文件处理

**启动方式**：
```bash
cd memcontext-n8n
python app.py
```

#### 2. n8n 平台

**运行位置**：你的 n8n 平台（本地或云端）

**功能**：
- 创建工作流
- 通过 HTTP Request 节点调用记忆服务
- 处理业务逻辑

**假设**：你已经安装并运行了 n8n 平台

#### 3. 两者如何通信？

**通信流程**：
```
┌─────────────────────────────────────────────────────────┐
│  n8n 平台（你的 n8n 实例）                              │
│  - 可以是本地 n8n（localhost:5678）                    │
│  - 也可以是云端 n8n                                     │
│  - 通过 HTTP Request 节点发送请求                       │
│      ↓                                                  │
│  http://localhost:5019/api/memory/search              │
│  或 http://你的服务器IP:5019/api/memory/search         │
│      ↓                                                  │
└─────────────────────────────────────────────────────────┘
                    │
                    │ HTTP 请求
                    ▼
┌─────────────────────────────────────────────────────────┐
│  memcontext-n8n/app.py (本地运行)                             │
│  - 运行在你的机器上                                      │
│  - 端口: 5019                                           │
│  - 接收 HTTP 请求                                        │
│      ↓                                                  │
│  调用 memcontext 模块处理记忆                           │
│      ↓                                                  │
│  返回 JSON 响应                                         │
└─────────────────────────────────────────────────────────┘
```

**关键点**：
- 如果 n8n 和 app.py 在同一台机器：使用 `http://localhost:5019`
- 如果 n8n 在云端，app.py 在本地：需要配置端口转发或使用公网 IP
- 通信使用标准的 HTTP/HTTPS 协议

### 总结

**架构特点**：
- ✅ 服务运行在本地，简单直接
- ✅ 通过 HTTP API 与 n8n 通信
- ✅ 支持本地和云端 n8n 平台

---

## 前置要求检查清单

在开始之前，请逐一检查以下项目：

### ✅ 必需软件检查

#### 1. Python 3.8 或更高版本

**检查方法**：
1. 按 `Win + R` 键，输入 `cmd`，按回车打开命令行
2. 输入以下命令：
   ```bash
   python --version
   ```
3. 应该看到类似输出：
   ```
   Python 3.11.5
   ```
   **如果看到**：`'python' 不是内部或外部命令`
   **解决方法**：
   - 下载安装 Python：[https://www.python.org/downloads/](https://www.python.org/downloads/)
   - 安装时**务必勾选** "Add Python to PATH"
   - 安装完成后，重新打开命令行再试

#### 2. pip 包管理器

**检查方法**：
```bash
pip --version
```

**应该看到**：
```
pip 23.2.1 from C:\Users\...\site-packages\pip (python 3.11)
```

**如果没有安装**：Python 3.4+ 自带 pip，如果提示找不到，重新安装 Python 并勾选 "Add Python to PATH"

#### 3. FFmpeg（用于视频处理，必需）

**检查方法**：
```bash
ffmpeg -version
```

**应该看到**：
```
ffmpeg version 6.x.x ...
```

**如果没有安装**：

**Windows 安装方法**：
1. 访问 [FFmpeg 官网](https://ffmpeg.org/download.html)
2. 下载 Windows 版本（推荐使用 [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/) 提供的构建版本）
3. 解压到任意目录（例如：`C:\ffmpeg`）
4. 将 `C:\ffmpeg\bin` 添加到系统环境变量 PATH 中：
   - 右键"此电脑" → "属性" → "高级系统设置" → "环境变量"
   - 在"系统变量"中找到 `Path`，点击"编辑"
   - 点击"新建"，输入 `C:\ffmpeg\bin`
   - 点击"确定"保存
5. 重新打开命令行，运行 `ffmpeg -version` 验证

**macOS 安装方法**：
```bash
# 使用 Homebrew
brew install ffmpeg
```

**Linux 安装方法**：
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

**验证安装**：
```bash
ffmpeg -version
```

#### 4. n8n 平台（已安装并运行）

**假设**：你已经安装并运行了 n8n 平台

**检查方法**：
- 访问你的 n8n 地址（例如：`http://localhost:5678`）
- 如果能正常打开 n8n 界面，说明 n8n 已运行

**如果没有安装 n8n**：
- 本地安装：访问 [n8n 官网](https://n8n.io/) 查看安装说明
- 云端使用：使用 n8n Cloud 或其他 n8n 托管服务

#### 5. Docker（用于运行 n8n，可选）

**如果使用 Docker 运行 n8n**，需要安装 Docker Desktop：

**检查方法**：
```bash
docker --version
```

**如果没有安装**：
- Windows/macOS：下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Linux：按照 [Docker 官方文档](https://docs.docker.com/engine/install/) 安装

### ✅ 必需账号和密钥

#### 1. LLM API Key（必需）

**支持的平台**：
- OpenAI（推荐）：[https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- 火山引擎：[https://console.volcengine.com/](https://console.volcengine.com/)
- 其他兼容 OpenAI API 的服务

**获取方法（以 OpenAI 为例）**：
1. 访问 [OpenAI 官网](https://platform.openai.com/)
2. 注册/登录账号
3. 进入 API Keys 页面
4. 点击 "Create new secret key"
5. 复制生成的 API Key（格式类似：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）
6. **重要**：API Key 只显示一次，请妥善保存
7. 将 API Key 填入 `.env` 文件中的 `LLM_API_KEY` 变量

#### 2. SiliconFlow API Key（可选）

**用途**：用于视频/音频转录

**获取方法**：
1. 访问 [SiliconFlow](https://siliconflow.cn/)
2. 注册账号
3. 在控制台获取 API Key

**注意**：如果不需要视频/音频功能，可以跳过这一步

---

## 第一步：下载代码

### 1.1 获取项目代码

#### 方式1：从 GitHub 克隆（推荐）

**前提**：已安装 Git

**步骤**：
1. 打开命令行
2. 进入你想存放项目的目录，例如：
   ```bash
   cd C:\Users\YourName\Projects
   ```
   或
   ```bash
   cd D:\project
   ```
3. 克隆项目（替换为实际的项目地址）：
   ```bash
   git clone <项目地址>
   ```
4. 进入项目目录：
   ```bash
   cd memcontext-memcontext
   ```

#### 方式2：下载 ZIP 文件

1. 在 GitHub 页面点击 "Code" → "Download ZIP"
2. 解压 ZIP 文件到本地目录（可以是任意位置）
3. 打开命令行，进入项目目录：
   ```bash
   cd <解压后的项目目录路径>
   ```
   例如：`cd C:\Users\YourName\Downloads\memcontext-memcontext`

### 1.2 验证项目结构

**检查项目目录结构**：

在命令行中执行：
```bash
dir
```

**应该看到类似**：
```
memcontext-n8n/
  - app.py
  - create_video_workflow.py
  - create_video_workflow.bat
  - docker-run-n8n.bat
  - README.md
memcontext-coze/
README.md
.env.example
...
```

**如果没有看到这些文件**：
- 检查是否在正确的目录
- 检查项目是否完整下载

### 1.3 确认当前目录

**重要**：后续所有操作都在项目**根目录**进行（不是 memcontext-n8n 目录）

**验证方法**：
```bash
cd
```

**应该显示**：
```
<你的项目根目录路径>
```
例如：`C:\Users\YourName\Projects\memcontext-memcontext`

如果不在项目根目录，执行：
```bash
cd <项目根目录路径>
```

---

## 第二步：安装 Python 依赖

### 2.1 检查 requirements.txt

**步骤**：
1. 确认项目根目录有 `requirements.txt` 文件：
   ```bash
   dir requirements.txt
   ```

2. 或者使用 memcontext-n8n 目录的 `requirements.txt`（仅包含 memcontext-n8n 需要的依赖）：
   ```bash
   dir memcontext-n8n\requirements.txt
   ```

### 2.2 安装项目依赖

**方法1：使用项目根目录的 requirements.txt（推荐，包含所有依赖）**

在项目**根目录**执行：
```bash
pip install -r requirements.txt
```

**方法2：使用 memcontext-n8n 目录的 requirements.txt（仅 memcontext-n8n 依赖）**

如果你只需要运行 memcontext-n8n，可以使用精简版：
```bash
pip install -r memcontext-n8n/requirements.txt
```

**注意**：使用方式2后，还需要安装 memcontext 包（见 2.3）

**执行过程**：
- 会显示安装进度，例如：
  ```
  Collecting flask
    Downloading flask-3.0.0-py3-none-any.whl (99 kB)
  ...
  Successfully installed flask-3.0.0 ...
  ```
- 等待安装完成（可能需要几分钟）

**如果遇到错误**：
- `pip 不是内部或外部命令`：检查 Python 是否正确安装
- `Permission denied`：尝试使用 `pip install --user -r requirements.txt`
- 网络错误：检查网络连接，或使用国内镜像：
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

**方法3：手动安装核心依赖（如果 requirements.txt 安装失败）**

如果 `requirements.txt` 不存在或安装失败，可以手动安装所有必需的依赖包：

**步骤1：安装基础依赖**
```bash
pip install flask python-dotenv requests
```

**步骤2：安装科学计算和机器学习库**
```bash
pip install numpy sentence-transformers transformers FlagEmbedding faiss-cpu
```

**步骤3：安装 OpenAI 和其他工具库**
```bash
pip install openai typing-extensions regex
```

**完整命令（一次性安装）**：
```bash
pip install flask python-dotenv requests numpy sentence-transformers transformers FlagEmbedding faiss-cpu openai typing-extensions regex
```

**注意**：这些是运行 memcontext-n8n 服务所需的核心依赖。如果使用 conda 环境，建议使用 conda 安装部分包：
```bash
conda install numpy -y
pip install flask python-dotenv requests sentence-transformers transformers FlagEmbedding faiss-cpu openai typing-extensions regex
```

### 2.3 安装 memcontext 包

**步骤**：
```bash
pip install -e .
```

**执行过程**：
- 会显示安装信息
- 如果已经安装过，会显示 "Requirement already satisfied"

**验证安装**：
```bash
python -c "import memcontext; print('memcontext 安装成功')"
```

**应该看到**：
```
memcontext 安装成功
```

---

## 第三步：配置文件

### 3.1 创建 .env 文件

**重要**：`.env` 文件需要在**两个位置**都创建：
1. **项目根目录**（必需）
2. **memcontext 目录**（必需）

#### .env 文件位置说明

`.env` 文件必须放在以下**两个位置**：

**位置1：项目根目录**（必需）
**位置2：memcontext 目录**（必需）

项目结构应该是这样的：

```
memcontext-memcontext/          ← 项目根目录
├── .env                        ← .env 文件位置1（必需）
├── memcontext-n8n/
│   ├── app.py
│   ├── create_video_workflow.py
│   ├── docker-run-n8n.bat
│   └── README.md
├── memcontext-mcp/
├── memcontext/
│   └── .env                    ← .env 文件位置2（必需）
├── memdemo/
└── requirements.txt
```

**为什么需要两个 .env 文件？**：

- **项目根目录的 .env**：用于 `memcontext-n8n`、`memdemo` 等服务从根目录加载配置
- **memcontext 目录的 .env**：用于 `memcontext` 包内的代码（如视频处理模块）加载配置

**注意**：两个 `.env` 文件内容应该**完全相同**，建议：
1. 先创建项目根目录的 `.env` 文件
2. 复制到 `memcontext` 目录

**验证方法**：

在项目根目录执行：
```bash
# 查看当前目录
cd

# 应该显示项目根目录路径，例如：
# D:\project\memcontext-memcontext

# 检查根目录的 .env 文件是否存在
dir .env

# 应该看到 .env 文件

# 检查 memcontext 目录的 .env 文件是否存在
dir memcontext\.env

# 应该看到 .env 文件

# 检查是否正确（应该同时看到 memcontext-n8n 和 memcontext 目录）
dir memcontext-n8n
dir memcontext
```

**常见错误**：
- ❌ 错误：只在根目录创建了 .env，忘记在 memcontext 目录创建
- ❌ 错误：只在 memcontext 目录创建了 .env，忘记在根目录创建
- ❌ 错误：将 .env 放在 `memcontext-n8n` 目录下
- ✅ 正确：在**项目根目录**和**memcontext 目录**都创建 .env 文件

#### Windows 用户创建方法

**方法1：使用命令行**

**步骤1：在项目根目录创建 .env**

在项目**根目录**执行：
```bash
# 首先确保在项目根目录
cd D:\project\memcontext-memcontext

# 创建根目录的 .env 文件
type nul > .env

# 验证创建成功
dir .env
```

**步骤2：复制到 memcontext 目录**

```bash
# 将根目录的 .env 复制到 memcontext 目录
copy .env memcontext\.env

# 验证复制成功
dir memcontext\.env
```

**一键创建两个 .env 文件（推荐）**：

在项目根目录执行以下命令，一次性创建两个 .env 文件：

```bash
# 在项目根目录执行
cd D:\project\memcontext-memcontext

# 创建根目录的 .env 文件
type nul > .env

# 复制到 memcontext 目录
copy .env memcontext\.env

# 验证创建成功
echo === 验证 .env 文件位置 ===
dir .env
dir memcontext\.env

echo === 如果两个位置都有 .env 文件，说明创建成功 ===
```

**方法2：使用记事本**

**步骤1：在项目根目录创建 .env**
1. 在项目根目录右键 → 新建 → 文本文档
2. 重命名为 `.env`（注意前面有个点）
3. 如果 Windows 提示"如果改变文件扩展名，文件可能不可用"，点击"是"

**步骤2：复制到 memcontext 目录**
1. 复制项目根目录的 `.env` 文件
2. 粘贴到 `memcontext` 目录
3. 重命名为 `.env`（如果被重命名了）

**方法3：使用代码编辑器**

**步骤1：在项目根目录创建 .env**
- 使用 VS Code、Notepad++ 等编辑器在项目根目录创建新文件
- 保存为 `.env`（注意前面有个点）

**步骤2：复制到 memcontext 目录**
- 复制项目根目录的 `.env` 文件到 `memcontext` 目录

**验证文件创建**：

在项目根目录执行：
```bash
dir .env
```

**应该看到**：
```
.env
```

**如果看不到**：
1. 确认当前目录是否是项目根目录（应该能看到 `memcontext-n8n`、`memcontext-mcp` 等目录）
2. Windows 可能默认隐藏以点开头的文件，在文件资源管理器中：
   - 点击"查看"选项卡
   - 勾选"隐藏的项目"
   - 即可看到 `.env` 文件

**验证 .env 文件位置是否正确**：
```bash
# 在项目根目录执行
cd

# 应该显示项目根目录，例如：
# D:\project\memcontext-memcontext

# 同时检查以下文件/目录是否存在：
dir .env              # 应该看到 .env 文件
dir memcontext-n8n    # 应该看到 memcontext-n8n 目录
dir requirements.txt  # 应该看到 requirements.txt 文件
```

如果以上检查都通过，说明 `.env` 文件位置正确。

### 3.2 编辑 .env 文件

**打开 .env 文件**（使用记事本或任何文本编辑器）

**完整配置模板**：

```env
# ============================================
# Memcontext-n8n API Key 配置（必需）
# ============================================
# 用于访问 memcontext-n8n 服务的 API Key
# 可以设置任意字符串，建议使用随机字符串
# 多个 Key 用逗号分隔
N8N_API_KEYS=your-secret-key-here

# ============================================
# n8n API Key 配置（可选）
# ============================================
# 用于调用 n8n API 的 Key（如果 n8n 需要 API Key 认证）
# 如果不需要，可以删除这一行
N8N_API_KEY=your-n8n-api-key-here

# ============================================
# LLM 配置（必需）
# ============================================
# LLM API Key
# OpenAI 格式：sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# 火山引擎：your-volcano-engine-api-key-here
LLM_API_KEY=sk-your-llm-api-key-here

# LLM API 地址
# OpenAI: https://api.openai.com/v1
# 火山引擎: https://ark.cn-beijing.volces.com/api/v3
LLM_BASE_URL=https://api.openai.com/v1

# LLM 模型名称
# OpenAI: gpt-4, gpt-3.5-turbo, gpt-4-turbo-preview
# 火山引擎: ep-20241208200000-xxxxx
LLM_MODEL=gpt-4

# ============================================
# Embedding 模型配置（可选）
# ============================================
# 用于文本向量化
# OpenAI: text-embedding-3-small, text-embedding-3-large
# 如果不设置，会使用默认值
EMBEDDING_MODEL=text-embedding-3-small

# ============================================
# SiliconFlow 配置（可选）
# ============================================
# 用于视频/音频转录
# 如果不需要视频/音频功能，可以删除这一行
SILICONFLOW_API_KEY=your-siliconflow-api-key-here
```

### 3.3 配置说明（详细）

#### N8N_API_KEYS（必需）

**作用**：这是访问 memcontext-n8n 服务的密钥，用于身份验证

**设置方法**：
```env
N8N_API_KEYS=your-secret-key-here
```

**安全提示**：
- 不要使用简单的密码（如 `123456`）
- 建议使用随机字符串，例如：`aB3xY9mK2pQ7wE5`
- 可以设置多个 Key，用逗号分隔：
  ```env
  N8N_API_KEYS=key1,key2,key3
  ```
- 将 `your-secret-key-here` 替换为你自己的随机字符串

#### LLM_API_KEY（必需）

**作用**：用于调用 LLM 服务的 API Key

**OpenAI 配置示例**：
```env
LLM_API_KEY=sk-your-openai-api-key-here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4
```

**火山引擎配置示例**：
```env
LLM_API_KEY=your-volcano-engine-api-key-here
LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
LLM_MODEL=ep-20241208200000-xxxxx
```

**获取方法**：
- OpenAI：登录 [OpenAI Platform](https://platform.openai.com/api-keys)，创建新的 API Key
- 火山引擎：登录 [火山引擎控制台](https://console.volcengine.com/)，获取 API Key

#### SILICONFLOW_API_KEY（可选）

**作用**：用于视频/音频转录

**如果不需要视频/音频功能**：
- 可以删除这一行
- 或者留空：`SILICONFLOW_API_KEY=`

**如果需要**：
1. 访问 [SiliconFlow](https://siliconflow.cn/)
2. 注册并登录
3. 在控制台获取 API Key
4. 填入配置

### 3.4 验证配置文件

**重要**：验证前请确保：
1. `.env` 文件在项目**根目录**（不是 memcontext-n8n 目录）
2. `.env` 文件在 **memcontext 目录**（必需）
3. 当前工作目录是项目根目录

**步骤1：确认 .env 文件位置**

在项目根目录执行：
```bash
# 检查当前目录
cd

# 应该显示项目根目录，例如：
# D:\project\memcontext-memcontext

# 检查根目录的 .env 文件是否存在
dir .env

# 应该看到根目录的 .env 文件

# 检查 memcontext 目录的 .env 文件是否存在
dir memcontext\.env

# 应该看到 memcontext 目录的 .env 文件

# 同时应该能看到 memcontext-n8n、memcontext-mcp 等目录
dir
```

**重要**：确保**两个位置**都有 `.env` 文件：
- ✅ 项目根目录：`dir .env` 应该看到文件
- ✅ memcontext 目录：`dir memcontext\.env` 应该看到文件

**步骤2：检查配置是否正确**

在项目**根目录**执行：
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('N8N_API_KEYS:', os.getenv('N8N_API_KEYS')[:10] if os.getenv('N8N_API_KEYS') else '未设置'); print('LLM_API_KEY:', os.getenv('LLM_API_KEY')[:10] if os.getenv('LLM_API_KEY') else '未设置')"
```

**应该看到**：
```
N8N_API_KEYS: my-secret-k
LLM_API_KEY: sk-xxxxxxx
```

**如果显示"未设置"**：
1. **检查 .env 文件位置**：
   - `.env` 文件必须在项目**根目录**（`memcontext-memcontext` 目录）
   - `.env` 文件必须在 **memcontext 目录**（`memcontext-memcontext\memcontext` 目录）
   - 不是在 `memcontext-n8n` 目录下
   - 确认方法：
     ```bash
     # 在项目根目录执行
     dir .env              # 应该看到根目录的 .env 文件
     dir memcontext\.env   # 应该看到 memcontext 目录的 .env 文件
     dir memcontext-n8n    # 应该看到 memcontext-n8n 目录
     ```

2. **检查 .env 文件格式**：
   - 没有多余的空格或引号
   - 变量名和值之间只有一个等号 `=`
   - 每行一个配置项

3. **检查变量名**：
   - 变量名大小写敏感（`N8N_API_KEYS` 不是 `n8n_api_keys`）
   - 确保没有拼写错误

4. **检查当前目录**：
   - 验证脚本必须在项目根目录执行
   - 如果从 `memcontext-n8n` 目录执行，需要使用 `load_dotenv(dotenv_path='../.env')`

**验证示例**：

```bash
# 在项目根目录执行
cd D:\project\memcontext-memcontext

# 检查文件结构
dir .env              # 应该看到根目录的 .env 文件
dir memcontext\.env   # 应该看到 memcontext 目录的 .env 文件
dir memcontext-n8n    # 应该看到 memcontext-n8n 目录
dir memcontext        # 应该看到 memcontext 目录
dir requirements.txt  # 应该看到 requirements.txt 文件

# 验证配置加载
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Config loaded:', 'OK' if os.getenv('LLM_API_KEY') else 'FAILED')"
```

---

## 第四步：启动服务

> 💡 **提示**：如果你已经按照 [快速开始](#快速开始---使用脚本快速上手) 章节完成了所有步骤，可以跳过这一步。

### 4.1 进入 memcontext-n8n 目录

**步骤**：
```bash
cd memcontext-n8n
```

**验证**：
```bash
cd
```

**应该显示**：
```
<你的项目根目录路径>\memcontext-n8n
```
例如：`C:\Users\YourName\Projects\memcontext-memcontext\memcontext-n8n`

### 4.2 启动服务

**方式1：直接启动（推荐）**

**启动命令**：
```bash
cd memcontext-n8n
python app.py
```

**方式2：使用批处理脚本（可选）**

如果你想创建一个启动脚本，可以在 `memcontext-n8n` 目录下创建 `start-service.bat`：

```batch
@echo off
chcp 65001 >nul
echo ========================================
echo Starting Memcontext-n8n Service
echo ========================================
echo.

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found, please install Python first
    pause
    exit /b 1
)

REM Check .env file
if not exist ..\.env (
    echo [WARNING] .env file not found in project root directory
    echo Please create .env file first
    echo.
)

echo Starting service...
echo Service will run on http://localhost:5019
echo Press Ctrl+C to stop the service
echo.

python app.py

pause
```

**使用脚本启动**：
```bash
cd memcontext-n8n
start-service.bat
```

**执行过程**：

**第一次启动**，会看到类似输出：
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5019
 * Running on http://192.168.1.100:5019
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-456-789
```

**重要提示**：
- ✅ 看到 "Running on http://127.0.0.1:5019" 说明启动成功
- ⚠️ 这个窗口**不能关闭**，关闭后服务会停止
- 🔄 如果需要停止服务，按 `Ctrl + C`

### 4.3 验证服务是否正常运行

#### 方法1：浏览器测试

1. 打开浏览器
2. 访问：`http://localhost:5019`
3. **应该看到**：`404 Not Found` 或类似错误页面
   - **这是正常的**！说明服务正在运行
   - 因为根路径 `/` 没有配置路由

#### 方法2：命令行测试

**打开另一个命令行窗口**（不要关闭运行服务的窗口），执行：

```bash
curl http://localhost:5019
```

**或者使用 PowerShell**：
```powershell
Invoke-WebRequest -Uri http://localhost:5019
```

**应该看到**：HTTP 响应（可能是 404，这是正常的）

#### 方法3：测试 API 接口

**在另一个命令行窗口执行**：

```bash
curl -X POST http://localhost:5019/api/memory/search -H "Authorization: Bearer your-secret-key-here" -H "Content-Type: application/json" -d "{\"user_id\":\"test\",\"query\":\"test\"}"
```

**注意**：将 `your-secret-key-here` 替换为你在 `.env` 文件中设置的 `N8N_API_KEYS` 的值

**如果看到 JSON 响应**（即使是错误），说明服务正常运行

---


## 第五步：在 n8n 平台安装插件

### 5.1 前提条件

**假设**：你已经安装并运行了 n8n 平台

- 本地 n8n：访问 `http://localhost:5678`
- 云端 n8n：访问你的 n8n Cloud 地址

### 5.2 使用 HTTP Request 节点（推荐）

**说明**：实际上，你**不需要安装任何插件**。n8n 自带的 **HTTP Request** 节点就可以直接调用记忆管理 API。

**步骤**：
1. 在 n8n 中创建工作流
2. 添加 **HTTP Request** 节点
3. 配置 API 地址和参数（见第六步）

### 5.3 验证服务连接

**步骤1：确保服务正在运行**

在另一个命令行窗口检查服务是否运行：
```bash
netstat -ano | findstr :5019
```

如果看到端口被占用，说明服务正在运行。

**步骤2：测试连接**

在 n8n 中创建一个简单的测试工作流：

1. 创建新工作流
2. 添加 **HTTP Request** 节点
3. 配置：
   - **Method**：`GET`
   - **URL**：`http://localhost:5019`（如果 n8n 和 app.py 在同一台机器）
   - 或 `http://你的服务器IP:5019`（如果 n8n 在云端）
4. 执行工作流

**如果看到响应**（即使是 404），说明连接正常。

---

## 工作流程图解

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户/外部系统                              │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │    n8n 工作流平台      │
            │  (你的 n8n 实例)       │
            │   http://localhost:5678│
            └───────────┬────────────┘
                        │
                        │ HTTP 请求
                        │ (localhost:5019)
                        ▼
        ┌───────────────────────────────┐
        │   memcontext-n8n 记忆管理服务  │
        │   (主机上运行)                 │
        │   http://localhost:5019       │
        │                                │
        │  ┌──────────────────────────┐ │
        │  │  Flask API 服务           │ │
        │  │  - /api/memory/search     │ │
        │  │  - /api/memory/add        │ │
        │  │  - /api/memory/add_multimodal│
        │  └───────────┬──────────────┘ │
        │              │                 │
        │              ▼                 │
        │  ┌──────────────────────────┐ │
        │  │  Memcontext 记忆系统      │ │
        │  │  - 短期记忆 (7条)         │ │
        │  │  - 中期记忆 (200条)       │ │
        │  │  - 长期知识 (1000条)      │ │
        │  └───────────┬──────────────┘ │
        │              │                 │
        │              ▼                 │
        │  ┌──────────────────────────┐ │
        │  │  数据存储                 │ │
        │  │  memcontext-n8n/data/    │ │
        │  └──────────────────────────┘ │
        └────────────────────────────────┘
                        │
                        │ 调用
                        ▼
        ┌───────────────────────────────┐
        │   外部服务                     │
        │  - LLM API (OpenAI/火山引擎)   │
        │  - Embedding API              │
        │  - SiliconFlow (音频转录)      │
        └───────────────────────────────┘
```

### 记忆检索工作流程

```
用户提问
   │
   ▼
┌─────────────────┐
│  n8n Webhook    │  接收用户问题
│  节点            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTTP Request   │  调用记忆检索接口
│  节点            │  POST /api/memory/search
└────────┬────────┘
         │
         │ 请求参数:
         │ {
         │   "user_id": "user123",
         │   "query": "用户之前提到过什么？"
         │ }
         ▼
┌─────────────────┐
│  memcontext-n8n │  处理请求
│  服务           │
│  /api/memory/   │
│  search         │
└────────┬────────┘
         │
         │ 1. 查找相关记忆
         │ 2. 调用 LLM 生成回复
         ▼
┌─────────────────┐
│  返回结果       │  {
│                 │    "code": 200,
│                 │    "data": {
│                 │      "response": "根据记忆..."
│                 │    }
│                 │  }
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  返回给用户     │  显示回复
└─────────────────┘
```

### 添加记忆工作流程

```
用户对话
   │
   ▼
┌─────────────────┐
│  n8n 工作流     │  捕获对话内容
│  节点            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTTP Request   │  调用添加记忆接口
│  节点            │  POST /api/memory/add
└────────┬────────┘
         │
         │ 请求参数:
         │ {
         │   "user_id": "user123",
         │   "user_input": "我喜欢喝咖啡",
         │   "agent_response": "好的，我记住了"
         │ }
         ▼
┌─────────────────┐
│  memcontext-n8n │  处理请求
│  服务           │
│  /api/memory/   │
│  add            │
└────────┬────────┘
         │
         │ 1. 添加到短期记忆
         │ 2. 如果短期记忆满，自动处理到中期记忆
         │ 3. 生成嵌入向量
         ▼
┌─────────────────┐
│  记忆存储       │  memcontext-n8n/data/users/user123/
│                 │  - short_term.json
│                 │  - mid_term.json
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  返回结果       │  {
│                 │    "code": 200,
│                 │    "data": {
│                 │      "success": true,
│                 │      "short_term_count": 1
│                 │    }
│                 │  }
└─────────────────┘
```

### 视频处理工作流程

```
视频文件
   │
   ▼
┌─────────────────┐
│  n8n Code 节点  │  Set Video Path
│                 │  file_path: "D:\\...\\video.mp4"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTTP Request   │  调用视频处理接口
│  节点            │  POST /api/memory/add_multimodal
└────────┬────────┘
         │
         │ 请求参数:
         │ {
         │   "user_id": "user123",
         │   "file_path": "D:\\...\\video.mp4",
         │   "converter_type": "video"
         │ }
         ▼
┌─────────────────┐
│  memcontext-n8n │  处理视频
│  服务           │
│  /api/memory/   │
│  add_multimodal │
└────────┬────────┘
         │
         │ 处理步骤:
         │ 1. 提取视频帧 (0-20%)
         │ 2. 提取音频 (20-40%)
         │ 3. 音频转录 (40-60%)
         │ 4. 分析视频内容 (60-80%)
         │ 5. 生成嵌入向量 (80-90%)
         │ 6. 存储到记忆系统 (90-100%)
         ▼
┌─────────────────┐
│  返回结果       │  {
│                 │    "code": 200,
│                 │    "data": {
│                 │      "success": true,
│                 │      "ingested_rounds": 5,
│                 │      "progress": [...]
│                 │    }
│                 │  }
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  后续检索       │  可以搜索视频内容
└─────────────────┘
```

### 完整对话流程示例

```
【第一次对话】
用户: "我喜欢喝咖啡"
   │
   ▼
┌─────────────────┐
│  n8n 工作流     │
│  1. 接收输入    │
│  2. 调用 LLM    │  生成回复: "好的，我记住了"
│  3. 添加记忆    │  POST /api/memory/add
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  记忆已保存     │  短期记忆: 1条
└─────────────────┘

【几天后】

用户: "我之前说过我喜欢什么？"
   │
   ▼
┌─────────────────┐
│  n8n 工作流     │
│  1. 接收问题    │
│  2. 检索记忆    │  POST /api/memory/search
│  3. 查找相关记忆│  找到: "我喜欢喝咖啡"
│  4. 调用 LLM    │  生成回复: "根据之前的对话，你提到过你喜欢喝咖啡"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  返回给用户     │  "根据之前的对话，你提到过你喜欢喝咖啡"
└─────────────────┘
```

### 数据流向图

```
┌──────────────┐
│  用户输入    │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────┐
│         n8n 工作流                  │
│                                     │
│  ┌──────────┐    ┌──────────────┐  │
│  │ Webhook  │───▶│ HTTP Request│  │
│  │ 节点      │    │ 节点          │  │
│  └──────────┘    └──────┬───────┘  │
│                         │          │
└─────────────────────────┼──────────┘
                          │
                          │ HTTP POST
                          │ Authorization: Bearer <key>
                          ▼
┌─────────────────────────────────────┐
│      memcontext-n8n 服务 (Flask)           │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  API 路由处理                │  │
│  │  - 验证 API Key              │  │
│  │  - 解析请求参数              │  │
│  └───────────┬──────────────────┘  │
│              │                      │
│              ▼                      │
│  ┌──────────────────────────────┐  │
│  │  Memcontext 记忆系统          │  │
│  │                              │  │
│  │  ┌────────────────────────┐  │  │
│  │  │ 短期记忆 (7条)          │  │  │
│  │  │ - 最新对话              │  │  │
│  │  │ - 快速访问              │  │  │
│  │  └────────────────────────┘  │  │
│  │                              │  │
│  │  ┌────────────────────────┐  │  │
│  │  │ 中期记忆 (200条)        │  │  │
│  │  │ - 近期重要信息          │  │  │
│  │  │ - 热度计算              │  │  │
│  │  └────────────────────────┘  │  │
│  │                              │  │
│  │  ┌────────────────────────┐  │  │
│  │  │ 长期知识 (1000条)       │  │  │
│  │  │ - 永久存储              │  │  │
│  │  │ - 用户画像              │  │  │
│  │  └────────────────────────┘  │  │
│  └───────────┬──────────────────┘  │
│              │                      │
│              │ 调用外部 API         │
│              ▼                      │
│  ┌──────────────────────────────┐  │
│  │  LLM API                     │  │
│  │  - 生成回复                  │  │
│  │  - 分析内容                  │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Embedding API                │  │
│  │  - 生成向量                  │  │
│  │  - 相似度搜索                │  │
│  └──────────────────────────────┘  │
│                                     │
└───────────────┬─────────────────────┘
                │
                │ JSON 响应
                ▼
┌─────────────────────────────────────┐
│        返回给 n8n                   │
│        {                            │
│          "code": 200,               │
│          "data": { ... }            │
│        }                            │
└─────────────────────────────────────┘
```

---

## 第六步：在 n8n 中创建工作流（详细版）

### 6.1 创建新工作流

**步骤1：打开 n8n**

访问：`http://localhost:5678` 并登录

**步骤2：创建工作流**

1. 点击左侧菜单的 **Workflows**
2. 点击右上角的 **+ Add workflow** 按钮
3. 会打开一个新的工作流编辑器

### 6.2 创建记忆检索工作流

#### 步骤1：添加 Manual Trigger 节点

1. 在工作流编辑器中，点击 **+** 按钮
2. 搜索 "Manual" 或 "Trigger"
3. 选择 **Manual Trigger** 节点
4. 点击添加到画布

**节点说明**：这个节点用于手动触发工作流，方便测试

#### 步骤2：添加 HTTP Request 节点

1. 点击 **+** 按钮
2. 搜索 "HTTP"
3. 选择 **HTTP Request** 节点
4. 点击添加到画布
5. 将 Manual Trigger 节点的输出连接到 HTTP Request 节点

#### 步骤3：配置 HTTP Request 节点

**点击 HTTP Request 节点**，在右侧配置面板设置：

**1. 基本设置**：
- **Method**：选择 `POST`
- **URL**：
  - **URL**：`http://localhost:5019/api/memory/search`（如果 n8n 和 app.py 在同一台机器）
  - 或 `http://你的服务器IP:5019/api/memory/search`（如果 n8n 在云端）

**2. Authentication**：
- 点击 **Authentication** 下拉菜单
- 选择 **Generic Credential Type**
- 选择 **Bearer Token**
- 在 **Token** 字段输入：你在 `.env` 文件中设置的 `N8N_API_KEYS` 的值
  - 例如：如果你在 `.env` 中设置了 `N8N_API_KEYS=your-secret-key-here`，则输入 `your-secret-key-here`

**3. Headers**：
- 点击 **Add Header** 或 **Send Headers** 开关
- 添加 Header：
  - **Name**：`Content-Type`
  - **Value**：`application/json`

**4. Body**：
- 找到 **Specify Body** 或 **Send Body** 选项
- 选择 **JSON**
- 在 JSON 框中输入：
  ```json
  {
    "user_id": "test_user",
    "query": "用户之前提到过什么？",
    "relationship_with_user": "friend",
    "style_hint": "友好"
  }
  ```

**5. Options（重要）**：
- 展开 **Options** 部分
- 找到 **Timeout** 选项
- 设置为 `30000`（30 秒，单位：毫秒）
  - 对于视频处理，建议设置为 `1800000`（30 分钟）

**6. 保存配置**：
- 点击右上角的 **Save** 按钮

#### 步骤4：执行测试

1. 点击 **Manual Trigger** 节点
2. 点击右上角的 **Execute Workflow** 按钮
3. 等待执行完成
4. 点击 **HTTP Request** 节点，查看输出

**成功输出示例**：
```json
{
  "code": 200,
  "message": "操作成功",
  "errorCode": 0,
  "data": {
    "response": "根据记忆，用户之前提到过...",
    "timestamp": "2024-01-01T12:00:00"
  }
}
```

### 6.3 创建添加记忆工作流

#### 步骤1：创建工作流

按照 6.2 的步骤创建新工作流，或修改现有工作流

#### 步骤2：配置 HTTP Request 节点

**基本设置**：
- **Method**：`POST`
- **URL**：`http://localhost:5019/api/memory/add`

**Authentication**：同上（Bearer Token）

**Body (JSON)**：
```json
{
  "user_id": "test_user",
  "user_input": "我喜欢喝咖啡",
  "agent_response": "好的，我记住了你喜欢喝咖啡"
}
```

#### 步骤3：执行测试

执行工作流，应该看到成功响应：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "success": true,
    "message": "记忆已添加到短期记忆",
    "short_term_count": 1,
    "is_full": false
  }
}
```

### 6.4 创建视频上传工作流

#### 方式1：使用自动化脚本（推荐）

项目提供了自动化脚本，可以快速创建工作流：

**步骤1：运行脚本**

在 `memcontext-n8n` 目录下执行：
```bash
cd memcontext-n8n
create_video_workflow.bat
```

或者直接运行 Python 脚本：
```bash
cd memcontext-n8n
python create_video_workflow.py
```

**注意**：脚本会自动检测项目根目录和 memcontext-n8n 目录，无需手动配置路径。

**步骤2：脚本会自动**：
- ✅ 创建工作流
- ✅ 配置所有节点
- ✅ 激活工作流

**步骤3：在 n8n 中查看**

1. 打开 n8n：`http://localhost:5678`
2. 找到工作流："Video Upload and Retrieval Workflow"
3. 点击打开，查看配置

#### 方式2：手动创建工作流

详细步骤请参考 6.2 和 6.3 的说明，配置视频上传相关的节点。

### 6.5 运行脚本测试工作流

#### 测试视频上传工作流

**步骤1：准备测试视频**

将测试视频文件放在 `memcontext-n8n` 目录下，例如 `test1.mp4`

**步骤2：运行 Docker 启动脚本（如果使用 Docker）**

```bash
cd memcontext-n8n
docker-run-n8n.bat
```

这会：
- 检查 Docker 状态
- 检查端口 5678 是否被占用
- 启动 n8n Docker 容器
- 挂载本地 `memcontext-n8n` 目录到容器

**步骤3：运行工作流创建脚本**

在另一个命令行窗口：

```bash
cd memcontext-n8n
create_video_workflow.bat
```

或者：

```bash
python create_video_workflow.py
```

**步骤4：在 n8n 中测试工作流**

1. 打开浏览器访问：`http://localhost:5678`
2. 登录（用户名：`admin`，密码：`admin`）
3. 找到 "Video Upload and Retrieval Workflow" 工作流
4. 点击打开工作流
5. 点击 "When clicking test" 节点
6. 点击右上角的 "Execute Workflow" 按钮
7. 等待执行完成（视频处理可能需要几分钟）
8. 查看 "Format Output" 节点的结果

**预期结果**：
- `video_upload.success` 应该为 `true`
- `memory_search.success` 应该为 `true`
- `summary.answer` 应该包含视频内容的描述

**如果测试失败**：
- 检查 memcontext-n8n 服务是否正在运行（端口 5019）
- 检查视频文件路径是否正确
- 检查 `.env` 文件配置是否正确
- 查看 n8n 节点的错误信息

---

## 完整测试流程

### 测试前准备

1. ✅ **确保 memcontext-n8n 服务正在运行**
   ```bash
   # 检查服务是否运行
   netstat -ano | findstr :5019
   ```
   如果看到端口被占用，说明服务正在运行

2. ✅ **确保 n8n 正在运行**
   - 访问 `http://localhost:5678` 能正常打开

3. ✅ **确保 `.env` 文件已配置**
   - 检查项目根目录是否有 `.env` 文件
   - 检查 memcontext 目录是否有 `.env` 文件
   - 确认 `N8N_API_KEYS` 和 `LLM_API_KEY` 已填写
   - 两个 `.env` 文件内容应该相同

### 测试方法1：在 n8n 中手动测试

**步骤1：创建测试工作流**

按照 6.2 的步骤创建记忆检索工作流

**步骤2：执行工作流**

1. 点击 "Manual Trigger" 节点
2. 点击 "Execute Workflow"
3. 查看执行结果

**步骤3：验证结果**

- ✅ 如果看到 `"code": 200`，说明测试成功
- ❌ 如果看到错误，参考"常见问题详细排查"章节

### 测试方法2：使用 curl 命令

**测试记忆检索**：
```bash
curl -X POST http://localhost:5019/api/memory/search ^
  -H "Authorization: Bearer your-secret-key-here" ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\":\"test_user\",\"query\":\"测试问题\"}"
```

**注意**：将 `your-secret-key-here` 替换为你在 `.env` 文件中设置的 `N8N_API_KEYS` 的值

**测试添加记忆**：
```bash
curl -X POST http://localhost:5019/api/memory/add ^
  -H "Authorization: Bearer your-secret-key-here" ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\":\"test_user\",\"user_input\":\"测试输入\",\"agent_response\":\"测试回复\"}"
```

**注意**：将 `your-secret-key-here` 替换为你在 `.env` 文件中设置的 `N8N_API_KEYS` 的值

### 测试检查清单

完成以下测试，确保所有功能正常：

- [ ] **基础连接测试**：服务能正常启动
- [ ] **API Key 验证**：使用正确的 API Key 能访问，错误的被拒绝
- [ ] **记忆检索**：能成功检索记忆并返回结果
- [ ] **添加记忆**：能成功添加记忆到系统
- [ ] **视频处理**：能成功处理视频文件（如果测试了视频功能）
- [ ] **错误处理**：缺少参数时返回正确的错误信息

---

## 常见问题详细排查

### 环境配置问题

#### Q1: 启动服务时提示 "ModuleNotFoundError: No module named 'flask'"

**原因**：缺少 Python 依赖包

**解决方法**：
```bash
pip install flask python-dotenv requests
```

或者使用 requirements.txt：
```bash
pip install -r requirements.txt
```

#### Q2: 提示 "LLM_API_KEY 环境变量未配置"

**原因**：`.env` 文件配置不正确或未加载

**解决方法**：
1. 检查 `.env` 文件是否在项目**根目录**（不是 memcontext-n8n 目录）
2. 检查 `.env` 文件是否在 **memcontext 目录**
3. 检查 `.env` 文件中的 `LLM_API_KEY` 是否正确填写
4. 确保两个 `.env` 文件内容相同
5. 确保 `.env` 文件格式正确（没有多余的空格或引号）
6. 重启服务

**验证方法**：
```bash
# 在项目根目录执行
dir .env              # 检查根目录的 .env
dir memcontext\.env   # 检查 memcontext 目录的 .env
```

#### Q3: 端口被占用

**错误信息**：
```
OSError: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次
```

**解决方法**：
1. 检查端口是否被占用：
   ```bash
   netstat -ano | findstr :5019
   ```
2. 如果看到进程 ID（最后一列），结束该进程：
   ```bash
   taskkill /PID <进程ID> /F
   ```
3. 或者修改 `app.py` 中的端口号（不推荐）

### 网络连接问题

#### Q4: n8n 无法连接到 memcontext-n8n 服务

**错误信息**：
```
The connection to the server was closed unexpectedly
Connection refused
```

**解决方法**：
1. **确保 memcontext-n8n 服务正在运行**：
   ```bash
   netstat -ano | findstr :5019
   ```
   如果看不到端口被占用，说明服务未启动

2. **检查 URL 配置**：
   - 如果 n8n 和 app.py 在同一台机器：使用 `http://localhost:5019`
   - 如果 n8n 在云端，app.py 在本地：需要配置端口转发或使用公网 IP

3. **如果 localhost 不可用**：
   ```bash
   ipconfig  # 查看 IPv4 地址，例如 192.168.1.100
   ```
   然后在 n8n 中使用：`http://192.168.1.100:5019`

### API 调用问题

#### Q5: "Bad request - please check your parameters"

**原因**：请求参数不正确

**解决方法**：
1. 检查请求的 JSON 格式是否正确
2. 检查必需参数是否都提供了：
   - `/api/memory/add` 需要：`user_id`, `user_input`, `agent_response`
   - `/api/memory/search` 需要：`user_id`, `query`
   - `/api/memory/add_multimodal` 需要：`user_id`, `file_path`
3. 检查参数名称是否正确（区分大小写）

#### Q6: "No converter registered for type=videorag"

**原因**：转换器类型配置错误

**解决方法**：
- 使用 `"converter_type": "video"` 而不是 `"videorag"`

#### Q7: 视频处理超时

**原因**：视频文件太大，处理时间超过超时限制

**解决方法**：
1. 在 n8n HTTP Request 节点中增加超时时间
2. 建议设置为 30 分钟（1800000 毫秒）或更长
3. 大视频文件需要更长时间，请耐心等待

#### Q8: 文件路径找不到

**原因**：路径格式错误或文件不存在

**解决方法**：
1. 使用**绝对路径**，例如：`C:\\Users\\YourName\\Projects\\memcontext-memcontext\\memcontext-n8n\\test1.mp4`
   - 或者使用相对路径（相对于项目根目录）：`memcontext-n8n\\test1.mp4`
2. Windows 路径使用双反斜杠 `\\` 或正斜杠 `/`
3. 确保文件确实存在
4. 注意：脚本会自动检测项目路径，建议使用相对路径或让脚本自动生成路径

### 其他问题

#### Q9: 服务启动后立即退出

**原因**：可能是端口被占用或配置错误

**解决方法**：
1. 检查端口 5019 是否被占用：
   ```bash
   netstat -ano | findstr :5019
   ```
2. 如果被占用，停止占用端口的程序或修改 `app.py` 中的端口号
3. 检查 `.env` 文件配置是否正确：
   - 检查项目根目录的 `.env` 文件
   - 检查 memcontext 目录的 `.env` 文件
   - 确保两个文件内容相同

#### Q10: 如何查看详细的错误信息？

**方法1：查看服务日志**
- 在运行 `python app.py` 的命令行窗口查看输出

**方法2：查看 n8n 节点输出**
- 在 n8n 工作流中，点击每个节点查看输入/输出数据
- 查看 "Executions" 页面查看执行历史


---