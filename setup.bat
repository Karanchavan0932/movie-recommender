@echo off
echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Setup complete! 
echo.
echo To run the app:
echo   1. Activate the environment: venv\Scripts\activate.bat
echo   2. Run the app: streamlit run app.py
echo.
pause
