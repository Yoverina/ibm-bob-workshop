@echo off
REM GnuCOBOL Installation Script for Windows
REM Run this file as Administrator

echo =========================================
echo GnuCOBOL Installation Script
echo =========================================
echo.

echo Checking if Chocolatey is installed...
where choco >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Chocolatey not found. Installing Chocolatey...
    echo.
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
    
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to install Chocolatey
        echo Please run this script as Administrator
        pause
        exit /b 1
    )
    
    echo Chocolatey installed successfully!
    echo.
    echo Please close this window and run the script again to install GnuCOBOL
    pause
    exit /b 0
) else (
    echo Chocolatey is already installed
    echo.
)

echo Installing GnuCOBOL...
choco install gnucobol -y

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install GnuCOBOL
    pause
    exit /b 1
)

echo.
echo =========================================
echo Installation Complete!
echo =========================================
echo.
echo Verifying installation...
cobc --version

if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS: GnuCOBOL is installed and ready to use!
    echo You can now run COBOL tests.
) else (
    echo.
    echo WARNING: GnuCOBOL may require a system restart
    echo Please restart your computer and try running: cobc --version
)

echo.
pause

@REM Made with Bob
