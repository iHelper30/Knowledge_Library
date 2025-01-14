#!/usr/bin/env python3
import os
import sys
import json
import yaml
import argparse
import jsonschema
from typing import Dict, List, Any

class TemplateValidator:
    """
    Comprehensive template validation utility
    """
    def __init__(self, template_path: str, schema_path: str = None):
        """
        Initialize template validator
        
        Args:
            template_path (str): Path to template directory
            schema_path (str, optional): Path to JSON schema
        """
        self.template_path = os.path.abspath(template_path)
        self.schema_path = schema_path or os.path.join(
            os.path.dirname(__file__), 'template_schema.json'
        )
        
        # Validate template path exists
        if not os.path.isdir(self.template_path):
            raise ValueError(f"Invalid template path: {self.template_path}")
    
    def _load_json_schema(self) -> Dict[str, Any]:
        """
        Load JSON schema for validation
        
        Returns:
            Parsed JSON schema
        """
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ Schema loading error: {e}")
            sys.exit(1)
    
    def validate_file_structure(self) -> Dict[str, Any]:
        """
        Validate basic template file structure
        
        Returns:
            Validation results dictionary
        """
        required_files = [
            'README.md', 
            'metadata.yml', 
            'template_config.json'
        ]
        
        results = {
            'is_valid': True,
            'missing_files': [],
            'details': {}
        }
        
        for file in required_files:
            file_path = os.path.join(self.template_path, file)
            if not os.path.exists(file_path):
                results['is_valid'] = False
                results['missing_files'].append(file)
                results['details'][file] = 'Missing'
            else:
                results['details'][file] = 'Present'
        
        return results
    
    def validate_metadata(self) -> Dict[str, Any]:
        """
        Validate metadata.yml content
        
        Returns:
            Validation results dictionary
        """
        results = {
            'is_valid': True,
            'errors': [],
            'details': {}
        }
        
        try:
            with open(os.path.join(self.template_path, 'metadata.yml'), 'r') as f:
                metadata = yaml.safe_load(f)
            
            required_fields = ['name', 'version', 'description', 'category']
            
            for field in required_fields:
                if field not in metadata:
                    results['is_valid'] = False
                    results['errors'].append(f"Missing required field: {field}")
                    results['details'][field] = 'Missing'
                else:
                    results['details'][field] = metadata[field]
            
            # Version validation
            if 'version' in metadata:
                try:
                    # Basic semantic versioning check
                    version_parts = metadata['version'].split('.')
                    if len(version_parts) != 3 or not all(part.isdigit() for part in version_parts):
                        results['is_valid'] = False
                        results['errors'].append("Invalid version format. Use semantic versioning (x.y.z)")
                except Exception:
                    results['is_valid'] = False
                    results['errors'].append("Invalid version format")
        
        except (FileNotFoundError, yaml.YAMLError) as e:
            results['is_valid'] = False
            results['errors'].append(f"Metadata parsing error: {e}")
        
        return results
    
    def validate_template_config(self) -> Dict[str, Any]:
        """
        Validate template_config.json content
        
        Returns:
            Validation results dictionary
        """
        results = {
            'is_valid': True,
            'errors': [],
            'details': {}
        }
        
        try:
            with open(os.path.join(self.template_path, 'template_config.json'), 'r') as f:
                config = json.load(f)
            
            # Load JSON schema
            schema = self._load_json_schema()
            
            try:
                # Validate against schema
                jsonschema.validate(instance=config, schema=schema)
            except jsonschema.ValidationError as e:
                results['is_valid'] = False
                results['errors'].append(f"Schema validation failed: {e}")
            
            results['details'] = config
        
        except (FileNotFoundError, json.JSONDecodeError) as e:
            results['is_valid'] = False
            results['errors'].append(f"Configuration parsing error: {e}")
        
        return results
    
    def validate(self) -> Dict[str, Any]:
        """
        Comprehensive template validation
        
        Returns:
            Complete validation report
        """
        file_structure = self.validate_file_structure()
        metadata = self.validate_metadata()
        template_config = self.validate_template_config()
        
        overall_validation = {
            'is_valid': all([
                file_structure['is_valid'],
                metadata['is_valid'],
                template_config['is_valid']
            ]),
            'file_structure': file_structure,
            'metadata': metadata,
            'template_config': template_config
        }
        
        return overall_validation

def main():
    """
    CLI for template validation
    """
    parser = argparse.ArgumentParser(description='Validate project template')
    
    parser.add_argument('template_path', 
                        help='Path to template directory')
    parser.add_argument('-s', '--schema', 
                        help='Path to custom JSON schema')
    parser.add_argument('-o', '--output', 
                        help='Output validation report file')
    
    args = parser.parse_args()
    
    try:
        validator = TemplateValidator(
            template_path=args.template_path, 
            schema_path=args.schema
        )
        
        validation_report = validator.validate()
        
        # Print results to console
        print(json.dumps(validation_report, indent=2))
        
        # Optionally write to file
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(validation_report, f, indent=2)
        
        # Exit with appropriate status
        sys.exit(0 if validation_report['is_valid'] else 1)
    
    except Exception as e:
        print(f"❌ Template validation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
