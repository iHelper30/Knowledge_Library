# Coding Standards and Best Practices Guide

## Code Style

### Naming Conventions
```python
# Variables
user_name = "John"      # Snake case for variables
MAX_RETRY_COUNT = 3     # Upper case for constants

# Functions
def calculate_total():   # Snake case for functions
    pass

# Classes
class UserAccount:      # Pascal case for classes
    pass

# Private members
_internal_value = 0     # Single underscore for internal use
__private_method()      # Double underscore for private
```

### Code Organization
```python
# File structure
#!/usr/bin/env python
"""Module docstring."""

# Standard library imports
import os
import sys

# Third party imports
import numpy as np
import pandas as pd

# Local application imports
from .models import User
from .utils import helper

# Constants
DEFAULT_TIMEOUT = 30

# Classes
class MainClass:
    """Class docstring."""
    pass

# Main execution
if __name__ == "__main__":
    main()
```

## Documentation

### Code Comments
```python
# Single line comment for simple explanations
x = x + 1  # Increment x

"""
Multi-line comment for complex explanations
that require multiple lines of text
to fully explain the concept
"""

def complex_function(param1, param2):
    """
    Function docstring with:
    - Purpose
    - Parameters
    - Return value
    - Examples
    """
    pass
```

### API Documentation
```python
class APIClient:
    """
    Client for interacting with the REST API.
    
    Attributes:
        base_url (str): The base URL for the API
        timeout (int): Request timeout in seconds
    """
    
    def get_user(self, user_id: int) -> dict:
        """
        Retrieve user information.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            dict: User information
            
        Raises:
            APIError: If the request fails
        """
        pass
```

## Error Handling

### Exception Handling
```python
try:
    # Attempt risky operation
    result = perform_operation()
except ValueError as e:
    # Handle specific exception
    logger.error(f"Invalid value: {e}")
except Exception as e:
    # Handle general exceptions
    logger.error(f"Unexpected error: {e}")
else:
    # Execute if no exception
    process_result(result)
finally:
    # Always execute
    cleanup_resources()
```

### Logging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug("Starting data processing")
    try:
        result = transform_data(data)
        logger.info("Data processing completed")
        return result
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise
```

## Performance

### Optimization
```python
# List comprehension instead of loop
numbers = [1, 2, 3, 4, 5]
squares = [n * n for n in numbers]  # Better than loop

# Generator for large datasets
def number_generator(n):
    for i in range(n):
        yield i * i

# Use sets for membership testing
valid_users = set(['user1', 'user2'])
if user in valid_users:  # O(1) lookup
    pass
```

### Resource Management
```python
# Context managers for resource handling
with open('file.txt', 'r') as file:
    content = file.read()

# Database connections
from contextlib import contextmanager

@contextmanager
def db_session():
    session = create_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

## Testing

### Unit Tests
```python
import unittest

class TestUserAccount(unittest.TestCase):
    def setUp(self):
        self.user = UserAccount("test@example.com")
    
    def test_email_validation(self):
        """Test email validation logic"""
        self.assertTrue(self.user.is_valid_email())
    
    def test_password_strength(self):
        """Test password strength requirements"""
        with self.assertRaises(ValueError):
            self.user.set_password("weak")
```

### Integration Tests
```python
class TestAPIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = APIClient()
    
    def test_user_workflow(self):
        # Create user
        user_id = self.api.create_user({"name": "Test"})
        
        # Verify user
        user = self.api.get_user(user_id)
        self.assertEqual(user["name"], "Test")
        
        # Update user
        self.api.update_user(user_id, {"name": "Updated"})
        
        # Delete user
        self.api.delete_user(user_id)
```

## Security

### Input Validation
```python
def process_user_input(user_input: str) -> str:
    """Validate and sanitize user input."""
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")
    
    # Remove dangerous characters
    sanitized = re.sub(r'[<>\'"]', '', user_input)
    
    # Validate length
    if len(sanitized) > 100:
        raise ValueError("Input too long")
    
    return sanitized
```

### Authentication
```python
def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate user with secure password verification.
    
    Args:
        username: User's username
        password: User's password
    
    Returns:
        bool: True if authentication successful
    """
    user = get_user(username)
    if not user:
        return False
    
    # Use secure password verification
    return verify_password(password, user.password_hash)
```

## Version Control

### Git Practices
```bash
# Branch naming
feature/user-authentication
bugfix/login-error
hotfix/security-patch

# Commit messages
feat: add user authentication
fix: resolve login error
docs: update API documentation
test: add user tests
refactor: improve error handling
```

### Code Review
```markdown
## Code Review Checklist

1. Functionality
   - [ ] Code works as intended
   - [ ] Edge cases handled
   - [ ] Error handling present

2. Code Quality
   - [ ] Follows style guide
   - [ ] Well documented
   - [ ] No duplicate code

3. Testing
   - [ ] Unit tests added
   - [ ] Tests pass
   - [ ] Coverage adequate
```

## Deployment

### CI/CD Pipeline
```yaml
# Example GitHub Actions workflow
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run tests
      run: |
        pip install -r requirements.txt
        python -m pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      if: github.ref == 'refs/heads/main'
      run: |
        # Deploy commands
```

### Environment Configuration
```python
# Configuration management
from decouple import config

class Config:
    """Application configuration."""
    
    # Basic config
    DEBUG = config('DEBUG', default=False, cast=bool)
    SECRET_KEY = config('SECRET_KEY')
    
    # Database
    DB_HOST = config('DB_HOST', default='localhost')
    DB_PORT = config('DB_PORT', default=5432, cast=int)
    
    # API keys
    API_KEY = config('API_KEY', default=None)
```

## Maintenance

### Code Cleanup
```python
# Remove unused imports
import os  # Used
import sys  # Unused - remove
from datetime import datetime  # Used

# Remove commented code
def process_data():
    # Old implementation
    # def old_process():
    #     pass
    
    return new_process()

# Remove debug code
def calculate_total():
    total = sum(values)
    # print("Debug:", total)  # Remove debug prints
    return total
```

### Technical Debt
```python
# TODO: Refactor this function to improve performance
def legacy_function():
    # Complex implementation that needs improvement
    pass

# FIXME: Handle edge case when user is None
def process_user(user):
    if user:
        return user.process()

# NOTE: Consider using async implementation for better scaling
def sync_operation():
    # Synchronous implementation
    pass
```

## Monitoring

### Health Checks
```python
def health_check():
    """
    Perform system health check.
    
    Returns:
        dict: Health status of various components
    """
    return {
        'status': 'healthy',
        'database': check_database(),
        'cache': check_cache(),
        'api': check_external_apis()
    }
```

### Performance Metrics
```python
from functools import wraps
import time

def measure_time(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper
```
