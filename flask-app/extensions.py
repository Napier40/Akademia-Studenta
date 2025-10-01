"""
Flask Extensions
Initialize all Flask extensions
"""

from flask_migrate import Migrate
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
migrate = Migrate()
babel = Babel()
csrf = CSRFProtect()


def init_extensions(app):
    """
    Initialize all Flask extensions with the app
    """
    from models import db
    
    # Initialize migrations (db already initialized in models.py)
    migrate.init_app(app, db)
    
    # Initialize CSRF protection
    csrf.init_app(app)
    
    # Initialize Babel for i18n
    babel.init_app(app, locale_selector=get_locale)
    
    print("✓ All extensions initialized")


def get_locale():
    """
    Determine the user's preferred locale
    """
    from flask import session, request
    
    # Check if language is set in session
    if 'language' in session:
        return session['language']
    
    # Try to get from request
    from flask import current_app
    return request.accept_languages.best_match(
        current_app.config['BABEL_SUPPORTED_LOCALES']
    )