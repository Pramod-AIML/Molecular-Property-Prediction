Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Starting Molecular Property Prediction Dashboard..." -ForegroundColor Green
Write-Host "Developer: M. Pramod (24BAI1417)" -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Cyan

& ".\venv\Scripts\python.exe" -m streamlit run app.py

