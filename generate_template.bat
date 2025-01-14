@echo off
REM Template Generation Batch Script

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python and ensure it's added to your system PATH.
    pause
    exit /b 1
)

REM Determine script location
set "SCRIPT_DIR=%~dp0"

REM Run template generation script
python "%SCRIPT_DIR%generate_template.py" %*

REM Pause to show output if not run from console
if "%1"=="" pause
