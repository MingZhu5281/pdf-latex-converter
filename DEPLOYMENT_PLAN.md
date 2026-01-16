# PDF to LaTeX Converter - Deployment Plan
*Simple, Standard, and Beginner-Friendly Website Deployment*

## Project Overview
A free-to-use website that converts PDF files to LaTeX code using OpenAI's GPT-4o multi-modal API. Users upload PDFs, and the AI generates corresponding LaTeX code.

## Technology Stack
- **Backend**: Python (Flask/FastAPI)
- **Frontend**: HTML, CSS, JavaScript (simple, no frameworks)
- **AI API**: OpenAI GPT-4o (multi-modal)
- **Server**: Rocky Linux 10.0 VM
- **Version Control**: Git
- **Web Server**: Nginx
- **Process Manager**: systemd
- **SSL**: Let's Encrypt (free)

## Prerequisites
- Rocky Linux 10.0 VM with root access
- Domain name (optional but recommended)
- OpenAI API key
- Basic Linux command line knowledge

---

## Phase 1: Project Setup & Development (Local)

### 1.1 Initialize Git Repository
```bash
# Create project directory
mkdir pdf-latex-converter
cd pdf-latex-converter

# Initialize git
git init
git add .
git commit -m "Initial commit: PDF to LaTeX converter"
```

### 1.2 Project Structure
```
pdf-latex-converter/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── pdf_processor.py
│   └── latex_generator.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   └── index.html
├── requirements.txt
├── config.py
├── .env.example
├── .gitignore
└── README.md
```

### 1.3 Core Dependencies (requirements.txt)
```
flask==3.0.0
openai==1.99.9
pymupdf==1.26.3
python-dotenv==1.0.0
gunicorn==21.2.0
```

### 1.4 Environment Configuration (.env.example)
```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=production
FLASK_SECRET_KEY=your_secret_key_here
MAX_FILE_SIZE=10485760
```

---

## Phase 2: Backend Development

### 2.1 Flask Application (app/main.py)
```python
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from .pdf_processor import PDFProcessor
from .latex_generator import LaTeXGenerator

app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Process PDF and generate LaTeX
        processor = PDFProcessor()
        latex_code = processor.convert_to_latex(file)
        
        return jsonify({
            'success': True,
            'latex_code': latex_code
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
```

### 2.2 PDF Processing (app/pdf_processor.py)
```python
import fitz  # PyMuPDF
import base64
from .latex_generator import LaTeXGenerator

class PDFProcessor:
    def __init__(self):
        self.latex_generator = LaTeXGenerator()
    
    def convert_to_latex(self, pdf_file):
        # Convert PDF pages to images
        images = self._pdf_to_images(pdf_file)
        
        # Generate LaTeX using AI
        latex_code = self.latex_generator.generate_latex(images)
        
        return latex_code
    
    def _pdf_to_images(self, pdf_file):
        # Implementation based on your notebook
        # Convert PDF pages to base64 encoded images
        pass
```

### 2.3 LaTeX Generation (app/latex_generator.py)
```python
import os
from openai import OpenAI

class LaTeXGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def generate_latex(self, images):
        # Implementation based on your notebook
        # Call GPT-4o API with images and generate LaTeX
        pass
```

---

## Phase 3: Frontend Development

### 3.1 HTML Template (templates/index.html)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF to LaTeX Converter</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <h1>PDF to LaTeX Converter</h1>
        <p>Upload a PDF file and get LaTeX code using AI</p>
        
        <div class="upload-section">
            <input type="file" id="pdfFile" accept=".pdf" />
            <button onclick="convertPDF()">Convert to LaTeX</button>
        </div>
        
        <div class="result-section" id="resultSection" style="display: none;">
            <h3>Generated LaTeX Code:</h3>
            <pre id="latexOutput"></pre>
            <button onclick="copyToClipboard()">Copy to Clipboard</button>
            <button onclick="downloadLatex()">Download .tex file</button>
        </div>
        
        <div class="loading" id="loading" style="display: none;">
            Converting... Please wait.
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

### 3.2 CSS Styling (static/css/style.css)
```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.upload-section {
    text-align: center;
    margin: 30px 0;
    padding: 20px;
    border: 2px dashed #ddd;
    border-radius: 10px;
}

button {
    background: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    margin: 10px;
}

button:hover {
    background: #0056b3;
}

.result-section pre {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    border: 1px solid #dee2e6;
}
```

### 3.3 JavaScript (static/js/main.js)
```javascript
async function convertPDF() {
    const fileInput = document.getElementById('pdfFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a PDF file');
        return;
    }
    
    const formData = new FormData();
    formData.append('pdf_file', file);
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultSection').style.display = 'none';
    
    try {
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('latexOutput').textContent = result.latex_code;
            document.getElementById('resultSection').style.display = 'block';
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function copyToClipboard() {
    const latexCode = document.getElementById('latexOutput').textContent;
    navigator.clipboard.writeText(latexCode);
    alert('LaTeX code copied to clipboard!');
}

function downloadLatex() {
    const latexCode = document.getElementById('latexOutput').textContent;
    const blob = new Blob([latexCode], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'converted.tex';
    a.click();
    window.URL.revokeObjectURL(url);
}
```

---

## Phase 4: Server Setup (Rocky Linux 10.0)

### 4.1 Initial Server Setup
```bash
# Update system
sudo dnf update -y

# Install essential packages
sudo dnf install -y git python3 python3-pip python3-devel nginx firewalld

# Start and enable services
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 4.2 Configure Firewall
```bash
# Allow SSH, HTTP, and HTTPS
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 4.3 Create Application User
```bash
# Create user for the application
sudo useradd -r -s /bin/false pdfconverter
sudo mkdir -p /var/www/pdf-latex-converter
sudo chown pdfconverter:pdfconverter /var/www/pdf-latex-converter
```

---

## Phase 5: Application Deployment

### 5.1 Clone and Setup Application
```bash
# Switch to application user
sudo -u pdfconverter bash

# Clone repository
cd /var/www/pdf-latex-converter
git clone https://github.com/MingZhu5281/pdf-latex-converter.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env.example .env
# Edit .env with your actual API keys
nano .env
```

### 5.2 Create Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/pdf-latex-converter.service
```

Service file content:
```ini
[Unit]
Description=PDF to LaTeX Converter
After=network.target

[Service]
Type=exec
User=pdfconverter
Group=pdfconverter
WorkingDirectory=/var/www/pdf-latex-converter
Environment=PATH=/var/www/pdf-latex-converter/venv/bin
ExecStart=/var/www/pdf-latex-converter/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### 5.3 Start Application Service
```bash
# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl start pdf-latex-converter
sudo systemctl enable pdf-latex-converter

# Check status
sudo systemctl status pdf-latex-converter
```

---

## Phase 6: Nginx Configuration

### 6.1 Configure Nginx
```bash
# Create nginx configuration
sudo nano /etc/nginx/conf.d/pdf-latex-converter.conf
```

Configuration content:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain or IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Increase upload size limit
    client_max_body_size 10M;
}
```

### 6.2 Test and Reload Nginx
```bash
# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

---

## Phase 7: SSL Certificate (Optional but Recommended)

### 7.1 Install Certbot
```bash
# Install EPEL and certbot
sudo dnf install -y epel-release
sudo dnf install -y certbot python3-certbot-nginx
```

### 7.2 Obtain SSL Certificate
```bash
# Get certificate (replace with your domain)
sudo certbot --nginx -d latexconverterai.com

# Test auto-renewal
sudo certbot renew --dry-run
```

---

## Phase 8: Testing and Monitoring

### 8.1 Test the Application
```bash
# Test locally
curl http://localhost:8000

# Test through nginx
curl http://latexconverterai.com
curl https://latexconverterai.com

```

### 8.2 Monitor Logs
```bash
# Application logs
sudo journalctl -u pdf-latex-converter -f
sudo journalctl -u pdf-latex-converter -n 50

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## Phase 9: Maintenance and Updates

### 9.1 Regular Updates
```bash
# Update system packages
sudo dnf update -y

# Update application
cd /var/www/pdf-latex-converter
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart pdf-latex-converter
```

### 9.2 Backup Strategy
```bash
# Backup application
sudo tar -czf /backup/pdf-latex-converter-$(date +%Y%m%d).tar.gz /var/www/pdf-latex-converter

# Backup nginx config
sudo cp /etc/nginx/conf.d/pdf-latex-converter.conf /backup/
```

---

## Troubleshooting Common Issues

### Application Won't Start
```bash
# Check service status
sudo systemctl status pdf-latex-converter

# Check logs
sudo journalctl -u pdf-latex-converter -n 50

# Check permissions
ls -la /var/www/pdf-latex-converter/
```

### Nginx Issues
```bash
# Check nginx status
sudo systemctl status nginx

# Check configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log
```

### File Upload Issues
```bash
# Check file permissions
sudo chown -R pdfconverter:pdfconverter /var/www/pdf-latex-converter

# Check nginx upload limits
grep client_max_body_size /etc/nginx/nginx.conf
```

---

## Security Considerations

1. **API Key Security**: Never commit API keys to git
2. **File Upload Limits**: Restrict file sizes and types
3. **User Permissions**: Run application with minimal privileges
4. **Firewall**: Only open necessary ports
5. **Regular Updates**: Keep system and dependencies updated
6. **SSL**: Use HTTPS in production

---

## Cost Breakdown

- **Server**: $5-10/month (VPS)
- **Domain**: $10-15/year (optional)
- **OpenAI API**: Pay-per-use (typically $0.01-0.10 per conversion)
- **SSL Certificate**: Free (Let's Encrypt)

**Total**: ~$5-15/month depending on usage

---

## Next Steps

1. **Local Development**: Build and test the application locally
2. **Git Repository**: Push code to GitHub/GitLab
3. **Server Setup**: Provision Rocky Linux VM
4. **Deployment**: Follow deployment steps
5. **Testing**: Verify functionality
6. **Monitoring**: Set up basic monitoring
7. **Documentation**: Create user documentation

---

## Support Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Nginx Documentation**: https://nginx.org/en/docs/
- **Rocky Linux Documentation**: https://docs.rockylinux.org/
- **OpenAI API Documentation**: https://platform.openai.com/docs/

---

*This plan is designed to be beginner-friendly while following industry best practices. Each step builds upon the previous one, allowing you to learn and understand the deployment process.*
