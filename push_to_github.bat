@echo off
REM Comprehensive Resource Library GitHub Push Script

REM Configure Git user
git config --global user.name "ihelp"
git config --global user.email "ihelp@example.com"

REM Ensure we're in the correct directory
cd /d C:\Projects\KnowledgeLibrary

REM Remove any existing git initialization if needed
rmdir /s /q .git 2>nul

REM Initialize new git repository
git init

REM Stage all files
git add .

REM Commit changes
git commit -m "Initial commit: Comprehensive Knowledge Library"

REM Create GitHub repository (requires GitHub CLI to be authenticated)
gh repo create Comprehensive_Resource_Library --public --source=. --remote=origin

REM Push to GitHub
git push -u origin main

REM Confirm successful push
echo Repository successfully pushed to GitHub!
