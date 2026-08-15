$Host.UI.RawUI.WindowTitle = "Restaurant Billing App"
Write-Host "Starting Restaurant Billing App..." -ForegroundColor Green

# Check if the virtual environment exists
if (-Not (Test-Path "env\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment 'env' not found!" -ForegroundColor Red
    Write-Host "Please make sure the environment is set up properly." -ForegroundColor Yellow
    Pause
    exit
}

# Activate the virtual environment
& ".\env\Scripts\Activate.ps1"

# Run the application
python app.py

# Keep window open if app crashes or exits
Write-Host "`nApplication closed." -ForegroundColor Cyan
Pause
