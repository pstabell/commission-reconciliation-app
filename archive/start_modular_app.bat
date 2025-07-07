@echo off
echo ========================================
echo  Sales Commission Tracker - Modular
echo  Starting Bulletproof Modular Version
echo ========================================

:: Check if we're in the right directory
if not exist "commission_app_modular.py" (
    echo ERROR: commission_app_modular.py not found!
    echo Please run this script from the app directory.
    pause
    exit /b 1
)

:: Check if pages directory exists
if not exist "pages" (
    echo ERROR: pages directory not found!
    echo Please ensure the modular architecture is properly set up.
    pause
    exit /b 1
)

:: Check if utils directory exists
if not exist "utils" (
    echo ERROR: utils directory not found!
    echo Please ensure the modular architecture is properly set up.
    pause
    exit /b 1
)

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and add it to your PATH
    pause
    exit /b 1
)

echo Checking Streamlit installation...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Streamlit is not installed
    echo Installing Streamlit...
    pip install streamlit
    if errorlevel 1 (
        echo ERROR: Failed to install Streamlit
        pause
        exit /b 1
    )
)

echo.
echo Starting Modular Commission App...
echo.
echo The app will open in your default web browser.
echo To stop the app, press Ctrl+C in this window.
echo.

:: Start the Streamlit app
streamlit run commission_app_modular.py

echo.
echo App stopped.
pause