# MemContext n8n Plugin

<div align="center">

**Multimodal Agent Memory Service for n8n Workflows**

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![n8n](https://img.shields.io/badge/n8n-Compatible-green.svg)](https://n8n.io/)

*Empower your n8n workflows with persistent memory capabilities, supporting text, video, audio, images, and more*

</div>

---

## Overview

MemContext n8n Integration is an n8n plugin service built on the [MemContext](README_zh.md) multimodal Agent memory framework. It provides powerful memory management capabilities for n8n workflows through a RESTful API, enabling your automated workflows to:

- **Persistent Memory**: Save and retrieve conversation history to build long-term user profiles
- **Multimodal Processing**: Support content understanding for videos, audio, images, documents, and more
- **Intelligent Retrieval**: Precise memory retrieval based on semantic similarity
- **Plug & Play**: No complex configuration required, call via HTTP Request node

### Core Features

- **Three-Tier Memory Architecture**: Short-term memory, Mid-term memory, Long-term knowledge base
- **Multimodal Support**: Unified processing for text, video, audio, images, and documents
- **RESTful API**: Standard HTTP interface for easy integration
- **User Isolation**: Multi-user memory management based on `user_id`
- **Secure Authentication**: Bearer Token authentication mechanism

---

## Prerequisites

### Required Software

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **FFmpeg** - For video/audio processing
  - Windows: `winget install FFmpeg`
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`
- **Docker Desktop** (optional) - For running n8n
  - Windows: `winget install Docker.DockerDesktop`
  - [Other platforms](https://www.docker.com/products/docker-desktop/)

### Required Accounts and Keys

- **LLM API Key** - OpenAI or OpenAI-compatible API service (e.g., Volcengine)
- **n8n Platform** - Local installation or cloud instance

---

## Quick Start

### Step 1: Environment Setup

#### 1.1 Create Python Virtual Environment

```bash
conda create -n memcontext-n8n python=3.10 -y
conda activate memcontext-n8n
```

#### 1.2 Install Dependencies

```bash
# Execute at MemContext project root directory
pip install -r requirements.txt
pip install -r ./memcontext-n8n/requirements.txt

# If using ByteDance Volcengine models, also install:
pip install volcengine-python-sdk[ark]
```

#### 1.3 Install System Dependencies

```bash
# Windows
winget install FFmpeg
ffmpeg -version

winget install Docker.DockerDesktop
docker --version
```

### Step 2: Start n8n Service

#### 2.1 Start n8n with Docker (Recommended)

```bash
# Enter memcontext-n8n directory
cd memcontext-n8n

# Run Docker startup script
docker-run-n8n.bat
```

The script will automatically check Docker status and port usage, then start the n8n container and mount local directories.

#### 2.2 Access n8n

Visit http://localhost:5678 and log in

### Step 3: Configure Environment Variables

Create a `.env` file in the **project root directory** as follows:

```env
# ============================================
# LLM API Configuration (Required)
# ============================================
LLM_API_KEY=YOUR-API-KEY
LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
LLM_MODEL=doubao-seed-1-6-flash-250828

# ============================================
# Embedding API Configuration (for vector database)
# ============================================
EMBEDDING_API_KEY=YOUR-API-KEY
EMBEDDING_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
EMBEDDING_MODEL=doubao-embedding-large-text-250515

# ============================================
# SiliconFlow API Configuration (optional, for audio transcription)
# ============================================
SILICONFLOW_API_KEY=YOUR-API-KEY
SILICONFLOW_MODEL=TeleAI/TeleSpeechASR
ENABLE_AUDIO_TRANSCRIPTION=true

# ============================================
# n8n API Key (Required, for service authentication)
# ============================================
# Create API Key in n8n: Settings → n8n API (bottom left)
N8N_API_KEY=YOUR-API-KEY
```

### Step 4: Start MemContext-n8n Plugin Service

```bash
cd memcontext-n8n
python app.py
```

The service will start at `http://localhost:5019`.

**Verify Service Running**:

```bash
# Check port usage
netstat -ano | findstr :5019

# Or test with curl
curl http://localhost:5019
```

### Step 5: Create Workflow Example

#### 5.1 Video Memory Workflow (Automated Script)

```bash
cd memcontext-n8n

# Prepare test video (~1 minute)
# Name the video as test1.mp4 and place it in the memcontext-n8n directory

# Run workflow creation script
create_video_workflow.bat
```

The script will automatically:

- Create video upload and retrieval workflow
- Configure all nodes
- Activate the workflow

#### 5.2 Execute Workflow in n8n

1. Visit http://localhost:5678
2. Find "Video Upload and Retrieval Workflow"
3. Click "Execute Workflow" to run
4. View execution results

**Expected Output**:

You can see a visual example of the entire process below:

![n8n Workflow Diagram](../assets/n8nworkflow.png)

- `video_upload.success`: `true`
- `memory_search.success`: `true`
- `summary.answer`: Contains video content description
