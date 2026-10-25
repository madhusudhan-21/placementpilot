@echo off
echo ===================================================
echo Starting PlacementPilot Web Application...
echo ===================================================
cd /d "%~dp0"
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    python app.py
) else (
    echo Error: Virtual environment (.venv) not found!
    echo Please create it using: python -m venv .venv
    pause
)
