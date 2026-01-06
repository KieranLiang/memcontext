@echo off
chcp 65001 >nul
echo ========================================
echo 创建视频上传和检索工作流
echo ========================================
echo.

REM 切换到脚本所在目录
cd /d "%~dp0"

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

REM 检查 .env 文件（在项目根目录）
if not exist ..\.env (
    echo [警告] 未找到 .env 文件（在项目根目录）
    echo 将使用默认配置
    echo.
)

REM 运行脚本
python create_video_workflow.py

if errorlevel 1 (
    echo.
    echo [错误] 脚本执行失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 完成！
echo ========================================
pause

