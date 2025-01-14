from flask import Blueprint, render_template, send_from_directory
import os

templates_bp = Blueprint('templates', __name__)

@templates_bp.route('/templates')
def template_library():
    """Render the template library page"""
    return render_template('templates.html')

@templates_bp.route('/template/<path:filename>')
def serve_template(filename):
    """Serve individual template files"""
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'Templates_NEW')
    return send_from_directory(template_dir, filename)
