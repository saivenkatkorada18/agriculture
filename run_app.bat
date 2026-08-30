@echo off
echo Starting Soil & Crop Health Analyzer...
start cmd /k "python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"
start cmd /k "cd frontend && npm run dev"
echo Backend running on http://127.0.0.1:8000
echo Frontend running on http://localhost:3000
