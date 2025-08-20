import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # File upload configuration
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB default
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # Application settings
    DEBUG = os.getenv('FLASK_ENV', 'production') == 'development'
    
    @staticmethod
    def validate_config():
        """Validate that required configuration is present"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required but not found in environment variables")
        
        return True
