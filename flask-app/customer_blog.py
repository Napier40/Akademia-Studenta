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
    
    @app.route('/blog/submit', methods=['GET', 'POST'])
    def submit_blog_post():
        """Allow customers to submit blog posts"""
        form = CustomerBlogPostForm()
        
        if form.validate_on_submit():
            # Get the selected language
            language = form.language.data
            
            # Create blog post with content in selected language
            # Auto-fill the other language with a placeholder or same content
            if language == 'en':
                title_en = form.title.data
                content_en = form.content.data
                excerpt_en = form.excerpt.data
                category_en = form.category.data
                # Use same content for Polish or placeholder
                title_pl = form.title.data
                content_pl = form.content.data
                excerpt_pl = form.excerpt.data
                category_pl = form.category.data
            else:  # Polish
                title_pl = form.title.data
                content_pl = form.content.data
                excerpt_pl = form.excerpt.data
                category_pl = form.category.data
                # Use same content for English or placeholder
                title_en = form.title.data
                content_en = form.content.data
                excerpt_en = form.excerpt.data
                category_en = form.category.data
            
            # Create slug from title
            slug = form.title.data.lower().replace(' ', '-')
            slug = ''.join(c for c in slug if c.isalnum() or c == '-')
            
            # Check if slug already exists
            existing = BlogPost.query.filter_by(slug=slug).first()
            if existing:
                slug = f"{slug}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            
            # Create post with pending status (requires admin approval)
            post = BlogPost(
                title_en=title_en,
                title_pl=title_pl,
                slug=slug,
                content_en=content_en,
                content_pl=content_pl,
                excerpt_en=excerpt_en,
                excerpt_pl=excerpt_pl,
                category_en=category_en,
                category_pl=category_pl,
                featured_image=form.featured_image.data,
                status='pending'  # Requires admin approval
            )
            
            db.session.add(post)
            db.session.commit()
            
            flash('Thank you! Your blog post has been submitted and is awaiting approval.', 'success')
            return redirect(url_for('blog'))
        
        return render_template('blog_submit.html', form=form)