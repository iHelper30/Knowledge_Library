import os
import json
import logging
from logging.handlers import RotatingFileHandler
import markdown2
from flask import Flask, render_template, jsonify, send_from_directory, request, abort
from flask_cors import CORS
import re
import uuid
from datetime import datetime
from typing import Dict, Any

# Import custom modules
from .error_handler import handle_error, validate_request, create_error_response, TemplateGenerationError
from .cache import TemplateMetadataCache

# Initialize cache
template_metadata_cache = TemplateMetadataCache()

# Configure Logging
def setup_logging(app):
    """Set up application logging."""
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'knowledge_library.log')
    
    # Rotating File Handler
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    
    # Console Handler
    console_handler = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    # Set logging level
    app.logger.setLevel(logging.INFO)

app = Flask(__name__)
setup_logging(app)
CORS(app)

# Paths
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'Templates_NEW')
MARKDOWN_DIR = os.path.join(os.path.dirname(__file__), '..', 'Templates_Markdown')
GENERATED_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'Generated_Templates')

# Ensure generated templates directory exists
os.makedirs(GENERATED_TEMPLATES_DIR, exist_ok=True)

# Error Handler
@app.errorhandler(Exception)
def handle_global_error(error):
    """Global error handler for the application."""
    error_response = handle_error(error)
    return create_error_response(error_response)

def sanitize_filename(filename):
    """Create a safe filename."""
    # Remove non-alphanumeric characters and replace spaces
    sanitized = re.sub(r'[^\w\-_\. ]', '', filename)
    sanitized = sanitized.replace(' ', '_')
    return sanitized[:255]  # Limit filename length

def load_template_metadata(template_path: str) -> Dict[str, Any]:
    """
    Advanced metadata loading with comprehensive error handling.
    
    Args:
        template_path (str): Path to template directory
    
    Returns:
        Dictionary of template metadata
    """
    try:
        # Check for metadata.json in multiple potential locations
        metadata_candidates = [
            os.path.join(template_path, 'metadata.json'),
            os.path.join(template_path, '.metadata', 'template.json'),
            os.path.join(template_path, 'config', 'metadata.json')
        ]
        
        metadata = {}
        for candidate in metadata_candidates:
            if os.path.exists(candidate):
                with open(candidate, 'r') as f:
                    try:
                        metadata = json.load(f)
                        break
                    except json.JSONDecodeError:
                        app.logger.warning(f"Invalid JSON in {candidate}")
        
        # Fallback metadata generation if no metadata found
        if not metadata:
            metadata = {
                'name': os.path.basename(template_path),
                'type': 'generic',
                'description': 'Auto-generated metadata',
                'created_at': datetime.utcnow().isoformat()
            }
        
        # Enrich metadata with additional information
        metadata['file_count'] = len([f for f in os.listdir(template_path) if os.path.isfile(os.path.join(template_path, f))])
        metadata['directory_count'] = len([d for d in os.listdir(template_path) if os.path.isdir(os.path.join(template_path, d))])
        
        return metadata
    
    except Exception as e:
        app.logger.error(f"Metadata loading error for {template_path}: {e}")
        return {
            'name': os.path.basename(template_path),
            'type': 'error',
            'description': f'Metadata loading failed: {str(e)}'
        }

@app.route('/api/template_metadata/<template_name>')
def get_template_metadata(template_name: str):
    """
    Comprehensive template metadata retrieval endpoint with caching.
    
    Args:
        template_name (str): Name of the template
    
    Returns:
        JSON response with template metadata
    """
    try:
        template_path = os.path.join(TEMPLATES_DIR, template_name)
        
        if not os.path.exists(template_path):
            raise TemplateGenerationError(
                'Template not found', 
                details={'template_name': template_name}
            )
        
        # Use cached metadata
        metadata = template_metadata_cache.get_metadata(template_path)
        
        # Validate template structure
        from tools.template_generator.validator import TemplateValidator
        validation_report = TemplateValidator.validate_template_structure(template_path)
        
        metadata['validation'] = validation_report
        
        return jsonify(metadata), 200
    
    except Exception as e:
        app.logger.error(f"Metadata retrieval error: {e}")
        return create_error_response(handle_error(e))

@app.route('/generate_template', methods=['POST'])
def generate_template():
    """Advanced template generation endpoint with comprehensive error handling."""
    try:
        # Validate request
        validate_request(request, ['template_type', 'name'])
        
        data = request.get_json()
        template_type = data['template_type']
        template_name = sanitize_filename(data.get('name', f'New_{template_type}_Template'))
        
        # Validate template type
        from tools.template_generator.validator import TemplateValidator
        valid_types = ['web_app', 'document', 'script', 'data_analysis']
        
        if template_type not in valid_types:
            raise TemplateGenerationError(
                f"Invalid template type. Must be one of: {', '.join(valid_types)}",
                details={'allowed_types': valid_types}
            )
        
        # Generate template
        template_id = str(uuid.uuid4())
        generated_path = os.path.join(GENERATED_TEMPLATES_DIR, f"{template_id}_{template_name}")
        os.makedirs(generated_path, exist_ok=True)
        
        # Log successful generation
        log_template_generation(template_type, template_name, 'success')
        
        return jsonify({
            'status': 'success',
            'template_id': template_id,
            'path': generated_path,
            'message': f'Template {template_name} generated successfully'
        }), 201
    
    except TemplateGenerationError as e:
        # Specific error handling for template generation
        app.logger.warning(f"Template generation failed: {e.message}")
        return create_error_response(handle_error(e))
    
    except Exception as e:
        # Catch-all for unexpected errors
        app.logger.error(f"Unexpected error in template generation: {e}", exc_info=True)
        return create_error_response(handle_error(e))

@app.route('/')
def index():
    """Main index page showing available templates."""
    app.logger.info("Index page accessed")
    # List templates from both NEW and Markdown directories
    new_templates = [d for d in os.listdir(TEMPLATES_DIR) if os.path.isdir(os.path.join(TEMPLATES_DIR, d))]
    markdown_templates = [d for d in os.listdir(MARKDOWN_DIR) if d.endswith('.md')]
    
    return render_template('index.html', 
                           new_templates=new_templates, 
                           markdown_templates=markdown_templates)

@app.route('/template/<template_name>')
def view_template(template_name):
    """View a specific template."""
    app.logger.info(f"Template {template_name} accessed")
    # Check in NEW templates first
    new_template_path = os.path.join(TEMPLATES_DIR, template_name)
    markdown_template_path = os.path.join(MARKDOWN_DIR, template_name)
    
    if os.path.exists(new_template_path):
        # For NEW templates, look for README or template.md
        readme_path = os.path.join(new_template_path, 'README.md')
        template_path = os.path.join(new_template_path, 'template.md')
        
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                readme_content = markdown2.markdown(f.read())
        else:
            readme_content = "No README available"
        
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                template_content = markdown2.markdown(f.read())
        else:
            template_content = "No template content available"
        
        metadata = load_template_metadata(new_template_path)
        
    elif os.path.exists(markdown_template_path):
        # For Markdown templates
        with open(markdown_template_path, 'r') as f:
            template_content = markdown2.markdown(f.read())
        readme_content = "Markdown Template"
        metadata = {}
    
    else:
        app.logger.warning(f"Template {template_name} not found")
        return "Template not found", 404
    
    return render_template('template_view.html', 
                           template_name=template_name, 
                           readme_content=readme_content,
                           template_content=template_content,
                           metadata=metadata)

@app.route('/api/templates')
def list_templates():
    """API endpoint to list all templates."""
    app.logger.info("API: Templates listed")
    new_templates = [d for d in os.listdir(TEMPLATES_DIR) if os.path.isdir(os.path.join(TEMPLATES_DIR, d))]
    markdown_templates = [d for d in os.listdir(MARKDOWN_DIR) if d.endswith('.md')]
    
    return jsonify({
        'new_templates': new_templates,
        'markdown_templates': markdown_templates
    })

@app.route('/api/template_types')
def list_template_types():
    """List available template types."""
    app.logger.info("API: Template types listed")
    types = [d for d in os.listdir(TEMPLATES_DIR) if os.path.isdir(os.path.join(TEMPLATES_DIR, d))]
    return jsonify(types)

@app.route('/api/template_preview/<template_name>')
def template_preview(template_name):
    """Provide a lightweight preview of a template."""
    app.logger.info(f"API: Template {template_name} preview requested")
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    
    if not os.path.exists(template_path):
        app.logger.warning(f"Template {template_name} not found")
        abort(404, description="Template not found")
    
    metadata = load_template_metadata(template_path)
    
    # Extract preview content
    preview = {
        'name': metadata['name'],
        'file_count': len(metadata['files']),
        'type': metadata['config'].get('template_type', 'Unknown'),
        'description': metadata['config'].get('description', 'No description available')
    }
    
    return jsonify(preview)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Lightweight health check endpoint for deployment platforms.
    
    Returns:
        JSON response with system status
    """
    from datetime import datetime
    import os
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'checks': {
            'database': 'not_applicable',
            'templates_dir': os.path.exists(TEMPLATES_DIR)
        }
    }), 200

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    app.logger.info(f"Static file {filename} served")
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), filename)

def log_template_generation(template_type, template_name, status):
    """Log template generation events."""
    log_entry = {
        'event': 'template_generation',
        'timestamp': datetime.utcnow().isoformat(),
        'template_type': template_type,
        'template_name': template_name,
        'status': status
    }
    app.logger.info(json.dumps(log_entry))

if __name__ == '__main__':
    # Create templates directory if not exists
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    os.makedirs(MARKDOWN_DIR, exist_ok=True)
    
    # Ensure static directory exists
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    os.makedirs(static_dir, exist_ok=True)
    
    app.run(debug=True, port=8000)
