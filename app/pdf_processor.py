import fitz  # PyMuPDF
import base64
import io
from .latex_generator import LaTeXGenerator
from .rate_limiter import RateLimitConfig

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
            # First, validate page count before processing
            is_valid, page_count, error_msg = self._validate_page_count(pdf_file)
            if not is_valid:
                raise ValueError(error_msg)
            
            print(f"Processing PDF with {page_count} pages (limit: {RateLimitConfig.MAX_PAGES_PER_CONVERSION})")
            
            # Convert PDF pages to images
            images = self._pdf_to_images(pdf_file)
            
            if not images:
                raise ValueError("No pages found in PDF or failed to process pages")
            
            # Generate LaTeX using AI
            latex_code = self.latex_generator.generate_latex(images)
            
            return latex_code
            
        except Exception as e:
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def _validate_page_count(self, pdf_file):
        """
        Validate PDF page count against limits
        
        Args:
            pdf_file: Flask file object containing PDF data
            
        Returns:
            tuple: (is_valid, page_count, error_message)
        """
        try:
            # Read PDF data
            pdf_data = pdf_file.read()
            pdf_file.seek(0)  # Reset file pointer for later use
            
            # Open PDF to get page count
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            page_count = len(doc)
            doc.close()
            
            # Check against limit
            if page_count > RateLimitConfig.MAX_PAGES_PER_CONVERSION:
                error_msg = (
                    f"PDF has {page_count} pages, but maximum allowed is "
                    f"{RateLimitConfig.MAX_PAGES_PER_CONVERSION} pages per conversion. "
                    "Please split your document into smaller files."
                )
                return False, page_count, error_msg
            
            if page_count == 0:
                return False, 0, "PDF appears to be empty or corrupted."
            
            return True, page_count, None
            
        except Exception as e:
            error_msg = f"Could not validate PDF: {str(e)}"
            return False, 0, error_msg
    
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
