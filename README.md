# Apex Intelligence Local Server

This is a simple local-only server version of Apex Intelligence.

## No Docker. No External Services. Just Python.

### Quick Start

1. Install Python 3.8+
   https://www.python.org/downloads/

2. Open the folder in PowerShell (Windows) or Terminal (Mac/Linux)

3. Run:

**Windows:**
```powershell
python -m pip install -r requirements.txt
python run.py
```

**Mac/Linux:**
```bash
python3 -m pip install -r requirements.txt
python3 run.py
```

4. Open in browser:
   http://localhost:8000/docs

### That's All

The server will run locally. Open your browser. Start using the API.

### What You Get

- Lead generation
- Deal negotiation workflow
- Growth audit creation
- Delivery planning
- Customer support
- CEO summary
- All approval gates

### API Endpoints

Once running, visit: http://localhost:8000/docs

You'll see all available endpoints and can test them directly.

### Example Commands

**Generate leads:**
```bash
curl -X POST http://localhost:8000/leads/generate -H "Content-Type: application/json" -d '{"city":"Austin, TX","category":"dental","limit":5}'
```

**Get CEO summary:**
```bash
curl http://localhost:8000/ceo/summary
```

**List all leads:**
```bash
curl http://localhost:8000/leads
```

### Database

Data is stored in `apex_intelligence.db` (SQLite)

Automatically created on first run.

### Stop the Server

Press `Ctrl+C` in the terminal

### That's It

No Docker. No Postgres. No Redis. No Celery.

Just a simple local Python server.
