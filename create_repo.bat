@echo off
REM GitHub Repository Creation Script

REM Ensure you're authenticated with 'gh auth login' before running

gh repo create Comprehensive_Resource_Library ^
    --public ^
    --description "Modular Knowledge Management System" ^
    --homepage "https://ihelp.github.io/Comprehensive_Resource_Library" ^
    --source=. ^
    --remote=origin ^
    --push
