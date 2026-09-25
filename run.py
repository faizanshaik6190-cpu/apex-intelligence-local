# Apex Intelligence
# Simple local server initialization

import sys
import subprocess
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("  APEX INTELLIGENCE - LOCAL SERVER")
    print("="*60 + "\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print("✅ Python version OK\n")
    
    # Install requirements
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("✅ Dependencies installed\n")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Import and run the app
    print("🚀 Starting local server...\n")
    
    try:
        from app.main import app
        import uvicorn
        
        print("="*60)
        print("  SERVER RUNNING")
        print("="*60)
        print("\n📍 API: http://localhost:8000")
        print("📖 Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop\n")
        print("="*60 + "\n")
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
