"""
Document Template Type Implementation
"""

import textwrap
from pathlib import Path
from typing import Dict, Any

from ..core import BaseTemplateType, TemplateTypeRegistry

class DocumentTemplateType(BaseTemplateType):
    """
    Specialized template type for documentation templates
    """
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate document template specific requirements
        
        Returns:
            Validation result dictionary
        """
        errors = []
        
        # Check for required files
        required_files = [
            'README.md',
            'metadata.yml',
            'template_config.json'
        ]
        
        for file in required_files:
            if not (self.base_path / file).exists():
                errors.append(f"Missing required file: {file}")
        
        # Additional document-specific validations
        readme_path = self.base_path / 'README.md'
        if readme_path.exists():
            readme_content = readme_path.read_text()
            if len(readme_content.split()) < 50:
                errors.append("README.md is too short")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def generate(self) -> Path:
        """
        Generate document template
        
        Returns:
            Path to generated template
        """
        # Generate README
        readme_content = textwrap.dedent(f'''
        # {self.name}
        
        ## Overview
        {self.config.get('description', 'A documentation template')}
        
        ### Version: {self.config.get('version', '0.1.0')}
        ### Author: {self.config.get('author', 'Unknown')}
        
        ## Getting Started
        
        ### Prerequisites
        
        ### Installation
        
        ### Usage
        
        ## Contributing
        
        ## License
        ''').strip()
        
        self._write_file('README.md', readme_content)
        
        # Generate metadata
        metadata_content = {
            'name': self.name,
            'version': self.config.get('version', '0.1.0'),
            'description': self.config.get('description', 'A documentation template'),
            'author': self.config.get('author', 'Unknown'),
            'category': 'document'
        }
        
        self._write_file('metadata.yml', yaml.safe_dump(metadata_content))
        
        # Generate template configuration
        config_content = {
            'template_type': 'document',
            'supported_formats': ['md', 'txt', 'rst'],
            'dependencies': []
        }
        
        self._write_file('template_config.json', json.dumps(config_content, indent=2))
        
        return self.base_path

# Register the template type
TemplateTypeRegistry.register('document', DocumentTemplateType)
