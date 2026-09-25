# Apex Intelligence Local App
# This project is a simple local-only Python server over SQLite.
# No Docker. No external database.

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Keep the app extremely simple and local-only.
# This project intentionally avoids Docker deployment.
