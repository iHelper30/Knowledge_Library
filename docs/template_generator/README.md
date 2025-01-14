# Template Generator Documentation

## Overview

The Template Generator is a powerful, flexible tool for creating project templates across various domains and technologies.

## 🚀 Features

### Template Types
- **Document**: Create documentation projects
- **Code**: Generate code project structures
- **Web App**: Scaffold web application templates
- **Data Science**: Set up data science project environments
- **Microservices**: Design microservices architectures

### Key Capabilities
- Dynamic template generation
- Comprehensive validation
- Secure file handling
- Extensible architecture
- CLI and programmatic interfaces

## 📦 Installation

### Prerequisites
- Python 3.9+
- pip

### Install from Source
```bash
git clone https://github.com/your-org/template-generator.git
cd template-generator
pip install -r requirements.txt
pip install -e .
```

## 🖥️ CLI Usage

### Generate a Template
```bash
# Generate a web application template
python -m tools.template_generator generate \
  --type web_app \
  --name MyWebProject \
  --version 0.1.0 \
  --author "Jane Doe"
```

### Validate a Template
```bash
# Validate an existing template
python -m tools.template_generator validate \
  path/to/template \
  --output validation_report.json
```

### List Available Template Types
```bash
python -m tools.template_generator list-types
```

## 🛠️ Programmatic Usage

```python
from tools.template_generator import TemplateGenerator, TemplateValidator

# Generate a template
generator = TemplateGenerator()
template_path = generator.generate(
    template_type='data_science',
    name='ML Research Project',
    version='0.1.0',
    author='John Smith'
)

# Validate the generated template
validator = TemplateValidator()
validation_result = validator.validate(template_path)
print(validation_result)
```

## 🔧 Extending Template Types

### Creating a Custom Template Type

1. Inherit from `BaseTemplateType`
2. Implement `validate()` and `generate()` methods
3. Register with `TemplateTypeRegistry`

```python
from tools.template_generator.core import BaseTemplateType, TemplateTypeRegistry

class MyCustomTemplateType(BaseTemplateType):
    def validate(self):
        # Implement validation logic
        pass
    
    def generate(self):
        # Implement template generation
        pass

# Register the new template type
TemplateTypeRegistry.register('custom', MyCustomTemplateType)
```

## 🔒 Security Considerations
- Templates are generated with strict path sanitization
- Hardcoded secrets are detected during validation
- Supports environment-based configuration

## 📊 Validation Rules

### Structure Validation
- Required files and directories
- Maximum directory depth
- File naming conventions

### Content Validation
- Minimum documentation length
- No unresolved placeholders
- Consistent formatting

### Metadata Validation
- Required fields
- Version format
- Author information

## 🔍 Advanced Features

### External Validators
- Plugin custom validation logic
- Integrate with security scanning tools
- Perform complex checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Write tests
5. Submit a pull request

## 📜 License
MIT License

## 🛡️ Support
For issues, feature requests, or contributions, please open a GitHub issue.
