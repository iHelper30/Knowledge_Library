#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate metadata
python Library_Resources/metadata_enricher.py

# Deploy to Cloudflare
wrangler publish

# Optional: Verify deployment
echo "Deployment of comprehensive-resource-library completed!"
