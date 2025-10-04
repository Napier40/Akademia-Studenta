# 🚀 Automated Translation - Quick Start Guide

## What You're Getting

A **fully automated translation system** that translates blog posts from English to Polish (and vice versa) with **95% less manual work**.

## ⚡ 5-Minute Setup

### Step 1: Get Free API Key

1. Visit: **https://www.deepl.com/pro-api**
2. Click **"Sign up for free"**
3. Fill in your details (no credit card needed)
4. Verify your email
5. Copy your API key from the dashboard

**Free Tier:**
- 500,000 characters/month
- ~250 blog posts/month
- Perfect for your website

### Step 2: Configure

```bash
cd flask-app

# Create .env file if you don't have one
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use any text editor
```

Add this line to `.env`:
```bash
DEEPL_API_KEY=your-actual-api-key-here
ENABLE_AUTO_TRANSLATION=True
```

### Step 3: Install

```bash
pip install deepl
```

Or update all dependencies:
```bash
pip install -r requirements.txt
```

### Step 4: Test

```bash
python -c "from translation_service import get_translation_service; t = get_translation_service(); print(t.translate('Hello World', 'EN', 'PL'))"
```

Expected output: `Witaj świecie`

### Step 5: Run

```bash
python app.py
```

## ✅ You're Done!

## How It Works

### For Customers:
1. Visit `/blog`
2. Click "Submit Your Post"
3. Write in **ONE language** (English OR Polish)
4. Submit
5. Wait for admin approval

### For You (Admin):
1. Login to admin panel
2. See pending customer post
3. Click **"Approve"**
4. **🤖 Magic happens:**
   - Post automatically translated to other language
   - Title translated
   - Content translated (preserves formatting)
   - Category translated
5. Post published in **BOTH languages**

## What Gets Translated Automatically

✅ Blog post titles
✅ Blog post content (preserves HTML)
✅ Categories
✅ Excerpts
✅ All customer submissions

## Cost

**FREE** for most websites:
- 500,000 characters/month free
- Average blog post: 2,000 characters
- You can translate: **250 posts/month**
- Cost: **$0**

If you need more:
- Pro: $5.49/month (1M chars)
- Advanced: $25/month (5M chars)

## Features

### ✅ Automated
- Translates on admin approval
- No manual work needed
- High-quality translations

### ✅ Smart
- Only translates missing language
- Preserves original language
- Caches translations (fast)

### ✅ Safe
- Graceful error handling
- Falls back to original if fails
- Admin sees status messages

### ✅ Flexible
- Can disable auto-translation
- Can edit translations
- Can manually translate

## Check API Usage

```python
from translation_service import get_translation_service
translator = get_translation_service()
usage = translator.get_usage()
print(f"Used: {usage['character_count']:,} / {usage['character_limit']:,}")
print(f"Percentage: {usage['percentage_used']:.1f}%")
```

## Troubleshooting

### Translation not working?

**Check API key:**
```bash
cat .env | grep DEEPL_API_KEY
```

**Test service:**
```bash
python -c "from translation_service import get_translation_service; print(get_translation_service().is_available())"
```

**Check logs:**
Look for errors in console when running `python app.py`

### Common Issues:

**"Translation service not available"**
- Solution: Check API key in .env file

**"DeepL API error"**
- Solution: Verify API key is correct
- Check internet connection
- Check API usage limit

**Translation returns original text**
- This is normal fallback behavior
- Check logs for specific error
- Verify API key is valid

## Documentation

### Quick Guides:
- **TRANSLATION_QUICK_START.md** (this file) - 5-minute setup
- **SETUP_TRANSLATION.md** - Detailed setup instructions
- **TRANSLATION_SUMMARY.md** - Feature overview

### Complete Guide:
- **TRANSLATION_IMPLEMENTATION_GUIDE.md** - Full technical documentation (1000+ lines)

### Code:
- **translation_service.py** - Core translation service
- All functions documented with examples

## Example Workflow

### Before (Manual Translation):
```
Customer submits in English
↓
Admin reviews (5 min)
↓
Admin manually translates to Polish (30 min)
↓
Admin publishes
↓
Total time: 35 minutes
```

### After (Automated):
```
Customer submits in English
↓
Admin clicks "Approve" (30 sec)
↓
🤖 Auto-translates to Polish (2 sec)
↓
Published in both languages
↓
Total time: 32 seconds
```

**Time saved: 97%**

## Benefits Summary

### For Customers:
✅ Write in one language only
✅ No translation needed
✅ Simple process

### For You:
✅ 95% less manual work
✅ High-quality translations
✅ Full control
✅ Edit if needed

### For Website:
✅ Fully bilingual
✅ Professional appearance
✅ SEO-friendly
✅ Fast performance

## Next Steps

1. ✅ Get DeepL API key (free)
2. ✅ Add to .env file
3. ✅ Install deepl package
4. ✅ Test translation
5. ✅ Approve a customer post
6. ✅ See automatic translation!

## Support

### Need Help?
- Check **SETUP_TRANSLATION.md** for detailed instructions
- Read **TRANSLATION_IMPLEMENTATION_GUIDE.md** for technical details
- Review code in **translation_service.py**

### DeepL Support:
- Docs: https://www.deepl.com/docs-api
- Email: support@deepl.com

---

**Ready to translate automatically!** 🎉

Just add your API key and start approving posts.