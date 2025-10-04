@echo off
title AI Corporation - Production Deployment

echo.
echo ========================================
echo   AI CORPORATION - PRODUCTION LAUNCH
echo ========================================
echo.

echo 🚀 Starting AI Corporation Production System...
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo 💡 Please run: python -m venv .venv
    echo 💡 Then: .venv\Scripts\activate.bat
    echo 💡 Then: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check for environment variables
if "%DISCORD_BOT_TOKEN%"=="" (
    echo ⚠️ DISCORD_BOT_TOKEN not set - Discord bot will be skipped
)

if "%GITHUB_TOKEN%"=="" (
    echo ⚠️ GITHUB_TOKEN not set - Evolution system will be limited
)

echo.
echo 🎯 Launching AI Corporation Production System...
echo.

REM Run the production deployment
python deploy_production.py

echo.
echo 👋 AI Corporation shutdown complete.
pause