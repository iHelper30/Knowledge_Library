"""
Template Validation Utility
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional

import jsonschema
import yaml

from .core import TemplateTypeRegistry

class TemplateValidator:
    """
    Comprehensive template validation manager
    """
    
    def __init__(self, 
                 schema_dir: Optional[Path] = None):
        """
        Initialize template validator
        
        Args:
            schema_dir (Path, optional): Directory containing validation schemas
        """
        self.schema_dir = schema_dir or Path(__file__).parent / 'schemas'
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _load_schema(self, template_type: str) -> Dict[str, Any]:
        """
        Load JSON schema for template type
        
        Args:
            template_type (str): Template type to validate
        
        Returns:
            Validation JSON schema
        """
        schema_path = self.schema_dir / f"{template_type}_schema.json"
        
        if not schema_path.exists():
            self.logger.warning(f"No schema found for type: {template_type}")
            return {}
        
        try:
            with open(schema_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Schema loading error: {e}")
            return {}
    
    def validate(self, 
                 template_path: Path, 
                 template_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a generated template
        
        Args:
            template_path (Path): Path to template directory
            template_type (str, optional): Specific template type to validate against
        
        Returns:
            Validation result dictionary
        """
        # Detect template type if not provided
        if not template_type:
            template_type = self._detect_template_type(template_path)
        
        # Get template type class
        template_class = TemplateTypeRegistry.get(template_type)
        if not template_class:
            return {
                'is_valid': False,
                'errors': [f"Unknown template type: {template_type}"]
            }
        
        # Instantiate template for validation
        template_instance = template_class(
            name=template_path.name,
            base_path=template_path
        )
        
        # Perform type-specific validation
        type_validation = template_instance.validate()
        
        # Perform schema validation if schema exists
        schema = self._load_schema(template_type)
        schema_errors = self._validate_against_schema(template_path, schema)
        
        return {
            'is_valid': type_validation['is_valid'] and not schema_errors,
            'type_validation': type_validation,
            'schema_errors': schema_errors
        }
    
    def _detect_template_type(self, template_path: Path) -> Optional[str]:
        """
        Attempt to detect template type based on directory structure
        
        Args:
            template_path (Path): Path to template directory
        
        Returns:
            Detected template type or None
        """
        # Implement type detection logic
        # This is a placeholder and should be expanded
        for template_type in TemplateTypeRegistry.list_types():
            # Add specific detection criteria
            if (template_path / f"{template_type}_specific_marker").exists():
                return template_type
        
        return None
    
    def _validate_against_schema(self, 
                                  template_path: Path, 
                                  schema: Dict[str, Any]) -> Optional[str]:
        """
        Validate template against JSON schema
        
        Args:
            template_path (Path): Path to template
            schema (dict): JSON schema
        
        Returns:
            Error message or None if valid
        """
        if not schema:
            return None
        
        try:
            # Implement schema validation logic
            jsonschema.validate(
                instance=self._load_template_metadata(template_path),
                schema=schema
            )
            return None
        except jsonschema.ValidationError as e:
            return str(e)
    
    def _load_template_metadata(self, template_path: Path) -> Dict[str, Any]:
        """
        Load template metadata
        
        Args:
            template_path (Path): Path to template directory
        
        Returns:
            Metadata dictionary
        """
        metadata_path = template_path / 'metadata.yml'
        
        if not metadata_path.exists():
            return {}
        
        try:
            with open(metadata_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Metadata loading error: {e}")
            return {}
