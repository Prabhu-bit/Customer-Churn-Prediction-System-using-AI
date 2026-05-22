#!/usr/bin/env pwsh
# ========================================================================
# Customer Churn Prediction System - FastAPI Launcher (PowerShell)
# ========================================================================

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "    CUSTOMER CHURN PREDICTION SYSTEM - FastAPI REST API" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""

# Check if venv is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

# Navigate to the app directory
Set-Location 08_Applications_UI_API

Write-Host ""
Write-Host "Starting FastAPI server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Access Swagger docs at: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Access ReDoc at: http://localhost:8000/redoc" -ForegroundColor Green
Write-Host ""

# Launch FastAPI
python fastapi_server.py

Read-Host "Press Enter to exit"
