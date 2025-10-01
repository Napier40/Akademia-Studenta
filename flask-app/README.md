# Flask Website - Bilingual (English/Polish) with Blog and Anonymous Comments

A complete Flask web application with Bootstrap 5, featuring bilingual support (English and Polish), blog functionality, and anonymous comment system.

## Features

✅ **Bilingual Support** - Full English and Polish translations
✅ **Language Switcher** - Easy switching between languages
✅ **Blog System** - Create and manage blog posts in both languages
✅ **Anonymous Comments** - Users can comment with or without providing their name
✅ **Contact Form** - With validation and CSRF protection
✅ **Bootstrap 5** - Modern, responsive design
✅ **Jinja2 Templates** - Clean, maintainable template structure
✅ **SQLAlchemy ORM** - Database management with migrations
✅ **Flask-Babel** - Professional internationalization
✅ **Form Validation** - Using Flask-WTF and WTForms
✅ **Security** - CSRF protection, input validation, XSS prevention

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### 2. Installation

```bash
# Clone or download the project
cd flask-implementation

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
# Initialize the database
flask init-db

# (Optional) Seed with sample data
flask seed-db
```

### 4. Compile Translations

```bash
# Compile Polish translations
pybabel compile -d translations
```

### 5. Run the Application

```bash
# Development mode
flask run

# Or with debug mode
python app.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure

```
flask-implementation/
├── app.py                          # Main application file
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── templates/                      # Jinja2 templates
│   ├── base.html                  # Base template with navigation
│   ├── index.html                 # Homepage
│   ├── services.html              # Services page
│   ├── blog.html                  # Blog listing
│   ├── blog_post.html             # Individual blog post
│   ├── contact.html               # Contact form
│   └── errors/                    # Error pages
│       ├── 404.html
│       └── 500.html
├── translations/                   # Translation files
│   ├── messages.pot               # Translation template
│   └── pl/                        # Polish translations
│       └── LC_MESSAGES/
│           ├── messages.po        # Polish translation source
│           └── messages.mo        # Compiled translations
├── static/                        # Static files (if needed)
│   ├── css/
│   ├── js/
│   └── images/
└── migrations/                    # Database migrations (auto-generated)
```

## Database Models

### BlogPost
- Bilingual fields (title, content, excerpt, category)
- Slug for URL-friendly links
- Featured image support
- View counter
- Status (draft/published)
- Timestamps

### Comment
- Anonymous posting support
- Optional rating (1-5 stars)
- Moderation status (pending/approved/rejected)
- IP tracking for spam prevention
- Relationship with BlogPost

### ContactInquiry
- Name, email, phone, subject, message
- Status tracking (new/in_progress/resolved)
- Timestamp

## Language Support

### Switching Languages

Users can switch between English and Polish using the language selector in the navigation bar. The selected language is stored in the session.

### Adding New Translations

1. **Extract translatable strings:**
```bash
pybabel extract -F babel.cfg -o translations/messages.pot .
```

2. **Update existing translations:**
```bash
pybabel update -i translations/messages.pot -d translations
```

3. **Edit translation files:**
Edit `translations/pl/LC_MESSAGES/messages.po`

4. **Compile translations:**
```bash
pybabel compile -d translations
```

### Adding a New Language

1. **Initialize new language (e.g., German):**
```bash
pybabel init -i translations/messages.pot -d translations -l de
```

2. **Edit the translation file:**
Edit `translations/de/LC_MESSAGES/messages.po`

3. **Compile:**
```bash
pybabel compile -d translations
```

4. **Update config:**
Add 'de' to `BABEL_SUPPORTED_LOCALES` in `app.py`

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///website.db
# For PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost/dbname

# Language
BABEL_DEFAULT_LOCALE=en
```

### Configuration Options

Edit `config.py` to customize:
- Database settings
- Session lifetime
- Upload limits
- Pagination settings
- Security options

## Usage Guide

### Creating Blog Posts

Blog posts must be created in both languages. Use the database directly or create an admin interface:

```python
from app import app, db, BlogPost
from datetime import datetime

with app.app_context():
    post = BlogPost(
        title_en='Your English Title',
        title_pl='Twój Polski Tytuł',
        slug='your-english-title',
        content_en='English content...',
        content_pl='Polska treść...',
        excerpt_en='English excerpt',
        excerpt_pl='Polski fragment',
        category_en='Business Tips',
        category_pl='Porady biznesowe',
        featured_image='https://example.com/image.jpg',
        status='published',
        published_at=datetime.utcnow()
    )
    db.session.add(post)
    db.session.commit()
```

### Moderating Comments

Comments are set to 'pending' by default. To approve:

```python
from app import app, db, Comment

with app.app_context():
    comment = Comment.query.get(comment_id)
    comment.status = 'approved'
    db.session.commit()
```

### Managing Contact Inquiries

```python
from app import app, db, ContactInquiry

with app.app_context():
    inquiries = ContactInquiry.query.filter_by(status='new').all()
    for inquiry in inquiries:
        print(f"{inquiry.name}: {inquiry.message}")
```

## Customization

### Changing Colors

Edit the CSS variables in `templates/base.html`:

```css
:root {
    --primary-color: #0d6efd;  /* Your brand color */
    --secondary-color: #6c757d;
}
```

### Adding New Pages

1. Create a new template in `templates/`
2. Add a route in `app.py`
3. Add navigation link in `templates/base.html`
4. Add translations to `.po` files

### Customizing Forms

Edit form classes in `app.py`:

```python
class YourForm(FlaskForm):
    field_name = StringField(_l('Label'), validators=[DataRequired()])
```

## Deployment

### Option 1: Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
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

### Option 2: DigitalOcean/VPS

```bash
# SSH into server
ssh user@your-server

# Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# Clone repository
git clone your-repo
cd flask-implementation

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up environment variables
nano .env

# Initialize database
flask init-db

# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/flask-implementation/static;
    }
}
```

### Option 3: Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN pybabel compile -d translations

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t flask-website .
docker run -p 5000:5000 flask-website
```

## Security Considerations

### Production Checklist

- [ ] Set strong SECRET_KEY
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set DEBUG=False
- [ ] Configure proper CORS
- [ ] Set up rate limiting
- [ ] Regular backups
- [ ] Monitor error logs
- [ ] Keep dependencies updated

### CSRF Protection

CSRF protection is enabled by default. All forms include `{{ form.hidden_tag() }}`.

### Input Validation

All forms use WTForms validators. Additional validation in routes.

### XSS Prevention

Jinja2 auto-escapes variables. Use `|safe` filter only for trusted content.

## Testing

### Manual Testing

```bash
# Test homepage
curl http://localhost:5000/

# Test language switching
curl http://localhost:5000/language/pl

# Test blog
curl http://localhost:5000/blog
```

### Unit Tests (Future)

Create `tests/` directory with test files:

```python
import unittest
from app import app, db

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
```

## Troubleshooting

### Common Issues

**1. Translations not working**
```bash
# Recompile translations
pybabel compile -d translations
# Restart Flask
```

**2. Database errors**
```bash
# Reset database
rm website.db
flask init-db
```

**3. Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**4. Language not switching**
- Check session configuration
- Clear browser cookies
- Verify BABEL_SUPPORTED_LOCALES

## Maintenance

### Regular Tasks

**Daily:**
- Monitor error logs
- Check pending comments
- Review contact inquiries

**Weekly:**
- Database backup
- Update dependencies
- Review analytics

**Monthly:**
- Security updates
- Performance optimization
- Content audit

### Database Backup

```bash
# SQLite
cp website.db website_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump dbname > backup_$(date +%Y%m%d).sql
```

## Support

For issues or questions:
1. Check this README
2. Review Flask documentation: https://flask.palletsprojects.com/
3. Check Flask-Babel docs: https://python-babel.github.io/flask-babel/
4. Review Bootstrap docs: https://getbootstrap.com/

## License

MIT License - Feel free to use and modify for your needs.

## Credits

- Flask: https://flask.palletsprojects.com/
- Bootstrap: https://getbootstrap.com/
- Bootstrap Icons: https://icons.getbootstrap.com/
- Flask-Babel: https://python-babel.github.io/flask-babel/
- Images: Unsplash (https://unsplash.com/)

---

**Ready to launch your bilingual website!** 🚀

For the complete implementation guide, see the main WEBSITE_REDESIGN_GUIDE.md file.