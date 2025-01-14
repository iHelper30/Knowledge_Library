"""
Advanced Template Validation Module
Provides comprehensive and extensible validation rules
"""

import re
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable

import jsonschema
import requests

class AdvancedTemplateValidator:
    """
    Comprehensive template validation with advanced rules
    """
    
    def __init__(self, 
                 custom_rules_path: Optional[Path] = None,
                 external_validators: Optional[List[Callable]] = None):
        """
        Initialize advanced validator
        
        Args:
            custom_rules_path: Path to custom validation rules
            external_validators: List of external validation functions
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.custom_rules = self._load_custom_rules(custom_rules_path)
        self.external_validators = external_validators or []
    
    def _load_custom_rules(self, rules_path: Optional[Path]) -> Dict[str, Any]:
        """
        Load custom validation rules from a configuration file
        
        Args:
            rules_path: Path to rules configuration
        
        Returns:
            Dictionary of custom validation rules
        """
        if not rules_path or not rules_path.exists():
            return {}
        
        try:
            if rules_path.suffix in ['.json']:
                return json.loads(rules_path.read_text())
            elif rules_path.suffix in ['.yml', '.yaml']:
                return yaml.safe_load(rules_path.read_text())
            else:
                self.logger.warning(f"Unsupported rules file type: {rules_path.suffix}")
                return {}
        except Exception as e:
            self.logger.error(f"Error loading custom rules: {e}")
            return {}
    
    def validate(self, template_path: Path) -> Dict[str, Any]:
        """
        Comprehensive template validation
        
        Args:
            template_path: Path to template directory
        
        Returns:
            Validation result dictionary
        """
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Basic structure checks
        structure_validation = self._validate_structure(template_path)
        validation_results['is_valid'] &= structure_validation['is_valid']
        validation_results['errors'].extend(structure_validation.get('errors', []))
        
        # Content checks
        content_validation = self._validate_content(template_path)
        validation_results['is_valid'] &= content_validation['is_valid']
        validation_results['errors'].extend(content_validation.get('errors', []))
        
        # Metadata validation
        metadata_validation = self._validate_metadata(template_path)
        validation_results['is_valid'] &= metadata_validation['is_valid']
        validation_results['errors'].extend(metadata_validation.get('errors', []))
        
        # Security checks
        security_validation = self._validate_security(template_path)
        validation_results['is_valid'] &= security_validation['is_valid']
        validation_results['errors'].extend(security_validation.get('errors', []))
        
        # External validators
        for validator in self.external_validators:
            try:
                external_result = validator(template_path)
                validation_results['is_valid'] &= external_result.get('is_valid', True)
                validation_results['errors'].extend(external_result.get('errors', []))
                validation_results['warnings'].extend(external_result.get('warnings', []))
            except Exception as e:
                validation_results['errors'].append(f"External validator error: {e}")
                validation_results['is_valid'] = False
        
        return validation_results
    
    def _validate_structure(self, template_path: Path) -> Dict[str, Any]:
        """
        Validate template directory structure
        
        Args:
            template_path: Path to template directory
        
        Returns:
            Validation result dictionary
        """
        result = {'is_valid': True, 'errors': []}
        
        # Check for required directories and files
        required_items = self.custom_rules.get('required_structure', [
            'README.md',
            'metadata.yml',
            'template_config.json'
        ])
        
        for item in required_items:
            item_path = template_path / item
            if not item_path.exists():
                result['errors'].append(f"Missing required item: {item}")
                result['is_valid'] = False
        
        # Check directory depth
        max_depth = self.custom_rules.get('max_directory_depth', 5)
        if self._get_max_depth(template_path) > max_depth:
            result['errors'].append(f"Directory depth exceeds {max_depth}")
            result['is_valid'] = False
        
        return result
    
    def _validate_content(self, template_path: Path) -> Dict[str, Any]:
        """
        Validate template content
        
        Args:
            template_path: Path to template directory
        
        Returns:
            Validation result dictionary
        """
        result = {'is_valid': True, 'errors': []}
        
        # README content checks
        readme_path = template_path / 'README.md'
        if readme_path.exists():
            readme_content = readme_path.read_text()
            
            # Minimum word count
            min_words = self.custom_rules.get('readme_min_words', 50)
            if len(readme_content.split()) < min_words:
                result['errors'].append(f"README must have at least {min_words} words")
                result['is_valid'] = False
            
            # Check for placeholders
            placeholders = ['{{', '}}', '[REPLACE', 'TODO:']
            for placeholder in placeholders:
                if placeholder in readme_content:
                    result['errors'].append(f"Unresolved placeholder found: {placeholder}")
                    result['is_valid'] = False
        
        return result
    
    def _validate_metadata(self, template_path: Path) -> Dict[str, Any]:
        """
        Validate template metadata
        
        Args:
            template_path: Path to template directory
        
        Returns:
            Validation result dictionary
        """
        result = {'is_valid': True, 'errors': []}
        
        # Validate metadata file
        metadata_path = template_path / 'metadata.yml'
        if not metadata_path.exists():
            result['errors'].append("Missing metadata.yml")
            result['is_valid'] = False
            return result
        
        try:
            with open(metadata_path, 'r') as f:
                metadata = yaml.safe_load(f)
            
            # Required metadata fields
            required_fields = ['name', 'version', 'description']
            for field in required_fields:
                if not metadata.get(field):
                    result['errors'].append(f"Missing required metadata field: {field}")
                    result['is_valid'] = False
            
            # Version format validation
            version_pattern = r'^\d+\.\d+\.\d+(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$'
            if not re.match(version_pattern, metadata.get('version', '')):
                result['errors'].append("Invalid version format")
                result['is_valid'] = False
        
        except yaml.YAMLError as e:
            result['errors'].append(f"Invalid metadata YAML: {e}")
            result['is_valid'] = False
        
        return result
    
    def _validate_security(self, template_path: Path) -> Dict[str, Any]:
        """
        Perform security checks on template
        
        Args:
            template_path: Path to template directory
        
        Returns:
            Validation result dictionary
        """
        result = {'is_valid': True, 'errors': []}
        
        # Check for potential security issues
        sensitive_files = ['.env', 'secrets.json', 'credentials.yml']
        for sensitive_file in sensitive_files:
            if (template_path / sensitive_file).exists():
                result['errors'].append(f"Sensitive file found: {sensitive_file}")
                result['is_valid'] = False
        
        # Scan for potential hardcoded secrets
        def scan_file_for_secrets(file_path):
            """
            Scan a file for potential hardcoded secrets
            """
            try:
                content = file_path.read_text()
                secret_patterns = [
                    r'(api_key|secret|password)\s*=\s*[\'"][^\'"]+[\'"]\s*',
                    r'(access_token|client_secret)\s*:\s*[\'"][^\'"]+[\'"]\s*'
                ]
                
                for pattern in secret_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        return True
                return False
            except Exception:
                return False
        
        # Recursively scan files
        for file_path in template_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.py', '.js', '.json', '.yml', '.yaml', '.txt']:
                if scan_file_for_secrets(file_path):
                    result['errors'].append(f"Potential hardcoded secret in {file_path.relative_to(template_path)}")
                    result['is_valid'] = False
        
        return result
    
    def _get_max_depth(self, path: Path, current_depth: int = 0) -> int:
        """
        Calculate maximum directory depth
        
        Args:
            path: Path to check
            current_depth: Current recursion depth
        
        Returns:
            Maximum directory depth
        """
        if not path.is_dir():
            return current_depth
        
        max_depth = current_depth
        for item in path.iterdir():
            if item.is_dir():
                max_depth = max(max_depth, self._get_max_depth(item, current_depth + 1))
        
        return max_depth

def external_dependency_validator(template_path: Path) -> Dict[str, Any]:
    """
    External validator to check template dependencies
    
    Args:
        template_path: Path to template directory
    
    Returns:
        Validation result dictionary
    """
    result = {'is_valid': True, 'warnings': []}
    
    # Check requirements.txt or similar
    requirements_files = ['requirements.txt', 'pyproject.toml', 'setup.py']
    
    for req_file in requirements_files:
        req_path = template_path / req_file
        if req_path.exists():
            try:
                # Basic dependency check
                with open(req_path, 'r') as f:
                    content = f.read()
                    
                    # Check for outdated or vulnerable packages
                    vulnerable_packages = _check_package_vulnerabilities(content)
                    if vulnerable_packages:
                        result['warnings'].extend([
                            f"Potential vulnerable package: {pkg}" 
                            for pkg in vulnerable_packages
                        ])
                        result['is_valid'] = False
            
            except Exception as e:
                result['warnings'].append(f"Error checking {req_file}: {e}")
                result['is_valid'] = False
    
    return result

def _check_package_vulnerabilities(requirements_content: str) -> List[str]:
    """
    Check packages against known vulnerability databases
    
    Args:
        requirements_content: Content of requirements file
    
    Returns:
        List of potentially vulnerable packages
    """
    # This is a simplified mock implementation
    # In a real-world scenario, you'd use services like:
    # - PyUp Safety
    # - Snyk
    # - GitHub Advisory Database
    
    try:
        # Example: Use GitHub Security Advisories API
        # Note: This requires an actual API key and implementation
        response = requests.get(
            'https://api.github.com/advisories', 
            params={'ecosystem': 'pip'}
        )
        
        if response.status_code == 200:
            advisories = response.json()
            # Implement actual vulnerability matching logic
            return [adv['package'] for adv in advisories]
        
        return []
    
    except Exception:
        # Fallback to a basic list of known vulnerable packages
        return ['requests<2.25.0', 'pillow<8.1.0', 'django<3.2']
