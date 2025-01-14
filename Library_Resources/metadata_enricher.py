from typing import Any, List, Optional, Union, Dict, Callable
import os
import json
import markdown2

class MetadataEnricher:

    def __init__(self: Any, root_path: str, *args: Any, **kwargs: Any) -> Any:
        self.root_path = root_path
        self.metadata_file = os.path.join(root_path, 'library_metadata.json')

    def extract_readme_summary(self: Any, folder_path: str) -> str:
        """Extract summary from README.md"""
        readme_path = os.path.join(folder_path, 'README.md')
        if not os.path.exists(readme_path):
            return 'No description available.'
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            summary = content.split('\n\n')[0] if content.split('\n\n') else content[:200]
            return summary

    def generate_folder_metadata(self: Any, folder_name: str) -> Dict[str, Any]:
        """Generate comprehensive metadata for a folder"""
        folder_path = os.path.join(self.root_path, folder_name)
        try:
            prefix, title = folder_name.split('_', 1)
        except ValueError:
            prefix, title = ('00', folder_name)
        categories = {'01-10': 'Introduction and Fundamentals', '11-20': 'Advanced Strategies', '21-30': 'Professional Development', '31-40': 'Tools and Resources', '41-50': 'Advanced Topics'}
        category = next((cat for range_key, cat in categories.items() if self._in_range(prefix, range_key)), 'Uncategorized')
        metadata = {'id': folder_name, 'title': title.replace('_', ' '), 'category': category, 'summary': self.extract_readme_summary(folder_path), 'tags': [word.lower() for word in title.split('_')], 'content_files': [f for f in os.listdir(folder_path) if f.endswith(('.md', '.txt', '.html'))], 'difficulty': self._determine_difficulty(folder_name)}
        return metadata

    def _in_range(self: Any, prefix: str, range_key: str) -> bool:
        """Check if prefix is in the specified range"""
        start, end = map(int, range_key.split('-'))
        return start <= int(prefix) <= end

    def _determine_difficulty(self: Any, folder_name: str) -> str:
        """Determine content difficulty based on folder name"""
        difficulty_map = {'01-05': 'Beginner', '06-15': 'Intermediate', '16-30': 'Advanced', '31-50': 'Expert'}
        prefix = folder_name.split('_')[0]
        return next((diff for range_key, diff in difficulty_map.items() if self._in_range(prefix, range_key)), 'Unspecified')

    def enrich_library_metadata(self: Any) -> Dict[str, Any]:
        """Generate comprehensive library metadata"""
        library_metadata = {'total_knowledge_blocks': 0, 'categories': {}, 'knowledge_blocks': {}}
        for folder in sorted(os.listdir(self.root_path)):
            if os.path.isdir(os.path.join(self.root_path, folder)) and folder.startswith(tuple((str(i).zfill(2) for i in range(1, 50)))):
                block_metadata = self.generate_folder_metadata(folder)
                library_metadata['knowledge_blocks'][folder] = block_metadata
                category = block_metadata['category']
                library_metadata['categories'][category] = library_metadata['categories'].get(category, 0) + 1
                library_metadata['total_knowledge_blocks'] += 1
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(library_metadata, f, indent=2)
        return library_metadata

def main(root_path: str, *args: Any, **kwargs: Any) -> Any:
    enricher = MetadataEnricher(root_path)
    library_metadata = enricher.enrich_library_metadata()
    print('Library Metadata Generated Successfully:')
    print(f'Total Knowledge Blocks: {library_metadata["total_knowledge_blocks"]}')
    print('Categories:', json.dumps(library_metadata['categories'], indent=2))

if __name__ == '__main__':
    root_path = 'C:\\Users\\ihelp\\KnowledgeLibrary\\Templates_NEW'
    main(root_path)