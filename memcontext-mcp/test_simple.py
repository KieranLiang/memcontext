#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 Memcontext MCP 服务器测试脚本
测试 MCP 工具的基本功能
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到路径，复用 memcontext 包
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from server_new import init_memcontext, add_memory, retrieve_memory, get_user_profile
import server_new  # 导入模块以访问全局变量

def test_mcp_tools():
    """测试 MCP 工具"""
    print("=" * 60)
    print("Memcontext MCP 工具测试")
    print("=" * 60)
    print()
    
    # 获取配置文件路径
    config_path = Path(__file__).parent / "config.json"
    
    if not config_path.exists():
        print(f"[X] 配置文件不存在: {config_path}")
        return False
    
    # 初始化 Memcontext
    print("1. 初始化 Memcontext...")
    try:
        memcontext_instance = init_memcontext(str(config_path))
        # 设置全局变量，让 MCP 工具函数可以访问
        server_new.memcontext_instance = memcontext_instance
        print(f"   [OK] Memcontext 初始化成功")
        print(f"   用户ID: {memcontext_instance.user_id}")
        print(f"   数据路径: {memcontext_instance.data_storage_path}")
        print()
    except Exception as e:
        print(f"   [X] 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 测试 add_memory
    print("2. 测试 add_memory 工具...")
    try:
        result = add_memory(
            user_input="这是一个测试对话：我喜欢使用 Python 编程",
            agent_response="Python 是一门很好的编程语言，适合各种应用场景"
        )
        if result.get("status") == "success":
            print(f"   [OK] 记忆添加成功")
            print(f"   时间戳: {result.get('timestamp')}")
        else:
            print(f"   [X] 记忆添加失败: {result.get('message')}")
            return False
        print()
    except Exception as e:
        print(f"   [X] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 测试 retrieve_memory
    print("3. 测试 retrieve_memory 工具...")
    try:
        result = retrieve_memory(
            query="用户喜欢什么编程语言？",
            max_results=5
        )
        if result.get("status") == "success":
            print(f"   [OK] 记忆检索成功")
            print(f"   查询: {result.get('query')}")
            print(f"   短期记忆数量: {result.get('short_term_count', 0)}")
            print(f"   检索到的页面数: {result.get('total_pages_found', 0)}")
            print(f"   用户知识条目数: {result.get('total_user_knowledge_found', 0)}")
        else:
            print(f"   [X] 记忆检索失败: {result.get('message')}")
            return False
        print()
    except Exception as e:
        print(f"   [X] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 测试 get_user_profile
    print("4. 测试 get_user_profile 工具...")
    try:
        result = get_user_profile(include_knowledge=True)
        if result.get("status") == "success":
            print(f"   [OK] 用户画像获取成功")
            print(f"   用户ID: {result.get('user_id')}")
            print(f"   助手ID: {result.get('assistant_id')}")
            user_profile = result.get('user_profile', '')
            if user_profile and user_profile.lower() != "no detailed user profile":
                print(f"   用户画像: {user_profile[:100]}..." if len(user_profile) > 100 else f"   用户画像: {user_profile}")
            else:
                print(f"   用户画像: 暂无详细画像")
        else:
            print(f"   [X] 用户画像获取失败: {result.get('message')}")
            return False
        print()
    except Exception as e:
        print(f"   [X] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("=" * 60)
    print("所有测试通过！")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_mcp_tools()
    sys.exit(0 if success else 1)

