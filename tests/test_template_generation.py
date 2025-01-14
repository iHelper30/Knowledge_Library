import os
import json
import pytest
from src.local_server import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_template_types_endpoint(client):
    """Test the template types API endpoint."""
    response = client.get('/api/template_types')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0, "No template types found"

def test_template_generation(client):
    """Test template generation endpoint."""
    template_data = {
        'template_type': 'document',
        'name': 'Test_Template'
    }
    
    response = client.post('/generate_template', 
                           data=json.dumps(template_data),
                           content_type='application/json')
    
    assert response.status_code == 201
    
    result = json.loads(response.data)
    assert result['status'] == 'success'
    assert 'template_id' in result
    assert 'path' in result

def test_invalid_template_generation(client):
    """Test template generation with invalid data."""
    invalid_data = {}
    
    response = client.post('/generate_template', 
                           data=json.dumps(invalid_data),
                           content_type='application/json')
    
    assert response.status_code == 400

def test_template_preview(client):
    """Test template preview endpoint."""
    # Assumes at least one template exists
    response = client.get('/api/template_types')
    template_types = json.loads(response.data)
    
    if template_types:
        first_template = template_types[0]
        preview_response = client.get(f'/api/template_preview/{first_template}')
        
        assert preview_response.status_code == 200
        
        preview_data = json.loads(preview_response.data)
        assert 'name' in preview_data
        assert 'file_count' in preview_data
        assert 'type' in preview_data
        assert 'description' in preview_data

def test_log_file_creation():
    """Verify log file is created during template generation."""
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    log_file = os.path.join(log_dir, 'knowledge_library.log')
    
    assert os.path.exists(log_dir), "Logs directory not created"
    assert os.path.exists(log_file), "Log file not created"

def test_generated_templates_directory():
    """Check generated templates directory exists."""
    generated_dir = os.path.join(os.path.dirname(__file__), '..', 'Generated_Templates')
    
    assert os.path.exists(generated_dir), "Generated templates directory not created"
    assert os.path.isdir(generated_dir), "Generated templates path is not a directory"
