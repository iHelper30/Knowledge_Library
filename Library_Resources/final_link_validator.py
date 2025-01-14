import os
import re
import json

def comprehensive_link_validation(base_path):
    validation_results = {
        'broken_references': [],
        'orphaned_links': [],
        'potential_issues': []
    }

    # Search files for any remaining 28_Feedback_Forms references
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(('.html', '.json', '.md', '.py')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Check for direct references to removed directory
                        if '28_Feedback_Forms' in content:
                            validation_results['broken_references'].append({
                                'file': file_path,
                                'context': 'Contains reference to removed directory'
                            })
                except Exception as e:
                    validation_results['potential_issues'].append({
                        'file': file_path,
                        'error': str(e)
                    })

    return validation_results

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    results = comprehensive_link_validation(base_path)
    
    print("Comprehensive Link Validation Results:")
    for category, issues in results.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        if issues:
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("  No issues found")

if __name__ == '__main__':
    main()
