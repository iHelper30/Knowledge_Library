@echo off
REM GitHub CLI Authentication Script

REM Use full path to GitHub CLI
"C:\Program Files\GitHub CLI\gh.exe" auth login -w

REM Check authentication status
"C:\Program Files\GitHub CLI\gh.exe" auth status
