@echo off
cd /d %~dp0
echo Starting FastAPI server on port 8002...
python -m uvicorn main:app --host 127.0.0.1 --port 8002 --reload
