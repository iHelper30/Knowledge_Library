#!/usr/bin/env python3
import os
import sys
import io
import json
import yaml
import argparse
import textwrap
from typing import Dict, List, Optional
from datetime import datetime

# Set stdout to handle Unicode
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class TemplateGenerator:
    """
    Advanced template generation utility with expanded template type support
    """
    TEMPLATE_TYPES = {
        'document': {
            'formats': ['md', 'txt', 'rst', 'adoc'],
            'description': 'Text-based documentation template',
            'default_structure': {
                'sections': ['introduction', 'content', 'conclusion'],
                'files': ['README.md', 'CHANGELOG.md']
            }
        },
        'presentation': {
            'formats': ['pptx', 'key', 'pdf', 'odp'],
            'description': 'Slide deck and presentation template',
            'default_structure': {
                'sections': ['title', 'content', 'appendix'],
                'files': ['slides.md', 'speaker_notes.txt']
            }
        },
        'code': {
            'formats': ['py', 'js', 'ts', 'java', 'cpp', 'go'],
            'description': 'Programming project template',
            'default_structure': {
                'sections': ['src', 'tests', 'docs'],
                'files': ['main.py', 'requirements.txt', '.gitignore']
            }
        },
        'script': {
            'formats': ['sh', 'bat', 'ps1', 'py'],
            'description': 'Automation and utility script template',
            'default_structure': {
                'sections': ['scripts', 'config', 'logs'],
                'files': ['main.sh', 'config.yml', 'README.md']
            }
        },
        'configuration': {
            'formats': ['yml', 'yaml', 'json', 'toml', 'ini'],
            'description': 'Configuration and settings template',
            'default_structure': {
                'sections': ['environments', 'settings', 'secrets'],
                'files': ['config.yml', 'README.md']
            }
        },
        # Extensible: Add more template types here
        'data_science': {
            'formats': ['ipynb', 'py', 'r'],
            'description': 'Data science and machine learning project',
            'default_structure': {
                'sections': ['notebooks', 'data', 'models', 'reports'],
                'files': ['requirements.txt', 'README.md', 'main.ipynb']
            }
        },
        'web_app': {
            'formats': ['html', 'js', 'css', 'py', 'ts'],
            'description': 'Web application project template',
            'default_structure': {
                'sections': ['frontend', 'backend', 'tests', 'docs'],
                'files': ['index.html', 'app.py', 'requirements.txt']
            }
        }
    }

    def __init__(self, 
                 template_name: str, 
                 output_dir: str = 'Templates_NEW',
                 template_type: str = 'document'):
        """
        Initialize template generator with advanced options
        """
        self.template_name = self._sanitize_name(template_name)
        self.output_dir = os.path.abspath(output_dir)
        
        # Validate and set template type
        self.template_type = template_type.lower()
        if self.template_type not in self.TEMPLATE_TYPES:
            print(f"Warning: Unknown template type '{template_type}'. Defaulting to 'document'.")
            self.template_type = 'document'
        
        self.template_config = self.TEMPLATE_TYPES[self.template_type]
        self.template_path = os.path.join(self.output_dir, self.template_name)
    
    @staticmethod
    def _sanitize_name(name: str) -> str:
        """
        Sanitize template name for filesystem
        
        Args:
            name (str): Input template name
        
        Returns:
            Sanitized template name
        """
        # Remove special characters, replace spaces with underscores
        return ''.join(
            char if char.isalnum() or char in ['_', '-'] else '_' 
            for char in name
        ).strip('_')
    
    def _create_readme(self) -> str:
        """
        Create README.md for the template
        
        Returns:
            Path to created README
        """
        readme_content = textwrap.dedent(f'''
        # {self.template_name.replace('_', ' ').title()}

        ## Overview
        A {self.template_config['description']} generated on {datetime.now().strftime('%Y-%m-%d')}.

        ## Usage
        [Provide detailed usage instructions]

        ## Requirements
        - [List any specific requirements]

        ## Installation
        [Describe installation steps]

        ## Contributing
        [Guidelines for contributing to this template]

        ## License
        [Specify license information]
        ''').strip()
        
        readme_path = os.path.join(self.template_path, 'README.md')
        os.makedirs(os.path.dirname(readme_path), exist_ok=True)
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        return readme_path
    
    def _create_metadata(self, 
                          version: str = '0.1.0', 
                          author: Optional[str] = None) -> str:
        """
        Create metadata.yml for the template
        
        Args:
            version (str): Template version
            author (str, optional): Template author
        
        Returns:
            Path to created metadata file
        """
        metadata = {
            'name': self.template_name.replace('_', ' ').title(),
            'version': version,
            'description': self.template_config['description'],
            'category': self.template_type,
        }
        
        if author:
            metadata['author'] = author
        
        metadata_path = os.path.join(self.template_path, 'metadata.yml')
        
        with open(metadata_path, 'w') as f:
            yaml.safe_dump(metadata, f, default_flow_style=False)
        
        return metadata_path
    
    def _create_template_config(self, 
                                 supported_formats: Optional[List[str]] = None,
                                 dependencies: Optional[List[Dict]] = None) -> str:
        """
        Create template_config.json
        
        Args:
            supported_formats (List[str], optional): Supported file formats
            dependencies (List[Dict], optional): Template dependencies
        
        Returns:
            Path to created config file
        """
        config = {
            'template_type': self.template_type,
            'supported_formats': supported_formats or self.template_config['formats'],
            'dependencies': dependencies or [],
            'compatibility': {
                'platforms': ['web', 'windows', 'linux', 'macos'],
                'min_version': '0.1.0'
            }
        }
        
        config_path = os.path.join(self.template_path, 'template_config.json')
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config_path
    
    def _create_assets_dir(self) -> str:
        """
        Create assets directory with placeholder
        
        Returns:
            Path to assets directory
        """
        assets_path = os.path.join(self.template_path, 'assets')
        os.makedirs(assets_path, exist_ok=True)
        
        # Create a placeholder file
        with open(os.path.join(assets_path, '.gitkeep'), 'w') as f:
            f.write("# Placeholder to keep empty directory in version control")
        
        return assets_path
    
    def generate(self, 
                 version: str = '0.1.0', 
                 author: Optional[str] = None,
                 supported_formats: Optional[List[str]] = None,
                 dependencies: Optional[List[Dict]] = None,
                 include_sections: bool = True) -> Dict[str, str]:
        """
        Enhanced template generation with more customization
        """
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create template directory
        os.makedirs(self.template_path, exist_ok=True)
        
        # Create sections if requested
        if include_sections:
            for section in self.template_config['default_structure']['sections']:
                section_path = os.path.join(self.template_path, section)
                os.makedirs(section_path, exist_ok=True)
                
                # Add placeholder files in sections
                with open(os.path.join(section_path, '.gitkeep'), 'w') as f:
                    f.write("# Placeholder for section")
        
        # Generate template files
        generated_files = {
            'readme': self._create_readme(),
            'metadata': self._create_metadata(version, author),
            'config': self._create_template_config(
                supported_formats or self.template_config['formats'], 
                dependencies
            ),
            'assets': self._create_assets_dir()
        }
        
        # Create default files for the template type
        for default_file in self.template_config['default_structure']['files']:
            file_path = os.path.join(self.template_path, default_file)
            with open(file_path, 'w') as f:
                f.write(f"# {default_file} for {self.template_name}")
        
        print(f"✅ Template '{self.template_name}' generated successfully in {self.template_path}")
        return generated_files

def main():
    """
    CLI for template generation with more options
    """
    parser = argparse.ArgumentParser(description='Generate a compliant project template')
    
    parser.add_argument('name', 
                        help='Name of the template (will be sanitized)')
    parser.add_argument('-t', '--type', 
                        choices=list(TemplateGenerator.TEMPLATE_TYPES.keys()),
                        default='document', 
                        help='Type of template')
    parser.add_argument('-o', '--output', 
                        default='Templates_NEW', 
                        help='Output directory for template')
    parser.add_argument('-v', '--version', 
                        default='0.1.0', 
                        help='Initial template version')
    parser.add_argument('-a', '--author', 
                        help='Template author name')
    parser.add_argument('--no-sections', 
                        action='store_false', 
                        dest='include_sections',
                        help='Disable automatic section creation')
    
    args = parser.parse_args()
    
    try:
        generator = TemplateGenerator(
            template_name=args.name, 
            output_dir=args.output, 
            template_type=args.type
        )
        
        generator.generate(
            version=args.version,
            author=args.author,
            include_sections=args.include_sections
        )
    
    except Exception as e:
        print(f"❌ Template generation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
