"""
Database Models for Flask Application
All SQLAlchemy models and database initialization
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize SQLAlchemy
db = SQLAlchemy()


# ============================================================================
# DATABASE MODELS - Define BEFORE init_db function
# ============================================================================

class BlogPost(db.Model):
    """
    Blog Post Model - Bilingual support for English and Polish
    """
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Bilingual title
    title_en = db.Column(db.String(200), nullable=False)
    title_pl = db.Column(db.String(200), nullable=False)
    
    # URL-friendly slug
    slug = db.Column(db.String(200), unique=True, nullable=False)
    
    # Bilingual content
    content_en = db.Column(db.Text, nullable=False)
    content_pl = db.Column(db.Text, nullable=False)
    
    # Bilingual excerpt/summary
    excerpt_en = db.Column(db.String(500))
    excerpt_pl = db.Column(db.String(500))
    
    # Featured image URL
    featured_image = db.Column(db.String(500))
    
    # Bilingual category
    category_en = db.Column(db.String(100))
    category_pl = db.Column(db.String(100))
    
    # Post status
    status = db.Column(
        db.String(20), 
        default='draft',
        nullable=False
    )  # draft, published, archived
    
    # View counter
    views_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    published_at = db.Column(db.DateTime)
    
    # Relationship with comments
    comments = db.relationship(
        'Comment', 
        backref='post', 
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<BlogPost {self.title_en}>'
    
    def get_title(self, language='en'):
        """Get title in specified language"""
        return self.title_pl if language == 'pl' else self.title_en
    
    def get_content(self, language='en'):
        """Get content in specified language"""
        return self.content_pl if language == 'pl' else self.content_en
    
    def get_excerpt(self, language='en'):
        """Get excerpt in specified language"""
        return self.excerpt_pl if language == 'pl' else self.excerpt_en
    
    def get_category(self, language='en'):
        """Get category in specified language"""
        return self.category_pl if language == 'pl' else self.category_en
    
    def increment_views(self):
        """Increment view counter"""
        self.views_count += 1
        db.session.commit()


class Comment(db.Model):
    """
    Comment Model - Anonymous commenting support
    """
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to blog post
    post_id = db.Column(
        db.Integer, 
        db.ForeignKey('blog_posts.id'), 
        nullable=False
    )
    
    # Commenter information (optional for anonymous)
    author_name = db.Column(db.String(100))
    author_email = db.Column(db.String(120))
    
    # Comment content
    content = db.Column(db.Text, nullable=False)
    
    # Optional rating (1-5 stars)
    rating = db.Column(db.Integer)
    
    # Moderation status
    status = db.Column(
        db.String(20), 
        default='pending',
        nullable=False
    )  # pending, approved, rejected, spam
    
    # IP address for spam prevention
    ip_address = db.Column(db.String(45))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    def __repr__(self):
        author = self.author_name or 'Anonymous'
        return f'<Comment by {author}>'
    
    def is_anonymous(self):
        """Check if comment is anonymous"""
        return not self.author_name
    
    def approve(self):
        """Approve comment"""
        self.status = 'approved'
        db.session.commit()
    
    def reject(self):
        """Reject comment"""
        self.status = 'rejected'
        db.session.commit()
    
    def mark_as_spam(self):
        """Mark comment as spam"""
        self.status = 'spam'
        db.session.commit()


class ContactInquiry(db.Model):
    """
    Contact Form Inquiry Model
    """
    __tablename__ = 'contact_inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Contact information
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    
    # Inquiry details
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Status tracking
    status = db.Column(
        db.String(20), 
        default='new',
        nullable=False
    )  # new, in_progress, resolved, closed
    
    # Newsletter subscription
    subscribe_newsletter = db.Column(db.Boolean, default=False)
    
    # IP address for spam prevention
    ip_address = db.Column(db.String(45))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    resolved_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<ContactInquiry from {self.name}>'
    
    def mark_in_progress(self):
        """Mark inquiry as in progress"""
        self.status = 'in_progress'
        db.session.commit()
    
    def mark_resolved(self):
        """Mark inquiry as resolved"""
        self.status = 'resolved'
        self.resolved_at = datetime.utcnow()
        db.session.commit()
    
    def close(self):
        """Close inquiry"""
        self.status = 'closed'
        db.session.commit()


# ============================================================================
# DATABASE INITIALIZATION - After models are defined
# ============================================================================

def init_db(app):
    """
    Initialize database with the Flask app
    Creates all tables if they don't exist
    
    IMPORTANT: This function is called AFTER all models are defined above
    """
    # Ensure instance directory exists
    instance_path = os.path.join(os.path.dirname(__file__), 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Create all tables within app context
    with app.app_context():
        # This will create tables for ALL models defined above
        db.create_all()
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        # Get database path for display
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            print(f"✓ Database initialized successfully")
            print(f"  Location: {db_path}")
            print(f"  Tables created: {', '.join(tables)}")
        else:
            print(f"✓ Database initialized successfully")
            print(f"  Tables created: {', '.join(tables)}")


# ============================================================================
# SAMPLE DATA SEEDING
# ============================================================================

def seed_sample_data():
    """
    Add sample blog posts to the database
    Only adds if database is empty
    
    Call this function within an app context:
        with app.app_context():
            seed_sample_data()
    """
    # Check if we already have posts
    if BlogPost.query.first():
        print("✓ Database already contains blog posts")
        return
    
    sample_posts = [
        {
            'title_en': 'Welcome to Our Blog',
            'title_pl': 'Witamy na naszym blogu',
            'slug': 'welcome-to-our-blog',
            'content_en': '''Welcome to our bilingual blog! This is a sample post to demonstrate the blog functionality.

This blog supports both English and Polish languages, allowing you to reach a wider audience. You can easily switch between languages using the language selector in the navigation bar.

Features include:
- Bilingual content support
- Anonymous commenting
- Comment ratings
- Post categories
- View counter
- And much more!

Feel free to explore and leave comments below.''',
            'content_pl': '''Witamy na naszym dwujęzycznym blogu! To jest przykładowy wpis demonstrujący funkcjonalność bloga.

Ten blog obsługuje zarówno język angielski, jak i polski, co pozwala dotrzeć do szerszej publiczności. Możesz łatwo przełączać się między językami za pomocą selektora języka na pasku nawigacyjnym.

Funkcje obejmują:
- Obsługa treści dwujęzycznych
- Anonimowe komentowanie
- Oceny komentarzy
- Kategorie wpisów
- Licznik wyświetleń
- I wiele więcej!

Zapraszamy do eksploracji i pozostawienia komentarzy poniżej.''',
            'excerpt_en': 'Welcome to our bilingual blog! Learn about our features and capabilities.',
            'excerpt_pl': 'Witamy na naszym dwujęzycznym blogu! Poznaj nasze funkcje i możliwości.',
            'category_en': 'Announcements',
            'category_pl': 'Ogłoszenia',
            'status': 'published',
            'published_at': datetime.utcnow()
        },
        {
            'title_en': 'Getting Started with Our Services',
            'title_pl': 'Rozpoczęcie pracy z naszymi usługami',
            'slug': 'getting-started-with-services',
            'content_en': '''Are you ready to get started with our services? This guide will help you understand what we offer and how to begin.

Our services are designed to help students succeed in their academic journey. Whether you need tutoring, study materials, or academic guidance, we're here to help.

How to Get Started:
1. Browse our services page to see what we offer
2. Contact us through the contact form
3. Schedule a consultation
4. Begin your journey to academic success

We look forward to working with you!''',
            'content_pl': '''Czy jesteś gotowy, aby rozpocząć korzystanie z naszych usług? Ten przewodnik pomoże Ci zrozumieć, co oferujemy i jak zacząć.

Nasze usługi zostały zaprojektowane, aby pomóc studentom odnieść sukces w ich akademickiej podróży. Niezależnie od tego, czy potrzebujesz korepetycji, materiałów do nauki czy wskazówek akademickich, jesteśmy tutaj, aby pomóc.

Jak zacząć:
1. Przeglądaj naszą stronę usług, aby zobaczyć, co oferujemy
2. Skontaktuj się z nami przez formularz kontaktowy
3. Umów się na konsultację
4. Rozpocznij swoją podróż do sukcesu akademickiego

Czekamy na współpracę z Tobą!''',
            'excerpt_en': 'Learn how to get started with our academic services and support.',
            'excerpt_pl': 'Dowiedz się, jak rozpocząć korzystanie z naszych usług akademickich i wsparcia.',
            'category_en': 'Guides',
            'category_pl': 'Przewodniki',
            'status': 'published',
            'published_at': datetime.utcnow()
        },
        {
            'title_en': 'Tips for Academic Success',
            'title_pl': 'Wskazówki dla sukcesu akademickiego',
            'slug': 'tips-for-academic-success',
            'content_en': '''Academic success doesn't happen by accident. It requires dedication, proper planning, and the right strategies. Here are some tips to help you succeed:

1. Time Management
   - Create a study schedule
   - Prioritize your tasks
   - Avoid procrastination

2. Effective Study Techniques
   - Active learning
   - Regular review sessions
   - Practice problems

3. Seek Help When Needed
   - Don't hesitate to ask questions
   - Join study groups
   - Use available resources

4. Maintain Balance
   - Get enough sleep
   - Exercise regularly
   - Take breaks

Remember, success is a journey, not a destination. Keep working hard and stay motivated!''',
            'content_pl': '''Sukces akademicki nie dzieje się przypadkowo. Wymaga poświęcenia, odpowiedniego planowania i właściwych strategii. Oto kilka wskazówek, które pomogą Ci odnieść sukces:

1. Zarządzanie czasem
   - Stwórz harmonogram nauki
   - Ustal priorytety zadań
   - Unikaj prokrastynacji

2. Skuteczne techniki nauki
   - Aktywne uczenie się
   - Regularne sesje powtórkowe
   - Zadania praktyczne

3. Szukaj pomocy, gdy jest potrzebna
   - Nie wahaj się zadawać pytań
   - Dołącz do grup studyjnych
   - Korzystaj z dostępnych zasobów

4. Utrzymuj równowagę
   - Śpij wystarczająco
   - Ćwicz regularnie
   - Rób przerwy

Pamiętaj, sukces to podróż, a nie cel. Pracuj ciężko i pozostań zmotywowany!''',
            'excerpt_en': 'Discover essential tips and strategies for achieving academic success.',
            'excerpt_pl': 'Odkryj niezbędne wskazówki i strategie osiągania sukcesu akademickiego.',
            'category_en': 'Tips & Advice',
            'category_pl': 'Porady i wskazówki',
            'status': 'published',
            'published_at': datetime.utcnow()
        }
    ]
    
    for post_data in sample_posts:
        post = BlogPost(**post_data)
        db.session.add(post)
    
    db.session.commit()
    print(f"✓ Added {len(sample_posts)} sample blog posts")