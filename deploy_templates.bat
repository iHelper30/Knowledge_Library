@echo off

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Generate metadata
python Library_Resources\metadata_enricher.py

REM Deploy to Cloudflare
wrangler publish

REM Optional: Verify deployment
echo Deployment of comprehensive-resource-library completed!
