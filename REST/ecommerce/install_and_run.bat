@echo off
echo ========================================
echo   E-Commerce Website Setup
echo ========================================
echo.

echo Step 1: Installing pip (if needed)...
python get-pip.py
echo.

echo Step 2: Installing Flask and Werkzeug...
python -m pip install Flask==3.0.0 Werkzeug==3.0.1
echo.

echo Step 3: Verifying installation...
python -c "import flask; import werkzeug; print('All dependencies installed successfully!')"
echo.

echo Step 4: Starting the application...
echo.
echo The application will start on: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.
cd ecommerce
python app.py

pause

@REM Made with Bob
