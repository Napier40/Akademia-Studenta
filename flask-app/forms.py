"""
WTForms for Flask Application
All form definitions and validators
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Optional, Length, NumberRange


class CommentForm(FlaskForm):
    """
    Form for submitting blog comments
    Supports anonymous commenting
    """
    author_name = StringField(
        'Name',
        validators=[Optional(), Length(max=100)]
    )
    
    author_email = StringField(
        'Email',
        validators=[Optional(), Email(), Length(max=120)]
    )
    
    content = TextAreaField(
        'Comment',
        validators=[
            DataRequired(message='Comment content is required'),
            Length(min=10, max=2000, message='Comment must be between 10 and 2000 characters')
        ]
    )
    
    rating = SelectField(
        'Rating',
        choices=[
            ('', 'No rating'),
            ('1', '1 star'),
            ('2', '2 stars'),
            ('3', '3 stars'),
            ('4', '4 stars'),
            ('5', '5 stars')
        ],
        validators=[Optional()]
    )


class ContactForm(FlaskForm):
    """
    Form for contact inquiries
    """
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Name is required'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters')
        ]
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Please enter a valid email address'),
            Length(max=120)
        ]
    )
    
    phone = StringField(
        'Phone',
        validators=[Optional(), Length(max=20)]
    )
    
    subject = StringField(
        'Subject',
        validators=[
            DataRequired(message='Subject is required'),
            Length(min=5, max=200, message='Subject must be between 5 and 200 characters')
        ]
    )
    
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message='Message is required'),
            Length(min=20, max=2000, message='Message must be between 20 and 2000 characters')
        ]
    )
    
    subscribe_newsletter = BooleanField(
        'Subscribe to newsletter',
        default=False
    )


class BlogSearchForm(FlaskForm):
    """
    Form for searching blog posts
    """
    query = StringField(
        'Search',
        validators=[Optional(), Length(max=200)]
    )
    
    category = SelectField(
        'Category',
        choices=[('', 'All Categories')],
        validators=[Optional()]
    )


class BlogPostForm(FlaskForm):
    """
    Form for creating/editing blog posts
    """
    title_en = StringField(
        'Title (English)',
        validators=[
            DataRequired(message='English title is required'),
            Length(min=5, max=200)
        ]
    )
    
    title_pl = StringField(
        'Title (Polish)',
        validators=[
            DataRequired(message='Polish title is required'),
            Length(min=5, max=200)
        ]
    )
    
    content_en = TextAreaField(
        'Content (English)',
        validators=[
            DataRequired(message='English content is required'),
            Length(min=50)
        ]
    )
    
    content_pl = TextAreaField(
        'Content (Polish)',
        validators=[
            DataRequired(message='Polish content is required'),
            Length(min=50)
        ]
    )
    
    excerpt_en = TextAreaField(
        'Excerpt (English)',
        validators=[Optional(), Length(max=500)]
    )
    
    excerpt_pl = TextAreaField(
        'Excerpt (Polish)',
        validators=[Optional(), Length(max=500)]
    )
    
    category_en = StringField(
        'Category (English)',
        validators=[Optional(), Length(max=100)]
    )
    
    category_pl = StringField(
        'Category (Polish)',
        validators=[Optional(), Length(max=100)]
    )
    
    featured_image = StringField(
        'Featured Image URL',
        validators=[Optional(), Length(max=500)]
    )
    
    status = SelectField(
        'Status',
        choices=[
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('archived', 'Archived')
        ],
        validators=[DataRequired()]
    )