import os
import shutil

def organize_templates(markdown_dir, templates_root):
    """
    Organize Markdown templates into structured folders
    
    :param markdown_dir: Directory containing Markdown files
    :param templates_root: Root directory for organized templates
    """
    # Ensure templates root exists
    os.makedirs(templates_root, exist_ok=True)
    
    # Template to folder name mapping
    template_mapping = {
        "Case Study Template.md": "01_Case_Study_Template",
        "Comprehensive White Paper Outline Template.md": "02_White_Paper_Template",
        "High-Converting Email Newsletter Template.md": "03_Email_Newsletter_Template",
        "Podcast Episode Outline Template.md": "04_Podcast_Episode_Template",
        "Press Release Template.md": "05_Press_Release_Template",
        "Sales Page Template.md": "06_Sales_Page_Template",
        "Social Media Carousel Post Template.md": "07_Social_Media_Carousel_Template",
        "The Ultimate Blog Post Template.md": "08_Blog_Post_Template",
        "Webinar_Workshop Outline Template.md": "09_Webinar_Workshop_Template"
    }
    
    # Process each template
    for filename, folder_name in template_mapping.items():
        # Full paths
        markdown_path = os.path.join(markdown_dir, filename)
        folder_path = os.path.join(templates_root, folder_name)
        
        # Create folder
        os.makedirs(folder_path, exist_ok=True)
        
        # Copy Markdown file
        dest_path = os.path.join(folder_path, "template.md")
        shutil.copy2(markdown_path, dest_path)
        
        print(f"Organized: {filename} -> {folder_name}/template.md")

def main():
    markdown_dir = r'C:\Users\ihelp\KnowledgeLibrary\Templates_Markdown'
    templates_root = r'C:\Users\ihelp\KnowledgeLibrary\Templates_NEW'
    
    organize_templates(markdown_dir, templates_root)

if __name__ == '__main__':
    main()
