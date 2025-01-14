"""
Web Application Template Type Implementation
"""

import os
import json
import textwrap
import yaml
from pathlib import Path
from typing import Dict, Any

from ..core import BaseTemplateType, TemplateTypeRegistry

class WebAppTemplateType(BaseTemplateType):
    """
    Specialized template type for web application projects
    """
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate web application template specific requirements
        
        Returns:
            Validation result dictionary
        """
        errors = []
        
        # Check for required files and directories
        required_items = [
            'README.md',
            'requirements.txt',
            'frontend',
            'backend',
            'tests',
            '.env.example'
        ]
        
        for item in required_items:
            path = self.base_path / item
            if not path.exists():
                errors.append(f"Missing required item: {item}")
        
        # Check frontend structure
        frontend_path = self.base_path / 'frontend'
        if frontend_path.exists():
            required_frontend = ['index.html', 'styles', 'scripts']
            for req in required_frontend:
                if not (frontend_path / req).exists():
                    errors.append(f"Missing frontend component: {req}")
        
        # Check backend structure
        backend_path = self.base_path / 'backend'
        if backend_path.exists():
            required_backend = ['app.py', 'models', 'routes']
            for req in required_backend:
                if not (backend_path / req).exists():
                    errors.append(f"Missing backend component: {req}")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def generate(self) -> Path:
        """
        Generate web application template
        
        Returns:
            Path to generated template
        """
        # Determine framework and language
        frontend_framework = self.config.get('frontend_framework', 'vanilla')
        backend_framework = self.config.get('backend_framework', 'flask')
        
        # README
        readme_content = textwrap.dedent(f'''
        # {self.name}

        ## Project Overview
        {self.config.get('description', 'A web application template')}

        ### Version: {self.config.get('version', '0.1.0')}
        ### Author: {self.config.get('author', 'Unknown')}

        ## Technology Stack
        - Frontend: {frontend_framework}
        - Backend: {backend_framework}

        ## Setup and Installation

        ### Prerequisites
        - Python 3.9+
        - Node.js (for frontend)

        ### Installation
        ```bash
        # Clone the repository
        git clone <repository_url>
        cd {self.name}

        # Setup backend
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt

        # Setup frontend
        cd frontend
        npm install
        ```

        ## Running the Application
        ```bash
        # Start backend
        python backend/app.py

        # Start frontend (if applicable)
        npm start
        ```

        ## Development

        ### Running Tests
        ```bash
        # Backend tests
        pytest backend/tests/

        # Frontend tests
        npm test
        ```

        ## Contributing
        1. Fork the repository
        2. Create your feature branch
        3. Commit your changes
        4. Push to the branch
        5. Create a Pull Request

        ## License
        {self.config.get('license', 'MIT License')}
        ''').strip()
        
        self._write_file('README.md', readme_content)
        
        # Environment Example
        env_content = '\n'.join([
            '# Application Configuration',
            'DEBUG=True',
            'SECRET_KEY=your_secret_key',
            'DATABASE_URL=sqlite:///app.db',
            'FRONTEND_URL=http://localhost:3000'
        ])
        self._write_file('.env.example', env_content)
        
        # Requirements
        requirements_content = '\n'.join([
            # Backend dependencies
            f'{backend_framework}',
            'python-dotenv',
            'sqlalchemy',
            'pytest',
            
            # Frontend dependencies
            'flask-cors' if backend_framework == 'flask' else '',
            'gunicorn'
        ])
        self._write_file('requirements.txt', requirements_content)
        
        # Frontend structure
        frontend_path = self.base_path / 'frontend'
        frontend_path.mkdir(exist_ok=True)
        
        # Index HTML
        index_content = textwrap.dedent(f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{self.name}</title>
            <link rel="stylesheet" href="styles/main.css">
        </head>
        <body>
            <div id="app">
                <h1>{self.name}</h1>
            </div>
            <script src="scripts/main.js"></script>
        </body>
        </html>
        ''').strip()
        self._write_file('frontend/index.html', index_content)
        
        # Frontend styles
        (frontend_path / 'styles').mkdir(exist_ok=True)
        main_css_content = '''
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        '''
        self._write_file('frontend/styles/main.css', main_css_content)
        
        # Frontend scripts
        (frontend_path / 'scripts').mkdir(exist_ok=True)
        main_js_content = '''
        document.addEventListener('DOMContentLoaded', () => {
            console.log('Web app initialized');
        });
        '''
        self._write_file('frontend/scripts/main.js', main_js_content)
        
        # Backend structure
        backend_path = self.base_path / 'backend'
        backend_path.mkdir(exist_ok=True)
        (backend_path / 'models').mkdir(exist_ok=True)
        (backend_path / 'routes').mkdir(exist_ok=True)
        (backend_path / 'tests').mkdir(exist_ok=True)
        
        # Backend app
        backend_app_content = textwrap.dedent(f'''
        """
        Main application module
        """
        from flask import Flask, jsonify

        app = Flask(__name__)

        @app.route('/')
        def index():
            """
            Root endpoint
            """
            return jsonify({{'message': 'Welcome to {self.name}'}})

        if __name__ == '__main__':
            app.run(debug=True)
        ''').strip()
        self._write_file('backend/app.py', backend_app_content)
        
        # Test placeholder
        test_content = textwrap.dedent('''
        """
        Backend test module
        """

        def test_index_route():
            """
            Test application root route
            """
            from backend.app import app
            client = app.test_client()
            response = client.get('/')
            assert response.status_code == 200
        ''').strip()
        self._write_file('backend/tests/test_app.py', test_content)
        
        # Metadata
        metadata_content = {
            'name': self.name,
            'version': self.config.get('version', '0.1.0'),
            'description': self.config.get('description', 'A web application template'),
            'author': self.config.get('author', 'Unknown'),
            'category': 'web_app',
            'frontend_framework': frontend_framework,
            'backend_framework': backend_framework
        }
        self._write_file('metadata.yml', yaml.safe_dump(metadata_content))
        
        # Template configuration
        config_content = {
            'template_type': 'web_app',
            'supported_formats': ['py', 'html', 'js', 'css'],
            'dependencies': [
                {'name': 'flask', 'version': '2.3.2', 'type': 'python'},
                {'name': 'gunicorn', 'version': '20.1.0', 'type': 'python'}
            ]
        }
        self._write_file('template_config.json', json.dumps(config_content, indent=2))
        
        return self.base_path

# Register the template type
TemplateTypeRegistry.register('web_app', WebAppTemplateType)
