# VS Code Setup Guide

## 🎯 Quick Fix for "no such table" Error

The error you're seeing happens when the database file isn't in the expected location. This has been fixed!

### What Was Fixed

1. **Absolute Database Path** - Database now uses absolute path instead of relative
2. **Instance Directory** - Automatically creates `instance/` directory
3. **Clear Location** - Shows exactly where database is created

### Database Location

The database is now created at:
```
flask-app/instance/website.db
```

---

## 🚀 Running in VS Code

### Method 1: Using VS Code Terminal (Recommended)

1. **Open Terminal in VS Code** (Ctrl+` or View → Terminal)

2. **Navigate to flask-app directory:**
   ```bash
   cd flask-app
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Verify database location:**
   You should see:
   ```
   ✓ Database tables created successfully
     Database location: /full/path/to/flask-app/instance/website.db
   ```

### Method 2: Using VS Code Debugger

1. **Create `.vscode/launch.json`:**
   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python: Flask",
               "type": "python",
               "request": "launch",
               "module": "flask",
               "env": {
                   "FLASK_APP": "app.py",
                   "FLASK_DEBUG": "1"
               },
               "args": [
                   "run",
                   "--no-debugger",
                   "--no-reload"
               ],
               "jinja": true,
               "justMyCode": true,
               "cwd": "${workspaceFolder}/flask-app"
           }
       ]
   }
   ```

2. **Press F5** to start debugging

### Method 3: Using Run Button

1. **Open `app.py` in VS Code**

2. **Click the ▶️ Run button** in the top right

3. **Select "Python File"**

---

## 🔍 Troubleshooting in VS Code

### Issue 1: "no such table: blog_posts"

**Cause:** Database not created or wrong location

**Solution:**
```bash
# 1. Delete old database (if exists)
rm -rf instance/website.db

# 2. Run the app
python app.py

# 3. Check the output for database location
# You should see: "Database location: /path/to/instance/website.db"
```

### Issue 2: Import Errors

**Cause:** Python not finding modules

**Solution:**
```bash
# Make sure you're in the flask-app directory
cd flask-app

# Install dependencies
pip install -r requirements.txt

# Run from flask-app directory
python app.py
```

### Issue 3: Wrong Working Directory

**Cause:** VS Code running from wrong folder

**Solution:**

1. **Check current directory in terminal:**
   ```bash
   pwd
   # Should show: /path/to/Akademia-Studenta/flask-app
   ```

2. **If wrong, navigate to correct directory:**
   ```bash
   cd flask-app
   ```

3. **Or set working directory in VS Code:**
   - Open Settings (Ctrl+,)
   - Search for "python.terminal.executeInFileDir"
   - Enable it

### Issue 4: Multiple Python Versions

**Cause:** VS Code using wrong Python interpreter

**Solution:**

1. **Select Python interpreter:**
   - Press Ctrl+Shift+P
   - Type "Python: Select Interpreter"
   - Choose Python 3.11 or higher

2. **Verify version:**
   ```bash
   python --version
   # Should show: Python 3.11.x or higher
   ```

---

## 📁 VS Code Workspace Setup

### Recommended Folder Structure

```
Akademia-Studenta/          # Open THIS folder in VS Code
├── flask-app/              # Application directory
│   ├── app.py             # Main entry point
│   ├── models.py          # Database models
│   ├── routes.py          # Routes
│   ├── forms.py           # Forms
│   ├── extensions.py      # Extensions
│   ├── config.py          # Configuration
│   ├── instance/          # Database location (auto-created)
│   │   └── website.db    # SQLite database
│   ├── templates/         # HTML templates
│   └── translations/      # i18n files
└── documentation files
```

### VS Code Settings

Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/instance": false
    },
    "python.analysis.extraPaths": [
        "${workspaceFolder}/flask-app"
    ]
}
```

---

## 🧪 Testing the Setup

### Quick Test Script

Create `test_setup.py` in flask-app directory:

```python
"""
Quick test to verify everything is working
"""
from app import create_app
from models import db, BlogPost

def test_database():
    app = create_app()
    
    with app.app_context():
        # Test database connection
        try:
            count = BlogPost.query.count()
            print(f"✓ Database working! Blog posts: {count}")
            return True
        except Exception as e:
            print(f"✗ Database error: {e}")
            return False

if __name__ == '__main__':
    print("Testing Flask application setup...")
    if test_database():
        print("\n✓ All tests passed!")
        print("✓ You can now run: python app.py")
    else:
        print("\n✗ Setup incomplete. Check errors above.")
```

Run it:
```bash
cd flask-app
python test_setup.py
```

---

## 🎨 VS Code Extensions (Recommended)

1. **Python** (Microsoft) - Python language support
2. **Pylance** (Microsoft) - Fast Python language server
3. **Jinja** (wholroyd) - Jinja template support
4. **SQLite Viewer** (alexcvzz) - View database contents
5. **Better Jinja** (samuelcolvin) - Better Jinja syntax
6. **Flask Snippets** (cstrap) - Flask code snippets

---

## 📊 Viewing the Database in VS Code

### Using SQLite Viewer Extension

1. **Install SQLite Viewer extension**

2. **Open database file:**
   - Navigate to `flask-app/instance/website.db`
   - Right-click → "Open Database"

3. **View tables:**
   - See blog_posts, comments, contact_inquiries
   - View data in each table

### Using Command Line

```bash
# Navigate to flask-app
cd flask-app

# Open SQLite
sqlite3 instance/website.db

# List tables
.tables

# View blog posts
SELECT * FROM blog_posts;

# Exit
.quit
```

---

## 🐛 Common VS Code Issues

### Issue: "Module not found"

**Fix:**
```bash
# Ensure you're in flask-app directory
cd flask-app

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Permission denied"

**Fix:**
```bash
# On Windows, run VS Code as administrator
# Or check file permissions:
chmod -R 755 flask-app/
```

### Issue: "Port already in use"

**Fix:**
```bash
# Kill existing Python processes
# Windows:
taskkill /F /IM python.exe

# Linux/Mac:
pkill -9 python

# Or use different port in app.py:
# app.run(debug=True, port=5002)
```

### Issue: Changes not reflecting

**Fix:**
1. Stop the server (Ctrl+C)
2. Clear Python cache:
   ```bash
   find . -type d -name __pycache__ -exec rm -rf {} +
   ```
3. Restart the server

---

## ✅ Verification Checklist

Before running the app, verify:

- [ ] You're in the `flask-app` directory
- [ ] Python 3.11+ is installed (`python --version`)
- [ ] Dependencies are installed (`pip list | grep Flask`)
- [ ] No other Flask app is running on port 5001
- [ ] You have write permissions in the directory

After running the app, verify:

- [ ] You see "✓ Database tables created successfully"
- [ ] You see the database location path
- [ ] The `instance/` directory exists
- [ ] The `instance/website.db` file exists
- [ ] The app is accessible at http://localhost:5001

---

## 🚀 Quick Start Commands

```bash
# 1. Navigate to project
cd Akademia-Studenta/flask-app

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Run the application
python app.py

# 4. Open in browser
# http://localhost:5001
```

---

## 📝 Notes for VS Code Users

1. **Always run from flask-app directory** - This ensures correct paths
2. **Check terminal output** - Look for database location message
3. **Use integrated terminal** - Better than external terminal
4. **Enable auto-save** - File → Auto Save
5. **Use Python virtual environment** - Recommended for isolation

---

## 🎓 Understanding the Structure

### Why instance/ directory?

Flask uses the `instance/` folder for:
- Database files
- Configuration files
- User-uploaded files
- Any instance-specific data

This folder is:
- ✅ Automatically created
- ✅ Excluded from git (in .gitignore)
- ✅ Safe for sensitive data

### Why absolute paths?

The config now uses absolute paths to ensure:
- ✅ Database created in correct location
- ✅ Works regardless of working directory
- ✅ No confusion about file location

---

## 💡 Pro Tips

1. **Use VS Code's integrated terminal** - Keeps everything in one place
2. **Set up debugging** - Use F5 to debug with breakpoints
3. **Install SQLite Viewer** - View database without leaving VS Code
4. **Use Python virtual environment** - Isolate project dependencies
5. **Enable auto-save** - Never lose changes

---

## 🆘 Still Having Issues?

If you're still seeing the "no such table" error:

1. **Delete everything and start fresh:**
   ```bash
   cd flask-app
   rm -rf instance/
   rm -rf __pycache__/
   python app.py
   ```

2. **Check the output carefully:**
   - Look for "Database location: /path/to/database"
   - Verify the path exists
   - Check if file was created

3. **Run the test script:**
   ```bash
   python test_setup.py
   ```

4. **Check VS Code terminal:**
   - Make sure you're in flask-app directory
   - Run `pwd` to verify location

---

**Last Updated:** 2025-10-01
**Tested with:** VS Code 1.85+, Python 3.11+
**Status:** ✅ Working