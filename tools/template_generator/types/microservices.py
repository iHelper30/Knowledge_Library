"""
Microservices Project Template Type Implementation
"""

import os
import json
import textwrap
import yaml
from pathlib import Path
from typing import Dict, Any, List

from ..core import BaseTemplateType, TemplateTypeRegistry

class MicroservicesTemplateType(BaseTemplateType):
    """
    Specialized template type for microservices architecture
    """
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate microservices template specific requirements
        
        Returns:
            Validation result dictionary
        """
        errors = []
        
        # Required project structure
        required_items = [
            'README.md',
            'docker-compose.yml',
            'services',
            'api_gateway',
            'shared',
            'deployment',
            'monitoring',
            'scripts'
        ]
        
        for item in required_items:
            path = self.base_path / item
            if not path.exists():
                errors.append(f"Missing required component: {item}")
        
        # Check service structure
        services_path = self.base_path / 'services'
        if services_path.exists():
            services = [d for d in services_path.iterdir() if d.is_dir()]
            if len(services) < 2:
                errors.append("Microservices project should have at least 2 services")
            
            # Check each service for basic requirements
            for service in services:
                if not (service / 'Dockerfile').exists():
                    errors.append(f"Missing Dockerfile for service: {service.name}")
                if not (service / 'requirements.txt').exists():
                    errors.append(f"Missing requirements.txt for service: {service.name}")
        
        # Check API Gateway
        api_gateway_path = self.base_path / 'api_gateway'
        if api_gateway_path.exists():
            if not (api_gateway_path / 'routes.py').exists():
                errors.append("Missing routes configuration in API Gateway")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def generate(self) -> Path:
        """
        Generate microservices project template
        
        Returns:
            Path to generated template
        """
        # Determine primary configuration
        language = self.config.get('language', 'python')
        framework = self.config.get('framework', 'fastapi')
        deployment_type = self.config.get('deployment', 'kubernetes')
        
        # README
        readme_content = textwrap.dedent(f'''
        # {self.name}

        ## Project Overview
        {self.config.get('description', 'A microservices architecture project')}

        ### Version: {self.config.get('version', '0.1.0')}
        ### Author: {self.config.get('author', 'Unknown')}

        ## Technology Stack
        - Language: {language}
        - Framework: {framework}
        - Deployment: {deployment_type}
        - API Gateway: Kong/Traefik
        - Service Discovery: Consul
        - Monitoring: Prometheus, Grafana

        ## Architecture
        ```
        {self.name}/
        ├── api_gateway/           # Central API routing
        ├── services/               # Individual microservices
        │   ├── service1/
        │   └── service2/
        ├── shared/                 # Shared libraries and utilities
        ├── deployment/             # Deployment configurations
        │   ├── kubernetes/
        │   └── docker/
        ├── monitoring/             # Observability tools
        └── scripts/                # Utility scripts
        ```

        ## Setup and Installation

        ### Prerequisites
        - Docker
        - Docker Compose
        - {deployment_type.capitalize()}

        ### Local Development
        ```bash
        # Clone the repository
        git clone <repository_url>
        cd {self.name}

        # Build and start services
        docker-compose up --build
        ```

        ## Microservices
        - Each service is independently deployable
        - Uses service discovery and distributed tracing
        - Supports horizontal scaling

        ## Contributing
        1. Fork the repository
        2. Create your feature branch
        3. Implement your microservice
        4. Write tests
        5. Create a Pull Request

        ## License
        {self.config.get('license', 'MIT License')}
        ''').strip()
        
        self._write_file('README.md', readme_content)
        
        # Docker Compose Configuration
        docker_compose_content = {
            'version': '3.8',
            'services': {
                'api_gateway': {
                    'build': './api_gateway',
                    'ports': ['8000:8000'],
                    'depends_on': []
                },
                'service1': {
                    'build': './services/service1',
                    'ports': ['8001:8001']
                },
                'service2': {
                    'build': './services/service2',
                    'ports': ['8002:8002']
                }
            },
            'networks': {
                'microservices_network': {
                    'driver': 'bridge'
                }
            }
        }
        
        with open(self.base_path / 'docker-compose.yml', 'w') as f:
            yaml.safe_dump(docker_compose_content, f, default_flow_style=False)
        
        # Create project structure
        (self.base_path / 'services' / 'service1').mkdir(parents=True, exist_ok=True)
        (self.base_path / 'services' / 'service2').mkdir(exist_ok=True)
        (self.base_path / 'api_gateway').mkdir(exist_ok=True)
        (self.base_path / 'shared').mkdir(exist_ok=True)
        (self.base_path / 'deployment' / 'kubernetes').mkdir(parents=True, exist_ok=True)
        (self.base_path / 'deployment' / 'docker').mkdir(exist_ok=True)
        (self.base_path / 'monitoring').mkdir(exist_ok=True)
        (self.base_path / 'scripts').mkdir(exist_ok=True)
        
        # Service 1 Implementation
        service1_app_content = textwrap.dedent(f'''
        """
        Service 1 Main Application
        """
        from fastapi import FastAPI
        import uvicorn

        app = FastAPI(title="{self.name} - Service 1")

        @app.get("/")
        async def root():
            """
            Health check endpoint
            """
            return {{"message": "Service 1 is running"}}

        @app.get("/service1/info")
        async def get_service_info():
            """
            Service information endpoint
            """
            return {{
                "name": "Service 1",
                "version": "{self.config.get('version', '0.1.0')}",
                "description": "First microservice"
            }}

        if __name__ == "__main__":
            uvicorn.run(app, host="0.0.0.0", port=8001)
        ''').strip()
        self._write_file('services/service1/main.py', service1_app_content)
        
        service1_requirements = '\n'.join([
            'fastapi',
            'uvicorn',
            'httpx',
            'pydantic'
        ])
        self._write_file('services/service1/requirements.txt', service1_requirements)
        
        service1_dockerfile = textwrap.dedent('''
        FROM python:3.9-slim

        WORKDIR /app

        # Install system dependencies
        RUN apt-get update && apt-get install -y \
            build-essential \
            && rm -rf /var/lib/apt/lists/*

        # Copy requirements and install Python dependencies
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt

        # Copy application code
        COPY . .

        # Expose service port
        EXPOSE 8001

        # Run the application
        CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
        ''').strip()
        self._write_file('services/service1/Dockerfile', service1_dockerfile)
        
        # Service 2 Implementation
        service2_app_content = textwrap.dedent(f'''
        """
        Service 2 Main Application
        """
        from fastapi import FastAPI
        import uvicorn
        import httpx

        app = FastAPI(title="{self.name} - Service 2")

        @app.get("/")
        async def root():
            """
            Health check endpoint
            """
            return {{"message": "Service 2 is running"}}

        @app.get("/service2/data")
        async def get_service_data():
            """
            Simulate data retrieval from another service
            """
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get("http://service1:8001/service1/info")
                    return {{
                        "service1_info": response.json(),
                        "additional_data": "Sample data from Service 2"
                    }}
                except Exception as e:
                    return {{"error": str(e)}}

        if __name__ == "__main__":
            uvicorn.run(app, host="0.0.0.0", port=8002)
        ''').strip()
        self._write_file('services/service2/main.py', service2_app_content)
        
        service2_requirements = '\n'.join([
            'fastapi',
            'uvicorn',
            'httpx',
            'pydantic'
        ])
        self._write_file('services/service2/requirements.txt', service2_requirements)
        
        service2_dockerfile = textwrap.dedent('''
        FROM python:3.9-slim

        WORKDIR /app

        # Install system dependencies
        RUN apt-get update && apt-get install -y \
            build-essential \
            && rm -rf /var/lib/apt/lists/*

        # Copy requirements and install Python dependencies
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt

        # Copy application code
        COPY . .

        # Expose service port
        EXPOSE 8002

        # Run the application
        CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
        ''').strip()
        self._write_file('services/service2/Dockerfile', service2_dockerfile)
        
        # API Gateway Implementation
        api_gateway_content = textwrap.dedent('''
        """
        API Gateway Configuration
        """
        from fastapi import FastAPI, Request
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn
        import httpx

        app = FastAPI(title="API Gateway")

        # CORS Middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.get("/")
        async def root():
            """
            API Gateway root endpoint
            """
            return {"message": "API Gateway is running"}

        @app.get("/services")
        async def list_services():
            """
            List available services
            """
            return {
                "services": [
                    {"name": "service1", "endpoint": "/service1"},
                    {"name": "service2", "endpoint": "/service2"}
                ]
            }

        @app.get("/service1/{path:path}")
        async def proxy_service1(path: str, request: Request):
            """
            Proxy requests to Service 1
            """
            async with httpx.AsyncClient() as client:
                url = f"http://service1:8001/{path}"
                response = await client.request(
                    method=request.method,
                    url=url,
                    headers=dict(request.headers),
                    content=await request.body()
                )
                return response.json()

        @app.get("/service2/{path:path}")
        async def proxy_service2(path: str, request: Request):
            """
            Proxy requests to Service 2
            """
            async with httpx.AsyncClient() as client:
                url = f"http://service2:8002/{path}"
                response = await client.request(
                    method=request.method,
                    url=url,
                    headers=dict(request.headers),
                    content=await request.body()
                )
                return response.json()

        if __name__ == "__main__":
            uvicorn.run(app, host="0.0.0.0", port=8000)
        ''').strip()
        self._write_file('api_gateway/main.py', api_gateway_content)
        
        api_gateway_requirements = '\n'.join([
            'fastapi',
            'uvicorn',
            'httpx',
            'pydantic',
            'python-multipart'
        ])
        self._write_file('api_gateway/requirements.txt', api_gateway_requirements)
        
        api_gateway_dockerfile = textwrap.dedent('''
        FROM python:3.9-slim

        WORKDIR /app

        # Install system dependencies
        RUN apt-get update && apt-get install -y \
            build-essential \
            && rm -rf /var/lib/apt/lists/*

        # Copy requirements and install Python dependencies
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt

        # Copy application code
        COPY . .

        # Expose gateway port
        EXPOSE 8000

        # Run the application
        CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
        ''').strip()
        self._write_file('api_gateway/Dockerfile', api_gateway_dockerfile)
        
        # Kubernetes Deployment Configuration
        k8s_service1_deployment = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': 'service1-deployment',
                'labels': {'app': 'service1'}
            },
            'spec': {
                'replicas': 2,
                'selector': {'matchLabels': {'app': 'service1'}},
                'template': {
                    'metadata': {'labels': {'app': 'service1'}},
                    'spec': {
                        'containers': [{
                            'name': 'service1',
                            'image': f'{self.name.lower()}-service1:latest',
                            'ports': [{'containerPort': 8001}]
                        }]
                    }
                }
            }
        }
        
        with open(self.base_path / 'deployment' / 'kubernetes' / 'service1-deployment.yml', 'w') as f:
            yaml.safe_dump(k8s_service1_deployment, f, default_flow_style=False)
        
        # Monitoring Configuration (Prometheus)
        prometheus_config = {
            'global': {
                'scrape_interval': '15s'
            },
            'scrape_configs': [
                {
                    'job_name': 'services',
                    'static_configs': [
                        {
                            'targets': [
                                'service1:8001',
                                'service2:8002',
                                'api_gateway:8000'
                            ]
                        }
                    ]
                }
            ]
        }
        
        with open(self.base_path / 'monitoring' / 'prometheus.yml', 'w') as f:
            yaml.safe_dump(prometheus_config, f, default_flow_style=False)
        
        # Utility Scripts
        deploy_script = textwrap.dedent('''
        #!/bin/bash
        set -e

        # Build and deploy microservices
        echo "Building services..."
        docker-compose build

        echo "Starting services..."
        docker-compose up -d

        echo "Deployment complete!"
        ''').strip()
        self._write_file('scripts/deploy.sh', deploy_script)
        os.chmod(self.base_path / 'scripts' / 'deploy.sh', 0o755)
        
        # Shared Utilities
        shared_utils_content = textwrap.dedent('''
        """
        Shared Utilities for Microservices
        """
        import logging
        from typing import Dict, Any

        def configure_logger(name: str) -> logging.Logger:
            """
            Create a standardized logger
            
            Args:
                name (str): Logger name
            
            Returns:
                Configured logger
            """
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            
            return logger

        def sanitize_config(config: Dict[str, Any]) -> Dict[str, Any]:
            """
            Sanitize configuration dictionary
            
            Args:
                config (dict): Input configuration
            
            Returns:
                Sanitized configuration
            """
            return {
                k: v for k, v in config.items()
                if v is not None and v != ''
            }
        ''').strip()
        self._write_file('shared/utils.py', shared_utils_content)
        
        # Metadata
        metadata_content = {
            'name': self.name,
            'version': self.config.get('version', '0.1.0'),
            'description': self.config.get('description', 'A microservices architecture project'),
            'author': self.config.get('author', 'Unknown'),
            'category': 'microservices',
            'language': language,
            'framework': framework,
            'deployment_type': deployment_type
        }
        self._write_file('metadata.yml', yaml.safe_dump(metadata_content))
        
        # Template configuration
        config_content = {
            'template_type': 'microservices',
            'supported_formats': ['py', 'yml', 'yaml', 'sh'],
            'dependencies': [
                {'name': 'fastapi', 'version': '0.68.0', 'type': 'python'},
                {'name': 'uvicorn', 'version': '0.15.0', 'type': 'python'},
                {'name': 'docker-compose', 'version': '1.29.2', 'type': 'system'}
            ]
        }
        self._write_file('template_config.json', json.dumps(config_content, indent=2))
        
        return self.base_path

# Register the template type
TemplateTypeRegistry.register('microservices', MicroservicesTemplateType)
