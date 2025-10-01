"""
Database Initialization Script
Run this to initialize the database and optionally add sample data
"""

import sys
from app import create_app
from models import db, seed_sample_data


def init_database():
    """
    Initialize the database
    Creates all tables and optionally seeds sample data
    """
    print("\n" + "="*60)
    print("🗄️  Database Initialization")
    print("="*60 + "\n")
    
    # Create app instance
    app = create_app()
    
    with app.app_context():
        # Drop all tables (optional - for fresh start)
        response = input("Do you want to drop existing tables? (y/N): ").strip().lower()
        if response == 'y':
            print("⚠️  Dropping all existing tables...")
            db.drop_all()
            print("✓ All tables dropped")
        
        # Create all tables
        print("\n📋 Creating database tables...")
        db.create_all()
        print("✓ All tables created successfully")
        
        # Ask about sample data
        response = input("\nDo you want to add sample blog posts? (Y/n): ").strip().lower()
        if response != 'n':
            print("\n📝 Adding sample blog posts...")
            seed_sample_data()
            print("✓ Sample data added successfully")
        else:
            print("⏭️  Skipping sample data")
    
    print("\n" + "="*60)
    print("✅ Database initialization complete!")
    print("="*60)
    print("\n💡 You can now run the application with: python app.py")
    print("   Or on Windows: run.bat\n")


if __name__ == '__main__':
    try:
        init_database()
    except KeyboardInterrupt:
        print("\n\n⚠️  Initialization cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        sys.exit(1)