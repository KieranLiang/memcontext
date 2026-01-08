@echo off
chcp 65001 >nul
echo ========================================
echo Create Video Upload and Retrieval Workflow
echo ========================================
echo.

REM Switch to script directory
cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found, please install Python first
    pause
    exit /b 1
)

REM Check .env file (in project root directory)
if not exist ..\.env (
    echo [WARNING] .env file not found (in project root directory)
    echo Will use default configuration
    echo.
)

REM Run script
python create_video_workflow.py

if errorlevel 1 (
    echo.
    echo [ERROR] Script execution failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Done!
echo ========================================
pause

