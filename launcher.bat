@echo off
REM ========================================================================
REM ONE-COMMAND LAUNCHER - Customer Churn Prediction System
REM Just run: launcher.bat
REM ========================================================================

cd /d %~dp0
for /f %%i in ('powershell -NoProfile -Command "$p = Start-Process -PassThru python -ArgumentList ''-m streamlit run 08_Applications_UI_API\streamlit_app.py --server.headless false --browser.serverAddress localhost --logger.level=error''; $p.Id"') do set STREAMLIT_PID=%%i
echo.
set /p STOP_APP=Press Enter to stop the app...
powershell -NoProfile -Command "$pids = @(%STREAMLIT_PID%); $netstat = netstat -ano -p tcp | Select-String ':8501'; foreach ($line in $netstat) { $parts = ($line.Line -split '\s+') | Where-Object { $_ }; if ($parts.Count -ge 5 -and $parts[-1] -match '^[0-9]+$') { $pids += [int]$parts[-1] } }; $pids = $pids | Sort-Object -Unique; foreach ($pid in $pids) { taskkill /f /t /pid $pid >$null 2>$null }"
pause
