#!/usr/bin/env pwsh
# ========================================================================
# Customer Churn Prediction System - Streamlit Launcher (PowerShell)
# ========================================================================

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "    CUSTOMER CHURN PREDICTION SYSTEM - Streamlit Web App" -ForegroundColor Green
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
Write-Host "Starting Streamlit app..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the app at: http://localhost:8501" -ForegroundColor Green
Write-Host ""

# Launch Streamlit in the background so Enter can stop it cleanly
$streamlitProcess = Start-Process -FilePath "python" -ArgumentList @("-m", "streamlit", "run", "streamlit_app.py") -PassThru -WindowStyle Normal

function Stop-StreamlitPort {
    $netstatLines = netstat -ano -p tcp | Select-String ":8501"
    $pids = @($streamlitProcess.Id)
    foreach ($line in $netstatLines) {
        $parts = ($line.Line -split '\s+') | Where-Object { $_ }
        if ($parts.Count -ge 5 -and $parts[-1] -match '^[0-9]+$') {
            $pids += [int]$parts[-1]
        }
    }

    $pids = $pids | Sort-Object -Unique
    foreach ($pid in $pids) {
        Start-Process -FilePath taskkill -ArgumentList @("/PID", $pid, "/T", "/F") -WindowStyle Hidden -Wait | Out-Null
    }

    $deadline = (Get-Date).AddSeconds(8)
    while ((Get-Date) -lt $deadline) {
        if (-not (netstat -ano -p tcp | Select-String ":8501")) {
            return
        }
        Start-Sleep -Milliseconds 250
    }
}

try {
    Read-Host "Press Enter to stop the app"
}
finally {
    if ($streamlitProcess -and -not $streamlitProcess.HasExited) {
        Stop-StreamlitPort
    }
    Write-Host "Streamlit app stopped." -ForegroundColor Yellow
}
