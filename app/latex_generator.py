import os
from openai import OpenAI

class LaTeXGenerator:
    """Handles LaTeX generation using OpenAI GPT-4o API"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
    
    def generate_latex(self, images):
        """
        Generate LaTeX code from PDF page images using GPT-4o
        
        Args:
            images: List of base64 encoded image strings
            
        Returns:
            str: Generated LaTeX code
        """
        try:
            # Prepare message content with images
            content = [
                {
                    "type": "text", 
                    "text": self._get_conversion_prompt()
                }
            ]
            
            # Add images to the content
            for image_data in images:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_data}",
                        "detail": "high"
                    }
                })
            
            # Prepare the message
            messages = [
                {
                    "role": "user",
                    "content": content
                }
            ]
            
            # Make API call
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.0,  # Use 0.0 for deterministic output
                max_tokens=4000   # Increase for longer documents
            )
            
            # Extract the generated LaTeX code
            if response and response.choices and len(response.choices) > 0:
                latex_code = response.choices[0].message.content
                
                # Clean up the response (remove code block markers if present)
                latex_code = self._clean_latex_output(latex_code)
                
                return latex_code
            else:
                raise Exception("No response received from OpenAI API")
                
        except Exception as e:
            raise Exception(f"LaTeX generation failed: {str(e)}")
    
    def _get_conversion_prompt(self):
        """
        Get the prompt for LaTeX conversion
        
        Returns:
            str: Conversion prompt for GPT-4o
        """
        return """Please convert the content of these PDF pages to LaTeX code. 

Requirements:
1. Create a complete, compilable LaTeX document
2. Include appropriate document class and packages
3. Preserve the structure, formatting, and mathematical expressions
4. Use proper LaTeX syntax for equations, tables, figures, etc.
5. Include section headings and proper formatting
6. If there are images or diagrams, describe them in comments
7. Make sure the output is clean and well-formatted

Return only the LaTeX code without any additional explanations or markdown formatting."""
    
    def _clean_latex_output(self, latex_code):
        """
        Clean up the LaTeX output from the API
        
        Args:
            latex_code: Raw LaTeX code from API
            
        Returns:
            str: Cleaned LaTeX code
        """
        # Remove markdown code block markers if present
        if latex_code.startswith('```latex'):
            latex_code = latex_code[8:]  # Remove ```latex
        elif latex_code.startswith('```'):
            latex_code = latex_code[3:]   # Remove ```
        
        if latex_code.endswith('```'):
            latex_code = latex_code[:-3]  # Remove trailing ```
        
        # Strip whitespace
        latex_code = latex_code.strip()
        
        # Ensure document starts with \documentclass if it doesn't already
        if not latex_code.startswith('\\documentclass'):
            # If it doesn't start with documentclass, wrap it in a basic document structure
            latex_code = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}

\\begin{{document}}

{latex_code}

\\end{{document}}"""
        
        return latex_code
