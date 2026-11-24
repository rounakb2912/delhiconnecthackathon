#!/bin/bash
echo "======================================================================"
echo " Starting Delhi Bus Traffic Model (Unified FastAPI + React Full-Stack)"
echo " Interface: http://localhost:8000"
echo " API Docs:  http://localhost:8000/docs"
echo "======================================================================"

if [ -f ".venv/bin/python" ]; then
    .venv/bin/python server.py
elif [ -f ".venv/Scripts/python.exe" ]; then
    .venv/Scripts/python.exe server.py
else
    python server.py
fi

