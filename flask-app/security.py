"""
Security Configuration
Rate limiting, authentication, and security headers
"""

from functools import wraps
from typing import Optional, Callable, Any
from flask import request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import time
from collections import defaultdict
from datetime import datetime, timedelta


class RateLimiter:
    """
    Simple in-memory rate limiter
    For production, use Redis-based rate limiting
    """
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.cleanup_interval = 3600  # Clean up old entries every hour
        self.last_cleanup = time.time()
    
    def is_allowed(
        self,
        key: str,
        max_requests: int = 100,
        window_seconds: int = 3600
    ) -> bool:
        """
        Check if request is allowed based on rate limit
        
        Args:
            key: Unique identifier (IP address, user ID, etc.)
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds
        
        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        
        # Cleanup old entries periodically
        if now - self.last_cleanup > self.cleanup_interval:
            self._cleanup()
            self.last_cleanup = now
        
        # Get request timestamps for this key
        timestamps = self.requests[key]
        
        # Remove timestamps outside the window
        cutoff = now - window_seconds
        timestamps[:] = [ts for ts in timestamps if ts > cutoff]
        
        # Check if limit exceeded
        if len(timestamps) >= max_requests:
            return False
        
        # Add current timestamp
        timestamps.append(now)
        return True
    
    def _cleanup(self):
        """Remove old entries to prevent memory bloat"""
        now = time.time()
        cutoff = now - 3600  # Keep last hour
        
        keys_to_delete = []
        for key, timestamps in self.requests.items():
            timestamps[:] = [ts for ts in timestamps if ts > cutoff]
            if not timestamps:
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            del self.requests[key]


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(
    max_requests: int = 100,
    window_seconds: int = 3600,
    key_func: Optional[Callable] = None
):
    """
    Rate limiting decorator
    
    Args:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds
        key_func: Function to generate rate limit key (default: IP address)
    
    Example:
        @rate_limit(max_requests=10, window_seconds=60)
        def my_route():
            return "Hello"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get rate limit key
            if key_func:
                key = key_func()
            else:
                key = request.remote_addr or 'unknown'
            
            # Check rate limit
            if not rate_limiter.is_allowed(key, max_requests, window_seconds):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Maximum {max_requests} requests per {window_seconds} seconds'
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class AdminAuth:
    """
    Admin authentication manager
    """
    
    # In production, store this in database
    ADMIN_CREDENTIALS = {
        'admin': generate_password_hash('admin123')
    }
    
    @staticmethod
    def verify_password(username: str, password: str) -> bool:
        """
        Verify admin credentials
        
        Args:
            username: Admin username
            password: Admin password
        
        Returns:
            True if credentials are valid
        """
        if username not in AdminAuth.ADMIN_CREDENTIALS:
            return False
        
        stored_hash = AdminAuth.ADMIN_CREDENTIALS[username]
        return check_password_hash(stored_hash, password)
    
    @staticmethod
    def login(username: str, password: str) -> bool:
        """
        Attempt admin login
        
        Args:
            username: Admin username
            password: Admin password
        
        Returns:
            True if login successful
        """
        if AdminAuth.verify_password(username, password):
            session['is_admin'] = True
            session['admin_username'] = username
            session['login_time'] = datetime.utcnow().isoformat()
            return True
        return False
    
    @staticmethod
    def logout():
        """Logout admin user"""
        session.pop('is_admin', None)
        session.pop('admin_username', None)
        session.pop('login_time', None)
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated as admin"""
        return session.get('is_admin', False)
    
    @staticmethod
    def get_username() -> Optional[str]:
        """Get current admin username"""
        return session.get('admin_username')


def admin_required(f: Callable) -> Callable:
    """
    Decorator to require admin authentication
    
    Example:
        @admin_required
        def admin_dashboard():
            return "Admin Dashboard"
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if not AdminAuth.is_authenticated():
            from flask import flash, redirect, url_for
            flash('Please login as admin to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


def add_security_headers(response):
    """
    Add security headers to response
    
    Headers added:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: SAMEORIGIN
    - X-XSS-Protection: 1; mode=block
    - Strict-Transport-Security: max-age=31536000; includeSubDomains
    - Content-Security-Policy: default-src 'self'
    """
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Only add HSTS in production with HTTPS
    if not current_app.debug:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Basic CSP - adjust based on your needs
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;"
    )
    
    return response


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize user input
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
    
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Truncate to max length
    text = text[:max_length]
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def validate_file_upload(filename: str, allowed_extensions: set) -> bool:
    """
    Validate uploaded file
    
    Args:
        filename: Name of uploaded file
        allowed_extensions: Set of allowed file extensions
    
    Returns:
        True if file is valid
    """
    if not filename:
        return False
    
    # Check if file has extension
    if '.' not in filename:
        return False
    
    # Get extension
    ext = filename.rsplit('.', 1)[1].lower()
    
    # Check if extension is allowed
    return ext in allowed_extensions