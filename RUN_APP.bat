@echo off
REM DOE Simulator Launcher
REM This script launches the Streamlit application

echo Launching DOE Simulator...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Install dependencies only on first run (check if streamlit is installed)
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies for the first time...
    echo This may take a moment...
    echo.
    python -m pip install -q -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Error: Failed to install dependencies
        echo Please run: python -m pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM Launch Streamlit
echo Starting application...
echo Your browser should open automatically. If not, visit http://localhost:8501
echo.
python -m streamlit run app.py

pause
