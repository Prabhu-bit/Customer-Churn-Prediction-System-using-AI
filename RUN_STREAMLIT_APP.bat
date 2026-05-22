@echo off
REM ========================================================================
REM Customer Churn Prediction System - Streamlit Launcher
REM ========================================================================

echo.
echo ========================================================================
echo    CUSTOMER CHURN PREDICTION SYSTEM - Streamlit Web App
echo ========================================================================
echo.

REM Check if venv is activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Navigate to the app directory
cd 08_Applications_UI_API

echo.
echo Starting Streamlit app...
echo.
echo Access the app at: http://localhost:8501
echo.

REM Launch Streamlit
for /f %%i in ('powershell -NoProfile -Command "$p = Start-Process -PassThru python -ArgumentList ''-m streamlit run streamlit_app.py''; $p.Id"') do set STREAMLIT_PID=%%i

echo.
set /p STOP_APP=Press Enter to stop the app...
powershell -NoProfile -Command "$pids = @(%STREAMLIT_PID%); $netstat = netstat -ano -p tcp | Select-String ':8501'; foreach ($line in $netstat) { $parts = ($line.Line -split '\s+') | Where-Object { $_ }; if ($parts.Count -ge 5 -and $parts[-1] -match '^[0-9]+$') { $pids += [int]$parts[-1] } }; $pids = $pids | Sort-Object -Unique; foreach ($pid in $pids) { taskkill /f /t /pid $pid >$null 2>$null }"

pause
