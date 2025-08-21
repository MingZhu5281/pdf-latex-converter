"""
Rate Limiting Module for PDF to LaTeX Converter
Implements user-based rate limiting with Redis backend
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request
import redis
import os
import hashlib

def get_user_id():
    """
    Get unique user identifier for rate limiting
    
    Uses IP address with optional user agent fingerprinting
    for better user identification without requiring authentication
    """
    # Get the real IP address (considering proxies)
    forwarded_ip = request.headers.get('X-Forwarded-For')
    real_ip = request.headers.get('X-Real-IP')
    remote_ip = forwarded_ip or real_ip or get_remote_address()
    
    # Create a more stable user identifier using IP + User Agent hash
    user_agent = request.headers.get('User-Agent', '')
    user_fingerprint = f"{remote_ip}:{hashlib.md5(user_agent.encode()).hexdigest()[:8]}"
    
    return f"user:{user_fingerprint}"

def create_limiter(app):
    """
    Create and configure Flask-Limiter with Redis backend
    
    Args:
        app: Flask application instance
        
    Returns:
        Limiter: Configured Flask-Limiter instance
    """
    
    # Redis configuration
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    try:
        # Try to connect to Redis
        redis_client = redis.from_url(redis_url, decode_responses=True)
        redis_client.ping()
        storage_uri = redis_url
        app.logger.info("✅ Connected to Redis for rate limiting")
    except Exception as e:
        # Fallback to in-memory storage (not recommended for production)
        storage_uri = "memory://"
        app.logger.warning(f"⚠️  Redis connection failed ({e}), using in-memory rate limiting")
        app.logger.warning("💡 For production, please configure Redis properly")
    
    # Create limiter instance
    limiter = Limiter(
        app=app,
        key_func=get_user_id,
        storage_uri=storage_uri,
        # Default limits for all endpoints (very permissive)
        default_limits=["1000 per day", "100 per hour"],
        headers_enabled=True,  # Include rate limit info in response headers
        swallow_errors=True,   # Don't crash on rate limiter errors
    )
    
    return limiter

class RateLimitConfig:
    """
    Rate limiting configuration for different endpoints
    
    User Requirements:
    - Maximum 5 conversions per user per day
    - Maximum 20 pages per conversion
    """
    
    # PDF Conversion endpoint - MOST RESTRICTIVE
    # 5 conversions per day as requested
    CONVERT_LIMITS = [
        "2 per minute",        # Prevent rapid-fire requests
        "5 per day"            # Daily limit as requested
    ]
    
    # Health check and static pages - Very permissive
    HEALTH_LIMITS = [
        "60 per minute",
        "1000 per day"
    ]
    
    # General API endpoints - Moderate
    GENERAL_LIMITS = [
        "30 per minute",
        "500 per day"
    ]
    
    # File upload validation - Allow multiple attempts
    UPLOAD_VALIDATION_LIMITS = [
        "10 per minute",
        "50 per day"
    ]
    
    # Page limits
    MAX_PAGES_PER_CONVERSION = 20
    
    @staticmethod
    def get_error_message(endpoint_type="general"):
        """
        Get user-friendly error messages for different endpoints
        
        Args:
            endpoint_type: Type of endpoint that hit the limit
            
        Returns:
            str: User-friendly error message
        """
        messages = {
            "convert": (
                "You've reached your daily limit of 5 PDF conversions. "
                "Please try again tomorrow. This helps us keep the service "
                "free and available for everyone!"
            ),
            "general": (
                "You're making too many requests. Please wait a moment and try again."
            ),
            "upload": (
                "Too many upload attempts. Please wait a moment before trying again."
            )
        }
        
        return messages.get(endpoint_type, messages["general"])

def validate_pdf_page_count(pdf_file):
    """
    Validate PDF page count without processing the entire file
    
    Args:
        pdf_file: Flask file object containing PDF data
        
    Returns:
        tuple: (is_valid, page_count, error_message)
    """
    try:
        import fitz  # PyMuPDF
        
        # Read PDF data
        pdf_data = pdf_file.read()
        pdf_file.seek(0)  # Reset file pointer
        
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
        
        return True, page_count, None
        
    except Exception as e:
        error_msg = f"Could not validate PDF: {str(e)}"
        return False, 0, error_msg

class RateLimitError(Exception):
    """Custom exception for rate limit related errors"""
    
    def __init__(self, message, retry_after=None, limit_type="general"):
        super().__init__(message)
        self.retry_after = retry_after
        self.limit_type = limit_type
