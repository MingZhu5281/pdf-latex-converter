import fitz  # PyMuPDF
import base64
import io
from .latex_generator import LaTeXGenerator

class PDFProcessor:
    """Handles PDF processing and conversion to LaTeX"""
    
    def __init__(self):
        self.latex_generator = LaTeXGenerator()
    
    def convert_to_latex(self, pdf_file):
        """
        Convert uploaded PDF file to LaTeX code
        
        Args:
            pdf_file: Flask file object containing PDF data
            
        Returns:
            str: Generated LaTeX code
        """
        try:
            # Convert PDF pages to images
            images = self._pdf_to_images(pdf_file)
            
            if not images:
                raise ValueError("No pages found in PDF or failed to process pages")
            
            # Generate LaTeX using AI
            latex_code = self.latex_generator.generate_latex(images)
            
            return latex_code
            
        except Exception as e:
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def _pdf_to_images(self, pdf_file):
        """
        Convert PDF pages to base64 encoded images
        
        Args:
            pdf_file: Flask file object containing PDF data
            
        Returns:
            list: List of base64 encoded image strings
        """
        try:
            # Read PDF data into memory
            pdf_data = pdf_file.read()
            pdf_file.seek(0)  # Reset file pointer
            
            # Open PDF document
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            images = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Convert page to high-resolution image
                # Using 300 DPI for good quality
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")
                
                # Encode to base64
                encoded_image = base64.b64encode(img_data).decode('utf-8')
                images.append(encoded_image)
            
            doc.close()
            return images
            
        except Exception as e:
            raise Exception(f"Failed to convert PDF to images: {str(e)}")
    
    def get_pdf_info(self, pdf_file):
        """
        Get basic information about the PDF
        
        Args:
            pdf_file: Flask file object containing PDF data
            
        Returns:
            dict: PDF information (page count, etc.)
        """
        try:
            pdf_data = pdf_file.read()
            pdf_file.seek(0)  # Reset file pointer
            
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            info = {
                'page_count': len(doc),
                'title': doc.metadata.get('title', ''),
                'author': doc.metadata.get('author', ''),
            }
            doc.close()
            
            return info
            
        except Exception as e:
            raise Exception(f"Failed to get PDF info: {str(e)}")
