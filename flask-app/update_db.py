"""
Database Migration Script
Adds new fields to existing models for customer blog submissions and admin replies
"""

from app import create_app
from models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Add new columns to blog_posts table
    try:
        with db.engine.connect() as conn:
            # Check if columns exist before adding
            result = conn.execute(text("PRAGMA table_info(blog_posts)"))
            columns = [row[1] for row in result]
            
            if 'is_customer_post' not in columns:
                conn.execute(text("ALTER TABLE blog_posts ADD COLUMN is_customer_post BOOLEAN DEFAULT 0"))
                print("✓ Added is_customer_post column")
            
            if 'customer_language' not in columns:
                conn.execute(text("ALTER TABLE blog_posts ADD COLUMN customer_language VARCHAR(2)"))
                print("✓ Added customer_language column")
            
            if 'customer_name' not in columns:
                conn.execute(text("ALTER TABLE blog_posts ADD COLUMN customer_name VARCHAR(100)"))
                print("✓ Added customer_name column")
            
            if 'customer_email' not in columns:
                conn.execute(text("ALTER TABLE blog_posts ADD COLUMN customer_email VARCHAR(120)"))
                print("✓ Added customer_email column")
            
            conn.commit()
    except Exception as e:
        print(f"Error updating blog_posts: {e}")
    
    # Add new columns to contact_inquiries table
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(contact_inquiries)"))
            columns = [row[1] for row in result]
            
            if 'admin_reply' not in columns:
                conn.execute(text("ALTER TABLE contact_inquiries ADD COLUMN admin_reply TEXT"))
                print("✓ Added admin_reply column")
            
            if 'replied_at' not in columns:
                conn.execute(text("ALTER TABLE contact_inquiries ADD COLUMN replied_at DATETIME"))
                print("✓ Added replied_at column")
            
            conn.commit()
    except Exception as e:
        print(f"Error updating contact_inquiries: {e}")
    
    print("\n✅ Database migration completed successfully!")
    print("\nYou can now:")
    print("1. Accept customer blog submissions in single language")
    print("2. Reply to customer inquiries from admin panel")