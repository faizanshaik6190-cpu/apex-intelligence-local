from pathlib import Path
import os
import sys
import subprocess

# Simple launcher for the local Apex Intelligence app.
# This file is intended to be used with Python and pip install.

APP_DIR = Path(__file__).resolve().parent

try:
    import PyQt6
    import requests
    import fastapi
except Exception:
    print("Installing app dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(APP_DIR / 'requirements.txt')])
    print("Dependencies installed. Please rerun the app.")
    input("Press Enter to exit...")
    sys.exit(0)

print("Launching Apex Intelligence...")
try:
    from app.main import app
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
except Exception as e:
    print(f"Startup failed: {e}")
    input("Press Enter to exit...")
