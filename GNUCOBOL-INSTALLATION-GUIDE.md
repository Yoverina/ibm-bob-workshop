# GnuCOBOL Installation Guide for Windows

## 📋 Quick Installation

I've created an installation script for you: **`install-gnucobol.cmd`**

### How to Run the Script:

1. **Right-click** on `install-gnucobol.cmd`
2. Select **"Run as administrator"**
3. Follow the on-screen instructions
4. The script will:
   - Install Chocolatey (if not already installed)
   - Install GnuCOBOL
   - Verify the installation

---

## 🔧 Manual Installation (Alternative)

### Option 1: Using Chocolatey (Recommended)

**Step 1: Install Chocolatey**
1. Open **Command Prompt as Administrator**
2. Run:
```cmd
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
```

**Step 2: Install GnuCOBOL**
3. Close and reopen Command Prompt as Administrator
4. Run:
```cmd
choco install gnucobol -y
```

**Step 3: Verify Installation**
```cmd
cobc --version
```

---

### Option 2: Direct Download (No Chocolatey)

1. Visit: https://sourceforge.net/projects/gnucobol/files/gnucobol/3.2/
2. Download: `GnuCOBOL_3.2_vs_bin.exe`
3. Run the installer
4. Follow the installation wizard
5. Ensure "Add to PATH" is checked during installation

---

### Option 3: Using Windows Subsystem for Linux (WSL)

If you have WSL installed:

```bash
sudo apt-get update
sudo apt-get install gnucobol -y
```

Then verify:
```bash
cobc --version
```

---

## ✅ After Installation

Once GnuCOBOL is installed, you can run the COBOL unit tests:

### Running Tests:

**PowerShell:**
```powershell
cd "Module-2-RPG-COBOL-Modernization/Module - COBOL Application/tests"
.\scripts\run-unit-tests.ps1
```

**Manual (CMD):**
```cmd
cd "Module-2-RPG-COBOL-Modernization\Module - COBOL Application\tests"

REM Compile framework
cobc -c framework\TESTUTIL.CBL -o framework\TESTUTIL.o
cobc -c framework\TESTASSERT.CBL -o framework\TESTASSERT.o

REM Compile and run test
cobc -x unit\TEST-INITFILE.CBL framework\TESTUTIL.o framework\TESTASSERT.o -o TEST-INITFILE
TEST-INITFILE.exe
```

---

## 🔍 Troubleshooting

### Issue: "cobc: command not found"

**Solution 1:** Restart your terminal/command prompt after installation

**Solution 2:** Add GnuCOBOL to PATH manually:
1. Search for "Environment Variables" in Windows
2. Edit "Path" under System Variables
3. Add: `C:\Program Files\GnuCOBOL\bin` (or your installation path)
4. Click OK and restart terminal

### Issue: Installation requires administrator privileges

**Solution:** Right-click Command Prompt or the script and select "Run as administrator"

---

## 📚 Additional Resources

- GnuCOBOL Official Site: https://gnucobol.sourceforge.io/
- Chocolatey: https://chocolatey.org/
- COBOL Test Documentation: See `Module-2-RPG-COBOL-Modernization/Module - COBOL Application/tests/README.md`

---

**Created**: 2026-06-23  
**For**: IBM Bob Workshop - Indonesia