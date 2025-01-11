from pathlib import Path
import re

def fix_css_paths():
    root = Path(__file__).parent
    pattern = re.compile(r'(href|src)="[^"]*templates/styles/theme\.css"')
    replacement = r'\1="../static/css/dark-theme.css"'
    
    # Find all index.html files
    for html_file in root.glob('*/index.html'):
        print(f"Processing {html_file}")
        content = html_file.read_text(encoding='utf-8')
        
        if 'templates/styles/theme.css' in content:
            # Replace both preload and stylesheet links
            updated = pattern.sub(replacement, content)
            html_file.write_text(updated, encoding='utf-8')
            print(f"Updated {html_file}")

if __name__ == '__main__':
    fix_css_paths()
