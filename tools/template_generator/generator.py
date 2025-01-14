"""
Template Generation Utility
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from .core import TemplateTypeRegistry, load_template_config, BaseTemplateType

class TemplateGenerator:
    """
    Centralized template generation manager
    """
    
    def __init__(self, 
                 output_dir: Path = Path('Templates_NEW'),
                 config_dir: Optional[Path] = None):
        """
        Initialize template generator
        
        Args:
            output_dir (Path): Base directory for generated templates
            config_dir (Path, optional): Directory containing template type configurations
        """
        self.output_dir = output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_dir = config_dir or Path(__file__).parent / 'types'
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _load_type_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Load template type configurations
        
        Returns:
            Dictionary of template type configurations
        """
        type_configs = {}
        
        if not self.config_dir.exists():
            self.logger.warning(f"Configuration directory not found: {self.config_dir}")
            return type_configs
        
        for config_file in self.config_dir.glob('*.json'):
            try:
                type_name = config_file.stem
                type_configs[type_name] = load_template_config(config_file)
            except Exception as e:
                self.logger.error(f"Error loading config for {type_name}: {e}")
        
        return type_configs
    
    def generate(self, 
                 template_type: str, 
                 name: str, 
                 version: str = '0.1.0',
                 author: Optional[str] = None) -> Path:
        """
        Generate a template of specified type
        
        Args:
            template_type (str): Type of template to generate
            name (str): Name of the template
            version (str): Template version
            author (str, optional): Template author
        
        Returns:
            Path to generated template
        """
        # Validate template type
        template_class = TemplateTypeRegistry.get(template_type)
        if not template_class:
            raise ValueError(f"Unknown template type: {template_type}")
        
        # Load type-specific configuration
        type_configs = self._load_type_configs()
        type_config = type_configs.get(template_type, {})
        
        # Create template-specific output directory
        template_path = self.output_dir / f"{name}_{template_type}"
        template_path.mkdir(parents=True, exist_ok=True)
        
        # Instantiate and generate template
        template_instance = template_class(
            name=name,
            base_path=template_path,
            config={
                'version': version,
                'author': author,
                **type_config
            }
        )
        
        generated_path = template_instance.generate()
        
        self.logger.info(f"Generated template: {generated_path}")
        return generated_path
    
    def list_template_types(self) -> List[str]:
        """
        List available template types
        
        Returns:
            List of registered template type names
        """
        return TemplateTypeRegistry.list_types()
