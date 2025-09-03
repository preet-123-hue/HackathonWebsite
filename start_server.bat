@echo off
echo ========================================
echo Starting Jharkhand Tourism Backend
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python first.
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask server...
echo Server will run on: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app_supabase.py

echo.
echo Server stopped.
pause