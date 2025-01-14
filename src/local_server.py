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
from werkzeug.exceptions import HTTPException

# Import custom modules
from .error_handler import handle_error, validate_request, create_error_response, TemplateGenerationError
from .cache import TemplateMetadataCache
from .static.favicon import serve_favicon  # Import favicon handler

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

# Favicon handling with robust error management
def create_default_favicon(static_dir):
    """
    Create a default favicon if one doesn't exist
    
    Args:
        static_dir (str): Directory to save favicon
    
    Returns:
        str: Path to favicon file
    """
    try:
        from PIL import Image, ImageDraw
        import os
        
        # Ensure static directory exists
        os.makedirs(static_dir, exist_ok=True)
        favicon_path = os.path.join(static_dir, 'favicon.ico')
        
        # Create favicon only if it doesn't exist
        if not os.path.exists(favicon_path):
            icon = Image.new('RGBA', (16, 16), (255, 255, 255, 0))
            draw = ImageDraw.Draw(icon)
            draw.rectangle([0, 0, 15, 15], fill=(33, 150, 243, 255))  # Material Blue
            icon.save(favicon_path, 'ICO')
        
        return favicon_path
    
    except Exception as e:
        app.logger.error(f"Favicon creation error: {e}")
        return None

# Add favicon route after app initialization
def setup_favicon(app):
    """
    Set up favicon route with error handling
    
    Args:
        app (Flask): Flask application instance
    """
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    
    @app.route('/favicon.ico')
    def favicon():
        try:
            favicon_path = create_default_favicon(static_dir)
            
            if favicon_path and os.path.exists(favicon_path):
                return send_from_directory(
                    os.path.dirname(favicon_path), 
                    os.path.basename(favicon_path), 
                    mimetype='image/x-icon'
                )
            
            # Fallback to no content
            return '', 204
        
        except Exception as e:
            app.logger.error(f"Favicon serving error: {e}")
            return '', 204

# Call favicon setup after CORS initialization
setup_favicon(app)

# Paths
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'Templates_NEW')
MARKDOWN_DIR = os.path.join(os.path.dirname(__file__), '..', 'Templates_Markdown')
GENERATED_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'Generated_Templates')

# Ensure generated templates directory exists
os.makedirs(GENERATED_TEMPLATES_DIR, exist_ok=True)

# Global error handler
@app.errorhandler(Exception)
def handle_global_error(error):
    """
    Global error handler for unhandled exceptions
    
    Provides a consistent error response and logs the error
    """
    # Log the full error traceback
    app.logger.error(f"Unhandled Exception: {str(error)}", exc_info=True)
    
    # Determine the appropriate error response
    if isinstance(error, HTTPException):
        return create_error_response({
            'message': error.description,
            'status_code': error.code,
            'details': {}
        })
    
    # For unexpected errors
    error_info = {
        'message': 'An unexpected server error occurred',
        'status_code': 500,
        'details': {
            'error_type': type(error).__name__,
            'error_message': str(error)
        }
    }
    
    return create_error_response(error_info)

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

def validate_template_type(template_type):
    """
    Adaptive template type validation
    - Allows predefined types
    - Permits custom types with optional additional checks
    - Provides clear, actionable feedback
    """
    PREDEFINED_TYPES = {'web_app', 'document', 'script', 'data_analysis'}
    
    if not template_type:
        raise TemplateGenerationError(
            "Template type is required", 
            details={'allowed_types': list(PREDEFINED_TYPES)}
        )
    
    # Normalize input
    normalized_type = template_type.lower().replace(' ', '_')
    
    # Primary validation
    if normalized_type in PREDEFINED_TYPES:
        return normalized_type
    
    # Custom type handling
    if len(normalized_type) > 3 and normalized_type.replace('_', '').isalnum():
        # Log custom type for future analysis
        app.logger.info(f"Custom template type created: {normalized_type}")
        return normalized_type
    
    raise TemplateGenerationError(
        f"Invalid template type: {template_type}. "
        f"Must be one of {', '.join(PREDEFINED_TYPES)} "
        "or a valid custom type.",
        details={
            'allowed_types': list(PREDEFINED_TYPES),
            'custom_type_guidelines': 'Must be at least 4 characters, alphanumeric'
        }
    )

@app.route('/generate_template', methods=['POST'])
def generate_template():
    """Advanced template generation endpoint with comprehensive error handling."""
    try:
        # Log incoming request details
        app.logger.info(f"Template generation request received: {request.get_json()}")
        
        # Validate request
        validate_request(request, ['template_type', 'name'])
        
        data = request.get_json()
        template_type = validate_template_type(data.get('template_type'))
        template_name = sanitize_filename(data.get('name', f'New_{template_type}_Template'))
        
        app.logger.info(f"Processing template generation: type={template_type}, name={template_name}")
        
        # Generate template with structured directory
        template_id = str(uuid.uuid4())[:8]  # Shorter ID
        template_dir_name = f"{template_id}_{template_name}"
        generated_path = os.path.join(TEMPLATES_DIR, template_dir_name)
        os.makedirs(generated_path, exist_ok=True)
        
        # Create template files
        readme_path = os.path.join(generated_path, 'README.md')
        template_path = os.path.join(generated_path, 'template.md')
        
        # Enhanced template content generation
        template_contents = {
            'web_app': f"# {template_name} Web Application Template\n\n## Overview\n\n## Key Features\n\n## Getting Started\n",
            'document': f"# {template_name} Document Template\n\n## Introduction\n\n## Main Sections\n\n## Conclusion\n",
            'script': f"# {template_name} Script Template\n\n## Purpose\n\n## Usage\n\n## Dependencies\n",
            'data_analysis': f"# {template_name} Data Analysis Template\n\n## Dataset\n\n## Methodology\n\n## Insights\n"
        }
        
        # Default content for custom types
        default_custom_content = f"# {template_name} Custom Template\n\n## Purpose\n\n## Key Components\n\n## Notes\n"
        
        # Write README with enhanced metadata
        with open(readme_path, 'w') as f:
            f.write(f"""# {template_name}
## Template Metadata
- **Type**: {template_type}
- **Generated**: {datetime.utcnow().isoformat()}
- **Template ID**: {template_id}
- **Origin**: {'Predefined' if template_type in {'web_app', 'document', 'script', 'data_analysis'} else 'Custom'}
""")
        
        # Write template content
        with open(template_path, 'w') as f:
            f.write(template_contents.get(template_type, default_custom_content))
        
        # Log successful generation
        log_template_generation(template_type, template_name, 'success')
        
        app.logger.info(f"Template generated successfully: {generated_path}")
        
        return jsonify({
            'status': 'success',
            'template_id': template_id,
            'path': template_dir_name,
            'message': f'Template {template_name} generated successfully',
            'type': template_type
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
    
    # Search in NEW templates directory
    new_template_path = None
    for potential_template in os.listdir(TEMPLATES_DIR):
        if potential_template.endswith(template_name):
            new_template_path = os.path.join(TEMPLATES_DIR, potential_template)
            break
    
    if not new_template_path or not os.path.exists(new_template_path):
        # If no template found, return a helpful message
        return render_template('template_view.html', 
                               template_name=template_name, 
                               readme_content="Template not found", 
                               template_content="No template content available")
    
    # Look for README and template files
    readme_path = os.path.join(new_template_path, 'README.md')
    template_path = os.path.join(new_template_path, 'template.md')
    
    # Read README
    try:
        with open(readme_path, 'r') as f:
            readme_content = markdown2.markdown(f.read())
    except FileNotFoundError:
        readme_content = "No README available"
    
    # Read template content
    try:
        with open(template_path, 'r') as f:
            template_content = markdown2.markdown(f.read())
    except FileNotFoundError:
        template_content = "No template content available"
    
    # Try to load metadata
    try:
        metadata = load_template_metadata(new_template_path)
    except Exception:
        metadata = {"name": os.path.basename(new_template_path)}
    
    return render_template('template_view.html', 
                           template_name=metadata.get('name', template_name), 
                           readme_content=readme_content, 
                           template_content=template_content)

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
    """
    List available template types with enhanced metadata
    
    Returns:
        JSON response with template types and additional information
    """
    PREDEFINED_TYPES = {
        'web_app': {
            'display_name': 'Web Application',
            'description': 'Templates for web-based projects',
            'icon': '💻'
        },
        'document': {
            'display_name': 'Document',
            'description': 'Structured document templates',
            'icon': '📄'
        },
        'script': {
            'display_name': 'Script',
            'description': 'Programming and automation scripts',
            'icon': '🖥️'
        },
        'data_analysis': {
            'display_name': 'Data Analysis',
            'description': 'Research and analytical project templates',
            'icon': '📊'
        }
    }
    
    # Log the template types request
    app.logger.info("Template types API endpoint accessed")
    
    return jsonify({
        'predefined_types': PREDEFINED_TYPES,
        'custom_type_guidelines': {
            'min_length': 4,
            'allowed_characters': 'Alphanumeric and underscores',
            'example_formats': ['machine_learning', 'project_proposal']
        }
    })

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
