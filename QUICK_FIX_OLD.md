# Quick Fix for Common Setup Issues

## Issue 1: Python 3.13 Compatibility (SQLAlchemy Error)

### The Problem

You're encountering this error:
```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> directly inherits TypingOnly but has additional attributes
```

This is because SQLAlchemy 2.0.23 is not fully compatible with Python 3.13.

## Issue 2: Flask-Babel API Error

### The Problem

You're encountering this error:
```
AttributeError: 'Babel' object has no attribute 'localeselector'
```

This is because Flask-Babel 4.0 changed its API and no longer uses the `@babel.localeselector` decorator.

## Issue 3: Database Not Initialized

### The Problem

You're encountering this error:
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: blog_posts
```

This means the database tables haven't been created yet. You need to initialize the database before running the application.

## Solution: Complete Setup (Fixes All Issues)

### Quick Fix (Recommended)

1. **Pull the latest changes from GitHub:**
   ```powershell
   cd C:\Users\jackj\OneDrive\Desktop\Web_Designs\Akademia-Studenta\Akademia-Studenta
   git pull origin main
   ```

2. **Activate your virtual environment:**
   ```powershell
   .venv\Scripts\activate
   ```

3. **Update all dependencies:**
   ```powershell
   cd flask-app
   pip install --upgrade -r requirements.txt
   ```

4. **Initialize the database:**
   ```powershell
   python init_db.py
   ```
   
   This will:
   - Create all database tables
   - Optionally add sample blog posts
   - Set up the database structure

5. **Compile translations:**
   ```powershell
   pybabel compile -d translations
   ```

6. **Run the application:**
   ```powershell
   flask run
   ```

This will fix the SQLAlchemy, Flask-Babel, and database initialization issues.

### Option 2: Use Python 3.12 (Recommended for Best Compatibility)

1. **Download Python 3.12:**
   - Go to: https://www.python.org/downloads/
   - Download Python 3.12.x (latest 3.12 version)
   - Install it (make sure to check "Add Python to PATH")

2. **Remove old virtual environment:**
   ```powershell
   cd C:\Users\jackj\OneDrive\Desktop\Web_Designs\Akademia-Studenta\Akademia-Studenta
   deactivate  # if currently activated
   rmdir /s .venv
   ```

3. **Create new virtual environment with Python 3.12:**
   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```powershell
   cd flask-app
   pip install -r requirements.txt
   ```

5. **Initialize database:**
   ```powershell
   flask init-db
   flask seed-db
   ```

6. **Compile translations:**
   ```powershell
   pybabel compile -d translations
   ```

7. **Run the application:**
   ```powershell
   flask run
   ```

### Option 3: Use Automated Setup Script (Easiest)

1. **Pull latest changes:**
   ```powershell
   cd C:\Users\jackj\OneDrive\Desktop\Web_Designs\Akademia-Studenta\Akademia-Studenta
   git pull origin main
   ```

2. **Run the setup script:**
   ```powershell
   cd flask-app
   setup.bat
   ```

3. **Run the application:**
   ```powershell
   run.bat
   ```

## Verify It's Working

After applying any of the above solutions, you should be able to:

1. Start the server without errors
2. Visit http://localhost:5000
3. See the homepage
4. Switch between English (EN) and Polish (PL) languages
5. Navigate to different pages (Blog, Services, Contact)

## If You Still Have Issues

Check the detailed troubleshooting guide in:
- `flask-app/WINDOWS_SETUP.md` - Comprehensive Windows setup guide
- `flask-app/README.md` - General usage guide
- `flask-app/FLASK_IMPLEMENTATION_GUIDE.md` - Detailed implementation guide

## Common Next Steps After Fixing

1. **Edit .env file** with your settings:
   ```powershell
   notepad flask-app\.env
   ```

2. **Generate a secure SECRET_KEY:**
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Add sample blog posts** (optional):
   ```powershell
   flask seed-db
   ```

## Need More Help?

The repository now includes:
- ✅ Updated requirements.txt with Python 3.13 compatible packages
- ✅ Comprehensive Windows setup guide
- ✅ Automated setup script (setup.bat)
- ✅ Easy run script (run.bat)
- ✅ Detailed troubleshooting documentation

All files are available at: https://github.com/Napier40/Akademia-Studenta