import os
import sys
import json
import logging
import subprocess
import yaml
import shutil
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('deployment.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TemplateValidationError(Exception):
    """Custom exception for template validation failures"""
    pass

class DeploymentManager:
    """
    Comprehensive deployment manager for templates and resources
    """
    def __init__(self, 
                 project_name: str = 'comprehensive-resource-library', 
                 base_deploy_dir: str = 'Library_Resources',
                 templates_dir: str = 'Templates_NEW'):
        """
        Initialize deployment configuration
        
        Args:
            project_name (str): Cloudflare Pages project name
            base_deploy_dir (str): Base directory for deployments
            templates_dir (str): Directory containing templates
        """
        # Load environment variables
        load_dotenv()
        
        # Validate critical environment variables
        self.validate_credentials()
        
        self.project_name = project_name
        self.base_deploy_dir = base_deploy_dir
        self.templates_dir = templates_dir
        
    def validate_credentials(self) -> None:
        """
        Validate critical deployment credentials
        """
        required_vars = [
            'CLOUDFLARE_API_TOKEN', 
            'CLOUDFLARE_ACCOUNT_ID'
        ]
        
        for var in required_vars:
            if not os.getenv(var):
                logger.error(f"Missing critical environment variable: {var}")
                raise EnvironmentError(f"Missing deployment credential: {var}")
    
    def get_templates(self) -> List[str]:
        """
        Discover all template directories
        
        Returns:
            List of template directory paths
        """
        try:
            return [
                template
                for template in os.listdir(self.templates_dir)
                if os.path.isdir(os.path.join(self.templates_dir, template))
            ]
        except Exception as e:
            logger.error(f"Error discovering templates: {e}")
            return []
    
    def prepare_deployment_directory(self) -> str:
        """
        Prepare deployment directory with backup mechanism
        """
        os.makedirs(self.base_deploy_dir, exist_ok=True)
        
        # Create backup of previous deployment
        previous_deployment_dir = os.path.join(self.base_deploy_dir, 'previous_deployment')
        
        # Remove existing backup if it exists
        if os.path.exists(previous_deployment_dir):
            shutil.rmtree(previous_deployment_dir)
        
        # If current deployment exists, move it to backup
        if os.listdir(self.base_deploy_dir):
            shutil.move(self.base_deploy_dir, previous_deployment_dir)
            os.makedirs(self.base_deploy_dir)
        
        return self.base_deploy_dir
    
    def copy_templates(self, templates: List[str], deploy_dir: str) -> None:
        """
        Copy templates to deployment directory
        
        Args:
            templates (List[str]): List of template paths
            deploy_dir (str): Destination deployment directory
        """
        import shutil
        
        for template in templates:
            template_name = template
            dest_path = os.path.join(deploy_dir, template_name)
            
            try:
                shutil.copytree(
                    os.path.join(self.templates_dir, template), 
                    dest_path
                )
                logger.info(f"Copied template: {template_name}")
            except Exception as e:
                logger.error(f"Failed to copy template {template_name}: {e}")
    
    def validate_template_structure(self, template_path: str) -> Dict[str, Any]:
        """
        Perform comprehensive validation of a template's structure
        
        Args:
            template_path (str): Path to the template directory
        
        Returns:
            Dict containing validation results
        
        Raises:
            TemplateValidationError if validation fails
        """
        validation_results = {
            'path': template_path,
            'is_valid': True,
            'errors': []
        }

        # Required files and directories
        required_files = [
            'README.md',
            'metadata.yml',
            'template_config.json'
        ]

        # Validate file existence
        for req_file in required_files:
            file_path = os.path.join(template_path, req_file)
            if not os.path.exists(file_path):
                validation_results['errors'].append(f"Missing required file: {req_file}")
                validation_results['is_valid'] = False

        # Validate metadata
        try:
            with open(os.path.join(template_path, 'metadata.yml'), 'r') as f:
                metadata = yaml.safe_load(f)
                
                # Check required metadata fields
                required_metadata_fields = [
                    'name', 
                    'version', 
                    'description', 
                    'category'
                ]
                
                for field in required_metadata_fields:
                    if field not in metadata:
                        validation_results['errors'].append(f"Missing metadata field: {field}")
                        validation_results['is_valid'] = False
        except (FileNotFoundError, yaml.YAMLError) as e:
            validation_results['errors'].append(f"Metadata validation failed: {str(e)}")
            validation_results['is_valid'] = False

        # Validate template configuration
        try:
            with open(os.path.join(template_path, 'template_config.json'), 'r') as f:
                config = json.load(f)
                
                # Check required configuration fields
                required_config_fields = [
                    'template_type', 
                    'supported_formats', 
                    'dependencies'
                ]
                
                for field in required_config_fields:
                    if field not in config:
                        validation_results['errors'].append(f"Missing config field: {field}")
                        validation_results['is_valid'] = False
        except (FileNotFoundError, json.JSONDecodeError) as e:
            validation_results['errors'].append(f"Configuration validation failed: {str(e)}")
            validation_results['is_valid'] = False

        return validation_results

    def validate_templates(self, templates: List[str]) -> List[Dict[str, Any]]:
        """
        Validate multiple templates
        
        Args:
            templates (List[str]): List of template directories to validate
        
        Returns:
            List of validation results for each template
        """
        validation_results = []
        
        for template in templates:
            full_template_path = os.path.join(self.templates_dir, template)
            try:
                result = self.validate_template_structure(full_template_path)
                validation_results.append(result)
                
                if not result['is_valid']:
                    logger.warning(f"Template validation failed for {template}: {result['errors']}")
            except Exception as e:
                logger.error(f"Unexpected error validating template {template}: {e}")
                validation_results.append({
                    'path': full_template_path,
                    'is_valid': False,
                    'errors': [str(e)]
                })
        
        return validation_results

    def rollback_deployment(self, deployment_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rollback a failed deployment
        
        Args:
            deployment_report (Dict): Deployment report from the failed deployment
        
        Returns:
            Rollback report dictionary
        """
        rollback_report = {
            'status': 'rollback_initiated',
            'timestamp': datetime.now().isoformat(),
            'original_deployment_status': deployment_report['status']
        }
        
        try:
            # Attempt to restore previous deployment state
            previous_deployment_dir = os.path.join(self.base_deploy_dir, 'previous_deployment')
            current_deployment_dir = self.base_deploy_dir
            
            # Check if previous deployment backup exists
            if os.path.exists(previous_deployment_dir):
                # Remove current deployment
                shutil.rmtree(current_deployment_dir)
                
                # Restore previous deployment
                shutil.move(previous_deployment_dir, current_deployment_dir)
                
                rollback_report['status'] = 'rollback_successful'
                logger.info("Deployment rollback completed successfully")
            else:
                rollback_report['status'] = 'rollback_failed'
                rollback_report['error'] = 'No previous deployment backup found'
                logger.error("Unable to rollback: No previous deployment backup")
        
        except Exception as e:
            rollback_report['status'] = 'rollback_failed'
            rollback_report['error'] = str(e)
            logger.error(f"Deployment rollback failed: {e}")
        
        # Save rollback report
        with open('rollback_report.json', 'w') as f:
            json.dump(rollback_report, f, indent=2)
        
        return rollback_report

    def deploy_to_cloudflare(self) -> Dict[str, Any]:
        """
        Execute Cloudflare Pages deployment
        
        Returns:
            Deployment report dictionary
        """
        try:
            # Validate templates before deployment
            templates = self.get_templates()
            validation_results = self.validate_templates(templates)
            
            # Filter out invalid templates
            valid_templates = [
                template for template, result in zip(templates, validation_results)
                if result['is_valid']
            ]
            
            if len(valid_templates) != len(templates):
                logger.warning(f"Skipping {len(templates) - len(valid_templates)} invalid templates")
            
            # Prepare deployment
            deploy_dir = self.prepare_deployment_directory()
            self.copy_templates(valid_templates, deploy_dir)
            
            # Deployment command
            deployment_command = [
                'npx', '@cloudflare/wrangler', 'pages', 'deploy',
                deploy_dir,
                '--project-name', self.project_name,
                '--branch', 'main'
            ]
            
            # Environment configuration
            env = os.environ.copy()
            
            try:
                # Execute deployment
                result = subprocess.run(
                    deployment_command,
                    capture_output=True,
                    text=True,
                    env=env,
                    check=True
                )
                
                # Create deployment report
                deployment_report = {
                    'status': 'success',
                    'templates_deployed': len(valid_templates),
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'template_validation': validation_results
                }
                
                logger.info("Deployment successful")
                
            except subprocess.CalledProcessError as e:
                deployment_report = {
                    'status': 'failed',
                    'error_code': e.returncode,
                    'stdout': e.stdout.decode('utf-8', errors='replace') if isinstance(e.stdout, bytes) else str(e.stdout),
                    'stderr': e.stderr.decode('utf-8', errors='replace') if isinstance(e.stderr, bytes) else str(e.stderr),
                    'template_validation': validation_results
                }
                
                logger.error(f"Deployment failed: {e}")
                
                # Trigger rollback
                rollback_report = self.rollback_deployment(deployment_report)
                deployment_report['rollback_report'] = rollback_report
            
            return deployment_report
        
        except Exception as e:
            logger.error(f"Deployment process failed: {e}")
            
            # Attempt emergency rollback
            emergency_rollback_report = self.rollback_deployment({
                'status': 'failed',
                'error': str(e)
            })
            
            return {
                'status': 'critical_failure',
                'error': str(e),
                'emergency_rollback': emergency_rollback_report
            }

def main():
    try:
        deployment_manager = DeploymentManager()
        deployment_report = deployment_manager.deploy_to_cloudflare()
        
        if deployment_report['status'] == 'failed':
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Deployment process failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
