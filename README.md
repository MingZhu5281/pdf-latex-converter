# PDF to LaTeX Converter

A free-to-use web application that converts PDF documents to LaTeX code using OpenAI's GPT-4o multi-modal API.

## Features

- 🤖 **AI-Powered**: Uses OpenAI GPT-4o for intelligent PDF to LaTeX conversion
- 📄 **Multi-Page Support**: Handles PDFs with multiple pages
- 🎨 **Beautiful UI**: Modern, responsive web interface
- 🔒 **Secure**: Files are processed securely and not stored
- ⚡ **Fast**: Quick conversion with real-time progress feedback
- 💾 **Export Options**: Copy to clipboard or download as .tex file

## Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **AI**: OpenAI GPT-4o API
- **PDF Processing**: PyMuPDF (fitz)

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd pdf-latex-converter
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python -m flask --app app.main run --debug
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
FLASK_ENV=development
FLASK_SECRET_KEY=your_secret_key_here
MAX_FILE_SIZE=10485760
```

## Usage

1. **Upload PDF**: Click "Choose PDF File" or drag and drop a PDF file
2. **Convert**: Click "Convert to LaTeX" to start the conversion
3. **Download**: Copy the LaTeX code or download as a .tex file

### File Limitations

- **Maximum file size**: 10MB
- **Supported format**: PDF only
- **Processing time**: Varies based on PDF complexity (typically 10-30 seconds)

## Deployment

For production deployment instructions, see [DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md).

## Project Structure

```
pdf-latex-converter/
├── app/
│   ├── __init__.py
│   ├── main.py              # Flask application
│   ├── pdf_processor.py     # PDF processing logic
│   └── latex_generator.py   # LaTeX generation with AI
├── static/
│   ├── css/
│   │   └── style.css        # Styles
│   └── js/
│       └── main.js          # Frontend JavaScript
├── templates/
│   └── index.html           # Main HTML template
├── requirements.txt         # Python dependencies
├── config.py               # Application configuration
├── env.example             # Environment variables example
├── .gitignore
└── README.md
```

## API Endpoints

- `GET /` - Main application page
- `POST /convert` - Convert PDF to LaTeX
- `GET /health` - Health check endpoint

## Development

### Adding New Features

1. **Backend changes**: Modify files in the `app/` directory
2. **Frontend changes**: Update `templates/index.html`, `static/css/style.css`, or `static/js/main.js`
3. **Configuration**: Update `config.py` or environment variables

### Testing

```bash
# Test the health endpoint
curl http://localhost:5000/health

# Test file upload (replace with actual PDF file)
curl -X POST -F "pdf_file=@test.pdf" http://localhost:5000/convert
```

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY is required"**
   - Make sure you've set the `OPENAI_API_KEY` in your `.env` file
   - Verify the API key is valid and has sufficient credits

2. **"File too large" error**
   - Check the file size limit in your `.env` file (`MAX_FILE_SIZE`)
   - Default limit is 10MB

3. **Import errors**
   - Make sure you've activated the virtual environment
   - Install dependencies with `pip install -r requirements.txt`

4. **Conversion fails**
   - Check the PDF file is not corrupted
   - Ensure your OpenAI API key has sufficient credits
   - Check the application logs for detailed error messages

### Logs

```bash
# View application logs (when running locally)
# Check the terminal where you started the Flask application

# View logs in production (systemd)
sudo journalctl -u pdf-latex-converter -f
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md) for deployment-specific issues
3. Create an issue in the repository

## Acknowledgments

- Built with [OpenAI GPT-4o](https://platform.openai.com/docs/)
- PDF processing powered by [PyMuPDF](https://pymupdf.readthedocs.io/)
- Web framework: [Flask](https://flask.palletsprojects.com/)

---

**Happy converting!** 🚀
