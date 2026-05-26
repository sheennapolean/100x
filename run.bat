@echo off
title Streamlit App Launcher

REM ============================================
REM Create virtual environment if it doesn't exist
REM ============================================

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM ============================================
REM Activate virtual environment
REM ============================================

call venv\Scripts\activate

REM ============================================
REM Upgrade pip
REM ============================================

echo Upgrading pip...
python -m pip install --upgrade pip

REM ============================================
REM Install requirements
REM ============================================

if exist requirements.txt (
    echo Installing requirements...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found!
    pause
    exit /b
)

REM ============================================
REM Launch Streamlit app
REM ============================================

if exist streamlit_app.py (
    echo Launching Streamlit app...
    streamlit run streamlit_app.py
) else (
    echo streamlit_app.py not found!
)

pause