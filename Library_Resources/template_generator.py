from typing import Dict, List, Optional, Union
import os
import json
from pathlib import Path
from content_processor import ContentProcessor

class TemplateGenerator:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.static_dir = self.root_path / 'static'
        self.processor = ContentProcessor(root_path)
        
    def generate_index_html(self, folder_name: str) -> str:
        """Generate index.html with dark theme for a given folder"""
        folder_path = self.root_path / folder_name
        metadata, content = self.processor.process_folder(folder_name)
        navigation = self.generate_navigation(folder_name)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{metadata.get('description', '')}">
    <meta name="keywords" content="{metadata.get('keywords', folder_name.lower())}">
    
    <!-- Open Graph / Social Media -->
    <meta property="og:title" content="{metadata.get('title', folder_name)}">
    <meta property="og:description" content="{metadata.get('description', '')}">
    <meta property="og:type" content="article">
    
    <!-- Preload critical assets -->
    <link rel="preload" href="../static/css/dark-theme.css" as="style">
    
    <title>{metadata.get('title', folder_name)} | Resource Library</title>
    <link rel="stylesheet" href="../static/css/dark-theme.css">
    
    <!-- Schema.org markup -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{metadata.get('title', folder_name)}",
        "description": "{metadata.get('description', '')}",
        "author": {{
            "@type": "Organization",
            "name": "iHelper.tech"
        }}
    }}
    </script>
</head>
<body class="dark-theme">
    <header class="nav-menu">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/">Home</a> / {metadata.get('title', folder_name)}
            </nav>
            <h1>{metadata.get('title', folder_name)}</h1>
            <p class="subtitle">{metadata.get('subtitle', '')}</p>
        </div>
    </header>

    <main class="container">
        <article class="content card">
            {content}
        </article>
        
        <nav class="pagination">
            {navigation['prev_link'] if navigation.get('prev_link') else ''}
            {navigation['next_link'] if navigation.get('next_link') else ''}
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
</html>"""

    def generate_navigation(self, current_folder: str) -> Dict[str, str]:
        """Generate navigation links"""
        nav_file = self.root_path / 'navigation.json'
        if not nav_file.exists():
            return {'prev_link': '', 'next_link': ''}
            
        nav_data = json.loads(nav_file.read_text())
        current = nav_data.get(current_folder, {})
        
        prev_link = ''
        if current.get('previous'):
            prev_title = current['previous'].split('_', 1)[1].replace('_', ' ')
            prev_link = f'<a href="../{current["previous"]}" class="prev">← {prev_title}</a>'
            
        next_link = ''
        if current.get('next'):
            next_title = current['next'].split('_', 1)[1].replace('_', ' ')
            next_link = f'<a href="../{current["next"]}" class="next">{next_title} →</a>'
            
        return {'prev_link': prev_link, 'next_link': next_link}

def main():
    """Process all knowledge blocks"""
    generator = TemplateGenerator('.')
    for folder in sorted(os.listdir('.')):
        if os.path.isdir(folder) and folder[0].isdigit():
            print(f"Processing {folder}...")
            html = generator.generate_index_html(folder)
            output_path = Path(folder) / 'index.html'
            output_path.write_text(html, encoding='utf-8')
            print(f"Created {output_path}")

if __name__ == '__main__':
    main()