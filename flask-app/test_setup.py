"""
Quick test to verify Flask application setup
Run this to check if everything is working correctly
"""

from app import create_app
from models import db, BlogPost, Comment, ContactInquiry
import os


def test_database():
    """Test database connection and tables"""
    print("\n" + "="*60)
    print("🧪 Testing Database Setup")
    print("="*60)
    
    app = create_app()
    
    with app.app_context():
        # Get database path
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            print(f"\n📍 Database location: {db_path}")
            
            # Check if file exists
            if os.path.exists(db_path):
                print(f"✓ Database file exists")
                file_size = os.path.getsize(db_path)
                print(f"  File size: {file_size} bytes")
            else:
                print(f"✗ Database file NOT found!")
                return False
        
        # Test tables
        print("\n📋 Testing Tables:")
        try:
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            expected_tables = ['blog_posts', 'comments', 'contact_inquiries']
            for table in expected_tables:
                if table in tables:
                    print(f"  ✓ {table}")
                else:
                    print(f"  ✗ {table} - MISSING!")
                    return False
            
        except Exception as e:
            print(f"  ✗ Error checking tables: {e}")
            return False
        
        # Test queries
        print("\n🔍 Testing Queries:")
        try:
            blog_count = BlogPost.query.count()
            print(f"  ✓ BlogPost query works - {blog_count} posts")
            
            comment_count = Comment.query.count()
            print(f"  ✓ Comment query works - {comment_count} comments")
            
            inquiry_count = ContactInquiry.query.count()
            print(f"  ✓ ContactInquiry query works - {inquiry_count} inquiries")
            
        except Exception as e:
            print(f"  ✗ Query error: {e}")
            return False
        
        return True


def test_imports():
    """Test if all modules can be imported"""
    print("\n" + "="*60)
    print("📦 Testing Imports")
    print("="*60 + "\n")
    
    modules = [
        ('app', 'create_app'),
        ('models', 'db, BlogPost, Comment, ContactInquiry'),
        ('routes', 'register_routes'),
        ('forms', 'CommentForm, ContactForm'),
        ('extensions', 'init_extensions'),
        ('config', 'Config'),
    ]
    
    all_ok = True
    for module_name, items in modules:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name} ({items})")
        except Exception as e:
            print(f"  ✗ {module_name} - Error: {e}")
            all_ok = False
    
    return all_ok


def test_config():
    """Test configuration"""
    print("\n" + "="*60)
    print("⚙️  Testing Configuration")
    print("="*60 + "\n")
    
    app = create_app()
    
    configs = [
        'SECRET_KEY',
        'SQLALCHEMY_DATABASE_URI',
        'BABEL_DEFAULT_LOCALE',
        'BABEL_SUPPORTED_LOCALES',
    ]
    
    for config_key in configs:
        value = app.config.get(config_key)
        if value:
            # Mask secret key
            if config_key == 'SECRET_KEY':
                display_value = value[:10] + '...' if len(value) > 10 else value
            else:
                display_value = value
            print(f"  ✓ {config_key}: {display_value}")
        else:
            print(f"  ✗ {config_key}: NOT SET")
    
    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 Flask Application Setup Test")
    print("="*60)
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test config
    results.append(("Configuration", test_config()))
    
    # Test database
    results.append(("Database", test_database()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60 + "\n")
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ All tests passed!")
        print("="*60)
        print("\n💡 You can now run the application:")
        print("   python app.py")
        print("\n🌐 Then visit: http://localhost:5001")
    else:
        print("❌ Some tests failed!")
        print("="*60)
        print("\n💡 Check the errors above and:")
        print("   1. Make sure you're in the flask-app directory")
        print("   2. Install dependencies: pip install -r requirements.txt")
        print("   3. Check VSCODE_SETUP.md for troubleshooting")
    
    print()
    return all_passed


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)