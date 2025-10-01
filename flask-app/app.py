"""
Flask Application - Bilingual Website with Blog and Anonymous Comments
Modular structure with separated concerns
"""

from flask import Flask
from config import Config
from models import init_db
from extensions import init_extensions
from routes import register_routes


def create_app(config_class=Config):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize database
    init_db(app)
    
    # Initialize extensions (Babel, CSRF, Migrate)
    init_extensions(app)
    
    # Register routes
    register_routes(app)
    
    # Register admin routes
    from admin import register_admin_routes
    register_admin_routes(app)
    
    # Context processor for templates
    @app.context_processor
    def inject_language():
        """Make current language available in all templates"""
        from flask import session
        from flask_babel import get_locale
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
    
    return app


# Create the application instance
app = create_app()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Flask Application")
    print("="*60)
    print("📍 URL: http://localhost:5000")
    print("🌍 Languages: English (EN) | Polish (PL)")
    print("📝 Blog: http://localhost:5000/blog")
    print("📧 Contact: http://localhost:5000/contact")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)