import re
import json
import markdown2
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Any
from datetime import datetime

class ContentProcessor:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.library_metadata = self._load_library_metadata()
        
    def _load_library_metadata(self) -> Dict[str, Any]:
        """Load global library metadata"""
        metadata_file = self.root_path / 'library_metadata.json'
        if metadata_file.exists():
            return json.loads(metadata_file.read_text(encoding='utf-8'))
        return {}
        
    def parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Extract frontmatter and content from markdown"""
        frontmatter_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
        match = frontmatter_pattern.match(content)
        
        if match:
            try:
                frontmatter = json.loads(match.group(1))
                content = content[match.end():]
                return frontmatter, content
            except json.JSONDecodeError:
                pass
        
        return {}, content
        
    def process_markdown(self, folder_path: Path) -> Tuple[Dict, str]:
        """Process markdown file with frontmatter and additional resources"""
        readme_path = folder_path / 'README.md'
        if not readme_path.exists():
            return self._generate_default_metadata(folder_path), '<p>Content coming soon.</p>'
            
        content = readme_path.read_text(encoding='utf-8')
        metadata, markdown_content = self.parse_frontmatter(content)
        
        # Enhance metadata with library-wide information
        metadata = self._enhance_metadata(metadata, folder_path)
        
        # Process content
        markdown_content = self._process_content(markdown_content, folder_path)
        
        # Convert to HTML with extras
        html_content = markdown2.markdown(
            markdown_content,
            extras=[
                'metadata', 'tables', 'fenced-code-blocks', 
                'header-ids', 'footnotes', 'smarty-pants'
            ]
        )
        
        # Add additional resources section if available
        resources = self._gather_resources(folder_path)
        if resources:
            html_content += resources
            
        return metadata, html_content
        
    def _enhance_metadata(self, metadata: Dict, folder_path: Path) -> Dict:
        """Enhance metadata with additional information"""
        folder_name = folder_path.name
        section_id = folder_name.split('_')[0]
        
        # Get section metadata from library_metadata.json
        section_metadata = self.library_metadata.get(section_id, {})
        
        enhanced = {
            'title': metadata.get('title', folder_name.split('_', 1)[1].replace('_', ' ')),
            'subtitle': metadata.get('subtitle', section_metadata.get('subtitle', '')),
            'description': metadata.get('description', section_metadata.get('description', '')),
            'keywords': metadata.get('keywords', folder_name.lower().split('_')),
            'category': section_metadata.get('category', ''),
            'difficulty': section_metadata.get('difficulty', 'Beginner'),
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'section_id': section_id,
            'related_sections': section_metadata.get('related_sections', [])
        }
        
        return enhanced
        
    def _process_content(self, content: str, folder_path: Path) -> str:
        """Process markdown content with enhanced features"""
        # Fix internal links
        content = self._fix_internal_links(content)
        
        # Process custom directives
        content = self._process_directives(content, folder_path)
        
        return content
        
    def _fix_internal_links(self, content: str) -> str:
        """Convert relative markdown links to proper HTML paths"""
        def replace_link(match):
            link_text = match.group(1)
            link_path = match.group(2)
            
            if link_path.endswith('.md'):
                link_path = link_path[:-3] + '.html'
            return f'[{link_text}]({link_path})'
            
        pattern = r'\[(.*?)\]\((.*?\.md)\)'
        return re.sub(pattern, replace_link, content)
        
    def _process_directives(self, content: str, folder_path: Path) -> str:
        """Process custom markdown directives"""
        # Process code includes
        content = re.sub(
            r'@include\(code:(.*?)\)',
            lambda m: self._include_code(m.group(1), folder_path),
            content
        )
        
        # Process file references
        content = re.sub(
            r'@include\(file:(.*?)\)',
            lambda m: self._include_file(m.group(1), folder_path),
            content
        )
        
        return content
        
    def _include_code(self, filepath: str, base_path: Path) -> str:
        """Include code file with syntax highlighting"""
        try:
            file_path = (base_path / filepath).resolve()
            if file_path.exists() and file_path.is_relative_to(self.root_path):
                ext = file_path.suffix.lstrip('.')
                code = file_path.read_text(encoding='utf-8')
                return f'```{ext}\n{code}\n```'
        except Exception:
            pass
        return f'<!-- Failed to include code from {filepath} -->'
        
    def _include_file(self, filepath: str, base_path: Path) -> str:
        """Include general file content"""
        try:
            file_path = (base_path / filepath).resolve()
            if file_path.exists() and file_path.is_relative_to(self.root_path):
                content = file_path.read_text(encoding='utf-8')
                return content
        except Exception:
            pass
        return f'<!-- Failed to include file {filepath} -->'
        
    def _gather_resources(self, folder_path: Path) -> str:
        """Gather and format additional resources in the folder"""
        resources = []
        
        # Look for specific file types
        for ext in ['.pdf', '.docx', '.xlsx', '.pptx', '.zip']:
            files = list(folder_path.glob(f'*{ext}'))
            if files:
                resources.append(f'<h3>Additional {ext.upper()[1:]} Resources</h3>')
                resources.append('<ul>')
                for file in files:
                    resources.append(f'<li><a href="{file.name}">{file.stem}</a></li>')
                resources.append('</ul>')
        
        if resources:
            return '\n<section class="additional-resources">\n<h2>Additional Resources</h2>\n' + '\n'.join(resources) + '\n</section>'
        return ''
        
    def _generate_default_metadata(self, folder_path: Path) -> Dict:
        """Generate default metadata for folders without README"""
        folder_name = folder_path.name
        section_id = folder_name.split('_')[0]
        title = folder_name.split('_', 1)[1].replace('_', ' ')
        
        return {
            'title': title,
            'subtitle': f'Resources and guides for {title.lower()}',
            'description': f'Comprehensive information about {title.lower()}',
            'keywords': folder_name.lower().split('_'),
            'category': 'Resources',
            'difficulty': 'Beginner',
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'section_id': section_id
        }
        
    def generate_section_nav(self, content: str) -> str:
        """Generate section navigation from content headers"""
        headers = re.findall(r'<h([2-3])[^>]*>(.*?)</h\1>', content)
        if not headers:
            return ''
            
        nav = ['<nav class="section-nav"><ul>']
        for level, title in headers:
            indent = '  ' * (int(level) - 2)
            nav.append(f'{indent}<li><a href="#{title.lower().replace(" ", "-")}">{title}</a></li>')
        nav.append('</ul></nav>')
        
        return '\n'.join(nav)

    def process_folder(self, folder_name: str) -> Tuple[Dict, str]:
        """Process a knowledge block folder"""
        folder_path = self.root_path / folder_name
        metadata, content = self.process_markdown(folder_path)
        
        # Generate section navigation
        section_nav = self.generate_section_nav(content)
        
        # Add section navigation before main content
        if section_nav:
            content = f'{section_nav}\n{content}'
            
        return metadata, content
