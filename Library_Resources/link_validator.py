import os
import re
import json

def validate_links(base_path):
    # Load navigation structure
    with open(os.path.join(base_path, 'navigation.json'), 'r') as f:
        navigation = json.load(f)
    
    # Validate directory structure
    directories = [d for d in os.listdir(base_path) 
                   if os.path.isdir(os.path.join(base_path, d)) 
                   and d.startswith(tuple('0123456789'))]
    
    # Validation results
    results = {
        'missing_directories': [],
        'navigation_inconsistencies': [],
        'missing_index_files': [],
        'orphaned_directories': []
    }
    
    # Check navigation consistency
    nav_keys = set(navigation.keys())
    dir_keys = set(directories)
    
    # Check for missing directories in navigation
    results['missing_directories'] = list(nav_keys - dir_keys)
    
    # Check for orphaned directories
    results['orphaned_directories'] = list(dir_keys - nav_keys)
    
    # Validate each directory
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        
        # Check for index.html
        if not os.path.exists(os.path.join(dir_path, 'index.html')):
            results['missing_index_files'].append(directory)
    
    return results

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    validation_results = validate_links(base_path)
    
    print("Link Validation Results:")
    for key, value in validation_results.items():
        print(f"{key.replace('_', ' ').title()}:")
        if value:
            for item in value:
                print(f"  - {item}")
        else:
            print("  No issues found")

if __name__ == '__main__':
    main()
