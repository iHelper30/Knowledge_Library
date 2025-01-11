import os
from pathlib import Path
import json
import shutil

class ContentGenerator:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.template_path = self.root_path / 'templates' / 'README_template.md'
        
    def load_metadata(self) -> dict:
        """Load metadata for all sections"""
        metadata_path = self.root_path / 'library_metadata.json'
        if metadata_path.exists():
            data = json.loads(metadata_path.read_text(encoding='utf-8'))
            return data.get('knowledge_blocks', {})
        return {}

    def generate_section_content(self, folder_name: str, metadata: dict) -> str:
        """Generate content for a section based on its metadata"""
        section_data = metadata.get(folder_name, {})
        if not section_data:
            return None
            
        title = section_data['title']
        category = section_data['category']
        difficulty = section_data.get('difficulty', 'Intermediate')
        
        # Parse the summary YAML-like content
        summary_lines = section_data['summary'].split('\n')
        summary_dict = {}
        try:
            summary_text = '\n'.join(summary_lines[2:-2])  # Extract JSON part
            summary_dict = json.loads(summary_text)
        except:
            summary_dict = {
                'description': 'A comprehensive guide and resource collection'
            }

        content = f"""# {title}

## Overview
{summary_dict.get('description', 'A comprehensive guide and resource collection.')}

## Category
This resource belongs to the "{category}" category and is suitable for {difficulty} level users.

## Key Topics
- Understanding {title} fundamentals
- Best practices in {title.lower()}
- Implementing {title.lower()} strategies

## Best Practices
1. Research and understand your {title.lower()} requirements
2. Follow established guidelines and standards
3. Regular review and updates of your {title.lower()} strategy

## Resources
- [Official Documentation](#) - Comprehensive guide to {title.lower()}
- [Community Forum](#) - Connect with other professionals
- [Best Practices Guide](#) - Industry-standard approaches

## Quick Tips
> {summary_dict.get('subtitle', f'Master {title.lower()} through practical application and continuous learning')}

## Next Steps
1. Review the documentation thoroughly
2. Practice with real-world examples
3. Join the community discussions
"""
        return content

    def process_all_folders(self) -> None:
        """Generate README.md files for all folders"""
        metadata = self.load_metadata()
        
        for folder in os.listdir(self.root_path):
            folder_path = self.root_path / folder
            if folder_path.is_dir() and not folder.startswith(('_', '.')):
                readme_path = folder_path / 'README.md'
                if not readme_path.exists():
                    content = self.generate_section_content(folder, metadata)
                    if content:
                        readme_path.write_text(content, encoding='utf-8')
                        print(f"Generated README.md for {folder}")

def main():
    root_path = os.path.dirname(os.path.abspath(__file__))
    generator = ContentGenerator(root_path)
    generator.process_all_folders()

if __name__ == '__main__':
    main()
