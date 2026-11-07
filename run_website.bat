@echo off
echo =========================================================================
echo Launching Molecular Property Prediction & ADMET Real-Time Web Platform...
echo Developer: M. Pramod (24BAI1417)
echo Website will open at: http://localhost:8000
echo Swagger API Docs at:  http://localhost:8000/docs
echo =========================================================================
.\venv\Scripts\python.exe -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
pause
