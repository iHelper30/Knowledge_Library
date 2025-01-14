"""
Command Line Interface for Template Generator
"""

import os
import sys
import json
import logging
import click
from pathlib import Path
from typing import Optional, List, Dict, Any

from .generator import TemplateGenerator
from .validator import TemplateValidator
from .core import TemplateTypeRegistry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('template_generator_cli')

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(verbose):
    """
    Template Generator CLI
    
    Generate, validate, and manage project templates
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

@cli.command()
@click.option('--type', '-t', required=True, help='Template type to generate')
@click.option('--name', '-n', required=True, help='Name of the template')
@click.option('--output', '-o', 
              default='Templates', 
              help='Output directory for generated template')
@click.option('--version', '-V', default='0.1.0', help='Template version')
@click.option('--author', '-a', default=None, help='Template author')
@click.option('--config', '-c', 
              type=click.Path(exists=True), 
              help='Path to additional configuration file')
def generate(
    type: str, 
    name: str, 
    output: str, 
    version: str, 
    author: Optional[str],
    config: Optional[str]
):
    """
    Generate a new project template
    """
    try:
        # Resolve output path
        output_path = Path(output).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Load additional configuration if provided
        extra_config = {}
        if config:
            with open(config, 'r') as f:
                extra_config = json.load(f)
        
        # Initialize generator
        generator = TemplateGenerator(output_dir=output_path)
        
        # Generate template
        template_path = generator.generate(
            template_type=type,
            name=name,
            version=version,
            author=author or os.getlogin(),
            **extra_config
        )
        
        click.echo(f"✅ Template generated successfully: {template_path}")
    except Exception as e:
        logger.error(f"Template generation failed: {e}")
        sys.exit(1)

@cli.command()
@click.argument('template_paths', nargs=-1, type=click.Path(exists=True))
@click.option('--output', '-o', 
              type=click.Path(), 
              help='Path to output validation report')
@click.option('--format', '-f', 
              type=click.Choice(['json', 'text']), 
              default='text', 
              help='Output format for validation report')
def validate(
    template_paths: List[str], 
    output: Optional[str],
    format: str
):
    """
    Validate one or more project templates
    """
    validator = TemplateValidator()
    validation_results = {}
    
    for path in template_paths:
        template_path = Path(path)
        
        try:
            result = validator.validate(template_path)
            validation_results[str(template_path)] = result
            
            # Print immediate results
            click.echo(f"Validating {template_path}:")
            click.echo(f"  Valid: {result['is_valid']}")
            
            if not result['is_valid']:
                click.echo("  Errors:")
                for error in result.get('errors', []):
                    click.echo(f"    - {error}")
        
        except Exception as e:
            logger.error(f"Validation failed for {path}: {e}")
            validation_results[str(template_path)] = {
                'is_valid': False,
                'errors': [str(e)]
            }
    
    # Output report if requested
    if output:
        output_path = Path(output)
        
        if format == 'json':
            with output_path.open('w') as f:
                json.dump(validation_results, f, indent=2)
        else:
            with output_path.open('w') as f:
                for path, result in validation_results.items():
                    f.write(f"Template: {path}\n")
                    f.write(f"  Valid: {result['is_valid']}\n")
                    if not result['is_valid']:
                        f.write("  Errors:\n")
                        for error in result.get('errors', []):
                            f.write(f"    - {error}\n")
        
        click.echo(f"Validation report saved to {output_path}")

@cli.command()
def list_types():
    """
    List available template types
    """
    types = TemplateTypeRegistry.list_types()
    
    click.echo("Available Template Types:")
    for template_type in types:
        click.echo(f"  - {template_type}")

@cli.command()
@click.argument('template_type', required=True)
def describe(template_type: str):
    """
    Describe a specific template type
    """
    template_class = TemplateTypeRegistry.get(template_type)
    
    if not template_class:
        click.echo(f"Error: Template type '{template_type}' not found.")
        sys.exit(1)
    
    # Use docstring as description
    description = template_class.__doc__ or "No description available."
    
    click.echo(f"Template Type: {template_type}")
    click.echo("Description:")
    click.echo(description)

def main():
    """
    Entry point for the CLI
    """
    cli()
