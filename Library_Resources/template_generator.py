from typing import Dict, List, Optional, Union
import os
import json
import markdown2
from pathlib import Path

class TemplateGenerator:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.template_dir = self.root_path / 'templates'
        self.static_dir = self.root_path / 'static'
        
    def generate_metadata(self, folder_name: str) -> Dict[str, Union[str, List[str]]]:
        """Generate metadata based on folder name and content"""
        name_parts = folder_name.split('_', 1)
        if len(name_parts) > 1:
            title = name_parts[1].replace('_', ' ')
        else:
            title = folder_name
            
        return {
            'title': title,
            'subtitle': f'Comprehensive guide to {title.lower()}',
            'meta_description': f'Resources and insights for {title.lower()}',
            'keywords': title.lower().split()
        }

    def read_readme(self, folder_path: Path) -> str:
        """Read and convert README.md to HTML"""
        readme_path = folder_path / 'README.md'
        if readme_path.exists():
            return markdown2.markdown(readme_path.read_text(encoding='utf-8'))
        return '<p>Content coming soon.</p>'

    def generate_navigation(self, current_folder: str) -> Dict[str, Optional[str]]:
        """Generate previous and next page links"""
        folders = sorted([f for f in os.listdir(self.root_path) 
                        if os.path.isdir(os.path.join(self.root_path, f))])
        
        try:
            current_index = folders.index(current_folder)
            prev_page = f'../{folders[current_index - 1]}' if current_index > 0 else None
            next_page = f'../{folders[current_index + 1]}' if current_index < len(folders) - 1 else None
        except ValueError:
            prev_page = next_page = None
            
        return {'prev': prev_page, 'next': next_page}

    def generate_index_html(self, folder_name: str) -> str:
        """Generate index.html with dark theme for a given folder"""
        folder_path = self.root_path / folder_name
        metadata = self.generate_metadata(folder_name)
        content = self.read_readme(folder_path)
        navigation = self.generate_navigation(folder_name)
        
        template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Resource Library</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{keywords}">
    <link rel="stylesheet" href="/static/css/dark-theme.css">
    <script src="/static/js/main.js" defer></script>
</head>
<body class="dark-theme">
    <header class="nav-menu">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/">Home</a> / {title}
            </nav>
            <h1 class="text-cyan">{title}</h1>
            <p class="subtitle">{subtitle}</p>
        </div>
    </header>

    <main class="container">
        <article class="content card">
            {content}
        </article>
        
        <nav class="pagination">
            {prev_link}
            {next_link}
        </nav>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 Resource Library. All rights reserved.</p>
            <nav class="footer-nav">
                <a href="/sitemap">Sitemap</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
    </footer>
</body>
</html>
"""
        prev_link = f'<a href="{navigation["prev"]}" class="prev">← Previous</a>' if navigation["prev"] else ''
        next_link = f'<a href="{navigation["next"]}" class="next">Next →</a>' if navigation["next"] else ''
        
        return template.format(
            title=metadata['title'],
            meta_description=metadata['meta_description'],
            keywords=','.join(metadata['keywords']),
            subtitle=metadata['subtitle'],
            content=content,
            prev_link=prev_link,
            next_link=next_link
        )

    def process_all_folders(self) -> None:
        """Process all folders and generate index.html files"""
        for folder in os.listdir(self.root_path):
            folder_path = self.root_path / folder
            if folder_path.is_dir() and not folder.startswith(('_', '.')):
                index_path = folder_path / 'index.html'
                if not index_path.exists():
                    index_content = self.generate_index_html(folder)
                    index_path.write_text(index_content, encoding='utf-8')
                    print(f"Generated index.html for {folder}")

def main():
    root_path = os.path.dirname(os.path.abspath(__file__))
    generator = TemplateGenerator(root_path)
    generator.process_all_folders()

if __name__ == '__main__':
    main()