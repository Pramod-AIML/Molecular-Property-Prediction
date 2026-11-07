@echo off
echo =========================================================================
echo Launching Molecular Property Prediction & ADMET FastAPI REST Service...
echo Swagger UI will open at: http://localhost:8000/docs
echo =========================================================================

.\venv\Scripts\python.exe -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
pause
