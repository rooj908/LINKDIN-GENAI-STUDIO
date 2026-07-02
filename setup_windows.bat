@echo off
echo ===================================================
echo   LinkedIn GenAI Content Studio - Windows Setup
echo ===================================================

echo Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ===================================================
echo   Setup complete!
echo   To run the app:
echo     1. .venv\Scripts\activate
echo     2. python -m streamlit run app.py
echo ===================================================
pause
