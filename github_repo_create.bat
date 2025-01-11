@echo off
REM GitHub Repository Creation Script

REM Change to project directory
cd /d C:\Projects\KnowledgeLibrary

REM Create README if not exists
if not exist "README.md" (
    echo # Comprehensive Resource Library > README.md
    echo. >> README.md
    echo A modular knowledge management system designed to transform content into a structured, navigable, and user-friendly library. >> README.md
)

REM Use GitHub CLI to create repository
"C:\Program Files\GitHub CLI\gh.exe" repo create Comprehensive_Resource_Library ^
    --public ^
    --description "Modular Knowledge Management System" ^
    --homepage "https://ihelp.github.io/Comprehensive_Resource_Library"

REM Add remote and push
git remote add origin https://github.com/ihelp/Comprehensive_Resource_Library.git
git branch -M main
git add README.md
git commit -m "Initial commit: Add README"
git push -u origin main

echo Repository created and initialized successfully!
