@echo off
echo ======================================================================
echo  Starting Delhi Bus Traffic Model (Unified FastAPI + React Full-Stack)
echo  Interface: http://localhost:8000
echo  API Docs:  http://localhost:8000/docs
echo ======================================================================

if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe server.py
) else (
    python server.py
)
pause

