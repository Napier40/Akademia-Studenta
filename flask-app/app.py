"""
Flask Application - Bilingual Website with Blog and Anonymous Comments
English and Polish language support
"""

from flask import (
    Flask, render_template, request, redirect, url_for, flash, session
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel, gettext, lazy_gettext as _l
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import os
from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, BooleanField, SelectField
)
from wtforms.validators import DataRequired, Email, Optional, Length

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///website.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'pl']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
babel = Babel()


# Babel locale selector
def get_locale():
    # Check if language is set in session
    if 'language' in session:
        return session['language']
    # Try to get from request
    return request.accept_languages.best_match(
        app.config['BABEL_SUPPORTED_LOCALES']
    )


babel.init_app(app, locale_selector=get_locale)

# ============================================
# DATABASE MODELS
# ============================================


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(255), nullable=False)
    title_pl = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content_en = db.Column(db.Text, nullable=False)
    content_pl = db.Column(db.Text, nullable=False)
    excerpt_en = db.Column(db.Text)
    excerpt_pl = db.Column(db.Text)
    featured_image = db.Column(db.String(500))
    category_en = db.Column(db.String(100))
    category_pl = db.Column(db.String(100))
    status = db.Column(db.String(20), default='published')
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_title(self, lang='en'):
        return self.title_en if lang == 'en' else self.title_pl
    
    def get_content(self, lang='en'):
        return self.content_en if lang == 'en' else self.content_pl
    
    def get_excerpt(self, lang='en'):
        return self.excerpt_en if lang == 'en' else self.excerpt_pl
    
    def get_category(self, lang='en'):
        return self.category_en if lang == 'en' else self.category_pl
    
    def __repr__(self):
        return f'<BlogPost {self.title_en}>'


class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    author_name = db.Column(db.String(100))
    author_email = db.Column(db.String(255))
    is_anonymous = db.Column(db.Boolean, default=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    status = db.Column(db.String(20), default='pending')
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment {self.id} on Post {self.post_id}>'


class ContactInquiry(db.Model):
    __tablename__ = 'contact_inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(255))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
# ============================================
# FORMS
# ============================================
from wtforms.validators import DataRequired, Email, Optional, Length

# ============================================
# FORMS
# ============================================


class CommentForm(FlaskForm):
    author_name = StringField(_l('Name'), validators=[Optional(), Length(max=100)])
    author_email = StringField(_l('Email'), validators=[Optional(), Email(), Length(max=255)])
    is_anonymous = BooleanField(_l('Post anonymously'))
    content = TextAreaField(_l('Your Feedback'), validators=[DataRequired(), Length(max=5000)])
    rating = SelectField(_l('Rating (Optional)'), 
                        choices=[(0, _l('No rating')), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                        coerce=int,
                        validators=[Optional()])


class ContactForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired(), Length(max=100)])
    email = StringField(_l('Email'), validators=[DataRequired(), Email(), Length(max=255)])
    phone = StringField(_l('Phone'), validators=[Optional(), Length(max=20)])
    subject = StringField(_l('Subject'), validators=[Optional(), Length(max=255)])
    message = TextAreaField(_l('Message'), validators=[DataRequired(), Length(max=5000)])


# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    """Homepage"""
    # Get latest blog posts for preview
    latest_posts = BlogPost.query.filter_by(status='published').order_by(BlogPost.published_at.desc()).limit(3).all()
    return render_template('index.html', latest_posts=latest_posts)


@app.route('/services')
def services():
    """Services page"""
    return render_template('services.html')


@app.route('/blog')
def blog():
    """Blog listing page"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    
    query = BlogPost.query.filter_by(status='published')
    
    # Filter by category if provided
    if category:
        lang = get_locale()
        if lang == 'en':
            query = query.filter_by(category_en=category)
        else:
            query = query.filter_by(category_pl=category)
    
    # Search if provided
    if search:
        lang = get_locale()
        if lang == 'en':
            query = query.filter(
                db.or_(
                    BlogPost.title_en.ilike(f'%{search}%'),
                    BlogPost.content_en.ilike(f'%{search}%')
                )
            )
        else:
            query = query.filter(
                db.or_(
                    BlogPost.title_pl.ilike(f'%{search}%'),
                    BlogPost.content_pl.ilike(f'%{search}%')
                )
            )
    
    # Paginate
    posts = query.order_by(BlogPost.published_at.desc()).paginate(
        page=page, per_page=9, error_out=False
    )
    
    return render_template('blog.html', posts=posts, category=category, search=search)


@app.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    post = BlogPost.query.filter_by(slug=slug, status='published').first_or_404()
    
    # Increment view count
    post.views_count += 1
    db.session.commit()
    
    # Get approved comments
    comments = Comment.query.filter_by(post_id=post.id, status='approved').order_by(Comment.created_at.desc()).all()
    
    # Comment form
    form = CommentForm()
    
    return render_template('blog_post.html', post=post, comments=comments, form=form)


@app.route('/blog/<slug>/comment', methods=['POST'])
def submit_comment(slug):
    """Submit a comment on a blog post"""
    post = BlogPost.query.filter_by(slug=slug, status='published').first_or_404()
    form = CommentForm()
    
    if form.validate_on_submit():
        # Check if anonymous
        is_anonymous = form.is_anonymous.data
        
        # Validate name and email if not anonymous
        if not is_anonymous:
            if not form.author_name.data or not form.author_email.data:
                flash(gettext('Name and email are required for non-anonymous comments.'), 'error')
                return redirect(url_for('blog_post', slug=slug))
        
        # Create comment
        comment = Comment(
            post_id=post.id,
            author_name=None if is_anonymous else form.author_name.data,
            author_email=None if is_anonymous else form.author_email.data,
            is_anonymous=is_anonymous,
            content=form.content.data,
            rating=form.rating.data if form.rating.data > 0 else None,
            status='pending',
            ip_address=request.remote_addr
        )
        
        db.session.add(comment)
        db.session.commit()
        
        flash(gettext('Thank you for your feedback! Your comment is pending approval.'), 'success')
        return redirect(url_for('blog_post', slug=slug))
    
    # If form validation fails
    flash(gettext('Please correct the errors in the form.'), 'error')
    return redirect(url_for('blog_post', slug=slug))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Create contact inquiry
        inquiry = ContactInquiry(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data,
            status='new'
        )
        
        db.session.add(inquiry)
        db.session.commit()
        
        flash(gettext('Your message has been sent successfully. We will get back to you soon!'), 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)


@app.route('/language/<lang>')
def set_language(lang):
    """Set language preference"""
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))


# ============================================
# TEMPLATE FILTERS
# ============================================

@app.template_filter('format_date')
def format_date(date, format='%B %d, %Y'):
    """Format date for display"""
    if date is None:
        return ""
    return date.strftime(format)


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


# ============================================
# CLI COMMANDS
# ============================================

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')


@app.cli.command()
def seed_db():
    """Seed the database with sample data."""
    # Create sample blog post
    post = BlogPost(
        title_en='Getting Started with Our Services',
        title_pl='Rozpoczęcie pracy z naszymi usługami',
        slug='getting-started-with-our-services',
        content_en='This is a comprehensive guide to getting started with our professional services...',
        content_pl='To jest kompleksowy przewodnik po rozpoczęciu pracy z naszymi profesjonalnymi usługami...',
        excerpt_en='Learn how to make the most of our professional services.',
        excerpt_pl='Dowiedz się, jak najlepiej wykorzystać nasze profesjonalne usługi.',
        category_en='Business Tips',
        category_pl='Porady biznesowe',
        featured_image='https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1200',
        status='published',
        published_at=datetime.utcnow()
    )
    
    db.session.add(post)
    db.session.commit()
    print('Database seeded with sample data.')


if __name__ == '__main__':
    app.run(debug=True)