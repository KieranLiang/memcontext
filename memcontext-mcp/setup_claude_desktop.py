#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置 Claude Desktop 的 MemoryOS MCP 服务器
"""

import os
import json
import sys
import platform
from pathlib import Path

def get_paths():
    """获取路径信息"""
    # Claude Desktop 的配置文件位置
    if platform.system() == 'Windows':
        claude_config_path = Path(os.getenv('APPDATA', '')) / 'Claude' / 'claude_desktop_config.json'
    elif platform.system() == 'Darwin':  # macOS
        claude_config_path = Path.home() / 'Library' / 'Application Support' / 'Claude' / 'claude_desktop_config.json'
    else:  # Linux
        claude_config_path = Path.home() / '.config' / 'claude' / 'claude_desktop_config.json'
    
    project_root = Path(__file__).parent.absolute()
    
    return {
        'claude_config': claude_config_path,
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

def update_claude_desktop_config(paths):
    """更新 Claude Desktop MCP 配置"""
    config_path = paths['claude_config']
    
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
        print(f"[OK] Claude Desktop MCP 配置已更新: {config_path}")
        print("\n配置内容:")
        print(json.dumps({'memcontext': mcp_config}, indent=2, ensure_ascii=False))
        return True
    except Exception as e:
        print(f"[X] 写入配置失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Claude Desktop Memcontext MCP 配置工具")
    print("=" * 60)
    print()
    
    paths = get_paths()
    
    print("路径信息:")
    print(f"  Python: {paths['python_path']}")
    print(f"  服务器脚本: {paths['server_script']}")
    print(f"  配置文件: {paths['config_file']}")
    print(f"  Claude Desktop 配置: {paths['claude_config']}")
    print()
    
    # 验证文件存在
    if not paths['server_script'].exists():
        print(f"[X] 服务器脚本不存在: {paths['server_script']}")
        return 1
    
    if not paths['config_file'].exists():
        print(f"[X] 配置文件不存在: {paths['config_file']}")
        return 1
    
    # 更新配置
    if update_claude_desktop_config(paths):
        print("\n" + "=" * 60)
        print("配置完成！")
        print("=" * 60)
        print("\n下一步:")
        print("1. 完全关闭并重新启动 Claude Desktop")
        print("2. 在 Claude Desktop 中测试:")
        print("   '请使用 Memcontext 添加一条记忆：我在 Claude Desktop 中使用 Python'")
        print("\n提示:")
        print("- Claude Desktop 会自动加载 MCP 工具")
        print("- 您可以直接说 '请使用 add_memory 工具' 来添加记忆")
        print("- 或说 '请从 MemoryOS 检索记忆' 来查询")
        print("\n配置文件位置:")
        print(f"  {paths['claude_config']}")
        return 0
    else:
        print("\n[X] 配置失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())

