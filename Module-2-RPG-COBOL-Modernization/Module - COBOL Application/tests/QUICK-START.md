# COBOL Unit Testing Framework - Quick Start Guide

## 🚀 Getting Started

This guide will help you run the COBOL unit tests quickly.

## ✅ What's Implemented

- ✅ Test framework (TESTUTIL.CBL, TESTASSERT.CBL)
- ✅ Sample unit test (TEST-INITFILE.CBL)
- ✅ PowerShell automation script
- ✅ Directory structure

## 📋 Prerequisites

### Option 1: GnuCOBOL (Recommended for Testing)

**Windows:**
1. Download GnuCOBOL from: https://gnucobol.sourceforge.io/
2. Install the Windows version
3. Add to PATH

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install gnucobol

# Mac (using Homebrew)
brew install gnucobol
```

### Option 2: WSL (Windows Subsystem for Linux)

If you're on Windows and prefer Linux tools:
```bash
# In WSL terminal
sudo apt-get update
sudo apt-get install gnucobol
```

### Option 3: Docker (No Installation Required)

Use a pre-configured GnuCOBOL Docker image:
```bash
docker run -it --rm -v ${PWD}:/workspace gnucobol/gnucobol bash
```

## 🏃 Running Tests

### Method 1: Using PowerShell Script (Windows)

```powershell
# Navigate to tests directory
cd "Module-2-RPG-COBOL-Modernization/Module - COBOL Application/tests"

# Run the test script
.\scripts\run-unit-tests.ps1
```

### Method 2: Manual Compilation (Any Platform)

```bash
# Navigate to tests directory
cd "Module-2-RPG-COBOL-Modernization/Module - COBOL Application/tests"

# Compile framework components
cobc -c framework/TESTUTIL.CBL -o framework/TESTUTIL.o
cobc -c framework/TESTASSERT.CBL -o framework/TESTASSERT.o

# Compile and run test
cobc -x unit/TEST-INITFILE.CBL framework/TESTUTIL.o framework/TESTASSERT.o -o TEST-INITFILE
./TEST-INITFILE
```

## 📊 Expected Output

When you run the tests, you should see:

```
=========================================
Setting up test environment...
=========================================
✓ Test environment ready
 
=========================================
Running: TEST-INITFILE
=========================================
 
TEST-INIT-001: Create account file successfully
  ✓ INIT-001: Account file created with status 00
TEST-INIT-002: Create customer file successfully
  ✓ INIT-002: Customer file created with status 00
TEST-INIT-003: Verify initial balance is zero
  ✓ INIT-003: Initial balance should be zero
TEST-INIT-004: Verify account type is set
  ✓ INIT-004: Account type should be SA (Savings)
TEST-INIT-005: Verify file status is valid
  ✓ INIT-005: File status should be valid
 
=========================================
TEST SUMMARY
=========================================
Total Assertions: 00005
Passed: 00005
Failed: 00000
Status: ✓ ALL TESTS PASSED
=========================================
```

## 🔧 Troubleshooting

### Issue: "cobc: command not found"

**Solution:** GnuCOBOL is not installed or not in PATH.
- Install GnuCOBOL (see Prerequisites above)
- Add to PATH: `export PATH=$PATH:/path/to/gnucobol/bin`

### Issue: PowerShell script won't run

**Solution:** Enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📁 Project Structure

```
tests/
├── framework/              # Test framework components
│   ├── TESTUTIL.CBL       # Test utilities (✅ Implemented)
│   └── TESTASSERT.CBL     # Assertion library (✅ Implemented)
├── unit/                   # Unit tests
│   └── TEST-INITFILE.CBL  # INITFILE tests (✅ Implemented)
├── scripts/                # Automation scripts
│   └── run-unit-tests.ps1 # PowerShell runner (✅ Implemented)
├── reports/                # Test reports (auto-generated)
└── temp/                   # Temporary files (auto-generated)
```

## 🎯 Next Steps

1. Run the existing test to verify framework works
2. Add more test cases to TEST-INITFILE.CBL
3. Create TEST-ACCTDEMO.CBL for ACCTDEMO program
4. Create TEST-ACCTMGMT.CBL for ACCTMGMT program
5. Implement TESTDATA.CBL for test data generation

## 📚 Documentation

- [README.md](./README.md) - Complete framework documentation
- [COBOL-UNIT-TEST-PLAN.md](./COBOL-UNIT-TEST-PLAN.md) - Test plan
- [TEST-FRAMEWORK-ARCHITECTURE.md](./TEST-FRAMEWORK-ARCHITECTURE.md) - Architecture
- [IMPLEMENTATION-ROADMAP.md](./IMPLEMENTATION-ROADMAP.md) - Implementation guide

---

**Last Updated**: 2026-06-23  
**Status**: Framework Ready - Tests Can Be Run