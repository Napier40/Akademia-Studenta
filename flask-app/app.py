"""
Flask Application - Bilingual Website with Blog and Anonymous Comments
Modular structure with separated concerns, enhanced with logging and security
"""

from typing import Optional
from flask import Flask, session
from flask_babel import get_locale
from config import Config
from models import init_db
from extensions import init_extensions
from routes import register_routes
from logging_config import setup_logging, get_logger
from security import add_security_headers


def create_app(config_class=Config) -> Flask:
    """
    Application factory pattern
    Creates and configures the Flask application with proper error handling
    
    Args:
        config_class: Configuration class to use
    
    Returns:
        Configured Flask application instance
    """
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Set up logging
    log_file = 'logs/app.log' if not app.config.get('TESTING') else None
    logger = setup_logging(
        app_name='flask_app',
        log_level=app.config.get('LOG_LEVEL', 'INFO'),
        log_file=log_file
    )
    logger.info("Initializing Flask application")
    
    # Initialize database
    try:
        init_db(app)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    # Initialize extensions (Babel, CSRF, Migrate)
    try:
        init_extensions(app)
        logger.info("Extensions initialized successfully")
    except Exception as e:
        logger.error(f"Extensions initialization failed: {e}")
        raise
    
    # Register routes
    try:
        register_routes(app)
        logger.info("Public routes registered")
    except Exception as e:
        logger.error(f"Public routes registration failed: {e}")
        raise
    
    # Register admin routes
    try:
        from admin import register_admin_routes
        register_admin_routes(app)
        logger.info("Admin routes registered")
    except Exception as e:
        logger.error(f"Admin routes registration failed: {e}")
        raise
    
    # Register customer blog routes
    try:
        from customer_blog import register_customer_blog_routes
        register_customer_blog_routes(app)
        logger.info("Customer blog routes registered")
    except Exception as e:
        logger.error(f"Customer blog routes registration failed: {e}")
        raise
    
    # Context processor for templates
    @app.context_processor
    def inject_language():
        """Make current language available in all templates"""
        return dict(
            current_language=session.get('language', 'en'),
            get_locale=get_locale
        )
    
    # Template filters
    @app.template_filter('format_date')
    def format_date(date):
        """Format datetime for display"""
        if date is None:
            return ''
        from datetime import datetime
        if isinstance(date, datetime):
            return date.strftime('%B %d, %Y')
        return str(date)
    
    # Add security headers to all responses
    @app.after_request
    def after_request(response):
        """Add security headers to all responses"""
        return add_security_headers(response)
    
    # Register error handlers
    register_error_handlers(app)
    
    logger.info("Application created successfully")
    return app


def register_error_handlers(app: Flask) -> None:
    """
    Register error handlers for common HTTP errors
    
    Args:
        app: Flask application instance
    """
    from flask import render_template, jsonify
    
    logger = get_logger('error_handlers')
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors"""
        logger.warning(f"404 error: {error}")
        if app.config.get('TESTING'):
            return jsonify({'error': 'Not found'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors"""
        logger.error(f"500 error: {error}", exc_info=True)
        from models import db
        db.session.rollback()
        if app.config.get('TESTING'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 Forbidden errors"""
        logger.warning(f"403 error: {error}")
        if app.config.get('TESTING'):
            return jsonify({'error': 'Forbidden'}), 403
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(429)
    def rate_limit_error(error):
        """Handle 429 Rate Limit errors"""
        logger.warning(f"429 error: Rate limit exceeded")
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429


# Create the application instance
app = create_app()


if __name__ == '__main__':
    logger = get_logger('main')
    
    print("\n" + "="*60)
    print("🚀 Starting Flask Application")
    print("="*60)
    print("📍 URL: http://localhost:5001")
    print("🌍 Languages: English (EN) | Polish (PL)")
    print("📝 Blog: http://localhost:5001/blog")
    print("📧 Contact: http://localhost:5001/contact")
    print("👤 Admin: http://localhost:5001/admin")
    print("="*60 + "\n")
    
    logger.info("Starting Flask development server on port 5001")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except Exception as e:
        logger.error(f"Application failed to start: {e}", exc_info=True)
        raise