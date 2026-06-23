@echo off
echo ========================================
echo E-Commerce Load Testing with Locust
echo ========================================
echo.

REM Check if the app is running
echo Checking if Flask app is running on port 5000...
netstat -ano | findstr :5000 >nul
if %errorlevel% equ 0 (
    echo [OK] Flask app is running on port 5000
) else (
    echo [WARNING] Flask app is NOT running on port 5000
    echo Please start the app first using run.bat
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Select Load Test Type:
echo ========================================
echo 1. Quick Test (Web UI - 10 users, 2 users/sec spawn rate)
echo 2. Standard Test (Web UI - 50 users, 5 users/sec spawn rate)
echo 3. Stress Test (Web UI - 100 users, 10 users/sec spawn rate)
echo 4. Headless Quick Test (CLI - 10 users, 30 seconds)
echo 5. Headless Standard Test (CLI - 50 users, 60 seconds)
echo 6. Custom Test (Web UI - specify your own parameters)
echo ========================================
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto quick_test
if "%choice%"=="2" goto standard_test
if "%choice%"=="3" goto stress_test
if "%choice%"=="4" goto headless_quick
if "%choice%"=="5" goto headless_standard
if "%choice%"=="6" goto custom_test

echo Invalid choice. Exiting...
pause
exit /b 1

:quick_test
echo.
echo Starting Quick Load Test (Web UI)...
echo Open http://localhost:8089 in your browser
echo Suggested: 10 users, 2 users/sec spawn rate
echo.
locust -f locustfile.py --host=http://127.0.0.1:5000
goto end

:standard_test
echo.
echo Starting Standard Load Test (Web UI)...
echo Open http://localhost:8089 in your browser
echo Suggested: 50 users, 5 users/sec spawn rate
echo.
locust -f locustfile.py --host=http://127.0.0.1:5000
goto end

:stress_test
echo.
echo Starting Stress Test (Web UI)...
echo Open http://localhost:8089 in your browser
echo Suggested: 100 users, 10 users/sec spawn rate
echo.
locust -f locustfile.py --host=http://127.0.0.1:5000 --users=100 --spawn-rate=10
goto end

:headless_quick
echo.
echo Starting Headless Quick Test...
echo 10 users, 2 users/sec spawn rate, 30 seconds duration
echo.
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=10 --spawn-rate=2 --run-time=30s --html=load_test_report_quick.html
echo.
echo Test completed! Report saved to: load_test_report_quick.html
start load_test_report_quick.html
goto end

:headless_standard
echo.
echo Starting Headless Standard Test...
echo 50 users, 5 users/sec spawn rate, 60 seconds duration
echo.
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=50 --spawn-rate=5 --run-time=60s --html=load_test_report_standard.html
echo.
echo Test completed! Report saved to: load_test_report_standard.html
start load_test_report_standard.html
goto end

:custom_test
echo.
echo Starting Custom Load Test (Web UI)...
echo Open http://localhost:8089 in your browser
echo You can specify your own parameters there
echo.
locust -f locustfile.py --host=http://127.0.0.1:5000
goto end

:end
echo.
echo ========================================
echo Load Test Session Ended
echo ========================================
pause

@REM Made with Bob
