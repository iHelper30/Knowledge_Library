# Template Structure Guide 📘

## Overview
This document provides comprehensive guidelines for creating templates in our deployment ecosystem. Adhering to these standards ensures smooth integration and validation.

## 🏗 Template Directory Structure

### Required Files
Each template MUST contain the following files:

1. **README.md**
   - Purpose: Provide an overview and documentation for the template
   - Requirements:
     - Markdown format
     - Clear description of template purpose
     - Usage instructions
     - Any dependencies or prerequisites

2. **metadata.yml**
   - Purpose: Provide structured metadata about the template
   - Required Fields:
     ```yaml
     name: string            # Template's human-readable name
     version: string         # Semantic versioning (e.g., "1.0.0")
     description: string     # Detailed template description
     category: string        # Classification (e.g., "documentation", "presentation")
     ```
   - Optional Fields:
     ```yaml
     author: string          # Template creator/maintainer
     tags: [string]          # Searchable keywords
     license: string         # License information
     ```

3. **template_config.json**
   - Purpose: Define template configuration and compatibility
   - Required Fields:
     ```json
     {
       "template_type": "string",        # Type of template (e.g., "document", "presentation")
       "supported_formats": ["string"],  # Supported file extensions
       "dependencies": [                 # List of required dependencies
         {
           "name": "string",
           "version": "string",
           "type": "string"
         }
       ]
     }
     ```
   - Optional Fields:
     ```json
     {
       "compatibility": {
         "platforms": ["string"],
         "min_version": "string"
       },
       "resources": {
         "memory": "string",
         "cpu": "string"
       }
     }
     ```

## 📁 Directory Layout Example
```
Template_Name/
│
├── README.md
├── metadata.yml
├── template_config.json
│
├── assets/                  # Optional: Supporting assets
│   ├── images/
│   └── styles/
│
├── examples/                # Optional: Example implementations
│   └── sample_document.md
│
└── scripts/                 # Optional: Template-specific scripts
    └── setup.sh
```

## 🚦 Validation Checks
Our deployment pipeline performs the following validation checks:

1. **File Existence**
   - Verifies presence of `README.md`, `metadata.yml`, and `template_config.json`

2. **Metadata Validation**
   - Checks for required fields
   - Validates version format
   - Ensures meaningful descriptions

3. **Configuration Validation**
   - Verifies template type
   - Checks dependency specifications
   - Validates supported formats

## ❌ Common Rejection Reasons
Templates may be rejected for:
- Missing required files
- Incomplete metadata
- Invalid configuration
- Unsupported dependencies
- Malformed JSON/YAML

## 🛠 Best Practices
- Keep templates modular and focused
- Document all dependencies
- Use semantic versioning
- Provide clear usage instructions
- Include example implementations

## 📦 Recommended Tools
- YAML Linter
- JSON Schema Validator
- Markdown Lint

## 🔍 Validation Example
```python
def validate_template(template_path):
    """
    Sample validation function demonstrating key checks
    """
    errors = []
    
    # Check file existence
    required_files = ['README.md', 'metadata.yml', 'template_config.json']
    for file in required_files:
        if not os.path.exists(os.path.join(template_path, file)):
            errors.append(f"Missing required file: {file}")
    
    # Validate metadata
    with open(os.path.join(template_path, 'metadata.yml'), 'r') as f:
        metadata = yaml.safe_load(f)
        
    required_metadata_fields = ['name', 'version', 'description', 'category']
    for field in required_metadata_fields:
        if field not in metadata:
            errors.append(f"Missing metadata field: {field}")
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }
```

## 🛠 Template Generation

### Using the Template Generator

We provide a convenient Python script to generate compliant templates quickly.

#### Prerequisites
- Python 3.9+
- `pyyaml` package installed

#### Installation
```bash
pip install pyyaml
```

#### CLI Usage
```bash
# Basic template generation
python generate_template.py "My Project Template"

# Specify template type
python generate_template.py "Data Analysis Template" -t code

# Set version and author
python generate_template.py "Documentation Template" -v 1.0.0 -a "John Doe"
```

#### Windows Users
Use the provided batch script:
```batch
generate_template.bat "My Project Template"
```

#### Template Types
- `document`: Text-based documents
- `presentation`: Slide decks
- `code`: Programming projects
- `script`: Automation scripts
- `configuration`: Configuration templates

#### CLI Options
- `-t, --type`: Template type (default: document)
- `-o, --output`: Output directory (default: Templates_NEW)
- `-v, --version`: Initial version (default: 0.1.0)
- `-a, --author`: Template author name

### Manual Template Creation

If you prefer manual creation, ensure your template includes:

1. `README.md`
2. `metadata.yml`
3. `template_config.json`
4. Optional `assets/` directory

#### Example Manual Template
```
My_Template/
├── README.md
├── metadata.yml
├── template_config.json
└── assets/
    └── .gitkeep
```

### Validation Checks

Run template validation:
```bash
python validate_template.py path/to/template
```

## 🤖 Automated Validation
Our deployment pipeline automatically validates templates before deployment.

### Common Validation Criteria
- All required files present
- Metadata completeness
- Configuration validity
- Dependency specifications

---

**Template Generation Tools**
- Generator Script: `generate_template.py`
- Validation Script: `validate_template.py`
- Schema: `template_schema.json`

## 🤝 Contributing
1. Fork the repository
2. Create your template following these guidelines
3. Submit a pull request
4. Pass validation checks

## 📞 Support
For questions or clarifications, please open an issue in the repository.

---

**Last Updated**: 2025-01-13
**Version**: 1.0.0
