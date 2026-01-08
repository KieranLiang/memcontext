@echo off
chcp 65001 >nul
REM Run n8n in Docker, mount local memcontext-n8n directory
REM This allows n8n in Docker to access the local memcontext-n8n folder

echo Checking Docker status...
docker ps >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Docker Desktop is not running!
    echo.
    echo Please start Docker Desktop first:
    echo 1. Press Win key, search for "Docker Desktop" and start it
    echo 2. Or run: start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo 3. Wait for Docker Desktop to fully start, then run this script again
    echo.
    pause
    exit /b 1
)

echo Docker is running normally!
echo.

REM Check if port 5678 is already in use
netstat -ano | findstr :5678 >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 5678 is already in use!
    echo.
    echo Checking if n8n container is running...
    docker ps -a --filter "name=n8n" --format "{{.Names}}" | findstr n8n >nul 2>&1
    if not errorlevel 1 (
        echo Found n8n container, stopping and removing...
        docker stop n8n >nul 2>&1
        docker rm n8n >nul 2>&1
        echo Old container cleaned up, waiting 2 seconds...
        timeout /t 2 /nobreak >nul
    ) else (
        echo n8n container not found, another program may be using port 5678
        echo Please manually stop the program using the port, or modify the script to use a different port
        echo.
        pause
        exit /b 1
    )
)

echo Starting n8n Docker container...
echo.
echo ========================================
echo Mount Configuration:
echo ========================================
echo Local path: %CD%\memcontext-n8n
echo Container path: /home/node/memcontext-n8n
echo.
echo Notes:
echo - Container port: 5678 (n8n Web UI)
echo - Local memcontext-n8n directory is mounted to /home/node/memcontext-n8n in container
echo - Container can access local memcontext-n8n service via host.docker.internal:5019
echo ========================================
echo.

docker run -it --rm ^
  --name n8n ^
  -p 5678:5678 ^
  -v "%CD%\memcontext-n8n":/home/node/memcontext-n8n ^
  -e N8N_BASIC_AUTH_ACTIVE=true ^
  -e N8N_BASIC_AUTH_USER=admin ^
  -e N8N_BASIC_AUTH_PASSWORD=admin ^
  -e NODE_ENV=production ^
  n8nio/n8n

pause

