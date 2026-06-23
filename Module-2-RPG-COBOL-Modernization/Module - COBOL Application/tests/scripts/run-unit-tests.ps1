# COBOL Unit Test Runner (PowerShell)
# Compiles and runs COBOL unit tests

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "COBOL UNIT TEST RUNNER" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Set paths
$TestDir = Split-Path -Parent $PSScriptRoot
$FrameworkDir = Join-Path $TestDir "framework"
$UnitDir = Join-Path $TestDir "unit"
$ReportsDir = Join-Path $TestDir "reports"

# Create reports directory if it doesn't exist
if (-not (Test-Path $ReportsDir)) {
    New-Item -ItemType Directory -Path $ReportsDir | Out-Null
}

# Check if GnuCOBOL is installed
Write-Host "Checking for GnuCOBOL..." -ForegroundColor Yellow
$cobc = Get-Command cobc -ErrorAction SilentlyContinue
if (-not $cobc) {
    Write-Host "ERROR: GnuCOBOL (cobc) not found!" -ForegroundColor Red
    Write-Host "Please install GnuCOBOL from: https://gnucobol.sourceforge.io/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "For Windows, you can:" -ForegroundColor Yellow
    Write-Host "1. Download GnuCOBOL Windows installer" -ForegroundColor Yellow
    Write-Host "2. Or use WSL (Windows Subsystem for Linux)" -ForegroundColor Yellow
    Write-Host "3. Or use Docker with GnuCOBOL image" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "ALTERNATIVE: Run tests manually with:" -ForegroundColor Cyan
    Write-Host "  cobc -x -I../copybooks framework/TESTUTIL.CBL framework/TESTASSERT.CBL unit/TEST-INITFILE.CBL -o TEST-INITFILE" -ForegroundColor Gray
    Write-Host "  ./TEST-INITFILE" -ForegroundColor Gray
    exit 1
}

Write-Host "✓ GnuCOBOL found: $($cobc.Source)" -ForegroundColor Green
Write-Host ""

# Compile framework components
Write-Host "Compiling test framework..." -ForegroundColor Yellow

Write-Host "  - Compiling TESTUTIL.CBL..." -ForegroundColor Gray
$testutil = Join-Path $FrameworkDir "TESTUTIL.CBL"
$testutilObj = Join-Path $FrameworkDir "TESTUTIL.o"
& cobc -c $testutil -o $testutilObj 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "    ✗ Failed to compile TESTUTIL.CBL" -ForegroundColor Red
    exit 1
}
Write-Host "    ✓ TESTUTIL.CBL compiled" -ForegroundColor Green

Write-Host "  - Compiling TESTASSERT.CBL..." -ForegroundColor Gray
$testassert = Join-Path $FrameworkDir "TESTASSERT.CBL"
$testassertObj = Join-Path $FrameworkDir "TESTASSERT.o"
& cobc -c $testassert -o $testassertObj 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "    ✗ Failed to compile TESTASSERT.CBL" -ForegroundColor Red
    exit 1
}
Write-Host "    ✓ TESTASSERT.CBL compiled" -ForegroundColor Green

Write-Host ""

# Compile and run unit tests
Write-Host "Running unit tests..." -ForegroundColor Yellow
Write-Host ""

$testFiles = Get-ChildItem -Path $UnitDir -Filter "TEST-*.CBL"
$totalTests = $testFiles.Count
$passedTests = 0
$failedTests = 0

foreach ($testFile in $testFiles) {
    $testName = $testFile.BaseName
    $testPath = $testFile.FullName
    $testExe = Join-Path $UnitDir $testName
    
    Write-Host "Compiling $testName..." -ForegroundColor Cyan
    
    # Compile test
    & cobc -x $testPath $testutilObj $testassertObj -o $testExe 2>&1 | Out-Null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ✗ Compilation failed for $testName" -ForegroundColor Red
        $failedTests++
        continue
    }
    
    Write-Host "  ✓ Compiled successfully" -ForegroundColor Green
    Write-Host ""
    
    # Run test
    Write-Host "Executing $testName..." -ForegroundColor Cyan
    & $testExe
    
    if ($LASTEXITCODE -eq 0) {
        $passedTests++
    } else {
        $failedTests++
    }
    
    Write-Host ""
}

# Summary
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "TEST EXECUTION SUMMARY" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Total Test Suites: $totalTests" -ForegroundColor White
Write-Host "Passed: $passedTests" -ForegroundColor Green
Write-Host "Failed: $failedTests" -ForegroundColor $(if ($failedTests -gt 0) { "Red" } else { "Green" })

if ($failedTests -eq 0) {
    Write-Host "Status: ✓ ALL TESTS PASSED" -ForegroundColor Green
} else {
    Write-Host "Status: ✗ SOME TESTS FAILED" -ForegroundColor Red
}
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Save results to file
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportFile = Join-Path $ReportsDir "test-results-$timestamp.txt"
@"
COBOL Unit Test Results
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
========================================
Total Test Suites: $totalTests
Passed: $passedTests
Failed: $failedTests
Status: $(if ($failedTests -eq 0) { "PASSED" } else { "FAILED" })
========================================
"@ | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "Results saved to: $reportFile" -ForegroundColor Gray
Write-Host ""

# Exit with appropriate code
exit $(if ($failedTests -eq 0) { 0 } else { 1 })

# Made with Bob
