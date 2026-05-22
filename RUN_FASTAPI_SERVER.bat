@echo off
REM ========================================================================
REM Customer Churn Prediction System - FastAPI Launcher
REM ========================================================================

echo.
echo ========================================================================
echo    CUSTOMER CHURN PREDICTION SYSTEM - FastAPI REST API
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
echo Starting FastAPI server...
echo.
echo Access Swagger docs at: http://localhost:8000/docs
echo Access ReDoc at: http://localhost:8000/redoc
echo.

REM Launch FastAPI
python fastapi_server.py

pause
