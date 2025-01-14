import os
import json

class ReadmeGenerator:
    def __init__(self):
        # Predefined template descriptions and keywords
        self.template_details = {
            "01_Case_Study_Template": {
                "summary": "A comprehensive template for creating compelling case studies that showcase business success stories, highlighting challenges, solutions, and measurable results.",
                "keywords": ["case study", "business storytelling", "success metrics", "customer journey", "problem-solution narrative"],
                "notes": "Ideal for marketing teams, sales professionals, and content creators looking to demonstrate real-world value and impact."
            },
            "02_White_Paper_Template": {
                "summary": "A structured template for developing in-depth, authoritative white papers that explore complex topics, provide research-backed insights, and establish thought leadership.",
                "keywords": ["white paper", "research document", "thought leadership", "industry analysis", "technical writing"],
                "notes": "Best used for B2B marketing, technical industries, and academic or professional research presentations."
            },
            "03_Email_Newsletter_Template": {
                "summary": "A high-converting email newsletter template designed to engage subscribers, deliver value, and drive meaningful action through strategic content structuring.",
                "keywords": ["email marketing", "newsletter", "subscriber engagement", "conversion optimization", "content strategy"],
                "notes": "Optimized for various industries, focusing on clear communication and compelling call-to-actions."
            },
            "04_Podcast_Episode_Template": {
                "summary": "A comprehensive outline template for planning and structuring podcast episodes, ensuring consistent quality, engaging content, and smooth narrative flow.",
                "keywords": ["podcast", "content planning", "episode structure", "interview guide", "audio content"],
                "notes": "Useful for podcasters, content creators, and media professionals seeking a systematic approach to episode development."
            },
            "05_Press_Release_Template": {
                "summary": "A professional press release template that follows industry standards, helping organizations communicate newsworthy information clearly and effectively.",
                "keywords": ["press release", "media communication", "public relations", "news announcement", "corporate communication"],
                "notes": "Designed to meet journalistic standards and maximize media pickup potential."
            },
            "06_Sales_Page_Template": {
                "summary": "A high-converting sales page template that guides potential customers through a persuasive narrative, addressing pain points and showcasing product value.",
                "keywords": ["sales page", "conversion optimization", "landing page", "copywriting", "marketing funnel"],
                "notes": "Crafted to increase conversion rates across various industries and product types."
            },
            "07_Social_Media_Carousel_Template": {
                "summary": "A strategic template for creating engaging multi-slide social media carousel posts that tell a story, educate, and drive audience interaction.",
                "keywords": ["social media", "carousel post", "content design", "visual storytelling", "audience engagement"],
                "notes": "Optimized for platforms like Instagram, LinkedIn, and Facebook to maximize content impact."
            },
            "08_Blog_Post_Template": {
                "summary": "The ultimate blog post template that provides a structured approach to creating high-quality, SEO-friendly content that resonates with readers and search engines.",
                "keywords": ["blog writing", "content strategy", "SEO", "long-form content", "audience engagement"],
                "notes": "Adaptable to various niches and writing styles, focusing on clarity and reader value."
            },
            "09_Webinar_Workshop_Template": {
                "summary": "A comprehensive template for planning and executing impactful webinars and workshops, ensuring structured content delivery and maximum audience engagement.",
                "keywords": ["webinar", "workshop", "online training", "content planning", "presentation structure"],
                "notes": "Ideal for educators, trainers, and professionals conducting online learning sessions."
            }
        }
    
    def generate_readme(self, template_folder):
        """
        Generate a README.md for a specific template folder
        
        :param template_folder: Name of the template folder
        :return: Markdown content for README.md
        """
        if template_folder not in self.template_details:
            raise ValueError(f"No details found for template: {template_folder}")
        
        details = self.template_details[template_folder]
        
        readme_content = f"""# {template_folder.replace('_', ' ')}

## Summary
{details['summary']}

## Keywords
{', '.join(details['keywords'])}

## Notes
{details['notes']}

## How to Use This Template
1. Review the entire template carefully
2. Customize the content to fit your specific needs
3. Replace placeholder text with your own information
4. Proofread and refine your document

## Best Practices
- Maintain the overall structure of the template
- Adapt the language to your brand voice
- Focus on clarity and value for your audience

## Template Version
Version: 1.0
Last Updated: {os.getenv('CURRENT_DATE', '2025-01-12')}
"""
        return readme_content
    
    def generate_all_readmes(self, templates_root):
        """
        Generate README.md for all template folders
        
        :param templates_root: Root directory containing template folders
        """
        for folder in os.listdir(templates_root):
            folder_path = os.path.join(templates_root, folder)
            if os.path.isdir(folder_path):
                readme_path = os.path.join(folder_path, 'README.md')
                readme_content = self.generate_readme(folder)
                
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(readme_content)
                
                print(f"Generated README for: {folder}")

def main():
    templates_root = r'C:\Users\ihelp\KnowledgeLibrary\Templates_NEW'
    generator = ReadmeGenerator()
    generator.generate_all_readmes(templates_root)

if __name__ == '__main__':
    main()
