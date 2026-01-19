#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置 Claude Code 的 MemoryOS MCP 服务器
使用 claude mcp add 命令来添加 MCP 服务器

根据 Claude Code 官方文档：
- 使用 claude mcp add --transport stdio <name> -- <command> [args...]
- 支持三种 scope: local, project, user
- 配置文件位置: ~/.claude.json (Windows: C:/Users/<用户名>/.claude.json)
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def get_paths():
    """获取路径信息"""
    project_root = Path(__file__).parent.absolute()
    
    return {
        'project_root': project_root,
        'server_script': project_root / 'server_new.py',
        'config_file': project_root / 'config.json',
        'python_path': sys.executable
    }

def find_claude_executable():
    """查找 claude 可执行文件"""
    # 首先尝试直接执行 claude 命令
    try:
        result = subprocess.run(
            ['claude', '--version'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=5
        )
        if result.returncode == 0:
            # 命令可用，尝试找到实际路径
            if platform.system() == 'Windows':
                try:
                    where_result = subprocess.run(
                        ['where.exe', 'claude'],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
                        timeout=5
                    )
                    if where_result.returncode == 0:
                        paths = where_result.stdout.strip().split('\n')
                        # 优先选择 .cmd 或 .exe 文件
                        for path in paths:
                            path = path.strip()
                            if path.endswith('.cmd') or path.endswith('.exe'):
                                if Path(path).exists():
                                    return path
                        # 如果没有找到 .cmd 或 .exe，尝试第一个结果
                        if paths:
                            first_path = paths[0].strip()
                            if not first_path.endswith(('.cmd', '.exe', '.bat')):
                                cmd_path = first_path + '.cmd'
                                if Path(cmd_path).exists():
                                    return cmd_path
                            return first_path
                except:
                    pass
            # 如果无法确定路径，返回 None（使用 'claude' 命令）
            return None
    except:
        pass
    
    # 尝试常见位置
    common_paths = []
    if platform.system() == 'Windows':
        user_home = Path.home()
        username = os.getenv('USERNAME', '')
        common_paths = [
            Path(os.getenv('APPDATA', '')) / 'npm' / 'claude.cmd',
            Path(os.getenv('APPDATA', '')) / 'npm' / 'claude',
            user_home / '.claude' / 'claude.exe',
            user_home / '.claude' / 'claude.cmd',
            Path(f'C:/Users/{username}') / '.claude' / 'claude.exe' if username else None,
            Path(os.getenv('LOCALAPPDATA', '')) / 'Programs' / 'Claude' / 'claude.exe',
        ]
        common_paths = [p for p in common_paths if p is not None]
    
    for path in common_paths:
        if path.exists():
            return str(path)
    
    return None

def get_claude_config_path():
    """获取 Claude 配置文件路径"""
    home = Path.home()
    if platform.system() == 'Windows':
        # Windows: C:\Users\<用户名>\.claude.json
        return home / '.claude.json'
    else:
        # macOS/Linux: ~/.claude.json
        return home / '.claude.json'

def check_claude_cli(claude_path=None):
    """检查 claude 命令是否可用"""
    if claude_path is None:
        claude_path = find_claude_executable()
        if claude_path:
            print(f"[信息] 找到 claude 可执行文件: {claude_path}")
    
    # 尝试执行 claude 命令
    try:
        cmd = [claude_path] if claude_path else ['claude']
        result = subprocess.run(
            cmd + ['--version'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=5,
            shell=False
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"[OK] Claude Code 已安装: {version}")
            if claude_path:
                print(f"     可执行文件路径: {claude_path}")
            return True, claude_path if claude_path else 'claude'
        else:
            print(f"[!] Claude 命令执行失败")
            if result.stderr:
                print(f"     错误: {result.stderr.strip()}")
            return False, claude_path
    except FileNotFoundError:
        print("[X] 未找到 claude 命令")
        if claude_path:
            print(f"     尝试的路径: {claude_path}")
        print("    请确保 Claude Code 已安装并且 claude 命令在 PATH 中")
        return False, claude_path
    except Exception as e:
        print(f"[X] 检查 Claude 命令时出错: {e}")
        return False, claude_path

def build_mcp_add_command(paths, scope='local', server_name='memcontext', claude_path=None):
    """构建 claude mcp add 命令
    
    根据文档格式：
    claude mcp add --transport stdio [--scope <scope>] <name> -- <command> [args...]
    
    所有选项（--transport, --env, --scope, --header）必须在服务器名称之前
    -- (双破折号) 分隔服务器名称和命令
    """
    python_path = paths['python_path']
    server_script = paths['server_script']
    config_file = paths['config_file']
    
    # 确保路径使用正斜杠（跨平台兼容）
    python_cmd = str(python_path).replace('\\', '/')
    server_cmd = str(server_script).replace('\\', '/')
    config_cmd = str(config_file).replace('\\', '/')
    
    # 构建命令列表
    # 根据文档：claude mcp add [options] <name> -- <command> [args...]
    claude_cmd = claude_path if claude_path else 'claude'
    cmd = [
        claude_cmd, 'mcp', 'add',
        '--transport', 'stdio',
        '--scope', scope,
        server_name,
        '--',
        python_cmd,
        server_cmd,
        '--config',
        config_cmd
    ]
    
    return cmd

def remove_mcp_server(scope='local', server_name='memcontext', claude_path=None):
    """移除 MCP 服务器"""
    claude_cmd = claude_path if claude_path else 'claude'
    cmd = [claude_cmd, 'mcp', 'remove', server_name, '-s', scope]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10,
            shell=False
        )
        if result.returncode == 0:
            print(f"[信息] 已移除旧的 {scope} scope 配置")
            return True
        else:
            # 如果服务器不存在，这也是正常的（不是错误）
            error_msg = result.stderr.lower() if result.stderr else ''
            if 'not found' in error_msg or 'does not exist' in error_msg:
                return True  # 服务器不存在，可以继续添加
            return False
    except Exception as e:
        # 移除失败不影响添加操作
        return False

def add_mcp_server(paths, scope='local', server_name='memcontext', claude_path=None):
    """添加 MCP 服务器到 Claude Code"""
    print(f"\n正在添加 MCP 服务器 '{server_name}' (scope: {scope})...")
    
    # 如果已存在，先尝试移除
    print(f"[信息] 检查是否已存在 {scope} scope 的配置...")
    remove_mcp_server(scope, server_name, claude_path)
    
    # 构建命令
    cmd = build_mcp_add_command(paths, scope, server_name, claude_path)
    
    print(f"\n执行命令:")
    print(f"  {' '.join(cmd)}")
    print()
    
    try:
        # 执行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30,
            shell=False
        )
        
        if result.returncode == 0:
            print("[OK] MCP 服务器已成功添加")
            if result.stdout:
                print(f"输出: {result.stdout}")
            return True
        else:
            print(f"[X] 添加 MCP 服务器失败 (退出码: {result.returncode})")
            if result.stderr:
                print(f"错误信息: {result.stderr}")
            if result.stdout:
                print(f"输出: {result.stdout}")
            # 检查是否是"已存在"的错误
            error_msg = result.stderr.lower() if result.stderr else ''
            if 'already exists' in error_msg:
                print("\n提示: 服务器已存在。如果需要更新配置，请先手动移除：")
                claude_cmd = claude_path if claude_path else 'claude'
                print(f"  {claude_cmd} mcp remove {server_name} -s {scope}")
            return False
            
    except subprocess.TimeoutExpired:
        print("[X] 命令执行超时")
        return False
    except Exception as e:
        print(f"[X] 执行命令时出错: {e}")
        return False

def list_mcp_servers(claude_path=None):
    """列出已配置的 MCP 服务器"""
    print("\n正在列出已配置的 MCP 服务器...")
    try:
        claude_cmd = claude_path if claude_path else 'claude'
        result = subprocess.run(
            [claude_cmd, 'mcp', 'list'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10,
            shell=False
        )
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"[!] 列出服务器失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"[!] 列出服务器时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Claude Code Memcontext MCP 配置工具")
    print("=" * 60)
    print()
    
    # 检查 Claude 命令
    claude_available, claude_path = check_claude_cli()
    if not claude_available:
        print("\n提示:")
        print("1. 确保已安装 Claude Code")
        print("2. 确保 claude 命令在系统 PATH 中")
        print("3. 在 Windows 上，可能需要重启终端或重新加载环境变量")
        print("4. 或者您可以手动指定 claude 可执行文件的完整路径")
        
        # 尝试使用 'claude' 命令（让系统自动解析）
        print("\n尝试使用系统 PATH 中的 'claude' 命令...")
        claude_available, claude_path = check_claude_cli('claude')
        if not claude_available:
            # 询问是否要手动指定路径
            try:
                manual_path = input("\n是否要手动指定 claude 路径? (y/n, 默认: n): ").strip().lower()
                if manual_path == 'y':
                    claude_path = input("请输入 claude 可执行文件的完整路径: ").strip()
                    if claude_path and Path(claude_path).exists():
                        claude_available, claude_path = check_claude_cli(claude_path)
                        if not claude_available:
                            return 1
                    else:
                        print("[X] 指定的路径不存在")
                        return 1
                else:
                    return 1
            except (EOFError, KeyboardInterrupt):
                print("\n[X] 用户取消操作")
                return 1
    
    # 显示配置目录信息
    config_path = get_claude_config_path()
    print(f"\n[信息] Claude 配置文件: {config_path}")
    if config_path.exists():
        print(f"      (文件存在)")
    else:
        print(f"      (文件不存在，将在首次添加服务器时创建)")
    
    paths = get_paths()
    
    print("\n路径信息:")
    print(f"  Python: {paths['python_path']}")
    print(f"  服务器脚本: {paths['server_script']}")
    print(f"  配置文件: {paths['config_file']}")
    if claude_path:
        print(f"  Claude 命令: {claude_path}")
    print()
    
    # 验证文件存在
    if not paths['server_script'].exists():
        print(f"[X] 服务器脚本不存在: {paths['server_script']}")
        return 1
    
    if not paths['config_file'].exists():
        print(f"[X] 配置文件不存在: {paths['config_file']}")
        return 1
    
    # 询问 scope
    print("\n选择配置范围 (scope):")
    print("  local  - 仅当前项目可用（默认，存储在 ~/.claude.json 的项目路径下）")
    print("  project - 项目共享（存储在项目根目录的 .mcp.json）")
    print("  user   - 用户全局可用（跨所有项目，存储在 ~/.claude.json）")
    print()
    
    scope_input = input("请输入 scope [local/project/user] (默认: local): ").strip().lower()
    if not scope_input:
        scope_input = 'local'
    
    if scope_input not in ['local', 'project', 'user']:
        print(f"[X] 无效的 scope: {scope_input}")
        return 1
    
    # 询问服务器名称
    server_name = input("请输入服务器名称 (默认: memcontext): ").strip()
    if not server_name:
        server_name = 'memcontext'
    
    # 添加 MCP 服务器
    if add_mcp_server(paths, scope_input, server_name, claude_path):
        print("\n" + "=" * 60)
        print("配置完成！")
        print("=" * 60)
        
        # 列出服务器以确认
        list_mcp_servers(claude_path)
        
        print("\n下一步:")
        print("1. 在 Claude Code 中使用 /mcp 命令查看 MCP 服务器状态")
        print("2. 测试 MCP 工具:")
        print("   '请使用 Memcontext 添加一条记忆：我在 Claude Code 中使用 Python'")
        print("\n提示:")
        print("- 使用 'claude mcp list' 查看所有配置的服务器")
        print("- 使用 'claude mcp get memcontext' 查看服务器详情")
        print("- 使用 'claude mcp remove memcontext' 移除服务器")
        print(f"- 配置范围: {scope_input}")
        if scope_input == 'project':
            print(f"- 项目配置文件: {paths['project_root'] / '.mcp.json'}")
        elif scope_input == 'user':
            print(f"- 用户配置文件: {config_path}")
        else:
            print(f"- 本地配置文件: {config_path} (项目路径下)")
        
        return 0
    else:
        print("\n[X] 配置失败")
        print("\n故障排除:")
        print("1. 确保 Claude Code 已正确安装")
        print("2. 检查 Python 路径是否正确")
        print("3. 检查服务器脚本和配置文件是否存在")
        print("4. 尝试手动运行命令:")
        cmd = build_mcp_add_command(paths, scope_input, server_name, claude_path)
        print(f"   {' '.join(cmd)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
