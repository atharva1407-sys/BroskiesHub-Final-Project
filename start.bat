@echo off
title Restaurant Billing App
echo Starting Restaurant Billing App...

:: Check if the virtual environment exists
if not exist "env\Scripts\activate.bat" (
    echo Error: Virtual environment 'env' not found!
    echo Please make sure the environment is set up properly.
    pause
    exit /b 1
)

:: Activate the virtual environment
call env\Scripts\activate.bat

:: Run the application
python app.py

:: Keep window open if app crashes or exits
echo.
echo Application closed.
pause
