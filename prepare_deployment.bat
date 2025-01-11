@echo off
REM Comprehensive Deployment Preparation Script

REM Set working directory
cd /d C:\Projects\KnowledgeLibrary

REM Ensure Library_Resources directory exists
if not exist "Library_Resources" mkdir Library_Resources

REM Run template generation scripts
python template_generator.py
python evolution_prototype.py

REM Authenticate Cloudflare
wrangler login

REM Initialize Cloudflare Pages project
wrangler pages project create comprehensive-resource-library ^
    --production-branch main ^
    --source-directory Library_Resources

REM Verify deployment configuration
python deployment_verification.py

REM Deploy to Cloudflare Pages
python cloudflare_deployment.py

echo Deployment preparation and initial deployment complete!
