#!/bin/bash

# Flight Track Viewer - Setup Script with UI (Linux/Mac)

echo "========================================="
echo "Flight Track Viewer - Setup (with UI)"
echo "========================================="
echo ""

# Check Python version
echo "[1/3] Checking Python installation..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    echo "[OK] Python $python_version found"
else
    echo "[ERROR] Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi
echo ""

# Install the package with UI dependencies
echo "[2/3] Installing Flight Track Viewer with UI support..."
echo "This may take a minute..."
echo ""
pip install -e ".[ui]"

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Installation failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "[OK] Installation complete!"
echo ""

# Launch the UI
echo "[3/3] Launching Flight Track Viewer UI..."
echo ""
python3 -m ftv.ui.app

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to launch UI."
    exit 1
fi
