#!/bin/bash
echo "Starting Flight Track Viewer..."
python3 -m ftv.ui

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to launch UI."
    exit 1
fi