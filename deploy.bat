@echo off
REM Comprehensive Resource Library Deployment Script

REM Configure Git
git config --global user.name "ihelp"
git config --global user.email "ihelp@example.com"

REM Add all files
git add .

REM Commit changes
git commit -m "Initial commit: Comprehensive Resource Library"

REM Push to GitHub
git push -u origin main
