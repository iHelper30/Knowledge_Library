"""
Data Science Project Template Type Implementation
"""

import os
import json
import textwrap
import yaml
from pathlib import Path
from typing import Dict, Any

from ..core import BaseTemplateType, TemplateTypeRegistry

class DataScienceTemplateType(BaseTemplateType):
    """
    Specialized template type for data science projects
    """
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate data science template specific requirements
        
        Returns:
            Validation result dictionary
        """
        errors = []
        
        # Check for required files and directories
        required_items = [
            'README.md',
            'requirements.txt',
            'notebooks',
            'src',
            'data',
            'models',
            'tests'
        ]
        
        for item in required_items:
            path = self.base_path / item
            if not path.exists():
                errors.append(f"Missing required item: {item}")
        
        # Check notebook structure
        notebooks_path = self.base_path / 'notebooks'
        if notebooks_path.exists():
            notebook_files = list(notebooks_path.glob('*.ipynb'))
            if len(notebook_files) < 1:
                errors.append("No Jupyter notebooks found")
        
        # Check source code structure
        src_path = self.base_path / 'src'
        if src_path.exists():
            required_modules = ['data_loader.py', 'preprocessing.py', 'model.py']
            for module in required_modules:
                if not (src_path / module).exists():
                    errors.append(f"Missing source module: {module}")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def generate(self) -> Path:
        """
        Generate data science project template
        
        Returns:
            Path to generated template
        """
        # Determine primary ML framework and language
        ml_framework = self.config.get('ml_framework', 'sklearn')
        language = self.config.get('language', 'python')
        
        # README
        readme_content = textwrap.dedent(f'''
        # {self.name}

        ## Project Overview
        {self.config.get('description', 'A data science project template')}

        ### Version: {self.config.get('version', '0.1.0')}
        ### Author: {self.config.get('author', 'Unknown')}

        ## Technology Stack
        - Language: {language}
        - ML Framework: {ml_framework}
        - Data Processing: pandas, numpy
        - Visualization: matplotlib, seaborn

        ## Project Structure
        ```
        {self.name}/
        ├── data/
        │   ├── raw/
        │   └── processed/
        ├── notebooks/
        │   └── exploratory_analysis.ipynb
        ├── src/
        │   ├── data_loader.py
        │   ├── preprocessing.py
        │   └── model.py
        ├── models/
        │   └── trained_models/
        └── tests/
            └── test_data_processing.py
        ```

        ## Setup and Installation
        ```bash
        # Clone the repository
        git clone <repository_url>
        cd {self.name}

        # Create virtual environment
        python -m venv venv
        source venv/bin/activate

        # Install dependencies
        pip install -r requirements.txt
        ```

        ## Workflow
        1. Data Collection
        2. Exploratory Data Analysis
        3. Data Preprocessing
        4. Model Training
        5. Model Evaluation
        6. Deployment

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
        
        # Requirements
        requirements_content = '\n'.join([
            # Data processing
            'pandas',
            'numpy',
            
            # Machine Learning
            ml_framework,
            'scikit-learn',
            
            # Visualization
            'matplotlib',
            'seaborn',
            
            # Notebook
            'jupyter',
            
            # Testing
            'pytest',
            'coverage'
        ])
        self._write_file('requirements.txt', requirements_content)
        
        # Create project structure
        (self.base_path / 'data' / 'raw').mkdir(parents=True, exist_ok=True)
        (self.base_path / 'data' / 'processed').mkdir(exist_ok=True)
        (self.base_path / 'notebooks').mkdir(exist_ok=True)
        (self.base_path / 'models' / 'trained_models').mkdir(parents=True, exist_ok=True)
        (self.base_path / 'tests').mkdir(exist_ok=True)
        (self.base_path / 'src').mkdir(exist_ok=True)
        
        # Jupyter Notebook
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# Exploratory Data Analysis\n",
                        f"## Project: {self.name}"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "import pandas as pd\n",
                        "import numpy as np\n",
                        "import matplotlib.pyplot as plt\n",
                        "import seaborn as sns\n",
                        "\n",
                        "# TODO: Load your dataset\n",
                        "# df = pd.read_csv('data/raw/your_dataset.csv')"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        with open(self.base_path / 'notebooks' / 'exploratory_analysis.ipynb', 'w') as f:
            json.dump(notebook_content, f, indent=2)
        
        # Source code modules
        data_loader_content = textwrap.dedent('''
        """
        Data loading utilities
        """
        import pandas as pd

        def load_data(filepath):
            """
            Load data from various sources
            
            Args:
                filepath (str): Path to data file
            
            Returns:
                DataFrame: Loaded data
            """
            # Supports CSV, Excel, JSON
            file_extension = filepath.split('.')[-1].lower()
            
            if file_extension == 'csv':
                return pd.read_csv(filepath)
            elif file_extension in ['xls', 'xlsx']:
                return pd.read_excel(filepath)
            elif file_extension == 'json':
                return pd.read_json(filepath)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        ''').strip()
        self._write_file('src/data_loader.py', data_loader_content)
        
        preprocessing_content = textwrap.dedent('''
        """
        Data preprocessing utilities
        """
        import pandas as pd
        import numpy as np
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.impute import SimpleImputer
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline

        def create_preprocessing_pipeline(
            numeric_features, 
            categorical_features
        ):
            """
            Create a preprocessing pipeline
            
            Args:
                numeric_features (list): List of numeric column names
                categorical_features (list): List of categorical column names
            
            Returns:
                Pipeline: Preprocessing pipeline
            """
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numeric_transformer, numeric_features),
                    ('cat', categorical_transformer, categorical_features)
                ])
            
            return preprocessor
        ''').strip()
        self._write_file('src/preprocessing.py', preprocessing_content)
        
        model_content = textwrap.dedent('''
        """
        Machine learning model utilities
        """
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report, mean_squared_error
        
        class ModelTrainer:
            """
            Generic model training utility
            """
            def __init__(self, model, preprocessor=None):
                """
                Initialize model trainer
                
                Args:
                    model: Scikit-learn compatible model
                    preprocessor: Optional preprocessing pipeline
                """
                self.model = model
                self.preprocessor = preprocessor
            
            def train(self, X, y, test_size=0.2):
                """
                Train model with optional preprocessing
                
                Args:
                    X (DataFrame): Features
                    y (Series): Target variable
                    test_size (float): Proportion of test set
                
                Returns:
                    dict: Training results
                """
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=42
                )
                
                if self.preprocessor:
                    X_train = self.preprocessor.fit_transform(X_train)
                    X_test = self.preprocessor.transform(X_test)
                
                self.model.fit(X_train, y_train)
                
                # Predict and evaluate
                y_pred = self.model.predict(X_test)
                
                return {
                    'model': self.model,
                    'test_score': self.model.score(X_test, y_test),
                    'classification_report': classification_report(y_test, y_pred)
                }
        ''').strip()
        self._write_file('src/model.py', model_content)
        
        # Test module
        test_content = textwrap.dedent('''
        """
        Data processing test module
        """
        import pytest
        from src.data_loader import load_data
        from src.preprocessing import create_preprocessing_pipeline

        def test_data_loader():
            """
            Test data loading functionality
            """
            # TODO: Replace with actual test data
            with pytest.raises(ValueError):
                load_data('nonexistent_file.unknown')
        
        def test_preprocessing_pipeline():
            """
            Test preprocessing pipeline creation
            """
            numeric_features = ['age', 'income']
            categorical_features = ['gender', 'education']
            
            pipeline = create_preprocessing_pipeline(
                numeric_features, 
                categorical_features
            )
            
            assert pipeline is not None
        ''').strip()
        self._write_file('tests/test_data_processing.py', test_content)
        
        # Metadata
        metadata_content = {
            'name': self.name,
            'version': self.config.get('version', '0.1.0'),
            'description': self.config.get('description', 'A data science project template'),
            'author': self.config.get('author', 'Unknown'),
            'category': 'data_science',
            'ml_framework': ml_framework,
            'language': language
        }
        self._write_file('metadata.yml', yaml.safe_dump(metadata_content))
        
        # Template configuration
        config_content = {
            'template_type': 'data_science',
            'supported_formats': ['py', 'ipynb', 'csv', 'json'],
            'dependencies': [
                {'name': 'pandas', 'version': '1.3.3', 'type': 'python'},
                {'name': 'scikit-learn', 'version': '0.24.2', 'type': 'python'}
            ]
        }
        self._write_file('template_config.json', json.dumps(config_content, indent=2))
        
        return self.base_path

# Register the template type
TemplateTypeRegistry.register('data_science', DataScienceTemplateType)
