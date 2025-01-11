#!/bin/bash
# GitHub Repository Creation Script for Comprehensive Knowledge Library

# Ensure GitHub CLI is authenticated
gh auth status

# Create public repository
gh repo create Comprehensive_Resource_Library \
    --public \
    --description "Modular Knowledge Management System" \
    --homepage "https://ihelp.github.io/Comprehensive_Resource_Library" \
    --source=. \
    --remote=origin

# Set default branch to main
gh repo edit ihelp/Comprehensive_Resource_Library --default-branch main

# Create initial README if not exists
if [ ! -f README.md ]; then
    echo "# Comprehensive Resource Library

A modular knowledge management system designed to transform content into a structured, navigable, and user-friendly library.

## Project Overview

- Automated template generation
- Intelligent navigation system
- Metadata enrichment
- Cloudflare Pages deployment

## Quick Start

\`\`\`bash
pip install -r requirements.txt
python template_generator.py
\`\`\`

## License

MIT License" > README.md
fi

# Add README and push
git add README.md
git commit -m "Add project README"
git push -u origin main

echo "Repository created and initialized successfully!"
