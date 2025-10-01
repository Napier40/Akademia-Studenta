@echo off
echo ========================================
echo Akademia Studenta - Starting Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist .venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Creating from .env.example...
    copy .env.example .env
    echo Please edit .env with your settings and run again.
    pause
    exit /b 1
)

REM Set Flask app
set FLASK_APP=app.py

echo Starting Flask application...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Run Flask
flask run

pause