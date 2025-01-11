import os
import re
from typing import Dict, Any, List

def improve_type_annotations(file_path: str) -> None:
    """
    Automatically improve type annotations in Python files
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add type hints for common patterns
    improvements = [
        # Add type hints for dictionaries
        (r'(\w+)\s*=\s*{}', r'\1: Dict[str, Any] = {}'),
        # Add type hints for lists
        (r'(\w+)\s*=\s*\[\]', r'\1: List[Any] = []'),
        # Add return type hints
        (r'def\s+(\w+)\s*\(.*\):', r'def \1(self, *args: Any, **kwargs: Any) -> Any:'),
    ]
    
    for pattern, replacement in improvements:
        content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w') as f:
        f.write(content)

def main():
    # Directories to search for Python files
    search_dirs = [
        'Library_Resources',
        'src'
    ]
    
    for directory in search_dirs:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        improve_type_annotations(file_path)
                        print(f"Improved type annotations in {file_path}")
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

if __name__ == '__main__':
    main()
