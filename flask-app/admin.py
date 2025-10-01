"""
Admin Routes for Blog Management
Simple admin interface for creating and managing blog posts
"""

from flask import render_template, request, redirect, url_for, flash, session
from models import db, BlogPost, Comment, ContactInquiry
from forms import BlogPostForm
from datetime import datetime
from functools import wraps


def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Please login as admin to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


def register_admin_routes(app):
    """Register all admin routes"""
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        """Admin login page"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Simple authentication (you should use proper authentication in production)
            if username == 'admin' and password == 'admin123':
                session['is_admin'] = True
                session['admin_username'] = username
                flash('Logged in successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid credentials!', 'error')
        
        return render_template('admin/login.html')
    
    
    @app.route('/admin/logout')
    def admin_logout():
        """Admin logout"""
        session.pop('is_admin', None)
        session.pop('admin_username', None)
        flash('Logged out successfully!', 'success')
        return redirect(url_for('index'))
    
    
    @app.route('/admin')
    @admin_required
    def admin_dashboard():
        """Admin dashboard"""
        # Get statistics
        total_posts = BlogPost.query.count()
        published_posts = BlogPost.query.filter_by(status='published').count()
        draft_posts = BlogPost.query.filter_by(status='draft').count()
        total_comments = Comment.query.count()
        pending_comments = Comment.query.filter_by(status='pending').count()
        total_inquiries = ContactInquiry.query.count()
        new_inquiries = ContactInquiry.query.filter_by(status='new').count()
        
        # Get recent posts
        recent_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(5).all()
        
        # Get pending comments
        pending_comments_list = Comment.query.filter_by(status='pending').order_by(Comment.created_at.desc()).limit(5).all()
        
        return render_template('admin/dashboard.html',
                             total_posts=total_posts,
                             published_posts=published_posts,
                             draft_posts=draft_posts,
                             total_comments=total_comments,
                             pending_comments=pending_comments,
                             total_inquiries=total_inquiries,
                             new_inquiries=new_inquiries,
                             recent_posts=recent_posts,
                             pending_comments_list=pending_comments_list)
    
    
    @app.route('/admin/posts')
    @admin_required
    def admin_posts():
        """List all blog posts"""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('admin/posts.html', posts=posts)
    
    
    @app.route('/admin/posts/new', methods=['GET', 'POST'])
    @admin_required
    def admin_new_post():
        """Create new blog post"""
        form = BlogPostForm()
        
        if form.validate_on_submit():
            # Create slug from English title
            slug = form.title_en.data.lower().replace(' ', '-')
            slug = ''.join(c for c in slug if c.isalnum() or c == '-')
            
            # Check if slug already exists
            existing = BlogPost.query.filter_by(slug=slug).first()
            if existing:
                slug = f"{slug}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            
            post = BlogPost(
                title_en=form.title_en.data,
                title_pl=form.title_pl.data,
                slug=slug,
                content_en=form.content_en.data,
                content_pl=form.content_pl.data,
                excerpt_en=form.excerpt_en.data,
                excerpt_pl=form.excerpt_pl.data,
                category_en=form.category_en.data,
                category_pl=form.category_pl.data,
                featured_image=form.featured_image.data,
                status=form.status.data
            )
            
            if post.status == 'published':
                post.published_at = datetime.utcnow()
            
            db.session.add(post)
            db.session.commit()
            
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('admin_posts'))
        
        return render_template('admin/post_form.html', form=form, title='New Post')
    
    
    @app.route('/admin/posts/<int:post_id>/edit', methods=['GET', 'POST'])
    @admin_required
    def admin_edit_post(post_id):
        """Edit blog post"""
        post = BlogPost.query.get_or_404(post_id)
        form = BlogPostForm(obj=post)
        
        if form.validate_on_submit():
            post.title_en = form.title_en.data
            post.title_pl = form.title_pl.data
            post.content_en = form.content_en.data
            post.content_pl = form.content_pl.data
            post.excerpt_en = form.excerpt_en.data
            post.excerpt_pl = form.excerpt_pl.data
            post.category_en = form.category_en.data
            post.category_pl = form.category_pl.data
            post.featured_image = form.featured_image.data
            
            old_status = post.status
            post.status = form.status.data
            
            # Set published_at if changing from draft to published
            if old_status != 'published' and post.status == 'published':
                post.published_at = datetime.utcnow()
            
            db.session.commit()
            
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('admin_posts'))
        
        return render_template('admin/post_form.html', form=form, post=post, title='Edit Post')
    
    
    @app.route('/admin/posts/<int:post_id>/delete', methods=['POST'])
    @admin_required
    def admin_delete_post(post_id):
        """Delete blog post"""
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        
        flash('Blog post deleted successfully!', 'success')
        return redirect(url_for('admin_posts'))
    
    
    @app.route('/admin/comments')
    @admin_required
    def admin_comments():
        """List all comments"""
        page = request.args.get('page', 1, type=int)
        status_filter = request.args.get('status', 'all')
        per_page = 20
        
        query = Comment.query
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        
        comments = query.order_by(Comment.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('admin/comments.html', comments=comments, status_filter=status_filter)
    
    
    @app.route('/admin/comments/<int:comment_id>/approve', methods=['POST'])
    @admin_required
    def admin_approve_comment(comment_id):
        """Approve comment"""
        comment = Comment.query.get_or_404(comment_id)
        comment.approve()
        
        flash('Comment approved!', 'success')
        return redirect(request.referrer or url_for('admin_comments'))
    
    
    @app.route('/admin/comments/<int:comment_id>/reject', methods=['POST'])
    @admin_required
    def admin_reject_comment(comment_id):
        """Reject comment"""
        comment = Comment.query.get_or_404(comment_id)
        comment.reject()
        
        flash('Comment rejected!', 'success')
        return redirect(request.referrer or url_for('admin_comments'))
    
    
    @app.route('/admin/comments/<int:comment_id>/delete', methods=['POST'])
    @admin_required
    def admin_delete_comment(comment_id):
        """Delete comment"""
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        
        flash('Comment deleted!', 'success')
        return redirect(request.referrer or url_for('admin_comments'))
    
    
    @app.route('/admin/inquiries')
    @admin_required
    def admin_inquiries():
        """List all contact inquiries"""
        page = request.args.get('page', 1, type=int)
        status_filter = request.args.get('status', 'all')
        per_page = 20
        
        query = ContactInquiry.query
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        
        inquiries = query.order_by(ContactInquiry.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('admin/inquiries.html', inquiries=inquiries, status_filter=status_filter)
    
    
    @app.route('/admin/inquiries/<int:inquiry_id>/mark-resolved', methods=['POST'])
    @admin_required
    def admin_resolve_inquiry(inquiry_id):
        """Mark inquiry as resolved"""
        inquiry = ContactInquiry.query.get_or_404(inquiry_id)
        inquiry.mark_resolved()
        
        flash('Inquiry marked as resolved!', 'success')
        return redirect(request.referrer or url_for('admin_inquiries'))