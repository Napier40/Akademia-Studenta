# Flask Application Restructure Guide

## Overview
The application has been completely restructured to follow Flask best practices with proper separation of concerns. All database-related code is now in `models.py`, making the codebase more maintainable and scalable.

## New Project Structure

```
flask-app/
├── app.py                  # Main application entry point (Application Factory)
├── models.py               # Database models and initialization
├── routes.py               # All view functions and URL routing
├── forms.py                # WTForms definitions
├── extensions.py           # Flask extensions initialization
├── config.py               # Configuration settings
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
├── babel.cfg               # Babel configuration
├── .env.example            # Environment variables template
│
├── templates/              # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── services.html
│   ├── blog.html
│   ├── blog_post.html
│   └── contact.html
│
└── translations/           # i18n translations
    ├── messages.pot
    └── pl/LC_MESSAGES/
        └── messages.po
```

## File Responsibilities

### 1. `app.py` - Application Entry Point
**Purpose:** Main application file using the Application Factory pattern

**Key Features:**
- Creates Flask application instance
- Loads configuration
- Initializes database
- Initializes extensions
- Registers routes
- Provides context processors
- Entry point for running the app

**Code Structure:**
```python
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    init_db(app)              # Initialize database
    init_extensions(app)       # Initialize extensions
    register_routes(app)       # Register routes
    
    return app

app = create_app()
```

### 2. `models.py` - Database Models
**Purpose:** All SQLAlchemy models and database initialization

**Contains:**
- `db` - SQLAlchemy instance
- `init_db(app)` - Database initialization function
- `BlogPost` - Blog post model with bilingual support
- `Comment` - Comment model with anonymous support
- `ContactInquiry` - Contact form inquiry model
- `seed_sample_data()` - Function to add sample blog posts

**Key Features:**
- Automatic table creation on app startup
- Bilingual field support (English/Polish)
- Helper methods for language-specific content
- Relationships between models
- Status tracking and moderation
- Timestamps and view counters

**Example Model:**
```python
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_pl = db.Column(db.String(200), nullable=False)
    # ... more fields
    
    def get_title(self, language='en'):
        return self.title_pl if language == 'pl' else self.title_en
```

### 3. `routes.py` - Application Routes
**Purpose:** All view functions and URL routing

**Contains:**
- `register_routes(app)` - Function to register all routes
- Homepage route (`/`)
- Services route (`/services`)
- Blog listing route (`/blog`)
- Blog post detail route (`/blog/<slug>`)
- Contact form route (`/contact`)
- Language switcher route (`/set-language/<language>`)

**Key Features:**
- Pagination for blog posts
- Search and filter functionality
- Form handling and validation
- Comment submission
- Contact inquiry submission
- Language switching

### 4. `forms.py` - WTForms
**Purpose:** Form definitions and validators

**Contains:**
- `CommentForm` - Blog comment form
- `ContactForm` - Contact inquiry form
- `BlogSearchForm` - Blog search form

**Key Features:**
- Field validation
- Custom error messages
- Optional fields for anonymous commenting
- Email validation
- Length constraints

### 5. `extensions.py` - Flask Extensions
**Purpose:** Initialize all Flask extensions

**Contains:**
- `migrate` - Flask-Migrate instance
- `babel` - Flask-Babel instance
- `csrf` - Flask-WTF CSRF protection
- `init_extensions(app)` - Initialize all extensions
- `get_locale()` - Babel locale selector

**Key Features:**
- Centralized extension management
- Locale detection from session
- CSRF protection for all forms

### 6. `config.py` - Configuration
**Purpose:** Application configuration settings

**Contains:**
- `Config` class with all settings
- Environment variable loading
- Database URI configuration
- Secret key management
- Babel configuration

### 7. `init_db.py` - Database Initialization
**Purpose:** Interactive database setup script

**Features:**
- Creates all database tables
- Optional table dropping for fresh start
- Optional sample data seeding
- Interactive prompts
- Error handling

## How Database Initialization Works

### Automatic Initialization (Recommended)
The database tables are now created automatically when you start the application:

```python
# In models.py
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Creates tables automatically
```

This means:
- ✅ No manual database setup required
- ✅ Tables created on first run
- ✅ Existing data preserved on subsequent runs
- ✅ Safe to restart the application

### Manual Initialization (Optional)
If you want to reset the database or add sample data:

```bash
python init_db.py
```

This script allows you to:
1. Drop existing tables (optional)
2. Create fresh tables
3. Add sample blog posts (optional)

## Benefits of New Structure

### 1. Separation of Concerns
- **Models** - Database logic only
- **Routes** - View logic only
- **Forms** - Form validation only
- **Extensions** - Extension configuration only

### 2. Maintainability
- Easy to find and modify specific functionality
- Clear file responsibilities
- Reduced code duplication

### 3. Scalability
- Easy to add new models in `models.py`
- Easy to add new routes in `routes.py`
- Easy to add new forms in `forms.py`

### 4. Testability
- Each module can be tested independently
- Application factory pattern enables test configurations
- Mock dependencies easily

### 5. Reusability
- Models can be imported anywhere
- Forms can be reused across routes
- Extensions configured once, used everywhere

## Migration from Old Structure

### What Changed?

**Old Structure (Single File):**
```python
# Everything in app.py
app = Flask(__name__)
db = SQLAlchemy(app)
babel = Babel(app)

class BlogPost(db.Model):
    # model definition

@app.route('/')
def index():
    # route logic
```

**New Structure (Modular):**
```python
# models.py
db = SQLAlchemy()
class BlogPost(db.Model):
    # model definition

# routes.py
def register_routes(app):
    @app.route('/')
    def index():
        # route logic

# app.py
app = create_app()
```

### Key Differences

1. **Database Initialization**
   - Old: `db = SQLAlchemy(app)` in app.py
   - New: `db = SQLAlchemy()` in models.py, then `init_db(app)`

2. **Route Registration**
   - Old: Routes defined directly with `@app.route()`
   - New: Routes registered via `register_routes(app)`

3. **Extensions**
   - Old: Extensions initialized directly in app.py
   - New: Extensions initialized in extensions.py

4. **Application Creation**
   - Old: Direct instantiation
   - New: Application factory pattern

## Running the Application

### First Time Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```
   
   The database tables will be created automatically!

3. **Optional - Add sample data:**
   ```bash
   python init_db.py
   ```

### Subsequent Runs

Simply run:
```bash
python app.py
```

Or on Windows:
```bash
run.bat
```

## Adding New Features

### Adding a New Model

1. Open `models.py`
2. Add your model class:
   ```python
   class NewModel(db.Model):
       __tablename__ = 'new_table'
       id = db.Column(db.Integer, primary_key=True)
       # ... more fields
   ```
3. Restart the app - table created automatically!

### Adding a New Route

1. Open `routes.py`
2. Add your route inside `register_routes(app)`:
   ```python
   @app.route('/new-page')
   def new_page():
       return render_template('new_page.html')
   ```

### Adding a New Form

1. Open `forms.py`
2. Add your form class:
   ```python
   class NewForm(FlaskForm):
       field = StringField('Label', validators=[DataRequired()])
   ```

## Troubleshooting

### Import Errors
If you get import errors, ensure all files are in the same directory:
```
flask-app/
├── app.py
├── models.py
├── routes.py
├── forms.py
└── extensions.py
```

### Database Errors
If you get database errors:
1. Delete `website.db`
2. Run `python app.py` - tables will be recreated

### Circular Import Errors
The new structure avoids circular imports by:
- Using application factory pattern
- Importing within functions when needed
- Proper initialization order

## Best Practices

1. **Always use the application factory**
   ```python
   app = create_app()
   ```

2. **Import models from models.py**
   ```python
   from models import db, BlogPost, Comment
   ```

3. **Import forms from forms.py**
   ```python
   from forms import CommentForm, ContactForm
   ```

4. **Use db.session for database operations**
   ```python
   db.session.add(object)
   db.session.commit()
   ```

5. **Handle errors properly**
   ```python
   try:
       db.session.commit()
   except Exception as e:
       db.session.rollback()
       flash('Error occurred', 'error')
   ```

## Summary

The restructured application provides:
- ✅ Clear separation of concerns
- ✅ Better maintainability
- ✅ Easier testing
- ✅ Scalable architecture
- ✅ Automatic database initialization
- ✅ Professional Flask structure

All database logic is now centralized in `models.py`, making it easy to manage and extend your data models.