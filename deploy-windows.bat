@echo off
echo 🚀 Loan AI System - Windows Deployment Script
echo =====================================

echo.
echo 📋 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

echo 📦 Installing dependencies...
cd /d "%~dp0"
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

echo 🔧 Starting Loan AI System...
echo 🌐 Application will be available at: http://localhost:5000
echo 📊 Health check at: http://localhost:5000/health
echo.
echo 🛑 Press Ctrl+C to stop the server
echo =====================================

cd backend
python app.py

pause
