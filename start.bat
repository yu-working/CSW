@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\activate" (
    echo [ERROR] cannot find .venv
    pause
    exit /b
)

call ".venv\Scripts\activate"

set DATA_FOLDER=data
set DEFAULT_DATA_FILE=default_data/FAQ_Default.xlsx

streamlit run app.py

pause
