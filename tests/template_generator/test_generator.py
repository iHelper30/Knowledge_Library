"""
Comprehensive Test Suite for Template Generator
"""

import os
import shutil
import tempfile
import pytest
from pathlib import Path

from tools.template_generator import TemplateGenerator, TemplateValidator
from tools.template_generator.core import TemplateTypeRegistry

class TestTemplateGenerator:
    """
    Test suite for template generation functionality
    """
    
    @pytest.fixture
    def temp_output_dir(self):
        """
        Create a temporary directory for template generation
        """
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_generator_initialization(self):
        """
        Test template generator initialization
        """
        generator = TemplateGenerator()
        assert generator is not None
        
        # Check registered template types
        template_types = generator.list_template_types()
        assert len(template_types) > 0
        assert 'document' in template_types
        assert 'code' in template_types
        assert 'web_app' in template_types
    
    @pytest.mark.parametrize('template_type', [
        'document', 'code', 'web_app'
    ])
    def test_template_generation(self, temp_output_dir, template_type):
        """
        Test generation of different template types
        """
        generator = TemplateGenerator(output_dir=temp_output_dir)
        
        template_path = generator.generate(
            template_type=template_type,
            name=f'Test {template_type.replace("_", " ").title()}',
            version='0.1.0',
            author='Test User'
        )
        
        # Validate generated template
        validator = TemplateValidator()
        validation_result = validator.validate(template_path)
        
        assert validation_result['is_valid'], \
            f"Template validation failed: {validation_result.get('errors', [])}"
        
        # Check basic template structure
        assert template_path.exists()
        assert (template_path / 'README.md').exists()
        assert (template_path / 'metadata.yml').exists()
        assert (template_path / 'template_config.json').exists()
    
    def test_invalid_template_type(self):
        """
        Test generation with an invalid template type
        """
        generator = TemplateGenerator()
        
        with pytest.raises(ValueError, match="Unknown template type"):
            generator.generate(
                template_type='non_existent_type',
                name='Invalid Template'
            )
    
    def test_template_type_registration(self):
        """
        Test dynamic template type registration
        """
        class TestTemplateType:
            """
            Dummy template type for testing registration
            """
            def __init__(self, name, base_path, config=None):
                pass
            
            def validate(self):
                return {'is_valid': True, 'errors': []}
            
            def generate(self):
                return Path('dummy_path')
        
        # Register a new template type
        TemplateTypeRegistry.register('test_type', TestTemplateType)
        
        generator = TemplateGenerator()
        assert 'test_type' in generator.list_template_types()
    
    def test_generator_configuration(self, temp_output_dir):
        """
        Test generator configuration options
        """
        generator = TemplateGenerator(
            output_dir=temp_output_dir,
            config_dir=Path(__file__).parent / 'test_configs'
        )
        
        template_path = generator.generate(
            template_type='document',
            name='Configured Template',
            version='0.2.0',
            author='Config Tester'
        )
        
        # Check if configuration was applied
        metadata_path = template_path / 'metadata.yml'
        assert metadata_path.exists()
        
        # Optional: Add more specific configuration checks
        # This depends on your specific configuration loading logic

class TestTemplateValidator:
    """
    Test suite for template validation
    """
    
    @pytest.fixture
    def temp_output_dir(self):
        """
        Create a temporary directory for template generation
        """
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.mark.parametrize('template_type', [
        'document', 'code', 'web_app'
    ])
    def test_template_validation(self, temp_output_dir, template_type):
        """
        Test validation of generated templates
        """
        generator = TemplateGenerator(output_dir=temp_output_dir)
        validator = TemplateValidator()
        
        template_path = generator.generate(
            template_type=template_type,
            name=f'Validation Test {template_type.replace("_", " ").title()}',
            version='0.1.0',
            author='Validator'
        )
        
        validation_result = validator.validate(template_path)
        
        assert validation_result['is_valid'], \
            f"Template validation failed: {validation_result}"
    
    def test_invalid_template_validation(self, temp_output_dir):
        """
        Test validation of an intentionally malformed template
        """
        # Create an empty directory to simulate an invalid template
        invalid_template_path = temp_output_dir / 'invalid_template'
        invalid_template_path.mkdir()
        
        validator = TemplateValidator()
        validation_result = validator.validate(invalid_template_path)
        
        assert not validation_result['is_valid'], \
            "Empty directory should not pass validation"

def test_module_imports():
    """
    Verify that all template types can be imported
    """
    from tools.template_generator.types import document, code, web_app
    
    assert document is not None
    assert code is not None
    assert web_app is not None
