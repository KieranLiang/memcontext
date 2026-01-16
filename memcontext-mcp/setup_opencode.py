#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenCode Memcontext MCP 服务器配置工具

此脚本用于自动配置 OpenCode 编辑器以使用 Memcontext MCP 服务器。
支持通过 npm 全局安装的 OpenCode (opencode-ai)。

功能：
- 自动检测 OpenCode 安装状态
- 自动查找或创建配置文件
- 配置 MCP 服务器连接
- 备份现有配置

使用方法：
    python setup_opencode.py

配置文件位置：
- Windows: C:\\Users\\<用户名>\\.config\\opencode\\opencode.json
- macOS/Linux: ~/.config/opencode/opencode.json
"""

import os
import json
import sys
import platform
import subprocess
from pathlib import Path
from typing import Tuple, Optional

def find_opencode_config() -> Tuple[Path, bool]:
    """
    查找 OpenCode 配置文件位置
    
    始终返回官方标准位置：.config/opencode/opencode.json
    
    Returns:
        Tuple[Path, bool]: (配置文件路径, 文件是否存在)
    """
    home = Path.home()
    
    # OpenCode 官方配置文件名是 opencode.json（不带点）
    # 标准位置：.config/opencode/opencode.json（Windows、macOS、Linux 都使用这个位置）
    official_path = home / '.config' / 'opencode' / 'opencode.json'
    
    # 检查官方位置是否存在
    config_exists = official_path.exists()
    
    # 检查是否存在旧位置的配置文件（仅用于提示用户）
    if platform.system() == 'Windows':
        # 检查用户目录下的 opencode.json
        home_path = home / 'opencode.json'
        if home_path.exists() and not config_exists:
            print(f"[!] 发现旧版配置文件: {home_path}")
            print(f"    新配置文件将在标准位置创建: {official_path}")
            print(f"    建议：将旧配置迁移到新位置")
        
        # 检查 APPDATA 下的文件
        appdata = os.getenv('APPDATA', '')
        if appdata:
            appdata_path = Path(appdata) / 'opencode' / 'opencode.json'
            if appdata_path.exists() and not config_exists:
                print(f"[!] 发现其他位置的配置文件: {appdata_path}")
                print(f"    新配置文件将在标准位置创建: {official_path}")
                print(f"    建议：将配置迁移到标准位置")
        
        # 检查兼容格式（带点的文件）
        dot_path = home / '.opencode.json'
        if dot_path.exists() and not config_exists:
            print(f"[!] 发现兼容格式配置文件: {dot_path}")
            print(f"    新配置文件将在标准位置创建: {official_path}")
            print(f"    建议：将 {dot_path.name} 重命名为 {official_path.name}")
    else:
        # macOS/Linux: 检查用户目录下的文件
        home_path = home / 'opencode.json'
        if home_path.exists() and not config_exists:
            print(f"[!] 发现旧版配置文件: {home_path}")
            print(f"    新配置文件将在标准位置创建: {official_path}")
            print(f"    建议：将旧配置迁移到新位置")
    
    # 始终返回官方标准位置
    return official_path, config_exists

def check_opencode_installed() -> Tuple[Optional[bool], Optional[str]]:
    """
    检查 OpenCode 是否已通过 npm 全局安装
    
    Returns:
        Tuple[Optional[bool], Optional[str]]: 
            - (True, npm_root): 已安装，返回 npm 全局包路径
            - (False, None): 未安装
            - (None, None): 无法确定（npm 命令不可用）
    """
    try:
        result = subprocess.run(
            ['npm', 'list', '-g', 'opencode-ai'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and 'opencode-ai' in result.stdout:
            # 尝试获取安装路径
            try:
                npm_root_result = subprocess.run(
                    ['npm', 'root', '-g'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if npm_root_result.returncode == 0:
                    npm_root = npm_root_result.stdout.strip()
                    return True, npm_root
            except:
                pass
            return True, None
        return False, None
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return None, None  # 无法确定

def get_paths() -> dict:
    """
    获取所有相关路径信息
    
    Returns:
        dict: 包含以下键的字典：
            - opencode_config: OpenCode 配置文件路径
            - config_exists: 配置文件是否存在
            - project_root: 项目根目录
            - server_script: MCP 服务器脚本路径
            - config_file: Memcontext 配置文件路径
            - python_path: Python 可执行文件路径
    """
    # 查找 OpenCode 配置文件
    opencode_config_path, config_exists = find_opencode_config()
    
    project_root = Path(__file__).parent.absolute()
    
    return {
        'opencode_config': opencode_config_path,
        'config_exists': config_exists,
        'project_root': project_root,
        'server_script': project_root / 'server_new.py',
        'config_file': project_root / 'config.json',
        'python_path': sys.executable
    }

def backup_config(config_path: Path) -> bool:
    """
    备份现有配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        bool: 备份是否成功
    """
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

def update_opencode_config(paths: dict) -> bool:
    """
    更新 OpenCode MCP 配置
    
    此函数会：
    1. 备份现有配置文件（如果存在）
    2. 读取现有配置（支持 JSONC 格式）
    3. 添加或更新 memcontext MCP 服务器配置
    4. 保存配置文件
    
    Args:
        paths: 路径信息字典（来自 get_paths()），包含：
            - opencode_config: OpenCode 配置文件路径
            - python_path: Python 可执行文件路径
            - server_script: MCP 服务器脚本路径
            - config_file: Memcontext 配置文件路径
        
    Returns:
        bool: 配置是否成功更新
    """
    config_path = paths['opencode_config']
    
    # 备份现有配置（如果存在）
    backup_config(config_path)
    
    # 读取现有配置
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 尝试解析 JSON（支持 JSONC 格式，去除注释）
                lines = content.split('\n')
                cleaned_lines = []
                for line in lines:
                    # 移除行内注释（// 后面的内容）
                    if '//' in line:
                        comment_pos = line.find('//')
                        # 检查是否在字符串内
                        in_string = False
                        for i in range(comment_pos):
                            if line[i] == '"' and (i == 0 or line[i-1] != '\\'):
                                in_string = not in_string
                        if not in_string:
                            line = line[:comment_pos]
                    cleaned_lines.append(line)
                cleaned_content = '\n'.join(cleaned_lines)
                config = json.loads(cleaned_content)
        except json.JSONDecodeError as e:
            print(f"[!] 现有配置文件格式错误: {e}")
            print("    将创建新配置文件")
            config = {}
    else:
        config = {}
    
    # 准备 MCP 配置（OpenCode 格式：使用 command 数组）
    # OpenCode 使用 command 数组格式，第一个元素是可执行文件，后续是参数
    python_path = paths['python_path'].replace('\\', '/')
    server_script = str(paths['server_script']).replace('\\', '/')
    config_file = str(paths['config_file']).replace('\\', '/')
    
    mcp_config = {
        "type": "local",
        "command": [
            python_path,
            server_script,
            "--config",
            config_file
        ],
        "enabled": True
    }
    
    # 确保 $schema 存在
    if '$schema' not in config:
        config['$schema'] = 'https://opencode.ai/config.json'
    
    # 确保 mcp 字段存在
    if 'mcp' not in config:
        config['mcp'] = {}
    
    # 检查是否已存在 memcontext 配置
    if 'memcontext' in config['mcp']:
        print("[!] 已存在 memcontext 配置，将更新")
    
    # 添加/更新 memcontext 配置
    config['mcp']['memcontext'] = mcp_config
    
    # 写入配置
    try:
        # 确保目录存在
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] OpenCode MCP 配置已更新: {config_path}")
        print("\n配置内容预览:")
        print(json.dumps({'memcontext': mcp_config}, indent=2, ensure_ascii=False))
        return True
    except PermissionError:
        print(f"[X] 写入配置失败: 没有权限写入文件 {config_path}")
        print("    请检查文件权限或使用管理员权限运行")
        return False
    except Exception as e:
        print(f"[X] 写入配置失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("OpenCode Memcontext MCP 配置工具")
    print("=" * 60)
    print()
    
    # 检查 OpenCode 是否已安装
    print("检查 OpenCode 安装状态...")
    installed, npm_root = check_opencode_installed()
    if installed:
        print("[OK] 检测到 OpenCode 已通过 npm 全局安装")
        if npm_root:
            print(f"   全局 npm 包路径: {npm_root}")
    elif installed is False:
        print("[!] 未检测到 OpenCode (opencode-ai) 的全局安装")
        print("    如果已安装，请确保使用: npm install -g opencode-ai")
    else:
        print("[!] 无法检查 OpenCode 安装状态（npm 命令不可用）")
    print()
    
    paths = get_paths()
    
    print("路径信息:")
    print(f"  Python: {paths['python_path']}")
    print(f"  服务器脚本: {paths['server_script']}")
    print(f"  配置文件: {paths['config_file']}")
    print(f"  OpenCode 配置: {paths['opencode_config']}")
    if paths['config_exists']:
        print(f"  [OK] 配置文件已存在，将更新配置")
        print(f"      文件位置: {paths['opencode_config']}")
    else:
        print(f"  [!] 配置文件不存在，将在以下位置创建:")
        print(f"      {paths['opencode_config']}")
    print()
    
    # 验证文件存在
    if not paths['server_script'].exists():
        print(f"[X] 服务器脚本不存在: {paths['server_script']}")
        return 1
    
    if not paths['config_file'].exists():
        print(f"[X] 配置文件不存在: {paths['config_file']}")
        return 1
    
    # 更新配置
    if update_opencode_config(paths):
        print("\n" + "=" * 60)
        print("配置完成！")
        print("=" * 60)
        print("\n下一步:")
        print("1. 完全关闭并重新启动 OpenCode")
        print("2. 在 OpenCode 中测试:")
        print("   '请使用 Memcontext 添加一条记忆：我在 OpenCode 中使用 Python'")
        print("\n提示:")
        print("- OpenCode 会自动加载 MCP 工具")
        print("- 您可以直接说 '请使用 add_memory 工具' 来添加记忆")
        print("- 或说 '请从 MemoryOS 检索记忆' 来查询")
        print("\n配置文件位置:")
        print(f"  {paths['opencode_config']}")
        print("\n重要说明:")
        print("- npm 全局安装的 OpenCode，配置文件应该是 opencode.json（不带点）")
        print("- 配置文件位置: Windows 和 macOS/Linux 都在 .config/opencode/ 目录下")
        print("- 不需要知道 OpenCode 的安装路径（node_modules 位置）")
        print("- 如果找到的是 .opencode.json（带点），建议重命名为 opencode.json（不带点）")
        print("\n如果 OpenCode 仍然无法识别 MCP 工具:")
        print("1. 确认配置文件名称是 opencode.json（不带点，不是 .opencode.json）")
        print("2. 检查配置文件格式是否正确（command 必须是数组）")
        print("3. 完全重启 OpenCode（不是重新加载）")
        print("4. 查看 OpenCode 的日志文件查找错误信息")
        return 0
    else:
        print("\n[X] 配置失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
