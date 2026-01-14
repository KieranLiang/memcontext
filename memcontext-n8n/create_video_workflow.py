#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create n8n workflow for video upload and retrieval
Workflow includes:
1. Manual trigger (can input video file path)
2. Add video memory (multimodal)
3. Search memory
4. Output results
"""

import requests
import json
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Auto-detect project root directory (find directory containing .env file)
def get_project_root():
    """Get project root directory"""
    current_dir = Path(__file__).parent.absolute()
    # Search upward for directory containing .env file
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / '.env').exists():
            return parent
    # If not found, use parent directory of current script's parent (assuming project structure is memcontext-memcontext/memcontext-n8n/)
    return current_dir.parent

# Get project root directory and memcontext-n8n directory
PROJECT_ROOT = get_project_root()
MEMCONTEXT_N8N_DIR = PROJECT_ROOT / 'memcontext-n8n'
# Default video file path (relative path, will be automatically converted to absolute path)
DEFAULT_VIDEO_PATH = MEMCONTEXT_N8N_DIR / 'test1.mp4'

# Convert path to Windows format (for n8n JavaScript code)
def path_to_js_string(path):
    """Convert path to JavaScript string format (Windows path, double backslashes)"""
    abs_path = Path(path).absolute()
    path_str = str(abs_path)
    # Escape backslashes to double backslashes for JavaScript strings
    # Windows paths don't allow single quotes, so no need to worry about quote escaping
    return path_str.replace('\\', '\\\\')

# Configuration
N8N_URL = "http://localhost:5678"
N8N_USER = "admin"
N8N_PASS = "admin"
API_URL = "http://host.docker.internal:5019"

# Read n8n API Key (for calling n8n API)
N8N_API_KEY = os.environ.get("N8N_API_KEY", "").strip()
# Clean possible newlines and extra spaces
if N8N_API_KEY:
    N8N_API_KEY = N8N_API_KEY.replace('\n', '').replace('\r', '').strip()

# Read memcontext API Key (for calling memcontext API)
api_keys_str = os.environ.get("N8N_API_KEYS", "").strip()
if api_keys_str:
    MEMCONTEXT_API_KEY = api_keys_str.split(',')[0].strip()
else:
    MEMCONTEXT_API_KEY = os.environ.get("N8N_API_KEY", "test-key")

print("=" * 60)
print("Create Video Upload and Retrieval Workflow")
print("=" * 60)
print(f"\nConfiguration:")
print(f"  Project root: {PROJECT_ROOT}")
print(f"  memcontext-n8n directory: {MEMCONTEXT_N8N_DIR}")
print(f"  Default video path: {DEFAULT_VIDEO_PATH}")
print(f"  n8n URL: {N8N_URL}")
print(f"  API URL: {API_URL}")
print(f"  Memcontext API Key: {MEMCONTEXT_API_KEY[:10]}...")
if N8N_API_KEY:
    print(f"  n8n API Key: {N8N_API_KEY[:20]}... (configured, length: {len(N8N_API_KEY)})")
else:
    print(f"  n8n API Key: not configured, will use Basic Auth")
print()

# Create workflow
print("[1/4] Creating workflow...")
workflow_data = {
    "name": "Video Upload and Retrieval Workflow",
    "nodes": [
        {
            "parameters": {},
            "id": "start",
            "name": "When clicking test",
            "type": "n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [250, 300]
        },
        {
            "parameters": {
                "jsCode": f"// Set video file path\n// Note: n8n runs in Docker, but memcontext-n8n service runs on host (accessed via host.docker.internal:5019)\n// So we need to use Windows path (host path) because the service reads files on the host\n// Method 1: Get video_path from input data (if provided when manually triggered)\n// Method 2: Use default path (auto-detected project path)\nconst inputData = $input.item.json || {{}};\n\n// Use Windows path (because memcontext-n8n service runs on host)\n// Default path: {path_to_js_string(DEFAULT_VIDEO_PATH)}\nconst videoPath = inputData.video_path || '{path_to_js_string(DEFAULT_VIDEO_PATH)}';\n\n// Remove quotes if path contains them\nconst cleanPath = videoPath.replace(/^[\\\"']|[\\\"']$/g, '');\n\n// Validate path format\nif (!cleanPath || cleanPath.trim() === '') {{\n  throw new Error('Video path cannot be empty');\n}}\n\nreturn {{\n  json: {{\n    file_path: cleanPath,\n    user_id: inputData.user_id || 'test_user_video',\n    agent_response: inputData.agent_response || 'Video uploaded and added to memory',\n    converter_type: inputData.converter_type || 'video',\n    query: inputData.query || 'What is the main content of this video?'\n  }}\n}};"
            },
            "id": "set_video_path",
            "name": "Set Video Path",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [450, 300]
        },
        {
            "parameters": {
                "url": f"{API_URL}/api/memory/add_multimodal",
                "method": "POST",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "Authorization",
                            "value": f"Bearer {MEMCONTEXT_API_KEY}"
                        },
                        {
                            "name": "Content-Type",
                            "value": "application/json"
                        }
                    ]
                },
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify({\n  user_id: $json.user_id,\n  file_path: $json.file_path,\n  agent_response: $json.agent_response,\n  converter_type: $json.converter_type\n}) }}",
                "options": {
                    "timeout": 1800000,
                    "response": {
                        "response": {
                            "neverError": True,
                            "responseFormat": "json"
                        }
                    },
                    "redirect": {
                        "redirect": {
                            "followRedirects": True
                        }
                    }
                }
            },
            "id": "add_video_memory",
            "name": "Add Video Memory",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [650, 300]
        },
        {
            "parameters": {
                "url": f"{API_URL}/api/memory/search",
                "method": "POST",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "Authorization",
                            "value": f"Bearer {MEMCONTEXT_API_KEY}"
                        },
                        {
                            "name": "Content-Type",
                            "value": "application/json"
                        }
                    ]
                },
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify({\n  user_id: $('Set Video Path').item.json.user_id,\n  query: $('Set Video Path').item.json.query || 'What is the main content of this video?',\n  relationship_with_user: 'friend',\n  style_hint: 'friendly'\n}) }}",
                "options": {}
            },
            "id": "search_memory",
            "name": "Search Memory",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [850, 300]
        },
        {
            "parameters": {
                "jsCode": "// Format output results\nconst addResult = $('Add Video Memory').item.json || {};\nconst searchResult = $('Search Memory').item.json || {};\n\n// Extract key information\nconst uploadSuccess = addResult.code === 200 || addResult.code === undefined;\nconst searchSuccess = searchResult.code === 200 || searchResult.code === undefined;\n\nreturn {\n  json: {\n    video_upload: {\n      success: uploadSuccess,\n      message: addResult.message || 'Video processing completed',\n      data: addResult.data || addResult,\n      ingested_rounds: addResult.data?.ingested_rounds || 0,\n      file_id: addResult.data?.file_id || null\n    },\n    memory_search: {\n      success: searchSuccess,\n      message: searchResult.message || 'Search completed',\n      response: searchResult.data?.response || searchResult.response || 'No related memory found',\n      timestamp: searchResult.data?.timestamp || null\n    },\n    summary: {\n      video_processed: uploadSuccess ? 'Success' : 'Failed',\n      memory_found: searchSuccess && (searchResult.data?.response || searchResult.response) ? 'Yes' : 'No',\n      answer: searchResult.data?.response || searchResult.response || 'No related memory found',\n      chunks_ingested: addResult.data?.ingested_rounds || 0\n    }\n  }\n};"
            },
            "id": "format_output",
            "name": "Format Output",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1050, 300]
        }
    ],
    "connections": {
        "When clicking test": {
            "main": [[{"node": "Set Video Path", "type": "main", "index": 0}]]
        },
        "Set Video Path": {
            "main": [[{"node": "Add Video Memory", "type": "main", "index": 0}]]
        },
        "Add Video Memory": {
            "main": [[{"node": "Search Memory", "type": "main", "index": 0}]]
        },
        "Search Memory": {
            "main": [[{"node": "Format Output", "type": "main", "index": 0}]]
        }
    },
    "settings": {},
    "staticData": None
}

# Prepare request headers
headers = {}
if N8N_API_KEY:
    headers["X-N8N-API-KEY"] = N8N_API_KEY
    auth = None
else:
    # Use Basic Auth
    from requests.auth import HTTPBasicAuth
    auth = HTTPBasicAuth(N8N_USER, N8N_PASS)

try:
    # Debug: show actual authentication method used
    if N8N_API_KEY:
        print(f"[DEBUG] Using API Key authentication, first 20 chars: {N8N_API_KEY[:20]}...")
        print(f"[DEBUG] Request header: X-N8N-API-KEY = {N8N_API_KEY[:30]}...")
    else:
        print(f"[DEBUG] Using Basic Auth: {N8N_USER}/{N8N_PASS}")
    
    response = requests.post(
        f"{N8N_URL}/api/v1/workflows",
        json=workflow_data,
        headers=headers,
        auth=auth if not N8N_API_KEY else None,
        timeout=10
    )
    
    if response.status_code in [200, 201]:
        workflow = response.json()
        workflow_id = workflow["id"]
        print(f"[SUCCESS] Workflow created, ID: {workflow_id}")
    else:
        print(f"[ERROR] Failed to create workflow: {response.status_code}")
        print(response.text)
        if response.status_code == 401:
            print(f"\n[DEBUG] Current API Key: {N8N_API_KEY[:50] if N8N_API_KEY else 'not configured'}...")
            print(f"[DEBUG] Please check if N8N_API_KEY in .env file is correct")
            print("\nTip: n8n requires API Key authentication")
            print("Please follow these steps to get API Key:")
            print("1. Open browser and visit: http://localhost:5678")
            print("2. Go to Settings -> API")
            print("3. Create a new API Key")
            print("4. Add to .env file: N8N_API_KEY=your_api_key")
        exit(1)
except Exception as e:
    print(f"[ERROR] Creation failed: {e}")
    exit(1)

# 2. Wait for workflow to be ready
print("\n[2/4] Waiting for workflow to be ready...")
time.sleep(2)

# 3. Activate workflow
print("[3/4] Activating workflow...")
try:
    # n8n requires active: true to activate workflow
    response = requests.post(
        f"{N8N_URL}/api/v1/workflows/{workflow_id}/activate",
        json={"active": True},
        headers=headers,
        auth=auth if not N8N_API_KEY else None,
        timeout=10
    )
    if response.status_code in [200, 204]:
        print("[SUCCESS] Workflow activated")
    else:
        print(f"[WARNING] Activation failed: {response.status_code}")
        print(f"Response: {response.text}")
        print("Tip: You can manually activate the workflow in n8n UI")
except Exception as e:
    print(f"[WARNING] Activation failed: {e}")
    print("Tip: You can manually activate the workflow in n8n UI")

print("\n" + "=" * 60)
print("Workflow creation completed!")
print("=" * 60)
print(f"\nWorkflow URL: {N8N_URL}/workflow/{workflow_id}")
print(f"\nUsage instructions:")
print("1. Open the URL above in your browser")
print("2. Click 'Set Video Path' node to modify the video path in code")
print("   Or add video_path field to input data when executing workflow")
print("3. Click 'When clicking test' node, then click 'Execute Workflow' to run")
print("4. Check the results in 'Format Output' node")
print("\nTips:")
print(f"- Default video path: {DEFAULT_VIDEO_PATH}")
print(f"- Project root: {PROJECT_ROOT}")
print("- Video path format example (Windows): D:\\\\project\\\\memcontext-memcontext\\\\memcontext-n8n\\\\test1.mp4")
print("- Or use forward slashes: D:/project/memcontext-memcontext/memcontext-n8n/test1.mp4")
print("- If path contains spaces, no quotes needed, n8n will handle it automatically")
print("- You can specify other video paths via video_path field in input data when executing workflow")

