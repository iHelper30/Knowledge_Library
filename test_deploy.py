import os
import sys
import json
import unittest
import tempfile
import shutil
import subprocess
from unittest.mock import patch, MagicMock

# Add the script's directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from deploy import DeploymentManager

class TestDeploymentManager(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment with temporary directories
        """
        # Create temporary directories
        self.test_base_dir = tempfile.mkdtemp()
        self.test_templates_dir = os.path.join(self.test_base_dir, 'Templates_NEW')
        os.makedirs(self.test_templates_dir)
        
        # Create mock templates
        template_names = [
            'Case_Study_Template', 
            'White_Paper_Template', 
            'Email_Newsletter_Template'
        ]
        
        for template in template_names:
            template_path = os.path.join(self.test_templates_dir, template)
            os.makedirs(template_path)
            # Create dummy files in each template
            with open(os.path.join(template_path, 'README.md'), 'w') as f:
                f.write(f"# {template} README")
    
    def tearDown(self):
        """
        Clean up temporary directories
        """
        shutil.rmtree(self.test_base_dir)
    
    @patch.dict(os.environ, {
        'CLOUDFLARE_API_TOKEN': 'test_token', 
        'CLOUDFLARE_ACCOUNT_ID': 'test_account'
    })
    def test_validate_credentials(self):
        """
        Test credential validation
        """
        try:
            manager = DeploymentManager(
                templates_dir=self.test_templates_dir,
                base_deploy_dir=os.path.join(self.test_base_dir, 'Library_Resources')
            )
            manager.validate_credentials()
        except Exception as e:
            self.fail(f"Credential validation failed: {e}")
    
    @patch.dict(os.environ, {
        'CLOUDFLARE_API_TOKEN': 'test_token', 
        'CLOUDFLARE_ACCOUNT_ID': 'test_account'
    })
    def test_get_templates(self):
        """
        Test template discovery
        """
        manager = DeploymentManager(
            templates_dir=self.test_templates_dir,
            base_deploy_dir=os.path.join(self.test_base_dir, 'Library_Resources')
        )
        templates = manager.get_templates()
        
        # Check that all templates are discovered
        self.assertEqual(len(templates), 3)
        self.assertTrue(all('Template' in template for template in templates))
    
    @patch.dict(os.environ, {
        'CLOUDFLARE_API_TOKEN': 'test_token', 
        'CLOUDFLARE_ACCOUNT_ID': 'test_account'
    })
    def test_prepare_deployment_directory(self):
        """
        Test deployment directory preparation
        """
        manager = DeploymentManager(
            templates_dir=self.test_templates_dir,
            base_deploy_dir=os.path.join(self.test_base_dir, 'Library_Resources')
        )
        deploy_dir = manager.prepare_deployment_directory()
        
        # Check directory creation
        self.assertTrue(os.path.exists(deploy_dir))
        self.assertTrue(os.path.isdir(deploy_dir))
    
    @patch.dict(os.environ, {
        'CLOUDFLARE_API_TOKEN': 'test_token', 
        'CLOUDFLARE_ACCOUNT_ID': 'test_account'
    })
    def test_copy_templates(self):
        """
        Test template copying mechanism
        """
        manager = DeploymentManager(
            templates_dir=self.test_templates_dir,
            base_deploy_dir=os.path.join(self.test_base_dir, 'Library_Resources')
        )
        deploy_dir = manager.prepare_deployment_directory()
        templates = manager.get_templates()
        
        manager.copy_templates(templates, deploy_dir)
        
        # Verify templates were copied
        copied_templates = os.listdir(deploy_dir)
        self.assertEqual(len(copied_templates), 3)
        self.assertTrue(all('Template' in template for template in copied_templates))
    
    @patch('subprocess.run')
    @patch.dict(os.environ, {
        'CLOUDFLARE_API_TOKEN': 'test_token', 
        'CLOUDFLARE_ACCOUNT_ID': 'test_account'
    })
    def test_deploy_to_cloudflare_success(self, mock_subprocess):
        """
        Test successful Cloudflare deployment
        """
        # Mock successful subprocess run
        mock_subprocess.return_value = MagicMock(
            returncode=0, 
            stdout='Deployment successful', 
            stderr=''
        )
        
        manager = DeploymentManager(
            templates_dir=self.test_templates_dir,
            base_deploy_dir=os.path.join(self.test_base_dir, 'Library_Resources')
        )
        report = manager.deploy_to_cloudflare()
        
        # Verify deployment report
        self.assertEqual(report['status'], 'success')
        self.assertEqual(report['templates_deployed'], 3)
    
    @patch('subprocess.run')
    @patch.dict(os.environ, {
        'CLOUDFLARE_API_TOKEN': 'test_token', 
        'CLOUDFLARE_ACCOUNT_ID': 'test_account'
    })
    def test_deploy_to_cloudflare_failure(self, mock_subprocess):
        """
        Test failed Cloudflare deployment
        """
        # Mock failed subprocess run
        mock_subprocess.side_effect = subprocess.CalledProcessError(
            returncode=1, 
            cmd=['wrangler', 'pages', 'deploy'],
            output=b'Deployment failed',
            stderr=b'Error details'
        )
        
        manager = DeploymentManager(
            templates_dir=self.test_templates_dir,
            base_deploy_dir=os.path.join(self.test_base_dir, 'Library_Resources')
        )
        
        try:
            report = manager.deploy_to_cloudflare()
            self.assertEqual(report['status'], 'failed')
        except Exception as e:
            self.fail(f"Deployment failure handling failed: {e}")

def run_tests():
    """
    Run all tests and generate a report
    """
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestDeploymentManager)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    
    # Generate test report
    report = {
        'total_tests': test_result.testsRun,
        'failures': len(test_result.failures),
        'errors': len(test_result.errors),
        'skipped': len(test_result.skipped),
        'successful': test_result.wasSuccessful()
    }
    
    with open('test_deployment_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    return test_result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
