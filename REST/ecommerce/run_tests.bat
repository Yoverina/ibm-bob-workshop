@echo off
echo ========================================
echo Running E-Commerce Unit Tests
echo ========================================
echo.

REM Check if pytest is installed
python -c "import pytest" 2>nul
if errorlevel 1 (
    echo Installing test dependencies...
    pip install -r requirements.txt
    echo.
)

echo Running tests with coverage report...
echo.
pytest test_app.py -v --cov=app --cov-report=html --cov-report=term

echo.
echo ========================================
echo Test Results Summary
echo ========================================
echo.
echo HTML Coverage Report: htmlcov\index.html
echo.
echo To view the HTML report, run:
echo start htmlcov\index.html
echo.
pause

@REM Made with Bob
