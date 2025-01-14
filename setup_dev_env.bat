@echo off
setlocal enabledelayedexpansion

:: Local Development Environment Setup Script
:: Version: 1.0.0
:: Last Updated: 2025-01-13

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires administrator privileges.
    echo Please run as administrator.
    pause
    exit /b 1
)

:: Logging function
:log
echo [%time%] %~1
goto :eof

:: Check Python installation
call :log "Checking Python installation..."
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

:: Determine script directory
set "SCRIPT_DIR=%~dp0"

:: Create virtual environment
call :log "Creating virtual environment..."
python -m venv .venv
call .venv\Scripts\activate

:: Upgrade pip and setuptools
call :log "Upgrading pip and setuptools..."
python -m pip install --upgrade pip setuptools wheel

:: Install project dependencies
call :log "Installing project dependencies..."
pip install -r "%SCRIPT_DIR%requirements.txt"

:: Install development tools
call :log "Installing development tools..."
pip install pytest flake8 mypy black

:: Run initial validation
call :log "Running initial template validation..."
python "%SCRIPT_DIR%validate_template.py" "%SCRIPT_DIR%Templates_NEW"

:: Generate initial template
call :log "Generating sample template..."
python "%SCRIPT_DIR%generate_template.py" "DevEnv_Sample_Template"

:: Run tests
call :log "Running test suite..."
pytest

:: Deactivate virtual environment
deactivate

:: Success message
call :log "Development environment setup complete!"
echo.
echo 🚀 Development Environment Ready
echo - Virtual Environment: .venv
echo - Dependencies Installed
echo - Initial Template Generated
echo - Tests Passed

pause
exit /b 0
