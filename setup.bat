@echo off
title Setup Restaurant Billing App
echo Setting up Restaurant Billing App for the first time...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not added to your PATH.
    echo Please install Python 3.8 or newer from https://www.python.org/
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "env\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv env
)

:: Activate the virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat

:: Install requirements
echo.
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Setup Complete!
echo You can now use "start.bat" to run the application anytime.
pause
