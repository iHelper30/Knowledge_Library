import os
import re
import ast
from typing import Dict, Any, List, Optional, Union, Callable

class TypeAnnotationTransformer(ast.NodeTransformer):
    def __init__(self):
        self.imports_to_add = set()
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        # Add return type annotation if missing
        if not node.returns:
            node.returns = ast.Name(id='Any', ctx=ast.Load())
            self.imports_to_add.add('Any')
        
        # Add type hints to arguments
        for arg in node.args.args:
            if not arg.annotation:
                arg.annotation = ast.Name(id='Any', ctx=ast.Load())
                self.imports_to_add.add('Any')
        
        return node
    
    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        # Add type hints for common variable assignments
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target = node.targets[0]
            value = node.value
            
            if isinstance(value, ast.List):
                node.annotation = ast.Name(id='List[Any]', ctx=ast.Load())
                self.imports_to_add.update(['List', 'Any'])
            elif isinstance(value, ast.Dict):
                node.annotation = ast.Name(id='Dict[str, Any]', ctx=ast.Load())
                self.imports_to_add.update(['Dict', 'Any'])
            elif isinstance(value, ast.Constant) and value.value is None:
                node.annotation = ast.Name(id='Optional[Any]', ctx=ast.Load())
                self.imports_to_add.update(['Optional', 'Any'])
        
        return node

def improve_file_type_annotations(file_path: str) -> None:
    """
    Comprehensively improve type annotations in a Python file
    """
    with open(file_path, 'r') as f:
        source_code = f.read()
    
    # Parse the source code into an AST
    tree = ast.parse(source_code)
    
    # Create and apply the transformer
    transformer = TypeAnnotationTransformer()
    modified_tree = transformer.visit(tree)
    
    # Prepare import statements
    import_lines = [f"from typing import {', '.join(sorted(transformer.imports_to_add))}\n"]
    
    # Convert modified AST back to source code
    modified_source = ast.unparse(modified_tree)
    
    # Add import statements at the beginning
    modified_source = ''.join(import_lines) + modified_source
    
    # Write back to file
    with open(file_path, 'w') as f:
        f.write(modified_source)
    
    print(f"Improved type annotations in {file_path}")

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
                    improve_file_type_annotations(file_path)

if __name__ == '__main__':
    main()
