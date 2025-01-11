from typing import 
from typing import List, Optional, Union, Callable
'\nConfiguration loader and environment management utilities.\n'
import os
import json
from typing import Dict, Any

class ConfigLoader:
    """
    Utility for loading and managing configuration from various sources.
    """

    @staticmethod
    def load_env_config() -> Dict[str, str]:
        """
        Load configuration from environment variables.

        Returns:
            Dict[str, str]: Dictionary of environment configurations
        """
        return {key: value for key, value in os.environ.items() if key.startswith('CRL_')}

    @staticmethod
    def load_json_config(file_path: str) -> Dict[str, Any]:
        """
        Load configuration from a JSON file.

        Args:
            file_path (str): Path to the JSON configuration file

        Returns:
            Dict[str, Any]: Parsed JSON configuration
        """
        try:
            with open(file_path, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            print(f'Configuration file not found: {file_path}')
            return {}
        except json.JSONDecodeError:
            print(f'Invalid JSON in configuration file: {file_path}')
            return {}