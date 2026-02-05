@echo off
REM Flight Track Viewer - Setup Script with UI (Windows)

echo =========================================
echo Flight Track Viewer - Setup (with UI)
echo =========================================
echo.

REM Check Python version
echo [1/3] Checking Python installation...
python --version 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Install the package with UI dependencies
echo [2/3] Installing Flight Track Viewer with UI support...
echo This may take a minute...
echo.
pip install -e ".[ui]"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo [OK] Installation complete!
echo.

REM Launch the UI
echo [3/3] Launching Flight Track Viewer UI...
echo.
python -m ftv.ui.app

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to launch UI.
    pause
    exit /b 1
)
