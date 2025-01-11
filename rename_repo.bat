@echo off
REM Rename GitHub Repository Script

REM Authenticate and rename repository
"C:\Program Files\GitHub CLI\gh.exe" repo rename Comprehensive_Resource_Library Comprehensive_Resource_Library_Old --yes

REM Create new repository
"C:\Program Files\GitHub CLI\gh.exe" repo create Comprehensive_Resource_Library ^
    --public ^
    --description "Modular Knowledge Management System" ^
    --homepage "https://ihelp.github.io/Comprehensive_Resource_Library" ^
    --source=. ^
    --remote=origin

REM Change to project directory
cd /d C:\Projects\KnowledgeLibrary

REM Create README if not exists
if not exist "README.md" (
    echo # Comprehensive Resource Library > README.md
    echo. >> README.md
    echo A modular knowledge management system designed to transform content into a structured, navigable, and user-friendly library. >> README.md
)

REM Configure Git
git config --global user.name "ihelp"
git config --global user.email "ihelp@example.com"

REM Add remote and push
git remote add origin https://github.com/ihelp/Comprehensive_Resource_Library.git
git branch -M main
git add .
git commit -m "Initial commit: Comprehensive Knowledge Library"
git push -u origin main

echo Repository renamed and new repository created successfully!
