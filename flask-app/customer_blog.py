"""
Customer Blog Routes
Allow customers to submit blog posts directly from the blog page
"""

from flask import render_template, request, redirect, url_for, flash, session
from models import db, BlogPost
from forms import CustomerBlogPostForm
from datetime import datetime


def register_customer_blog_routes(app):
    """Register customer blog submission routes"""
    
    @app.route('/blog/submit', methods=['POST'])
    def submit_blog_post():
        """
        Handle customer blog post submission
        Customers submit in ONE language only
        """
        form = CustomerBlogPostForm()
        
        if form.validate_on_submit():
            # Get the selected language
            language = form.language.data
            
            # Create slug from title
            slug = form.title.data.lower().replace(' ', '-')
            slug = ''.join(c for c in slug if c.isalnum() or c == '-')
            
            # Check if slug already exists
            existing = BlogPost.query.filter_by(slug=slug).first()
            if existing:
                slug = f"{slug}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            
            # Create post with content ONLY in the submitted language
            # The other language fields will be empty (admin can fill them later if needed)
            if language == 'en':
                title_en = form.title.data
                content_en = form.content.data
                category_en = form.category.data or 'Customer Submissions'
                # Leave Polish fields empty
                title_pl = ''
                content_pl = ''
                category_pl = ''
            else:  # Polish
                title_pl = form.title.data
                content_pl = form.content.data
                category_pl = form.category.data or 'Wpisy klientów'
                # Leave English fields empty
                title_en = ''
                content_en = ''
                category_en = ''
            
            # Create post with pending status (requires admin approval)
            post = BlogPost(
                title_en=title_en or 'Pending Translation',
                title_pl=title_pl or 'Oczekuje na tłumaczenie',
                slug=slug,
                content_en=content_en or 'Content pending translation',
                content_pl=content_pl or 'Treść oczekuje na tłumaczenie',
                category_en=category_en,
                category_pl=category_pl,
                status='pending',  # Requires admin approval
                is_customer_post=True,
                customer_language=language,
                customer_name=form.author_name.data,
                customer_email=form.author_email.data
            )
            
            db.session.add(post)
            db.session.commit()
            
            flash('Thank you! Your blog post has been submitted and is awaiting approval.', 'success')
            return redirect(url_for('blog'))
        
        # If form validation fails, redirect back to blog with errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
        
        return redirect(url_for('blog'))