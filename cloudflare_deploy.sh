#!/bin/bash

# Cloudflare Pages Deployment Script

# Ensure Cloudflare Wrangler is installed
npm install -g @cloudflare/wrangler

# Login to Cloudflare
wrangler login

# Create Cloudflare Pages project
wrangler pages project create comprehensive-resource-library \
    --production-branch main \
    --source-directory Library_Resources

# Deploy the project
wrangler pages deploy Library_Resources \
    --project-name comprehensive-resource-library \
    --branch main

# Output deployment URL
echo "Deployment complete. Access your site at:"
wrangler pages url comprehensive-resource-library
