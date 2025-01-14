"""
Core infrastructure for template type management
"""

import os
import json
import yaml
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Type, Optional, List

class BaseTemplateType(ABC):
    """
    Abstract base class for template types
    Defines core methods for template generation and validation
    """
    
    def __init__(self, 
                 name: str, 
                 base_path: Path, 
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize template type with core configuration
        
        Args:
            name (str): Name of the template
            base_path (Path): Base directory for template generation
            config (dict, optional): Template-specific configuration
        """
        self.name = name
        self.base_path = base_path
        self.config = config or {}
        self.logger = logging.getLogger(f"template.{self.__class__.__name__}")
    
    @abstractmethod
    def validate(self) -> Dict[str, Any]:
        """
        Validate template type specific requirements
        
        Returns:
            Validation result dictionary
        """
        pass
    
    @abstractmethod
    def generate(self) -> Path:
        """
        Generate template with type-specific logic
        
        Returns:
            Path to generated template
        """
        pass
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename to prevent security issues
        
        Args:
            filename (str): Input filename
        
        Returns:
            Sanitized filename
        """
        return "".join(
            char if char.isalnum() or char in ['-', '_', '.'] 
            else '_' for char in filename
        ).rstrip('.')
    
    def _write_file(self, 
                    relative_path: str, 
                    content: str, 
                    mode: str = 'w') -> Path:
        """
        Safely write file within template directory
        
        Args:
            relative_path (str): Path relative to template base
            content (str): File content
            mode (str): File write mode
        
        Returns:
            Path to created file
        """
        safe_path = self.base_path / self._sanitize_filename(relative_path)
        
        # Ensure directory exists
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        safe_path.write_text(content)
        
        return safe_path

class TemplateTypeRegistry:
    """
    Dynamic template type registration and management
    """
    _types: Dict[str, Type[BaseTemplateType]] = {}
    
    @classmethod
    def register(cls, 
                 name: str, 
                 template_type: Type[BaseTemplateType]) -> None:
        """
        Register a new template type
        
        Args:
            name (str): Unique identifier for template type
            template_type (Type[BaseTemplateType]): Template type class
        """
        if name in cls._types:
            logging.warning(f"Overwriting existing template type: {name}")
        
        cls._types[name] = template_type
    
    @classmethod
    def get(cls, name: str) -> Optional[Type[BaseTemplateType]]:
        """
        Retrieve a registered template type
        
        Args:
            name (str): Template type name
        
        Returns:
            Registered template type or None
        """
        return cls._types.get(name)
    
    @classmethod
    def list_types(cls) -> List[str]:
        """
        List all registered template types
        
        Returns:
            List of registered template type names
        """
        return list(cls._types.keys())

def load_template_config(config_path: Path) -> Dict[str, Any]:
    """
    Load template configuration from JSON or YAML
    
    Args:
        config_path (Path): Path to configuration file
    
    Returns:
        Parsed configuration dictionary
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        if config_path.suffix in ['.json']:
            return json.loads(config_path.read_text())
        elif config_path.suffix in ['.yml', '.yaml']:
            return yaml.safe_load(config_path.read_text())
        else:
            raise ValueError(f"Unsupported configuration file type: {config_path.suffix}")
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        logging.error(f"Error parsing configuration: {e}")
        raise
