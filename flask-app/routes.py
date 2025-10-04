"""
Application Routes
All view functions and URL routing
"""

from flask import render_template, request, redirect, url_for, flash, session
from flask_babel import gettext
from models import db, BlogPost, Comment, ContactInquiry
from forms import CommentForm, ContactForm, BlogSearchForm
from sqlalchemy import or_


def register_routes(app):
    """
    Register all application routes
    """
    
    @app.route('/')
    def index():
        """Homepage"""
        # Get latest 3 published blog posts
        latest_posts = BlogPost.query.filter_by(
            status='published'
        ).order_by(
            BlogPost.published_at.desc()
        ).limit(3).all()
        
        return render_template('index.html', latest_posts=latest_posts)
    
    
    @app.route('/services')
    def services():
        """Services page"""
        return render_template('services.html')
    
    
    @app.route('/blog')
    def blog():
        """Blog listing page with pagination and search"""
        from forms import CustomerBlogPostForm
        
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        # Get search query
        search_query = request.args.get('q', '')
        category = request.args.get('category', '')
        
        # Base query - only published posts
        query = BlogPost.query.filter_by(status='published')
        
        # Apply search filter
        if search_query:
            lang = session.get('language', 'en')
            if lang == 'pl':
                query = query.filter(
                    or_(
                        BlogPost.title_pl.contains(search_query),
                        BlogPost.content_pl.contains(search_query),
                        BlogPost.excerpt_pl.contains(search_query)
                    )
                )
            else:
                query = query.filter(
                    or_(
                        BlogPost.title_en.contains(search_query),
                        BlogPost.content_en.contains(search_query),
                        BlogPost.excerpt_en.contains(search_query)
                    )
                )
        
        # Apply category filter
        if category:
            lang = session.get('language', 'en')
            if lang == 'pl':
                query = query.filter_by(category_pl=category)
            else:
                query = query.filter_by(category_en=category)
        
        # Order by published date
        query = query.order_by(BlogPost.published_at.desc())
        
        # Paginate results
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        posts = pagination.items
        
        # Get all categories for filter
        lang = session.get('language', 'en')
        if lang == 'pl':
            categories = db.session.query(BlogPost.category_pl).distinct().all()
            categories = [cat[0] for cat in categories if cat[0]]
        else:
            categories = db.session.query(BlogPost.category_en).distinct().all()
            categories = [cat[0] for cat in categories if cat[0]]
        
        # Create customer blog submission form
        form = CustomerBlogPostForm()
        
        return render_template(
            'blog.html',
            posts=posts,
            pagination=pagination,
            search_query=search_query,
            selected_category=category,
            categories=categories,
            form=form
        )
    
    
    @app.route('/blog/<slug>', methods=['GET', 'POST'])
    def blog_post(slug):
        """Individual blog post page with comments"""
        post = BlogPost.query.filter_by(slug=slug).first_or_404()
        
        # Increment view counter
        post.increment_views()
        
        # Get approved comments
        comments = Comment.query.filter_by(
            post_id=post.id,
            status='approved'
        ).order_by(Comment.created_at.desc()).all()
        
        # Comment form
        form = CommentForm()
        
        if form.validate_on_submit():
            # Create new comment
            comment = Comment(
                post_id=post.id,
                author_name=form.author_name.data or None,
                author_email=form.author_email.data or None,
                content=form.content.data,
                rating=int(form.rating.data) if form.rating.data else None,
                ip_address=request.remote_addr,
                status='pending'  # Requires moderation
            )
            
            db.session.add(comment)
            db.session.commit()
            
            flash(gettext('Thank you for your comment! It will be visible after moderation.'), 'success')
            return redirect(url_for('blog_post', slug=slug))
        
        return render_template(
            'blog_post.html',
            post=post,
            comments=comments,
            form=form
        )
    
    
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        """Contact form page"""
        form = ContactForm()
        
        if form.validate_on_submit():
            # Create new contact inquiry
            inquiry = ContactInquiry(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data or None,
                subject=form.subject.data,
                message=form.message.data,
                subscribe_newsletter=form.subscribe_newsletter.data,
                ip_address=request.remote_addr,
                status='new'
            )
            
            db.session.add(inquiry)
            db.session.commit()
            
            flash(gettext('Thank you for contacting us! We will respond as soon as possible.'), 'success')
            return redirect(url_for('contact'))
        
        return render_template('contact.html', form=form)
    
    
    @app.route('/set-language/<language>')
    def set_language(language):
        """Set user's preferred language"""
        if language in app.config['BABEL_SUPPORTED_LOCALES']:
            session['language'] = language
        
        # Redirect back to the previous page
        return redirect(request.referrer or url_for('index'))
    
    
    @app.route('/api/translate', methods=['POST'])
    def api_translate():
        """
        API endpoint for on-demand translation
        Used by admin panel for manual translation requests
        """
        from flask import jsonify
        
        data = request.get_json()
        
        text = data.get('text', '')
        source = data.get('source', 'EN')
        target = data.get('target', 'PL')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        try:
            from translation_service import get_translation_service
            translator = get_translation_service()
            
            if not translator.is_available():
                return jsonify({'error': 'Translation service not available'}), 503
            
            translation = translator.translate(text, source, target)
            
            return jsonify({
                'translation': translation,
                'source': source,
                'target': target,
                'success': True
            })
        except Exception as e:
            return jsonify({'error': str(e), 'success': False}), 500
    
    
    @app.route('/api/translation-usage')
    def api_translation_usage():
        """
        Get translation API usage statistics
        Admin only endpoint
        """
        from flask import jsonify
        
        # Check if user is admin
        if not session.get('is_admin'):
            return jsonify({'error': 'Unauthorized'}), 401
        
        try:
            from translation_service import get_translation_service
            translator = get_translation_service()
            
            if not translator.is_available():
                return jsonify({'error': 'Translation service not available'}), 503
            
            usage = translator.get_usage()
            
            if usage:
                return jsonify({
                    'usage': usage,
                    'success': True
                })
            else:
                return jsonify({'error': 'Could not retrieve usage data'}), 500
        except Exception as e:
            return jsonify({'error': str(e), 'success': False}), 500