# Setup Summary - Akademia Studenta

## What You Need to Do Right Now

Follow these steps in order to get your Flask application running:

### Step 1: Pull Latest Changes (IMPORTANT!)

```powershell
cd C:\Users\jackj\OneDrive\Desktop\Web_Designs\Akademia-Studenta\Akademia-Studenta
git pull origin main
```

This gets all the fixes for:
- ✅ Python 3.13 compatibility (SQLAlchemy 2.0.35)
- ✅ Flask-Babel API compatibility
- ✅ Database initialization script
- ✅ Automated setup scripts

### Step 2: Choose Your Setup Method

#### Option A: Automated Setup (EASIEST - Recommended)

```powershell
cd flask-app
setup.bat
```

Wait for it to complete, then:

```powershell
run.bat
```

**Done!** Visit http://localhost:5000

---

#### Option B: Manual Setup (More Control)

```powershell
# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Update dependencies
cd flask-app
pip install --upgrade -r requirements.txt

# 3. Initialize database
python init_db.py
# Type 'y' when asked to add sample posts

# 4. Compile translations
pybabel compile -d translations

# 5. Run application
flask run
```

**Done!** Visit http://localhost:5000

---

#### Option C: Fresh Start (If you have issues)

```powershell
# 1. Remove old virtual environment
deactivate
rmdir /s .venv

# 2. Run automated setup
cd flask-app
setup.bat

# 3. Run application
run.bat
```

**Done!** Visit http://localhost:5000

---

## What You Should See

After successful setup:

1. **Console output:**
   ```
   * Running on http://127.0.0.1:5000
   * Debug mode: on
   ```

2. **In browser (http://localhost:5000):**
   - Homepage with hero section
   - 3 sample blog posts
   - Language switcher (EN/PL) in navigation
   - Services, Blog, Contact links

3. **You can:**
   - Switch between English and Polish
   - View blog posts
   - Read individual posts
   - Leave comments (anonymous or with name)
   - Submit contact form

## Files You Got from GitHub

```
Akademia-Studenta/
├── README.md                      # Main repository info
├── QUICK_FIX.md                   # Quick solutions for common issues
├── TROUBLESHOOTING.md             # Comprehensive troubleshooting
├── SETUP_SUMMARY.md               # This file
│
└── flask-app/                     # Main application
    ├── app.py                     # Flask application
    ├── init_db.py                 # Database initialization (NEW!)
    ├── config.py                  # Configuration
    ├── requirements.txt           # Updated dependencies
    ├── setup.bat                  # Automated setup script
    ├── run.bat                    # Easy run script
    ├── .env.example               # Environment template
    ├── README.md                  # Usage guide
    ├── WINDOWS_SETUP.md           # Windows setup guide
    ├── FLASK_IMPLEMENTATION_GUIDE.md  # Technical guide
    │
    ├── templates/                 # HTML templates
    │   ├── base.html
    │   ├── index.html
    │   ├── blog.html
    │   ├── blog_post.html
    │   ├── services.html
    │   └── contact.html
    │
    └── translations/              # Bilingual support
        ├── messages.pot
        └── pl/LC_MESSAGES/
            └── messages.po
```

## What Was Fixed

| Issue | Status | Fix |
|-------|--------|-----|
| SQLAlchemy Python 3.13 error | ✅ Fixed | Updated to 2.0.35 |
| Flask-Babel API error | ✅ Fixed | Updated initialization |
| Database not initialized | ✅ Fixed | Created init_db.py |
| Missing setup automation | ✅ Fixed | Created setup.bat |
| Missing documentation | ✅ Fixed | Added multiple guides |

## Quick Command Reference

```powershell
# Pull latest changes
git pull origin main

# Activate virtual environment
.venv\Scripts\activate

# Initialize database
python init_db.py

# Run application
flask run
# or
run.bat

# Stop server
Ctrl+C
```

## Configuration

After setup, edit `.env` file:

```powershell
notepad flask-app\.env
```

Generate a secure SECRET_KEY:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

## Testing the Application

### Test Language Switching
1. Visit http://localhost:5000
2. Click "PL" in navigation
3. Page should reload in Polish
4. Click "EN" to switch back

### Test Blog
1. Click "Blog" in navigation
2. Should see 3 sample posts
3. Click on a post to read it
4. Try leaving a comment (anonymous or with name)

### Test Forms
1. Go to Contact page
2. Fill out the form
3. Submit (data saved to database)

## Sample Blog Posts Included

After running `init_db.py` with 'y', you get:

1. **Getting Started with Our Services** (EN) / **Rozpoczęcie pracy z naszymi usługami** (PL)
2. **5 Tips for Business Growth** (EN) / **5 wskazówek dotyczących rozwoju firmy** (PL)
3. **Industry Trends 2025** (EN) / **Trendy branżowe 2025** (PL)

## Next Steps

After getting it running:

1. **Customize content:**
   - Edit blog posts in database
   - Update services page
   - Change branding and colors

2. **Add your own content:**
   - Create new blog posts
   - Update contact information
   - Add your own images

3. **Deploy to production:**
   - See FLASK_IMPLEMENTATION_GUIDE.md
   - Options: Heroku, DigitalOcean, AWS

## Need Help?

### Quick Issues
- See `QUICK_FIX.md`

### Detailed Troubleshooting
- See `TROUBLESHOOTING.md`

### Windows-Specific Help
- See `flask-app/WINDOWS_SETUP.md`

### Technical Details
- See `flask-app/FLASK_IMPLEMENTATION_GUIDE.md`

### General Usage
- See `flask-app/README.md`

## Support Resources

- **Repository:** https://github.com/Napier40/Akademia-Studenta
- **Flask Docs:** https://flask.palletsprojects.com/
- **Bootstrap Docs:** https://getbootstrap.com/
- **Python Docs:** https://docs.python.org/

## Success Checklist

- [ ] Pulled latest changes from GitHub
- [ ] Virtual environment activated
- [ ] Dependencies installed/updated
- [ ] Database initialized with sample data
- [ ] Translations compiled
- [ ] Server running without errors
- [ ] Can access http://localhost:5000
- [ ] Homepage loads correctly
- [ ] Language switching works (EN ↔ PL)
- [ ] Blog posts visible
- [ ] Can view individual posts
- [ ] Forms work

## If Something Goes Wrong

1. **Don't panic!** Most issues are easy to fix
2. **Check the error message** - it usually tells you what's wrong
3. **Try the automated setup:** `setup.bat`
4. **Check TROUBLESHOOTING.md** for your specific error
5. **Start fresh if needed** - delete `.venv` and run `setup.bat`

---

## TL;DR (Too Long; Didn't Read)

```powershell
cd C:\Users\jackj\OneDrive\Desktop\Web_Designs\Akademia-Studenta\Akademia-Studenta
git pull origin main
cd flask-app
setup.bat
run.bat
```

Then visit: http://localhost:5000

**That's it!** 🎉

---

**Last Updated:** January 2025
**Repository:** https://github.com/Napier40/Akademia-Studenta
**Status:** All known issues fixed ✅