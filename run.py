#!/usr/bin/env python3
"""
PDF to LaTeX Converter - Application Entry Point
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import and create the Flask application
from app.main import create_app

app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"Starting PDF to LaTeX Converter on {host}:{port}")
    print(f"Debug mode: {'ON' if debug else 'OFF'}")
    print(f"Access the application at: http://{host}:{port}")
    
    app.run(debug=debug, host=host, port=port)
