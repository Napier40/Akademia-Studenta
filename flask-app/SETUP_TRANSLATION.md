# Translation Setup Guide

## Quick Start (5 Minutes)

### Step 1: Get DeepL API Key (FREE)

1. Go to https://www.deepl.com/pro-api
2. Click "Sign up for free"
3. Fill in your details
4. Verify your email
5. Copy your API key from the dashboard

**Free Tier Includes:**
- 500,000 characters/month
- No credit card required
- Perfect for most websites

### Step 2: Configure Your Application

1. **Create `.env` file** (if you don't have one):
```bash
cd flask-app
cp .env.example .env
```

2. **Add your DeepL API key** to `.env`:
```bash
# Open .env and add:
DEEPL_API_KEY=your-actual-api-key-here
ENABLE_AUTO_TRANSLATION=True
```

### Step 3: Install Dependencies

```bash
pip install deepl
```

Or update all dependencies:
```bash
pip install -r requirements.txt
```

### Step 4: Test Translation Service

```bash
python -c "from translation_service import get_translation_service; t = get_translation_service(); print(t.translate('Hello World', 'EN', 'PL'))"
```

Expected output: `Witaj świecie`

### Step 5: Restart Application

```bash
python app.py
```

## ✅ You're Done!

Translation is now active. Here's what happens automatically:

### 1. Customer Submits Blog Post
- Customer writes in English OR Polish
- Submits to `/blog`
- Post goes to "pending" status

### 2. Admin Approves Post
- Admin clicks "Approve" on dashboard
- **Auto-translation happens automatically**
- Post is published in BOTH languages

### 3. Translation Quality
- High-quality EN ↔ PL translation
- Preserves formatting and HTML
- Cached for performance

## How to Use

### For Admins:

#### Approve Customer Posts (Auto-Translate):
1. Login to admin panel
2. Go to Dashboard
3. See pending customer posts
4. Click "Approve"
5. **Translation happens automatically**
6. Post published in both languages

#### Manual Translation (Admin Panel):
1. Edit any blog post
2. Fill in one language
3. Click "Auto-Translate" button
4. Other language fills automatically

#### Check API Usage:
```bash
# In Python console or script
from translation_service import get_translation_service
translator = get_translation_service()
usage = translator.get_usage()
print(f"Used: {usage['character_count']}/{usage['character_limit']}")
print(f"Percentage: {usage['percentage_used']}%")
```

### For Customers:

#### Submit Blog Post:
1. Go to `/blog`
2. Click "Submit Your Post"
3. Choose language (EN or PL)
4. Write in ONE language only
5. Submit
6. Admin will approve and auto-translate

## Features

### ✅ What's Automated:
- Blog post translation on approval
- Title translation
- Content translation (preserves HTML)
- Category translation
- Excerpt translation

### ✅ What's Cached:
- All translations cached in memory
- No duplicate API calls
- Fast performance

### ✅ What's Tracked:
- Original language stored
- Customer name/email stored
- Translation status visible

## API Usage Monitoring

### Check Usage in Admin Panel:

Add this to your admin dashboard template:

```html
<div class="card">
    <div class="card-header">
        <h5>Translation API Usage</h5>
    </div>
    <div class="card-body">
        <div id="translation-usage">Loading...</div>
    </div>
</div>

<script>
fetch('/api/translation-usage')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const usage = data.usage;
            document.getElementById('translation-usage').innerHTML = `
                <p>Characters used: ${usage.character_count.toLocaleString()} / ${usage.character_limit.toLocaleString()}</p>
                <div class="progress">
                    <div class="progress-bar" style="width: ${usage.percentage_used}%">
                        ${usage.percentage_used.toFixed(1)}%
                    </div>
                </div>
            `;
        }
    });
</script>
```

## Cost Estimation

### Free Tier (500,000 chars/month):
- Average blog post: 2,000 characters
- **You can translate: 250 blog posts/month**
- **Cost: $0**

### If You Need More:

**Pro Tier ($5.49/month):**
- 1,000,000 characters/month
- 500 blog posts/month

**Advanced Tier ($25/month):**
- 5,000,000 characters/month
- 2,500 blog posts/month

## Troubleshooting

### Translation Not Working?

1. **Check API Key:**
```bash
# In Python console
import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv('DEEPL_API_KEY'))
```

2. **Check Service Status:**
```bash
python -c "from translation_service import get_translation_service; print(get_translation_service().is_available())"
```

3. **Check Logs:**
```bash
# Look for translation errors in console output
python app.py
```

### Common Issues:

**"Translation service not available"**
- API key not set in .env
- API key invalid
- Solution: Check your API key

**"DeepL API error"**
- API limit reached
- Network issue
- Solution: Check usage, verify internet connection

**"Translation returns original text"**
- Service not initialized
- API error (falls back to original)
- Solution: Check logs for specific error

## Advanced Configuration

### Disable Auto-Translation:

In `.env`:
```bash
ENABLE_AUTO_TRANSLATION=False
```

### Change Cache Timeout:

In `config.py`:
```python
TRANSLATION_CACHE_TIMEOUT = 7200  # 2 hours
```

### Custom Translation Logic:

Edit `translation_service.py`:
```python
def translate_blog_post(post):
    # Add your custom logic here
    # Example: Only translate if post is longer than 100 chars
    if len(post.content_en or post.content_pl) < 100:
        return False
    
    # Continue with translation...
```

## Testing

### Test Translation Service:

```python
from translation_service import get_translation_service

translator = get_translation_service()

# Test basic translation
result = translator.translate("Hello World", "EN", "PL")
print(result)  # Should print: Witaj świecie

# Test HTML translation
html = "<p>Hello <strong>World</strong></p>"
result = translator.translate_html(html, "EN", "PL")
print(result)  # Should preserve HTML tags

# Test language detection
text = "Witaj świecie"
lang = translator.detect_language(text)
print(lang)  # Should print: PL

# Check usage
usage = translator.get_usage()
print(usage)
```

### Test Blog Post Translation:

```python
from models import BlogPost
from translation_service import translate_blog_post

# Get a pending post
post = BlogPost.query.filter_by(status='pending').first()

# Translate it
success = translate_blog_post(post)
print(f"Translation successful: {success}")

# Check results
print(f"Title EN: {post.title_en}")
print(f"Title PL: {post.title_pl}")
```

## Best Practices

### 1. Monitor Usage
- Check usage weekly
- Set up alerts at 80% usage
- Upgrade plan if needed

### 2. Quality Control
- Review auto-translated posts
- Edit if needed
- Keep original language available

### 3. Performance
- Translations are cached
- No duplicate API calls
- Fast user experience

### 4. Fallback
- If translation fails, original language is used
- No errors shown to users
- Admin sees warning message

## Support

### DeepL Support:
- Documentation: https://www.deepl.com/docs-api
- Support: support@deepl.com

### Application Issues:
- Check logs in console
- Review `translation_service.py`
- Test with simple examples first

## Summary

✅ **Setup Time:** 5 minutes
✅ **Cost:** Free (500K chars/month)
✅ **Quality:** Excellent for EN ↔ PL
✅ **Automation:** Fully automated on approval
✅ **Performance:** Cached and fast
✅ **Maintenance:** Minimal

Your translation system is now ready to use!