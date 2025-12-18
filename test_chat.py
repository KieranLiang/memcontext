#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试对话脚本：针对已上传的视频进行对话

使用说明：
1. 确保 Flask 服务器正在运行（python memdemo/app.py）
2. 确保已经通过 test_memdemo.py 上传了视频
3. 运行此脚本进行对话测试
"""

import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

SERVER = "http://127.0.0.1:5019"
INIT_ENDPOINT = f"{SERVER}/init_memory"
CHAT_ENDPOINT = f"{SERVER}/chat"

def init_memory_session(session, user_id="video_user7"):
    """初始化记忆系统会话"""
    print(f"🔧 初始化记忆系统 (user_id: {user_id})...")
    response = session.post(INIT_ENDPOINT, json={"user_id": user_id})
    response.raise_for_status()
    data = response.json()
    if data.get("success"):
        print(f"✅ 初始化成功！session_id: {data.get('session_id')}")
        return data.get('session_id')
    else:
        raise RuntimeError(f"初始化失败: {data}")

def chat(session, message):
    """发送对话消息"""
    print(f"\n💬 用户: {message}")
    response = session.post(CHAT_ENDPOINT, json={"message": message})
    response.raise_for_status()
    result = response.json()
    
    if "error" in result:
        print(f"❌ 错误: {result['error']}")
        return None
    
    ai_response = result.get("response", "")
    print(f"🤖 AI: {ai_response}")
    return ai_response

def main():
    """主函数"""
    print("="*60)
    print("🧠 MemContext 视频对话测试")
    print("="*60)
    
    # 创建会话（保持 cookies）
    session = requests.Session()
    
    try:
        # 1. 初始化记忆系统
        session_id = init_memory_session(session)
        
        # 2. 示例对话问题
        questions = [
            "这个视频的主要内容是什么？",
            "视频中出现了哪些关键场景？",
            "视频的时长是多少？",
            "视频中有哪些重要信息？",
            "请总结一下视频的要点。"
        ]
        
        # 3. 依次提问
        for i, question in enumerate(questions, 1):
            print(f"\n{'='*60}")
            print(f"问题 {i}/{len(questions)}")
            print(f"{'='*60}")
            chat(session, question)
            
            # 可以选择是否在每个问题之间暂停
            # input("\n按 Enter 继续下一个问题...")
        
        # 4. 交互式对话（可选）
        print(f"\n{'='*60}")
        print("进入交互式对话模式（输入 'exit' 退出）")
        print(f"{'='*60}")
        
        while True:
            user_input = input("\n您: ").strip()
            if user_input.lower() in ['exit', 'quit', '退出']:
                break
            if not user_input:
                continue
            chat(session, user_input)
        
        print("\n👋 再见！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误：请确保 Flask 服务器正在运行")
        print("   启动命令: cd memdemo && python app.py")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
