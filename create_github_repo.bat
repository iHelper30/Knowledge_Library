@echo off
REM GitHub Repository Creation Wrapper

REM Change to project directory
cd /d C:\Projects\KnowledgeLibrary

REM Run bash script using Git Bash
"C:\Program Files\Git\bin\bash.exe" github_repo_create.sh

REM Check exit status
if %errorlevel% neq 0 (
    echo Repository creation failed
    exit /b %errorlevel%
)

echo Repository created successfully!
