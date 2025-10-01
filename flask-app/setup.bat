@echo off
echo ========================================
echo Akademia Studenta - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.12 from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Detected Python version: %PYTHON_VERSION%
echo.

REM Warn about Python 3.13
echo %PYTHON_VERSION% | findstr /C:"3.13" >nul
if not errorlevel 1 (
    echo WARNING: You are using Python 3.13
    echo Some packages may have compatibility issues.
    echo We recommend using Python 3.12 for best compatibility.
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit...
    pause >nul
)

echo Step 1: Creating virtual environment...
if exist .venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)
echo.

echo Step 2: Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Try running: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check the error messages above
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo Step 5: Setting up environment file...
if exist .env (
    echo .env file already exists. Skipping...
) else (
    copy .env.example .env
    echo .env file created. Please edit it with your settings.
)
echo.

echo Step 6: Initializing database...
set FLASK_APP=app.py
flask init-db
if errorlevel 1 (
    echo ERROR: Failed to initialize database
    pause
    exit /b 1
)
echo Database initialized!
echo.

echo Step 7: Compiling translations...
pybabel compile -d translations
if errorlevel 1 (
    echo WARNING: Failed to compile translations
    echo Installing Babel...
    pip install Babel
    pybabel compile -d translations
)
echo Translations compiled!
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the application:
echo   1. Make sure virtual environment is activated: .venv\Scripts\activate
echo   2. Run: flask run
echo   3. Open browser: http://localhost:5000
echo.
echo For more information, see WINDOWS_SETUP.md
echo.
pause