@echo off
REM Comprehensive Deployment Commit and Push Script

REM Change to project directory
cd /d C:\Projects\KnowledgeLibrary

REM Configure Git user
git config --global user.name "ihelp"
git config --global user.email "ihelp@example.com"

REM Stage all changes
git add .

REM Commit with detailed message
git commit -m "Comprehensive Deployment Configuration

- Updated GitHub Actions workflow
- Added Cloudflare Pages deployment scripts
- Enhanced deployment verification
- Configured security scanning
- Prepared for continuous deployment"

REM Push to GitHub
git push origin main

echo Deployment configuration pushed successfully!
