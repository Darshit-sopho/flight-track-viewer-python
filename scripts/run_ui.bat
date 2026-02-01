@echo off
echo Starting Flight Track Viewer...
python -m ftv.ui

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to launch UI.
    pause
    exit /b 1
)