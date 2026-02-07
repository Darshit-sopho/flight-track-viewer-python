#!/usr/bin/env python3
"""
Run the Flight Track Analyzer backend server
"""

import uvicorn
from src.main import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )