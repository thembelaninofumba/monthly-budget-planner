@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Set up the Python environment first using the README instructions.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" -m streamlit run app.py
if errorlevel 1 pause
