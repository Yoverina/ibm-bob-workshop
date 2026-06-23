# PowerShell Script to Download Java 21
# Run this script as Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Java 21 Installation Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check current Java version
Write-Host "Current Java Version:" -ForegroundColor Yellow
try {
    java -version 2>&1 | Select-Object -First 3
} catch {
    Write-Host "Java not found or not in PATH" -ForegroundColor Red
}
Write-Host ""

# Java 21 Download URLs
$jdk21Url = "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe"
$downloadPath = "$env:TEMP\jdk-21_windows-x64_bin.exe"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Options:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Option 1: Download Oracle JDK 21 (Recommended)" -ForegroundColor Green
Write-Host "  - Official Oracle JDK"
Write-Host "  - Free for development use"
Write-Host "  - URL: https://www.oracle.com/java/technologies/downloads/#java21"
Write-Host ""
Write-Host "Option 2: Download OpenJDK 21 (Alternative)" -ForegroundColor Green  
Write-Host "  - Open source alternative"
Write-Host "  - URL: https://adoptium.net/temurin/releases/?version=21"
Write-Host ""
Write-Host "Option 3: Use Chocolatey Package Manager" -ForegroundColor Green
Write-Host "  - Command: choco install openjdk21"
Write-Host ""
Write-Host "Option 4: Use winget (Windows Package Manager)" -ForegroundColor Green
Write-Host "  - Command: winget install Microsoft.OpenJDK.21"
Write-Host ""

$choice = Read-Host "Would you like to download Oracle JDK 21 now? (y/n)"

if ($choice -eq 'y' -or $choice -eq 'Y') {
    Write-Host ""
    Write-Host "Downloading Java 21..." -ForegroundColor Yellow
    Write-Host "Download URL: $jdk21Url" -ForegroundColor Gray
    Write-Host "Saving to: $downloadPath" -ForegroundColor Gray
    Write-Host ""
    
    try {
        # Download Java 21 installer
        Invoke-WebRequest -Uri $jdk21Url -OutFile $downloadPath -UseBasicParsing
        
        Write-Host "Download completed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Run the installer: $downloadPath" -ForegroundColor White
        Write-Host "2. Follow the installation wizard" -ForegroundColor White
        Write-Host "3. Set JAVA_HOME environment variable" -ForegroundColor White
        Write-Host "4. Add Java to PATH" -ForegroundColor White
        Write-Host ""
        
        $install = Read-Host "Would you like to run the installer now? (y/n)"
        if ($install -eq 'y' -or $install -eq 'Y') {
            Write-Host "Launching installer..." -ForegroundColor Yellow
            Start-Process -FilePath $downloadPath -Wait
            
            Write-Host ""
            Write-Host "Installation complete!" -ForegroundColor Green
            Write-Host ""
            Write-Host "IMPORTANT: Set environment variables:" -ForegroundColor Yellow
            Write-Host "1. JAVA_HOME = C:\Program Files\Java\jdk-21" -ForegroundColor White
            Write-Host "2. Add to PATH: %JAVA_HOME%\bin" -ForegroundColor White
            Write-Host ""
            Write-Host "After setting environment variables, restart PowerShell and run:" -ForegroundColor Cyan
            Write-Host "  java -version" -ForegroundColor White
            Write-Host "  cd 'Module-1-Java-Modernization/Module-Java Application'" -ForegroundColor White
            Write-Host "  ./mvnw.cmd test" -ForegroundColor White
        }
    } catch {
        Write-Host "Error downloading Java 21: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please download manually from:" -ForegroundColor Yellow
        Write-Host "https://www.oracle.com/java/technologies/downloads/#java21" -ForegroundColor Cyan
    }
} else {
    Write-Host ""
    Write-Host "Manual Installation Steps:" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Visit: https://www.oracle.com/java/technologies/downloads/#java21" -ForegroundColor White
    Write-Host "2. Download: Windows x64 Installer" -ForegroundColor White
    Write-Host "3. Run the installer" -ForegroundColor White
    Write-Host "4. Set JAVA_HOME environment variable:" -ForegroundColor White
    Write-Host "   - Open System Properties > Environment Variables" -ForegroundColor Gray
    Write-Host "   - Add JAVA_HOME = C:\Program Files\Java\jdk-21" -ForegroundColor Gray
    Write-Host "   - Add to PATH: %JAVA_HOME%\bin" -ForegroundColor Gray
    Write-Host "5. Restart PowerShell" -ForegroundColor White
    Write-Host "6. Verify: java -version" -ForegroundColor White
    Write-Host "7. Run tests: ./mvnw.cmd test" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Quick Install with Package Managers:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Using Chocolatey:" -ForegroundColor Yellow
Write-Host "  choco install openjdk21" -ForegroundColor White
Write-Host ""
Write-Host "Using winget:" -ForegroundColor Yellow
Write-Host "  winget install Microsoft.OpenJDK.21" -ForegroundColor White
Write-Host ""
Write-Host "Using scoop:" -ForegroundColor Yellow
Write-Host "  scoop bucket add java" -ForegroundColor White
Write-Host "  scoop install openjdk21" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"

# Made with Bob
