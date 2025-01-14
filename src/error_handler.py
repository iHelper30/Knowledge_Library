import logging
from typing import Dict, Any
from flask import jsonify, Request

class KnowledgeLibraryError(Exception):
    """Base exception for Knowledge Library errors."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

class TemplateGenerationError(KnowledgeLibraryError):
    """Specific error for template generation failures."""
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, status_code=400)
        self.details = details or {}

class ValidationError(Exception):
    def errors(self):
        # This method should return a dictionary of validation errors
        # For demonstration purposes, it's left empty
        return {}

def handle_error(error: Exception) -> Dict[str, Any]:
    """
    Centralized error handling with comprehensive error mapping.
    
    Args:
        error (Exception): The caught exception
    
    Returns:
        dict: Standardized error response
    """
    # Default error response
    error_info = {
        'message': 'An unexpected error occurred',
        'status_code': 500,
        'details': {}
    }
    
    # Specific error type handling
    if isinstance(error, TemplateGenerationError):
        error_info = {
            'message': str(error),
            'status_code': 400,
            'details': error.details if hasattr(error, 'details') else {}
        }
    
    elif isinstance(error, ValidationError):
        error_info = {
            'message': 'Validation failed',
            'status_code': 422,
            'details': {
                'validation_errors': error.errors()
            }
        }
    
    elif isinstance(error, FileNotFoundError):
        error_info = {
            'message': 'Resource not found',
            'status_code': 404,
            'details': {
                'path': str(error)
            }
        }
    
    # Log the error for server-side tracking
    logging.error(f"Error Handling: {error_info}")
    
    return error_info

def validate_request(request: Request, required_fields: list) -> None:
    """
    Validate incoming request for required fields.
    
    Args:
        request (Request): Flask request object
        required_fields (list): List of required field names
    
    Raises:
        TemplateGenerationError: If validation fails
    """
    data = request.get_json(silent=True) or {}
    
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise TemplateGenerationError(
            f"Missing required fields: {', '.join(missing_fields)}",
            details={'missing_fields': missing_fields}
        )

def create_error_response(error: Dict[str, Any]):
    """
    Create a standardized Flask error response.
    
    Args:
        error (Dict): Error details dictionary
    
    Returns:
        Flask JSON response
    """
    return jsonify(error), error.get('status_code', 500)
