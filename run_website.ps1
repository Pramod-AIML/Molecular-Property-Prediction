Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "Launching Molecular Property Prediction & ADMET Real-Time Web Platform..." -ForegroundColor Green
Write-Host "Developer: M. Pramod (24BAI1417)" -ForegroundColor Yellow
Write-Host "Website will open at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Swagger API Docs at:  http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "=========================================================================" -ForegroundColor Cyan

& ".\venv\Scripts\python.exe" -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload

