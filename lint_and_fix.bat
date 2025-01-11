@echo off
REM Comprehensive Linting and Code Quality Script

REM Change to project directory
cd /d C:\Projects\KnowledgeLibrary

REM Install linting tools
pip install flake8 autopep8 mypy

REM Run flake8 to identify issues
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

REM Automatically fix some common style issues
autopep8 --in-place --aggressive --aggressive -r .

REM Run type checking
mypy .

REM Stage and commit fixes
git add .
git commit -m "Code quality improvements: Linting and type checking fixes"

echo Linting and fixing complete!
