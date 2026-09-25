import sys
import subprocess
from pathlib import Path

# This is the exact one-click launcher for Windows.
# It installs dependencies and launches the app automatically.

APP_DIR = Path(__file__).resolve().parent

print("Installing Python dependencies...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(APP_DIR / 'requirements.txt')])
print("Dependencies installed.")

print("Launching Apex Intelligence...")
subprocess.check_call([sys.executable, str(APP_DIR / 'launch_app.py')])
