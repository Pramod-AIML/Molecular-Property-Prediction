Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "Launching Molecular Property Prediction & ADMET FastAPI REST Service..." -ForegroundColor Green
Write-Host "Swagger UI will open at: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "=========================================================================" -ForegroundColor Cyan

& ".\venv\Scripts\python.exe" -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload

