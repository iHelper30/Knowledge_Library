@echo off
REM Comprehensive Resource Library Staging Script

REM Change to project directory
cd /d C:\Projects\KnowledgeLibrary

REM Configure Git user
git config --global user.name "ihelp"
git config --global user.email "ihelp@example.com"

REM Initialize git repository if not already initialized
if not exist ".git" (
    git init
)

REM Create .gitignore to exclude unnecessary files
echo # Comprehensive Resource Library Gitignore > .gitignore
echo .env >> .gitignore
echo *.log >> .gitignore
echo __pycache__/ >> .gitignore
echo .pytest_cache/ >> .gitignore
echo .venv/ >> .gitignore
echo .DS_Store >> .gitignore

REM Stage all files, respecting .gitignore
git add .

REM Commit with detailed message
git commit -m "Initial commit: Comprehensive Knowledge Library

- Complete project structure
- Metadata generation scripts
- Navigation and template systems
- Cloudflare deployment workflow
- Initial documentation and resources"

REM Display commit information
git log -n 1

echo Staging and initial commit completed successfully!
