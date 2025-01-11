from typing import 
from typing import List, Union, Callable
'\nEnvironment Variable Loader Utility\nProvides secure and flexible environment configuration management\n'
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

class EnvLoader:
    """
    Utility class for loading and managing environment variables
    """

    @staticmethod
    def load_env(env_file: Optional[str]=None) -> None:
        """
        Load environment variables from .env file

        Args:
            env_file (Optional[str]): Path to .env file.
                                      Defaults to .env in project root
        """
        if env_file is None:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            env_file = os.path.join(project_root, '.env')
        load_dotenv(env_file)

    @staticmethod
    def get_env(key: str, default: Optional[str]=None) -> Optional[str]:
        """
        Retrieve an environment variable

        Args:
            key (str): Environment variable name
            default (Optional[str]): Default value if not found

        Returns:
            Optional[str]: Value of the environment variable
        """
        return os.getenv(key, default)

    @staticmethod
    def get_sensitive_env(key: str) -> Optional[str]:
        """
        Retrieve a sensitive environment variable with additional checks

        Args:
            key (str): Sensitive environment variable name

        Returns:
            Optional[str]: Value of the environment variable

        Raises:
            ValueError: If sensitive variable is not set
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(f'Sensitive environment variable {key} is not set')
        return value

    @staticmethod
    def get_bool_env(key: str, default: bool=False) -> bool:
        """
        Retrieve a boolean environment variable

        Args:
            key (str): Environment variable name
            default (bool): Default value if not found

        Returns:
            bool: Boolean representation of the environment variable
        """
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')