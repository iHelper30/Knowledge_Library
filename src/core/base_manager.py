from typing import 
from typing import Any
from typing import Optional, Union, Callable
'\nBase management class for core project functionality.\n'
import logging
from typing import Any, Dict

class BaseManager:
    """
    A foundational management class providing common utilities
    and patterns for project components.
    """

    def __init__(self: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Initialize the BaseManager with optional configuration.

        Args:
            config (Dict[str, Any], optional): Configuration dictionary. Defaults to None.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config or {}

    def log(self: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Centralized logging method.

        Args:
            message (str): Log message
            level (str, optional): Logging level. Defaults to 'info'.
        """
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message)

    def validate_config(self: Any, required_keys: list) -> bool:
        """
        Validate that all required configuration keys are present.

        Args:
            required_keys (list): List of keys that must be in config

        Returns:
            bool: True if all keys are present, False otherwise
        """
        missing_keys = [key for key in required_keys if key not in self.config]
        if missing_keys:
            self.log(f'Missing configuration keys: {missing_keys}', 'warning')
            return False
        return True