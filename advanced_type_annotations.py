import os
import re
from typing import Dict, Any, List, Union, Optional

def add_type_imports(file_path: str) -> str:
    """
    Add necessary type imports to the file
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Define import sets
    standard_imports = {
        'typing': ['Dict', 'List', 'Any', 'Optional', 'Union', 'Callable']
    }
    
    # Check and add imports
    for module, types in standard_imports.items():
        missing_types = [t for t in types if t not in content and not re.search(rf'from\s+{module}\s+import\s+{t}', content)]
        
        if missing_types:
            import_line = f"from {module} import {', '.join(missing_types)}\n"
            content = import_line + content
    
    return content

def improve_method_signatures(content: str) -> str:
    """
    Improve method signatures with type hints
    """
    # Add type hints to method definitions
    method_pattern = r'def\s+(\w+)\s*\((self)?([^)]*)\):'
    
    def replace_method(match):
        method_name = match.group(1)
        self_arg = match.group(2) or ''
        params = match.group(3) or ''
        
        # Add type hints to parameters
        typed_params = []
        for param in params.split(','):
            param = param.strip()
            if param and '=' not in param:
                typed_params.append(f"{param}: Any")
            else:
                typed_params.append(param)
        
        new_signature = f"def {method_name}(self{', ' if typed_params else ''}{', '.join(typed_params)}) -> Any:"
        return new_signature
    
    content = re.sub(method_pattern, replace_method, content)
    return content

def improve_variable_annotations(content: str) -> str:
    """
    Add type annotations to variables
    """
    # Add type hints for common variable patterns
    variable_patterns = [
        (r'(\w+)\s*=\s*{}', r'\1: Dict[str, Any] = {}'),
        (r'(\w+)\s*=\s*\[\]', r'\1: List[Any] = []'),
        (r'(\w+)\s*=\s*None', r'\1: Optional[Any] = None')
    ]
    
    for pattern, replacement in variable_patterns:
        content = re.sub(pattern, replacement, content)
    
    return content

def process_file(file_path: str) -> None:
    """
    Comprehensively improve type annotations in a file
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Apply improvements
        content = add_type_imports(file_path)
        content = improve_method_signatures(content)
        content = improve_variable_annotations(content)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"Improved type annotations in {file_path}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

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
                    process_file(file_path)

if __name__ == '__main__':
    main()
