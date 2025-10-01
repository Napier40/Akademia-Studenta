# Troubleshooting Checklist

Quick reference for common issues and their solutions.

## Before You Start

Make sure you have:
- [ ] Python 3.11 or 3.12 installed (3.13 works but may have issues)
- [ ] Git installed
- [ ] Virtual environment activated (you should see `(.venv)` in your prompt)
- [ ] You're in the correct directory: `flask-app`

## Step-by-Step Troubleshooting

### 1. Pull Latest Changes

```powershell
cd C:\Users\jackj\OneDrive\Desktop\Web_Designs\Akademia-Studenta\Akademia-Studenta
git pull origin main
```

### 2. Activate Virtual Environment

```powershell
.venv\Scripts\activate
```

**If this fails:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\activate
```

### 3. Update Dependencies

```powershell
cd flask-app
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

### 4. Initialize Database

```powershell
python init_db.py
```

When prompted, type `y` to add sample blog posts.

**If this fails:**
- Make sure you're in the `flask-app` directory
- Try: `py init_db.py` instead of `python init_db.py`
- Delete old database: `del instance\website.db` and try again

### 5. Compile Translations

```powershell
pybabel compile -d translations
```

**If pybabel is not found:**
```powershell
pip install Babel
pybabel compile -d translations
```

### 6. Run Application

```powershell
flask run
```

**Alternative:**
```powershell
python app.py
```

**Or use the run script:**
```powershell
run.bat
```

## Common Error Messages

### Error: "AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'>"

**Cause:** SQLAlchemy incompatibility with Python 3.13

**Solution:**
```powershell
pip install --upgrade SQLAlchemy==2.0.35
```

### Error: "AttributeError: 'Babel' object has no attribute 'localeselector'"

**Cause:** Flask-Babel API changed in version 4.0

**Solution:** Pull latest changes from GitHub (already fixed in repository)
```powershell
git pull origin main
```

### Error: "no such table: blog_posts"

**Cause:** Database not initialized

**Solution:**
```powershell
python init_db.py
```

### Error: "flask: command not found"

**Cause:** Flask not in PATH or virtual environment not activated

**Solution:**
```powershell
.venv\Scripts\activate
python -m flask run
```

### Error: "Port 5000 already in use"

**Cause:** Another application is using port 5000

**Solution:**
```powershell
# Use different port
flask run --port 5001

# Or kill the process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Error: "No module named 'app'"

**Cause:** Wrong directory

**Solution:**
```powershell
cd flask-app
python init_db.py
```

### Error: "Template not found"

**Cause:** Running from wrong directory

**Solution:**
```powershell
cd C:\Users\jackj\OneDrive\Desktop\Web_Designs\Akademia-Studenta\Akademia-Studenta\flask-app
flask run
```

### Error: "Database is locked"

**Cause:** Another process is using the database

**Solution:**
```powershell
# Close all Flask instances
# Delete and recreate database
del instance\website.db
python init_db.py
```

## Quick Reset (Nuclear Option)

If nothing works, start fresh:

```powershell
# 1. Navigate to project
cd C:\Users\jackj\OneDrive\Desktop\Web_Designs\Akademia-Studenta\Akademia-Studenta

# 2. Pull latest changes
git pull origin main

# 3. Remove virtual environment
deactivate
rmdir /s .venv

# 4. Run automated setup
cd flask-app
setup.bat

# 5. Run application
run.bat
```

## Verification Checklist

After setup, verify everything works:

- [ ] Server starts without errors
- [ ] Can access http://localhost:5000
- [ ] Homepage loads with content
- [ ] Can switch between EN and PL languages
- [ ] Blog page shows posts
- [ ] Can view individual blog posts
- [ ] Services page loads
- [ ] Contact form displays
- [ ] Can submit comments (they go to pending status)

## File Structure Check

Make sure you have these files:

```
flask-app/
├── app.py                  ✓ Main application
├── init_db.py             ✓ Database initialization
├── config.py              ✓ Configuration
├── requirements.txt       ✓ Dependencies
├── .env                   ✓ Environment variables
├── templates/             ✓ HTML templates
│   ├── base.html
│   ├── index.html
│   ├── blog.html
│   ├── blog_post.html
│   ├── services.html
│   └── contact.html
└── translations/          ✓ Translation files
    └── pl/LC_MESSAGES/
        └── messages.po
```

## Environment Variables Check

Your `.env` file should contain:

```
SECRET_KEY=your-secret-key-here
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///website.db
```

Generate a secure SECRET_KEY:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

## Getting Help

If you're still stuck:

1. **Check the error message carefully** - It usually tells you what's wrong
2. **Read the detailed guides:**
   - `QUICK_FIX.md` - Quick solutions
   - `WINDOWS_SETUP.md` - Comprehensive setup
   - `README.md` - General usage
   - `FLASK_IMPLEMENTATION_GUIDE.md` - Technical details

3. **Search for the error:**
   - Google the exact error message
   - Check Stack Overflow
   - Check Flask documentation

4. **Common resources:**
   - Flask docs: https://flask.palletsprojects.com/
   - SQLAlchemy docs: https://www.sqlalchemy.org/
   - Python docs: https://docs.python.org/

## Success Indicators

You know it's working when:

✅ Server starts with: `Running on http://127.0.0.1:5000`
✅ No error messages in the console
✅ Browser shows the homepage
✅ Language switcher works (EN/PL)
✅ Blog posts are visible
✅ All pages load correctly

## Still Not Working?

Try the automated setup:

```powershell
cd flask-app
setup.bat
```

This script will:
- Check Python version
- Create virtual environment
- Install dependencies
- Initialize database
- Compile translations
- Guide you through the process

Then run:
```powershell
run.bat
```

---

**Last Updated:** After fixing SQLAlchemy, Flask-Babel, and database initialization issues.

**Repository:** https://github.com/Napier40/Akademia-Studenta