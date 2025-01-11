import os
import sys
import subprocess
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def deploy_to_cloudflare():
    """
    Comprehensive Cloudflare Pages Deployment Script
    """
    # Retrieve Cloudflare Credentials
    CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
    CLOUDFLARE_ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID')

    if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ACCOUNT_ID:
        print("❌ Cloudflare credentials not found in environment")
        sys.exit(1)

    # Project Configuration
    PROJECT_NAME = 'comprehensive-resource-library'
    SOURCE_DIRECTORY = 'Library_Resources'

    # Ensure source directory exists
    if not os.path.exists(SOURCE_DIRECTORY):
        os.makedirs(SOURCE_DIRECTORY)

    # Deployment Command
    deployment_command = [
        'npx',
        '@cloudflare/wrangler',
        'pages',
        'deploy',
        SOURCE_DIRECTORY,
        '--project-name', PROJECT_NAME,
        '--branch', 'main'
    ]

    # Environment Configuration
    env = os.environ.copy()
    env['CLOUDFLARE_API_TOKEN'] = CLOUDFLARE_API_TOKEN
    env['CLOUDFLARE_ACCOUNT_ID'] = CLOUDFLARE_ACCOUNT_ID

    try:
        # Execute Deployment
        result = subprocess.run(
            deployment_command,
            capture_output=True,
            text=True,
            env=env
        )

        # Deployment Report
        deployment_report = {
            'status': 'success' if result.returncode == 0 else 'failed',
            'stdout': result.stdout,
            'stderr': result.stderr
        }

        # Save Deployment Report
        with open('deployment_report.json', 'w') as f:
            json.dump(deployment_report, f, indent=2)

        # Print Deployment Logs
        print("🚀 Cloudflare Deployment Logs:")
        print(result.stdout)

        if result.returncode != 0:
            print("❌ Deployment Failed:")
            print(result.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"❌ Deployment Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    deploy_to_cloudflare()
