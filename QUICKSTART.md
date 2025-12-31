# 🚀 Quick Start 快速开始指南

本文档将指导您快速启动项目、上传视频并进行对话。

## 📋 前置要求

- Python 3.9+
- 豆包（字节跳动）API Key（用于 LLM 和 Embedding）

## 🔧 1. 环境配置

### 1.1 安装依赖

```bash
# 安装项目依赖
pip install -r requirements.txt

# 安装 demo 依赖
cd memdemo
pip install -r requirements.txt
cd ..
```

### 1.2 配置环境变量

复制 `.env.default` 为 `.env` 并填写您的 API Key：

```bash
cp .env.default .env
```

编辑 `.env` 文件，填入您的豆包 API Key：

```bash
# LLM API 配置（用于内容分析和智能对话）
LLM_API_KEY=your_doubao_llm_api_key_here
LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
LLM_MODEL=doubao-seed-1-6-flash-250828

# 向量化 Embedding API 配置（用于向量数据库）
EMBEDDING_API_KEY=your_doubao_embedding_api_key_here
EMBEDDING_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
EMBEDDING_MODEL=doubao-embedding-large-text-250515
```

## 🎬 2. 启动服务

### 2.1 启动 Flask 服务器

```bash
cd memdemo
python app.py
```

服务器将在 `http://127.0.0.1:5019` 启动（默认端口为 5019）。

您应该看到类似以下的输出：

```
 * Running on http://127.0.0.1:5019
 * Debug mode: off
```

> **提示**：您也可以使用提供的启动脚本：
> ```bash
> cd memdemo
> bash start_demo.sh
> ```

## 📹 3. 上传视频

### 3.1 使用 test_memdemo.py 上传视频

在另一个终端窗口中，运行测试脚本：

```bash
# 确保在项目根目录
cd /root/repo/memcontext-dev

# 运行测试脚本
python test_memdemo.py
```

### 3.2 修改视频路径

编辑 `test_memdemo.py`，修改您要上传的视频路径：

```python
def main():
    session = requests.Session()
    session_id = init_memory(session)
    print(f"Session ready: {session_id}")

    # 修改这里的视频路径为您的视频文件路径
    result = add_video(
        session=session, 
        video_path="/path/to/your/video.mp4",  # 改为您的视频路径
        auto_summary=False
    )
    
    # ... 其余代码
```

### 3.3 执行上传

运行脚本后，系统将：

1. **初始化记忆系统**：创建用户会话
2. **上传视频**：将视频文件上传到 FileStorageManager
3. **处理视频**：使用 VideoRAG 进行视频解析和索引
4. **返回结果**：包括 `file_id`、存储路径等信息

示例输出：

```
Session ready: abc123def456
使用 FileStorageManager 自动管理的存储路径
{
  "success": true,
  "file_id": "c54ec6be2544cf536a1c3879aad84609",
  "storage_path": "/root/repo/memcontext-dev/files/videos/c54ec6be2544cf536a1c3879aad84609/",
  ...
}

文件已通过 FileStorageManager 管理
file_id: c54ec6be2544cf536a1c3879aad84609
存储路径: /root/repo/memcontext-dev/files/videos/c54ec6be2544cf536a1c3879aad84609/
```

> **注意**：视频处理可能需要较长时间，具体取决于视频大小和复杂度。请耐心等待。

## 💬 4. 针对视频内容进行对话

### 4.1 使用 API 进行对话

#### 方法一：使用 curl

```bash
# 使用之前获取的 session_id
SESSION_ID="your_session_id_here"  # 从 test_memdemo.py 的输出中获取

# 发送对话请求
curl -X POST http://127.0.0.1:5019/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "这个视频的主要内容是什么？"
  }' \
  --cookie "session=your_flask_session_cookie"
```

#### 方法二：使用 Python requests

创建一个新的 Python 脚本 `test_chat.py`：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json

SERVER = "http://127.0.0.1:5019"

# 创建一个 session 以保持 cookies
session = requests.Session()

# 1. 初始化记忆系统（如果还没有初始化）
init_response = session.post(
    f"{SERVER}/init_memory",
    json={"user_id": "video_user7"}
)
print("初始化结果:", init_response.json())

# 2. 发送对话消息
chat_response = session.post(
    f"{SERVER}/chat",
    json={
        "message": "这个视频的主要内容是什么？"
    }
)

result = chat_response.json()
print("\n对话结果:")
print(json.dumps(result, ensure_ascii=False, indent=2))

# 3. 继续对话
chat_response2 = session.post(
    f"{SERVER}/chat",
    json={
        "message": "视频中有哪些关键场景？"
    }
)

result2 = chat_response2.json()
print("\n第二次对话结果:")
print(json.dumps(result2, ensure_ascii=False, indent=2))
```

运行脚本：

```bash
python test_chat.py
```

### 4.2 通过 Web 界面对话

1. 打开浏览器访问 `http://127.0.0.1:5019`
2. 在页面中输入您的用户 ID（例如：`video_user7`）
3. 点击"初始化记忆系统"
4. 上传视频（如果还没有上传）
5. 在聊天框中输入问题，例如：
   - "这个视频的主要内容是什么？"
   - "视频中出现了哪些人物？"
   - "视频的拍摄地点在哪里？"
   - "视频中提到了哪些重要信息？"

### 4.3 查询特定视频文件

如果系统中存储了多个视频，您可以指定查询特定的视频：

```python
# 通过 file_id 查询
chat_response = session.post(
    f"{SERVER}/chat",
    json={
        "message": "file_id:c54ec6be2544cf536a1c3879aad84609 这个视频的主要内容是什么？"
    }
)

# 或者通过文件名查询
chat_response = session.post(
    f"{SERVER}/chat",
    json={
        "message": "original.mp4 这个视频的主要内容是什么？"
    }
)
```

## 📚 5. API 端点说明

### 5.1 核心端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/init_memory` | POST | 初始化记忆系统 |
| `/chat` | POST | 发送对话消息 |
| `/add_multimodal_memory` | POST | 上传多媒体内容（视频、图片等） |
| `/memory_state` | GET | 获取记忆状态 |

### 5.2 请求示例

#### 初始化记忆系统

```bash
curl -X POST http://127.0.0.1:5019/init_memory \
  -H "Content-Type: application/json" \
  -d '{"user_id": "video_user7"}'
```

响应：

```json
{
  "success": true,
  "session_id": "abc123def456",
  "user_id": "video_user7",
  "model": "doubao-seed-1-6-flash-250828",
  "embedding_provider": "doubao"
}
```

#### 发送对话

```bash
curl -X POST http://127.0.0.1:5019/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "这个视频的主要内容是什么？"}'
```

响应：

```json
{
  "response": "根据视频内容，主要内容包括...",
  "context_used": {
    "short_term": [...],
    "mid_term": [...],
    "long_term": [...]
  }
}
```

## 📖 6. 更多信息

- 详细架构说明：参见 [README.md](README.md)
- VideoRAG 文档：参见 [doc/VideoRag_docs.md](doc/VideoRag_docs.md)
- 文件存储说明：参见 [memcontext/file_storage/README.md](memcontext/file_storage/README.md)
