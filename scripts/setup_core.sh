#!/bin/bash

# Flight Track Viewer - Core Installation (Linux/Mac)
# Installs only core dependencies without UI

echo "========================================="
echo "Flight Track Viewer - Core Setup"
echo "(without UI)"
echo "========================================="
echo ""

# Check Python version
echo "[1/2] Checking Python installation..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    echo "[OK] Python $python_version found"
else
    echo "[ERROR] Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi
echo ""

# Install the package without UI dependencies
echo "[2/2] Installing Flight Track Viewer (core only)..."
echo "This may take a minute..."
echo ""
pip install -e .

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Installation failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "[OK] Core installation complete!"
echo ""
echo "You can now use the ftv package programmatically:"
echo "  from ftv import run"
echo "  result = run()"
echo ""
echo "To install UI support later, run:"
echo "  pip install -e \".[ui]\""
echo ""
