"""
Unit Tests for Database Models
"""

import unittest
from datetime import datetime
from app import create_app
from models import db, BlogPost, Comment, ContactInquiry


class TestModels(unittest.TestCase):
    """Test database models"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_blog_post_creation(self):
        """Test creating a blog post"""
        post = BlogPost(
            title_en="Test Post",
            title_pl="Test Post PL",
            slug="test-post",
            content_en="Test content",
            content_pl="Test content PL",
            status="published"
        )
        db.session.add(post)
        db.session.commit()
        
        self.assertIsNotNone(post.id)
        self.assertEqual(post.title_en, "Test Post")
        self.assertEqual(post.status, "published")
    
    def test_blog_post_get_title(self):
        """Test get_title method"""
        post = BlogPost(
            title_en="English Title",
            title_pl="Polish Title",
            slug="test",
            content_en="Content",
            content_pl="Content PL"
        )
        
        self.assertEqual(post.get_title('en'), "English Title")
        self.assertEqual(post.get_title('pl'), "Polish Title")
    
    def test_blog_post_increment_views(self):
        """Test view counter increment"""
        post = BlogPost(
            title_en="Test",
            title_pl="Test",
            slug="test",
            content_en="Content",
            content_pl="Content"
        )
        db.session.add(post)
        db.session.commit()
        
        initial_views = post.views_count
        post.increment_views()
        
        self.assertEqual(post.views_count, initial_views + 1)
    
    def test_comment_creation(self):
        """Test creating a comment"""
        post = BlogPost(
            title_en="Test",
            title_pl="Test",
            slug="test",
            content_en="Content",
            content_pl="Content"
        )
        db.session.add(post)
        db.session.commit()
        
        comment = Comment(
            post_id=post.id,
            author_name="John Doe",
            author_email="john@example.com",
            content="Great post!",
            status="pending"
        )
        db.session.add(comment)
        db.session.commit()
        
        self.assertIsNotNone(comment.id)
        self.assertEqual(comment.author_name, "John Doe")
        self.assertEqual(comment.status, "pending")
    
    def test_contact_inquiry_creation(self):
        """Test creating a contact inquiry"""
        inquiry = ContactInquiry(
            name="Jane Doe",
            email="jane@example.com",
            subject="Question",
            message="I have a question",
            status="new"
        )
        db.session.add(inquiry)
        db.session.commit()
        
        self.assertIsNotNone(inquiry.id)
        self.assertEqual(inquiry.name, "Jane Doe")
        self.assertEqual(inquiry.status, "new")
    
    def test_customer_blog_post(self):
        """Test customer blog post tracking"""
        post = BlogPost(
            title_en="Customer Post",
            title_pl="",
            slug="customer-post",
            content_en="Customer content",
            content_pl="",
            is_customer_post=True,
            customer_language="en",
            customer_name="John Customer",
            customer_email="john@customer.com",
            status="pending"
        )
        db.session.add(post)
        db.session.commit()
        
        self.assertTrue(post.is_customer_post)
        self.assertEqual(post.customer_language, "en")
        self.assertEqual(post.customer_name, "John Customer")
        self.assertEqual(post.status, "pending")


if __name__ == '__main__':
    unittest.main()