@echo off
REM Flight Track Viewer - Core Installation (Windows)
REM Installs only core dependencies without UI

echo =========================================
echo Flight Track Viewer - Core Setup
echo (without UI)
echo =========================================
echo.

REM Check Python version
echo [1/2] Checking Python installation...
python --version 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Install the package without UI dependencies
echo [2/2] Installing Flight Track Viewer (core only)...
echo This may take a minute...
echo.
pip install -e .

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo [OK] Core installation complete!
echo.
echo You can now use the ftv package programmatically:
echo   from ftv import run
echo   result = run()
echo.
echo To install UI support later, run:
echo   pip install -e ".[ui]"
echo.
pause
