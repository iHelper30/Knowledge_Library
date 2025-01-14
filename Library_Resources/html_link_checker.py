import os
import re
from bs4 import BeautifulSoup

def check_html_links(base_path):
    link_issues = {
        'broken_internal_links': [],
        'missing_target_directories': [],
        'potential_link_errors': []
    }
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    # Check links in each HTML file
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check href links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                
                # Skip external and anchor links
                if href.startswith(('http', '#', 'mailto:', 'tel:')):
                    continue
                
                # Construct full path
                full_link_path = os.path.normpath(os.path.join(os.path.dirname(html_file), href))
                
                # Check if link target exists
                if not os.path.exists(full_link_path):
                    link_issues['broken_internal_links'].append({
                        'source_file': html_file,
                        'broken_link': href
                    })
    
    return link_issues

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    link_validation = check_html_links(base_path)
    
    print("HTML Link Validation Results:")
    for category, issues in link_validation.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        if issues:
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("  No issues found")

if __name__ == '__main__':
    main()
