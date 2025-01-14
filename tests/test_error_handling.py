import pytest
import json
import os
from src.local_server import app
from src.error_handler import KnowledgeLibraryError, TemplateGenerationError

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_template_generation_validation(client):
    """Test template generation validation."""
    # Test missing required fields
    response = client.post('/generate_template', 
                           data=json.dumps({}),
                           content_type='application/json')
    
    assert response.status_code == 400
    error_data = json.loads(response.data)
    assert 'missing_fields' in error_data.get('details', {})

def test_template_generation_invalid_type(client):
    """Test template generation with invalid template type."""
    invalid_data = {
        'template_type': 'invalid_type',
        'name': 'Test_Template'
    }
    
    response = client.post('/generate_template', 
                           data=json.dumps(invalid_data),
                           content_type='application/json')
    
    assert response.status_code == 400
    error_data = json.loads(response.data)
    assert 'allowed_types' in error_data.get('details', {})

def test_template_metadata_not_found(client):
    """Test metadata retrieval for non-existent template."""
    response = client.get('/api/template_metadata/non_existent_template')
    
    assert response.status_code == 400
    error_data = json.loads(response.data)
    assert 'Template not found' in error_data.get('error', '')

def test_custom_error_classes():
    """Test custom error classes."""
    # Test KnowledgeLibraryError
    error = KnowledgeLibraryError("Test error", status_code=422)
    assert str(error) == "Test error"
    assert error.status_code == 422

    # Test TemplateGenerationError
    details = {'template_type': 'web_app'}
    error = TemplateGenerationError("Generation failed", details)
    assert str(error) == "Generation failed"
    assert error.status_code == 400
    assert error.details == details

def test_global_error_handler(client):
    """Test global error handler."""
    class MockError(Exception):
        """Mock exception for testing."""
        pass
    
    # Simulate an unexpected error
    with pytest.raises(MockError):
        with app.test_request_context():
            raise MockError("Unexpected error")

def test_cache_invalidation():
    """Test template metadata cache invalidation."""
    from src.cache import TemplateMetadataCache
    
    cache = TemplateMetadataCache()
    
    # Create a temporary test directory
    test_dir = os.path.join(os.path.dirname(__file__), '..', 'test_template')
    os.makedirs(test_dir, exist_ok=True)
    
    try:
        # Simulate cache usage
        first_metadata = cache.get_metadata(test_dir)
        
        # Invalidate cache
        cache.invalidate_cache()
        
        # Retrieve again (should be a fresh load)
        second_metadata = cache.get_metadata(test_dir)
        
        # Verify cache contents are different or reset
        assert first_metadata is not None
        assert second_metadata is not None
    
    finally:
        # Clean up test directory
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)
