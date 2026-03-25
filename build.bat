@echo off
REM Build script for DOE Simulator executable
REM This will create a standalone .exe file

echo ================================
echo DOE Simulator Build Script
echo ================================
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)

echo.
echo Building executable...
echo This may take a few minutes...
echo.

REM Run PyInstaller with the spec file
pyinstaller doe_simulator.spec --distpath .\dist --workpath .\build

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ================================
echo Build Complete!
echo ================================
echo.
echo Executable created at:
echo   .\dist\DOE_Simulator.exe
echo.
echo To run the application:
echo   .\dist\DOE_Simulator.exe
echo.
echo Or double-click dist\DOE_Simulator.exe
echo.
pause
