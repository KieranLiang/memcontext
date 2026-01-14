#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置 Cursor 的 MemoryOS MCP 服务器
"""

import os
import json
import sys
from pathlib import Path

def get_paths():
    """获取路径信息"""
    # Cursor 的 MCP 配置文件位置
    cursor_config_path = Path.home() / '.cursor' / 'mcp.json'
    
    project_root = Path(__file__).parent.absolute()
    
    return {
        'cursor_config': cursor_config_path,
        'project_root': project_root,
        'server_script': project_root / 'server_new.py',
        'config_file': project_root / 'config.json',
        'python_path': sys.executable
    }

def backup_config(config_path):
    """备份现有配置"""
    if config_path.exists():
        backup_path = config_path.with_suffix('.json.bak')
        try:
            import shutil
            shutil.copy2(config_path, backup_path)
            print(f"[备份] 已备份现有配置到: {backup_path}")
            return True
        except Exception as e:
            print(f"[!] 备份失败: {e}")
            return False
    return True

def update_cursor_config(paths):
    """更新 Cursor MCP 配置"""
    config_path = paths['cursor_config']
    
    # 确保目录存在
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 备份现有配置
    backup_config(config_path)
    
    # 读取现有配置
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[!] 现有配置文件格式错误: {e}")
            print("    将创建新配置文件")
            config = {}
    else:
        config = {}
    
    # 准备 MCP 配置
    mcp_config = {
        "command": paths['python_path'].replace('\\', '/'),
        "args": [
            str(paths['server_script']).replace('\\', '/'),
            "--config",
            str(paths['config_file']).replace('\\', '/')
        ],
        "env": {}
    }
    
    # 确保 mcpServers 存在
    if 'mcpServers' not in config:
        config['mcpServers'] = {}
    
    # 检查是否已存在 memcontext 配置
    if 'memcontext' in config['mcpServers']:
        print("[!] 已存在 memcontext 配置，将更新")
    
    # 添加/更新 memcontext 配置
    config['mcpServers']['memcontext'] = mcp_config
    
    # 写入配置
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"[OK] Cursor MCP 配置已更新: {config_path}")
        print("\n配置内容:")
        print(json.dumps({'memcontext': mcp_config}, indent=2, ensure_ascii=False))
        return True
    except Exception as e:
        print(f"[X] 写入配置失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Cursor Memcontext MCP 配置工具")
    print("=" * 60)
    print()
    
    paths = get_paths()
    
    print("路径信息:")
    print(f"  Python: {paths['python_path']}")
    print(f"  服务器脚本: {paths['server_script']}")
    print(f"  配置文件: {paths['config_file']}")
    print(f"  Cursor 配置: {paths['cursor_config']}")
    print()
    
    # 验证文件存在
    if not paths['server_script'].exists():
        print(f"[X] 服务器脚本不存在: {paths['server_script']}")
        return 1
    
    if not paths['config_file'].exists():
        print(f"[X] 配置文件不存在: {paths['config_file']}")
        return 1
    
    # 更新配置
    if update_cursor_config(paths):
        print("\n" + "=" * 60)
        print("配置完成！")
        print("=" * 60)
        print("\n下一步:")
        print("1. 完全关闭并重新启动 Cursor")
        print("2. 在 Cursor 的 AI 聊天中测试:")
        print("   '请使用 MemoryOS 添加一条记忆：我在 Cursor 中使用 Python'")
        print("\n提示:")
        print("- Cursor 会自动加载 MCP 工具")
        print("- 您可以直接说 '请使用 add_memory 工具' 来添加记忆")
        print("- 或说 '请从 MemoryOS 检索记忆' 来查询")
        return 0
    else:
        print("\n[X] 配置失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())

