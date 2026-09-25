@echo off
echo.
echo ============================================================
echo   APEX INTELLIGENCE - LOCAL SERVER
echo ============================================================
echo.
echo Installing dependencies...
python -m pip install -q -r requirements.txt
echo.
echo Starting server...
echo.
echo ============================================================
echo   SERVER RUNNING
echo ============================================================
echo.
echo API:  http://localhost:8000
echo Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.
echo ============================================================
echo.
python run.py
pause
