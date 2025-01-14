import os
import docx
from markdownify import markdownify

class DocxToMarkdownConverter:
    def __init__(self, input_dir, output_dir):
        """
        Initialize converter with input and output directories
        
        :param input_dir: Directory containing .docx files
        :param output_dir: Directory to save converted Markdown files
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def convert_docx_to_markdown(self, filename):
        """
        Convert a single .docx file to Markdown
        
        :param filename: Name of the .docx file to convert
        :return: Markdown content as string
        """
        # Full path to the input file
        input_path = os.path.join(self.input_dir, filename)
        
        try:
            # Read the Word document
            doc = docx.Document(input_path)
            
            # Extract text from paragraphs
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            
            # Join paragraphs
            html_content = '<html><body>' + '\n'.join(f'<p>{p}</p>' for p in full_text) + '</body></html>'
            
            # Convert to Markdown
            markdown_content = markdownify(html_content, heading_style="ATX")
            
            return markdown_content
        
        except Exception as e:
            print(f"Error converting {filename}: {e}")
            return None
    
    def batch_convert(self):
        """
        Convert all .docx files in the input directory to Markdown
        """
        # Track conversion results
        conversion_results = {
            'total_files': 0,
            'converted_files': 0,
            'failed_files': []
        }
        
        # Iterate through files in input directory
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.docx'):
                conversion_results['total_files'] += 1
                
                # Convert filename to Markdown filename
                md_filename = os.path.splitext(filename)[0] + '.md'
                
                # Convert document
                markdown_content = self.convert_docx_to_markdown(filename)
                
                if markdown_content:
                    # Write Markdown to file
                    output_path = os.path.join(self.output_dir, md_filename)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    
                    conversion_results['converted_files'] += 1
                else:
                    conversion_results['failed_files'].append(filename)
        
        # Print conversion summary
        print("\n--- Conversion Summary ---")
        print(f"Total files: {conversion_results['total_files']}")
        print(f"Successfully converted: {conversion_results['converted_files']}")
        print(f"Failed files: {conversion_results['failed_files']}")
        
        return conversion_results

def main():
    # Directories for input and output
    input_dir = r'C:\Users\ihelp\KnowledgeLibrary\Templates_NEW'
    output_dir = r'C:\Users\ihelp\KnowledgeLibrary\Templates_Markdown'
    
    # Create converter
    converter = DocxToMarkdownConverter(input_dir, output_dir)
    
    # Perform batch conversion
    converter.batch_convert()

if __name__ == '__main__':
    main()
