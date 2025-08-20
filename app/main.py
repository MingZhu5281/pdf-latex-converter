from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from .pdf_processor import PDFProcessor
from .latex_generator import LaTeXGenerator

def create_app():
    """Application factory pattern"""
    # Create Flask app with correct template and static directories
    app = Flask(__name__, 
               template_folder='../templates',
               static_folder='../static')
    
    # Load configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 10485760))
    app.config['DEBUG'] = os.getenv('FLASK_ENV', 'production') == 'development'
    
    # Initialize processors
    pdf_processor = PDFProcessor()
    
    return app

# Create the app instance
app = create_app()

# Initialize processors outside factory for this simple structure
pdf_processor = PDFProcessor()

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    """Convert PDF to LaTeX endpoint"""
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check file extension
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Please upload a PDF file'}), 400
    
    # Check file size (10MB limit)
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    max_size = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB default
    if file_size > max_size:
        return jsonify({'error': f'File too large. Maximum size is {max_size/1024/1024:.1f}MB'}), 400
    
    try:
        # Process PDF and generate LaTeX
        latex_code = pdf_processor.convert_to_latex(file)
        
        return jsonify({
            'success': True,
            'latex_code': latex_code
        })
    except Exception as e:
        app.logger.error(f"Conversion error: {str(e)}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'pdf-latex-converter'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
