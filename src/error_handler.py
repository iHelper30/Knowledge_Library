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

def handle_error(error: Exception) -> Dict[str, Any]:
    """
    Centralized error handling and logging.
    
    Args:
        error (Exception): The caught exception
    
    Returns:
        Standardized error response dictionary
    """
    if isinstance(error, KnowledgeLibraryError):
        logging.error(f"{error.__class__.__name__}: {error.message}")
        return {
            'error': error.message,
            'status_code': error.status_code,
            'details': getattr(error, 'details', {})
        }
    
    # Generic error handling
    logging.exception("Unhandled exception")
    return {
        'error': 'An unexpected error occurred',
        'status_code': 500,
        'details': {
            'type': error.__class__.__name__,
            'message': str(error)
        }
    }

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
