import os
import sys
import json
import yaml
import unittest
import tempfile
import shutil
from typing import Dict, Any

from deploy import DeploymentManager

class MockDeploymentManager(DeploymentManager):
    """
    Mock DeploymentManager that skips credential validation for testing
    """
    def validate_credentials(self) -> None:
        """
        Override credential validation for testing
        """
        pass  # No-op for tests

class TestTemplateValidation(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment with temporary directories and mock templates
        """
        # Create temporary base directory
        self.test_base_dir = tempfile.mkdtemp()
        self.templates_dir = os.path.join(self.test_base_dir, 'Templates_NEW')
        os.makedirs(self.templates_dir)
        
        # Create valid template
        self.valid_template_path = os.path.join(self.templates_dir, 'Valid_Template')
        os.makedirs(self.valid_template_path)
        
        # Create valid template files
        with open(os.path.join(self.valid_template_path, 'README.md'), 'w') as f:
            f.write("# Valid Template\n\nThis is a valid template.")
        
        with open(os.path.join(self.valid_template_path, 'metadata.yml'), 'w') as f:
            yaml.safe_dump({
                'name': 'Valid Template',
                'version': '1.0.0',
                'description': 'A template for testing',
                'category': 'documentation'
            }, f)
        
        with open(os.path.join(self.valid_template_path, 'template_config.json'), 'w') as f:
            json.dump({
                'template_type': 'document',
                'supported_formats': ['md', 'txt'],
                'dependencies': []
            }, f)
        
        # Create invalid templates
        self.create_invalid_templates()
    
    def create_invalid_templates(self):
        """
        Create various invalid template scenarios
        """
        # Missing README
        missing_readme_path = os.path.join(self.templates_dir, 'Missing_Readme_Template')
        os.makedirs(missing_readme_path)
        
        with open(os.path.join(missing_readme_path, 'metadata.yml'), 'w') as f:
            yaml.safe_dump({
                'name': 'Incomplete Template',
                'version': '0.1.0',
                'description': 'An incomplete template',
                'category': 'test'
            }, f)
        
        # Incomplete Metadata
        incomplete_metadata_path = os.path.join(self.templates_dir, 'Incomplete_Metadata_Template')
        os.makedirs(incomplete_metadata_path)
        
        with open(os.path.join(incomplete_metadata_path, 'README.md'), 'w') as f:
            f.write("# Incomplete Metadata Template")
        
        with open(os.path.join(incomplete_metadata_path, 'metadata.yml'), 'w') as f:
            yaml.safe_dump({
                'name': 'Incomplete Metadata',
                # Missing other required fields
            }, f)
        
        # Invalid Configuration
        invalid_config_path = os.path.join(self.templates_dir, 'Invalid_Config_Template')
        os.makedirs(invalid_config_path)
        
        with open(os.path.join(invalid_config_path, 'README.md'), 'w') as f:
            f.write("# Invalid Config Template")
        
        with open(os.path.join(invalid_config_path, 'metadata.yml'), 'w') as f:
            yaml.safe_dump({
                'name': 'Invalid Config Template',
                'version': '0.1.0',
                'description': 'Template with invalid config',
                'category': 'test'
            }, f)
        
        with open(os.path.join(invalid_config_path, 'template_config.json'), 'w') as f:
            json.dump({
                # Missing required fields
                'notes': 'Incomplete configuration'
            }, f)
    
    def tearDown(self):
        """
        Clean up temporary directories
        """
        shutil.rmtree(self.test_base_dir)
    
    def test_valid_template_validation(self):
        """
        Test validation of a completely valid template
        """
        manager = MockDeploymentManager(
            templates_dir=self.templates_dir,
            base_deploy_dir=os.path.join(self.test_base_dir, 'Library_Resources')
        )
        
        validation_result = manager.validate_template_structure(
            os.path.join(self.templates_dir, 'Valid_Template')
        )
        
        self.assertTrue(validation_result['is_valid'], 
                        f"Valid template failed validation: {validation_result['errors']}")
        self.assertEqual(len(validation_result['errors']), 0, 
                         "Valid template should have no validation errors")
    
    def test_invalid_templates(self):
        """
        Test validation of various invalid template scenarios
        """
        manager = MockDeploymentManager(
            templates_dir=self.templates_dir,
            base_deploy_dir=os.path.join(self.test_base_dir, 'Library_Resources')
        )
        
        invalid_template_paths = [
            'Missing_Readme_Template',
            'Incomplete_Metadata_Template',
            'Invalid_Config_Template'
        ]
        
        for template in invalid_template_paths:
            full_path = os.path.join(self.templates_dir, template)
            validation_result = manager.validate_template_structure(full_path)
            
            self.assertFalse(validation_result['is_valid'], 
                             f"Template {template} should be invalid")
            self.assertTrue(len(validation_result['errors']) > 0, 
                            f"Template {template} should have validation errors")
    
    def test_templates_validation(self):
        """
        Test validation of multiple templates
        """
        manager = MockDeploymentManager(
            templates_dir=self.templates_dir,
            base_deploy_dir=os.path.join(self.test_base_dir, 'Library_Resources')
        )
        
        # Get all templates
        templates = [t for t in os.listdir(self.templates_dir) 
                     if os.path.isdir(os.path.join(self.templates_dir, t))]
        
        validation_results = manager.validate_templates(templates)
        
        # Check validation results
        self.assertEqual(len(validation_results), len(templates), 
                         "Should have a validation result for each template")
        
        # Count valid and invalid templates
        valid_templates = [r for r in validation_results if r['is_valid']]
        invalid_templates = [r for r in validation_results if not r['is_valid']]
        
        self.assertEqual(len(valid_templates), 1, 
                         "Should have exactly one valid template")
        self.assertEqual(len(invalid_templates), 3, 
                         "Should have three invalid templates")

def run_tests():
    """
    Run all tests and generate a report
    """
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplateValidation)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    
    # Generate test report
    report = {
        'total_tests': test_result.testsRun,
        'failures': len(test_result.failures),
        'errors': len(test_result.errors),
        'skipped': len(test_result.skipped),
        'successful': test_result.wasSuccessful()
    }
    
    with open('template_validation_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    return test_result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
