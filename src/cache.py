import os
import json
from typing import Dict, Any
from functools import lru_cache
from datetime import datetime, timedelta

class TemplateMetadataCache:
    """
    Efficient caching mechanism for template metadata.
    Supports in-memory and persistent caching strategies.
    """
    
    def __init__(self, cache_dir: str = None, max_size: int = 100):
        """
        Initialize the template metadata cache.
        
        Args:
            cache_dir (str, optional): Directory to store persistent cache
            max_size (int, optional): Maximum number of items to cache in memory
        """
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), '..', 'cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # In-memory LRU cache
        self.memory_cache = lru_cache(maxsize=max_size)(self._load_metadata)
    
    def _get_cache_path(self, template_name: str) -> str:
        """Generate cache file path for a template."""
        return os.path.join(self.cache_dir, f"{template_name}_metadata.json")
    
    def _load_metadata(self, template_path: str) -> Dict[str, Any]:
        """
        Load metadata with caching logic.
        
        Args:
            template_path (str): Path to template directory
        
        Returns:
            Metadata dictionary
        """
        cache_file = self._get_cache_path(os.path.basename(template_path))
        
        # Fallback metadata if path doesn't exist
        if not os.path.exists(template_path):
            return {
                'name': os.path.basename(template_path),
                'type': 'error',
                'description': 'Template path not found'
            }
        
        # Check persistent cache first
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                cache_time = datetime.fromisoformat(cached_data.get('cached_at', datetime.utcnow().isoformat()))
                
                # Check cache freshness (1 hour)
                if datetime.utcnow() - cache_time < timedelta(hours=1):
                    return cached_data['metadata']
        
        # If no valid cache, generate fallback metadata
        metadata = {
            'name': os.path.basename(template_path),
            'type': 'generic',
            'description': 'Auto-generated metadata',
            'created_at': datetime.utcnow().isoformat(),
            'file_count': len([f for f in os.listdir(template_path) if os.path.isfile(os.path.join(template_path, f))]),
            'directory_count': len([d for d in os.listdir(template_path) if os.path.isdir(os.path.join(template_path, d))])
        }
        
        # Update persistent cache
        cache_data = {
            'metadata': metadata,
            'cached_at': datetime.utcnow().isoformat()
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        return metadata
    
    def get_metadata(self, template_path: str) -> Dict[str, Any]:
        """
        Retrieve metadata with efficient caching.
        
        Args:
            template_path (str): Path to template directory
        
        Returns:
            Metadata dictionary
        """
        return self.memory_cache(template_path)
    
    def invalidate_cache(self, template_name: str = None):
        """
        Invalidate cache for a specific template or entire cache.
        
        Args:
            template_name (str, optional): Name of template to invalidate
        """
        if template_name:
            cache_file = self._get_cache_path(template_name)
            if os.path.exists(cache_file):
                os.remove(cache_file)
        else:
            # Clear entire cache directory
            for file in os.listdir(self.cache_dir):
                os.remove(os.path.join(self.cache_dir, file))
        
        # Clear memory cache
        self.memory_cache.cache_clear()
