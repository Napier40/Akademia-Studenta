# Windows Setup Guide for Akademia Studenta

This guide will help you set up the Flask application on Windows.

## Prerequisites

- Python 3.11 or 3.12 (Python 3.13 has some compatibility issues with older packages)
- Git for Windows
- A text editor (VS Code recommended)

## Step-by-Step Installation

### 1. Check Python Version

Open Command Prompt or PowerShell and check your Python version:

```powershell
python --version
```

**Important:** If you have Python 3.13, you should either:
- Downgrade to Python 3.12 (recommended)
- Or wait for all packages to be updated for Python 3.13 compatibility

To install Python 3.12:
1. Download from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your terminal after installation

### 2. Clone the Repository

```powershell
cd C:\Users\YourUsername\Desktop
git clone https://github.com/Napier40/Akademia-Studenta.git
cd Akademia-Studenta\flask-app
```

### 3. Create Virtual Environment

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# You should see (.venv) in your prompt
```

**Troubleshooting:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

**If you encounter errors:**

1. **SQLAlchemy compatibility error with Python 3.13:**
   - Solution: Use Python 3.12 instead
   - Or install the latest SQLAlchemy: `pip install SQLAlchemy==2.0.35`

2. **Microsoft Visual C++ error:**
   - Download and install: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Select "Desktop development with C++"

3. **Greenlet error:**
   - Try: `pip install greenlet --no-binary :all:`
   - Or: `pip install greenlet==3.0.3`

### 6. Set Up Environment Variables

```powershell
# Copy the example environment file
copy .env.example .env

# Edit .env with Notepad
notepad .env
```

Update the following in `.env`:
```
SECRET_KEY=your-random-secret-key-here-change-this
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///website.db
```

To generate a secure SECRET_KEY, run in Python:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 7. Initialize Database

```powershell
# Set Flask app environment variable
set FLASK_APP=app.py

# Initialize database
flask init-db

# (Optional) Add sample data
flask seed-db
```

### 8. Compile Translations

```powershell
pybabel compile -d translations
```

**If pybabel is not found:**
```powershell
pip install Babel
pybabel compile -d translations
```

### 9. Run the Application

```powershell
flask run
```

Or:
```powershell
python app.py
```

The application should now be running at: http://localhost:5000

### 10. Test the Application

Open your browser and visit:
- Homepage: http://localhost:5000
- Blog: http://localhost:5000/blog
- Services: http://localhost:5000/services
- Contact: http://localhost:5000/contact

Test language switching by clicking EN/PL in the navigation.

## Common Issues and Solutions

### Issue 1: "flask: command not found"

**Solution:**
```powershell
# Make sure virtual environment is activated
.venv\Scripts\activate

# Or use python -m flask
python -m flask run
```

### Issue 2: Port 5000 already in use

**Solution:**
```powershell
# Use a different port
flask run --port 5001
```

Or find and kill the process using port 5000:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Issue 3: Database locked error

**Solution:**
```powershell
# Delete the database and recreate
del instance\website.db
flask init-db
```

### Issue 4: Template not found

**Solution:**
Make sure you're running the app from the `flask-app` directory:
```powershell
cd C:\path\to\Akademia-Studenta\flask-app
flask run
```

### Issue 5: Import errors

**Solution:**
```powershell
# Reinstall all dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Issue 6: Python 3.13 Compatibility

**Error:** `AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> directly inherits TypingOnly...`

**Solution:**
1. **Recommended:** Use Python 3.12
   ```powershell
   # Deactivate current environment
   deactivate
   
   # Remove old virtual environment
   rmdir /s .venv
   
   # Create new environment with Python 3.12
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Alternative:** Update SQLAlchemy
   ```powershell
   pip install --upgrade SQLAlchemy
   ```

## Development Tips

### Running in Debug Mode

Edit `.env`:
```
FLASK_ENV=development
DEBUG=True
```

Then run:
```powershell
flask run --debug
```

### Viewing Database

Install DB Browser for SQLite:
- Download: https://sqlitebrowser.org/
- Open: `instance\website.db`

### Deactivating Virtual Environment

```powershell
deactivate
```

### Updating Dependencies

```powershell
pip install --upgrade -r requirements.txt
```

## IDE Setup (VS Code)

1. Install VS Code: https://code.visualstudio.com/
2. Install Python extension
3. Open folder: `Akademia-Studenta\flask-app`
4. Select Python interpreter: `.venv\Scripts\python.exe`
5. Install recommended extensions:
   - Python
   - Pylance
   - Jinja
   - SQLite Viewer

## Next Steps

1. Read the main [README.md](README.md) for usage instructions
2. Check [FLASK_IMPLEMENTATION_GUIDE.md](FLASK_IMPLEMENTATION_GUIDE.md) for detailed documentation
3. Customize the application for your needs
4. Add your own blog posts and content

## Getting Help

If you encounter issues not covered here:
1. Check the error message carefully
2. Search for the error on Google or Stack Overflow
3. Check Flask documentation: https://flask.palletsprojects.com/
4. Check SQLAlchemy documentation: https://www.sqlalchemy.org/

## Production Deployment

For deploying to production, see the deployment section in [FLASK_IMPLEMENTATION_GUIDE.md](FLASK_IMPLEMENTATION_GUIDE.md).

**Important for production:**
- Use PostgreSQL instead of SQLite
- Set strong SECRET_KEY
- Set DEBUG=False
- Use a production WSGI server (Gunicorn, uWSGI)
- Set up HTTPS
- Configure proper logging