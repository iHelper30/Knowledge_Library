import os
import sys
from unittest.mock import patch, MagicMock
from deployment_verification import verify_cloudflare_deployment

def load_test_env():
    """Load test environment variables"""
    with open('.env.test') as f:
        for line in f:
            key, value = line.strip().split('=')
            os.environ[key] = value

def mock_successful_response():
    """Create a mock successful API response"""
    return MagicMock(
        json=lambda: {
            'success': True,
            'result': {
                'deployment_enabled': True,
                'production_branch': 'main',
                'url': 'https://test.pages.dev'
            }
        }
    )

def mock_deployments_response():
    """Create a mock deployments API response"""
    return MagicMock(
        json=lambda: {
            'result': [{
                'status': 'success',
                'url': 'https://test.pages.dev'
            }]
        }
    )

def test_deployment_verification():
    """Test the deployment verification process"""
    # Load test environment
    load_test_env()
    
    # Mock requests
    with patch('requests.get') as mock_get:
        # Configure mock responses
        mock_get.side_effect = [
            mock_successful_response(),
            mock_deployments_response(),
            MagicMock(status_code=200)  # Health check response
        ]
        
        try:
            verify_cloudflare_deployment()
            print("[+] Deployment verification test passed")
            return True
        except SystemExit as e:
            if e.code != 0:
                print("[-] Deployment verification test failed")
            return e.code == 0
        except Exception as e:
            print(f"[X] Unexpected error: {e}")
            return False

if __name__ == '__main__':
    success = test_deployment_verification()
    sys.exit(0 if success else 1)
