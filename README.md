# Akademia Studenta

## Bilingual Flask Website with Blog and Anonymous Comments

This repository contains a complete Flask web application with bilingual support (English and Polish), blog functionality, and anonymous comment system.

### Features

✅ **Bilingual Support** - Full English and Polish translations
✅ **Language Switcher** - Easy switching between languages
✅ **Blog System** - Create and manage blog posts in both languages
✅ **Anonymous Comments** - Users can comment with or without providing their name
✅ **Contact Form** - With validation and CSRF protection
✅ **Bootstrap 5** - Modern, responsive design
✅ **Jinja2 Templates** - Clean, maintainable template structure

### Project Structure

```
flask-app/
├── app.py                          # Main Flask application
├── config.py                       # Configuration
├── requirements.txt                # Dependencies
├── babel.cfg                       # Babel config
├── .env.example                    # Environment template
├── README.md                       # Usage guide
├── FLASK_IMPLEMENTATION_GUIDE.md   # Implementation guide
│
├── templates/                      # Jinja2 templates
│   ├── base.html                  # Base with navigation
│   ├── index.html                 # Homepage
│   ├── services.html              # Services page
│   ├── blog.html                  # Blog listing
│   ├── blog_post.html             # Blog post detail
│   └── contact.html               # Contact form
│
└── translations/                   # i18n files
    ├── messages.pot               # Translation template
    └── pl/LC_MESSAGES/
        └── messages.po            # Polish translations
```

### Quick Start

1. Clone the repository
```bash
git clone https://github.com/Napier40/Akademia-Studenta.git
cd Akademia-Studenta/flask-app
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Initialize the database
```bash
flask init-db
flask seed-db  # Optional: add sample data
```

6. Compile translations
```bash
pybabel compile -d translations
```

7. Run the application
```bash
flask run
```

Visit http://localhost:5000 in your browser.

### Language Support

The application supports both English and Polish languages. Users can switch between languages using the language selector in the navigation bar.

### Documentation

For detailed implementation guide, see [FLASK_IMPLEMENTATION_GUIDE.md](flask-app/FLASK_IMPLEMENTATION_GUIDE.md).