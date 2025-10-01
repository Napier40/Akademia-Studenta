# Flask Implementation Guide - Bilingual Website with Blog

Complete guide for implementing a bilingual (English/Polish) Flask website with Bootstrap, blog functionality, and anonymous comments.

## Table of Contents

1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Installation & Setup](#installation--setup)
4. [Project Structure](#project-structure)
5. [Database Design](#database-design)
6. [Internationalization (i18n)](#internationalization-i18n)
7. [Templates & Bootstrap](#templates--bootstrap)
8. [Forms & Validation](#forms--validation)
9. [Routes & Views](#routes--views)
10. [Deployment](#deployment)
11. [Customization](#customization)
12. [Best Practices](#best-practices)

---

## Overview

This Flask implementation provides:
- **Bilingual support** (English/Polish) with easy language switching
- **Blog system** with posts in both languages
- **Anonymous comment system** with moderation
- **Contact form** with validation
- **Bootstrap 5** for responsive design
- **Jinja2 templates** for clean HTML
- **SQLAlchemy ORM** for database management
- **Flask-Babel** for internationalization

---

## Technology Stack

### Backend
- **Flask 3.0** - Web framework
- **SQLAlchemy 2.0** - ORM for database
- **Flask-Migrate** - Database migrations
- **Flask-WTF** - Form handling
- **Flask-Babel** - Internationalization

### Frontend
- **Bootstrap 5.3** - CSS framework
- **Bootstrap Icons** - Icon library
- **Jinja2** - Template engine

### Database
- **SQLite** (development)
- **PostgreSQL** (production recommended)

---

## Installation & Setup

### Step 1: Create Project Directory

```bash
mkdir flask-implementation
cd flask-implementation
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

### Step 5: Initialize Database

```bash
# Create database tables
flask init-db

# (Optional) Add sample data
flask seed-db
```

### Step 6: Compile Translations

```bash
# Compile Polish translations
pybabel compile -d translations
```

### Step 7: Run Application

```bash
# Development server
flask run

# Or with Python directly
python app.py
```

Visit: http://localhost:5000

---

## Project Structure

```
flask-implementation/
│
├── app.py                      # Main application file
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── babel.cfg                   # Babel configuration
├── .env                        # Environment variables (not in git)
├── .env.example               # Example environment file
│
├── templates/                  # Jinja2 templates
│   ├── base.html              # Base template
│   ├── index.html             # Homepage
│   ├── services.html          # Services page
│   ├── blog.html              # Blog listing
│   ├── blog_post.html         # Blog post detail
│   ├── contact.html           # Contact form
│   └── errors/                # Error pages
│       ├── 404.html
│       └── 500.html
│
├── translations/               # Translation files
│   ├── messages.pot           # Translation template
│   └── pl/                    # Polish translations
│       └── LC_MESSAGES/
│           ├── messages.po    # Translation source
│           └── messages.mo    # Compiled (auto-generated)
│
├── static/                     # Static files
│   ├── css/                   # Custom CSS
│   ├── js/                    # Custom JavaScript
│   └── images/                # Images
│
├── migrations/                 # Database migrations (auto-generated)
│   └── versions/
│
└── instance/                   # Instance folder (auto-generated)
    └── website.db             # SQLite database
```

---

## Database Design

### BlogPost Model

Stores blog posts in both languages:

```python
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Bilingual fields
    title_en = db.Column(db.String(255), nullable=False)
    title_pl = db.Column(db.String(255), nullable=False)
    content_en = db.Column(db.Text, nullable=False)
    content_pl = db.Column(db.Text, nullable=False)
    excerpt_en = db.Column(db.Text)
    excerpt_pl = db.Column(db.Text)
    category_en = db.Column(db.String(100))
    category_pl = db.Column(db.String(100))
    
    # Common fields
    slug = db.Column(db.String(255), unique=True, nullable=False)
    featured_image = db.Column(db.String(500))
    status = db.Column(db.String(20), default='published')
    views_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Helper methods
    def get_title(self, lang='en'):
        return self.title_en if lang == 'en' else self.title_pl
```

### Comment Model

Supports anonymous posting:

```python
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    
    # Optional user info (null if anonymous)
    author_name = db.Column(db.String(100))
    author_email = db.Column(db.String(255))
    is_anonymous = db.Column(db.Boolean, default=False)
    
    # Comment content
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    
    # Moderation
    status = db.Column(db.String(20), default='pending')
    ip_address = db.Column(db.String(45))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### ContactInquiry Model

Stores contact form submissions:

```python
class ContactInquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(255))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## Internationalization (i18n)

### Flask-Babel Setup

```python
from flask_babel import Babel, gettext, lazy_gettext as _l

babel = Babel(app)

@babel.localeselector
def get_locale():
    # Check session for language preference
    if 'language' in session:
        return session['language']
    # Fall back to browser preference
    return request.accept_languages.best_match(['en', 'pl'])
```

### Translation Workflow

#### 1. Mark Strings for Translation

In Python code:
```python
from flask_babel import gettext, lazy_gettext as _l

# For immediate translation
flash(gettext('Message sent successfully!'), 'success')

# For lazy translation (forms, etc.)
name = StringField(_l('Name'), validators=[DataRequired()])
```

In templates:
```html
<h1>{{ _('Welcome to Our Services') }}</h1>
<p>{{ _('We provide professional services') }}</p>
```

#### 2. Extract Translatable Strings

```bash
pybabel extract -F babel.cfg -o translations/messages.pot .
```

#### 3. Update Translation Files

```bash
# Update existing translations
pybabel update -i translations/messages.pot -d translations

# Or initialize new language
pybabel init -i translations/messages.pot -d translations -l pl
```

#### 4. Edit Translation Files

Edit `translations/pl/LC_MESSAGES/messages.po`:

```po
msgid "Welcome to Our Services"
msgstr "Witamy w naszych usługach"
```

#### 5. Compile Translations

```bash
pybabel compile -d translations
```

### Language Switching

```python
@app.route('/language/<lang>')
def set_language(lang):
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))
```

In template:
```html
<a href="{{ url_for('set_language', lang='en') }}">EN</a>
<a href="{{ url_for('set_language', lang='pl') }}">PL</a>
```

---

## Templates & Bootstrap

### Base Template Structure

```html
<!DOCTYPE html>
<html lang="{{ get_locale() }}">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg">
        <!-- Nav content -->
    </nav>
    
    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <!-- Main Content -->
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer>
        <!-- Footer content -->
    </footer>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Bootstrap Components Used

- **Navbar** - Responsive navigation
- **Cards** - Service and blog post display
- **Forms** - Contact and comment forms
- **Alerts** - Flash messages
- **Pagination** - Blog post pagination
- **Grid System** - Responsive layouts
- **Buttons** - Call-to-action elements

---

## Forms & Validation

### Form Definition

```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class CommentForm(FlaskForm):
    author_name = StringField(_l('Name'), 
                             validators=[Optional(), Length(max=100)])
    author_email = StringField(_l('Email'), 
                              validators=[Optional(), Email()])
    is_anonymous = BooleanField(_l('Post anonymously'))
    content = TextAreaField(_l('Your Feedback'), 
                           validators=[DataRequired(), Length(max=5000)])
    rating = SelectField(_l('Rating'), 
                        choices=[(0, 'No rating'), (1, '1'), ...],
                        coerce=int)
```

### Form Rendering

```html
<form method="POST">
    {{ form.hidden_tag() }}  <!-- CSRF token -->
    
    <div class="mb-3">
        {{ form.author_name.label(class="form-label") }}
        {{ form.author_name(class="form-control") }}
        {% if form.author_name.errors %}
            <div class="text-danger">{{ form.author_name.errors[0] }}</div>
        {% endif %}
    </div>
    
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Form Processing

```python
@app.route('/blog/<slug>/comment', methods=['POST'])
def submit_comment(slug):
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            post_id=post.id,
            author_name=None if form.is_anonymous.data else form.author_name.data,
            content=form.content.data,
            status='pending'
        )
        db.session.add(comment)
        db.session.commit()
        
        flash(gettext('Comment submitted!'), 'success')
        return redirect(url_for('blog_post', slug=slug))
    
    flash(gettext('Please correct errors'), 'error')
    return redirect(url_for('blog_post', slug=slug))
```

---

## Routes & Views

### Homepage Route

```python
@app.route('/')
def index():
    latest_posts = BlogPost.query.filter_by(status='published')\
                                 .order_by(BlogPost.published_at.desc())\
                                 .limit(3).all()
    return render_template('index.html', latest_posts=latest_posts)
```

### Blog Listing with Pagination

```python
@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(status='published')\
                          .order_by(BlogPost.published_at.desc())\
                          .paginate(page=page, per_page=9)
    return render_template('blog.html', posts=posts)
```

### Blog Post Detail

```python
@app.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug, status='published')\
                         .first_or_404()
    
    # Increment view count
    post.views_count += 1
    db.session.commit()
    
    comments = Comment.query.filter_by(post_id=post.id, status='approved')\
                            .order_by(Comment.created_at.desc()).all()
    
    form = CommentForm()
    return render_template('blog_post.html', post=post, 
                          comments=comments, form=form)
```

---

## Deployment

### Production Checklist

- [ ] Set strong SECRET_KEY
- [ ] Use PostgreSQL database
- [ ] Set DEBUG=False
- [ ] Configure proper logging
- [ ] Set up HTTPS
- [ ] Configure CORS if needed
- [ ] Set up database backups
- [ ] Configure error monitoring
- [ ] Set up rate limiting
- [ ] Compile translations

### Heroku Deployment

```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Install Gunicorn
pip install gunicorn
pip freeze > requirements.txt

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create Heroku app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Initialize database
heroku run flask init-db
```

### VPS Deployment with Nginx

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone repository
git clone your-repo
cd flask-implementation

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Configure environment
cp .env.example .env
nano .env

# Initialize database
flask init-db

# Create systemd service
sudo nano /etc/systemd/system/flask-app.service
```

Systemd service file:
```ini
[Unit]
Description=Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/flask-implementation
Environment="PATH=/path/to/flask-implementation/venv/bin"
ExecStart=/path/to/flask-implementation/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/flask-implementation/static;
    }
}
```

Start services:
```bash
sudo systemctl start flask-app
sudo systemctl enable flask-app
sudo systemctl restart nginx
```

---

## Customization

### Adding New Pages

1. Create template in `templates/`
2. Add route in `app.py`
3. Add navigation link in `base.html`
4. Add translations

### Changing Design

Edit CSS in `templates/base.html` or create `static/css/custom.css`

### Adding New Languages

```bash
# Initialize new language
pybabel init -i translations/messages.pot -d translations -l de

# Edit translations
nano translations/de/LC_MESSAGES/messages.po

# Compile
pybabel compile -d translations

# Update config
# Add 'de' to BABEL_SUPPORTED_LOCALES in app.py
```

---

## Best Practices

### Security
- Always use CSRF protection
- Validate all user input
- Use parameterized queries (SQLAlchemy does this)
- Set strong SECRET_KEY
- Use HTTPS in production
- Implement rate limiting

### Performance
- Use database indexes
- Implement caching
- Optimize images
- Minify CSS/JS in production
- Use CDN for static assets

### Code Quality
- Follow PEP 8 style guide
- Write docstrings
- Use type hints
- Keep functions small
- Separate concerns

### Database
- Use migrations for schema changes
- Regular backups
- Monitor query performance
- Use connection pooling

---

## Conclusion

This Flask implementation provides a solid foundation for a bilingual website with blog and comment functionality. The modular structure makes it easy to extend and customize according to your needs.

For questions or issues, refer to:
- Flask documentation: https://flask.palletsprojects.com/
- Flask-Babel: https://python-babel.github.io/flask-babel/
- Bootstrap: https://getbootstrap.com/
- SQLAlchemy: https://www.sqlalchemy.org/

**Your bilingual Flask website is ready to launch!** 🚀