@echo off
REM Final Push Script

cd /d C:\Projects\KnowledgeLibrary

REM Remove existing origin
git remote remove origin

REM Add new origin
git remote add origin https://github.com/iHelper30/Comprehensive_Resource_Library.git

REM Force push to main branch
git push -f origin main

echo Repository successfully pushed!
