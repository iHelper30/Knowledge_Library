"""
Code Project Template Type Implementation
"""

import os
import json
import textwrap
import yaml
from pathlib import Path
from typing import Dict, Any

from ..core import BaseTemplateType, TemplateTypeRegistry

class CodeTemplateType(BaseTemplateType):
    """
    Specialized template type for code projects
    """
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate code project template specific requirements
        
        Returns:
            Validation result dictionary
        """
        errors = []
        
        # Check for required files and directories
        required_files = [
            'README.md',
            'requirements.txt',
            'setup.py',
            'src',
            'tests'
        ]
        
        for item in required_files:
            path = self.base_path / item
            if not path.exists():
                errors.append(f"Missing required item: {item}")
        
        # Check source code structure
        src_path = self.base_path / 'src'
        if src_path.exists():
            if not any(src_path.iterdir()):
                errors.append("Source directory is empty")
        
        # Check test coverage
        tests_path = self.base_path / 'tests'
        if tests_path.exists():
            test_files = list(tests_path.glob('test_*.py'))
            if len(test_files) < 1:
                errors.append("No test files found")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def generate(self) -> Path:
        """
        Generate code project template
        
        Returns:
            Path to generated template
        """
        # Determine primary language
        language = self.config.get('language', 'python')
        
        # README
        readme_content = textwrap.dedent(f'''
        # {self.name}

        ## Project Overview
        {self.config.get('description', 'A code project template')}

        ### Version: {self.config.get('version', '0.1.0')}
        ### Author: {self.config.get('author', 'Unknown')}

        ## Setup and Installation

        ### Prerequisites
        - {language.capitalize()}
        - pip/poetry

        ### Installation
        ```bash
        # Clone the repository
        git clone <repository_url>
        cd {self.name}

        # Install dependencies
        pip install -r requirements.txt
        ```

        ## Development

        ### Running Tests
        ```bash
        pytest tests/
        ```

        ### Contributing
        1. Fork the repository
        2. Create your feature branch
        3. Commit your changes
        4. Push to the branch
        5. Create a Pull Request

        ## License
        {self.config.get('license', 'MIT License')}
        ''').strip()
        
        self._write_file('README.md', readme_content)
        
        # Requirements
        requirements_content = '\n'.join([
            'pytest',
            'coverage',
            'flake8',
            'mypy'
        ])
        self._write_file('requirements.txt', requirements_content)
        
        # Setup.py
        setup_content = {
            'name': self.name.lower().replace(' ', '_'),
            'version': self.config.get('version', '0.1.0'),
            'description': self.config.get('description', 'A code project'),
            'author': self.config.get('author', 'Unknown'),
            'packages': ['src'],
            'install_requires': []
        }
        self._write_file('setup.py', json.dumps(setup_content, indent=2))
        
        # Source directory structure
        src_path = self.base_path / 'src'
        src_path.mkdir(exist_ok=True)
        (src_path / '__init__.py').touch()
        
        # Main module
        main_module_content = textwrap.dedent('''
        """
        Main module for the project
        """

        def main():
            """
            Entry point for the application
            """
            print("Hello from the project!")

        if __name__ == "__main__":
            main()
        ''').strip()
        self._write_file('src/main.py', main_module_content)
        
        # Tests directory
        tests_path = self.base_path / 'tests'
        tests_path.mkdir(exist_ok=True)
        (tests_path / '__init__.py').touch()
        
        # Sample test
        test_content = textwrap.dedent('''
        """
        Sample test module
        """

        def test_main():
            """
            Placeholder test
            """
            assert True
        ''').strip()
        self._write_file('tests/test_main.py', test_content)
        
        # Metadata
        metadata_content = {
            'name': self.name,
            'version': self.config.get('version', '0.1.0'),
            'description': self.config.get('description', 'A code project template'),
            'author': self.config.get('author', 'Unknown'),
            'category': 'code',
            'language': language
        }
        self._write_file('metadata.yml', yaml.safe_dump(metadata_content))
        
        # Template configuration
        config_content = {
            'template_type': 'code',
            'supported_formats': ['py', 'md', 'txt'],
            'dependencies': [
                {'name': 'pytest', 'version': '7.3.1', 'type': 'python'}
            ]
        }
        self._write_file('template_config.json', json.dumps(config_content, indent=2))
        
        return self.base_path

# Register the template type
TemplateTypeRegistry.register('code', CodeTemplateType)
