# Quick Start Guide - Customer Blog Submission Changes

## What You Need to Know

### 🎯 Main Changes
1. **Customer blog submission is now ON THE BLOG PAGE** - no separate page
2. **Customers submit in ONE language** (English OR Polish) - not both
3. **Admin reviews all customer posts** before they go live
4. **Admin can reply to customer inquiries** directly from the admin panel

## Getting Started

### Step 1: Update Your Database
```bash
cd flask-app
python update_db.py
```

This adds new fields for:
- Customer post tracking
- Admin replies to inquiries

### Step 2: Push Changes to GitHub
```bash
git push origin main
```

### Step 3: Start the Application
```bash
python app.py
```

Visit: http://localhost:5001

## How to Use

### For Customers (Public Users):

1. **Go to the Blog page** (`/blog`)
2. **Click "Submit Your Post"** button at the top
3. **Form expands** - fill it out:
   - Choose language (EN or PL)
   - Enter title
   - Write content (minimum 50 characters)
   - Optionally add category, name, email
4. **Click Submit**
5. **See confirmation** - "Your post is awaiting approval"

### For Admins:

#### Moderating Customer Posts:
1. **Login** to admin panel (admin/admin123)
2. **Dashboard shows pending posts** with:
   - "Customer" badge
   - Language indicator (EN/PL)
   - Customer name (if provided)
3. **Choose action:**
   - **Approve** → Publishes immediately
   - **Edit** → Modify before publishing
   - **Reject** → Removes from queue

#### Replying to Inquiries:
1. **Go to Admin → Inquiries**
2. **Click on an inquiry** to expand it
3. **Type your reply** in the text area
4. **Click "Send Reply"**
5. **Status changes** to "replied"

## Key Features

### ✅ Customer Submission
- Single language (no translation needed)
- Embedded on blog page (no navigation)
- Optional contact info
- Pending status (requires approval)

### ✅ Admin Moderation
- Clear customer post identification
- Language tracking
- Quick approve/edit/reject
- Full content control

### ✅ Customer Communication
- Reply to inquiries
- Track reply status
- Maintain conversation history

## File Structure

```
flask-app/
├── forms.py                    # Updated: Single language form
├── models.py                   # Updated: Customer tracking fields
├── customer_blog.py            # Updated: Single language logic
├── routes.py                   # Updated: Form integrated in blog route
├── admin.py                    # Updated: Reply functionality
├── templates/
│   ├── blog.html              # Updated: Embedded submission form
│   └── admin/
│       ├── dashboard.html     # Updated: Customer post indicators
│       └── inquiries.html     # Updated: Reply interface
├── update_db.py               # NEW: Database migration
├── CUSTOMER_BLOG_CHANGES.md   # NEW: Detailed documentation
├── IMPLEMENTATION_SUMMARY.md  # NEW: Technical overview
└── QUICK_START.md            # NEW: This file
```

## Testing Checklist

- [ ] Run `python update_db.py` successfully
- [ ] Start application without errors
- [ ] Visit `/blog` and see "Submit Your Post" button
- [ ] Click button and form expands
- [ ] Submit a test post in English
- [ ] Submit a test post in Polish
- [ ] Login to admin panel
- [ ] See pending posts on dashboard
- [ ] Approve a post
- [ ] Edit a post
- [ ] Reject a post
- [ ] Submit a contact inquiry
- [ ] Reply to inquiry from admin panel

## Troubleshooting

### Form not showing?
- Check that you're on the `/blog` page
- Verify Bootstrap JS is loaded
- Check browser console for errors

### Database errors?
- Run `python update_db.py` again
- Check file permissions on `instance/website.db`
- Verify SQLAlchemy connection

### Pending posts not visible?
- Check post status is 'pending'
- Verify `is_customer_post` flag is True
- Login to admin panel

### Can't reply to inquiries?
- Verify database migration ran
- Check `admin_reply` field exists
- Ensure you're logged in as admin

## Need More Help?

📖 **Detailed Documentation:**
- `CUSTOMER_BLOG_CHANGES.md` - Complete feature documentation
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- `TROUBLESHOOTING.md` - Common issues and solutions

🔧 **Support:**
- Check application logs for errors
- Verify database schema: `sqlite3 instance/website.db ".schema"`
- Review git commit history for changes

## Summary

✅ **Customer blog submission** is now easier and integrated
✅ **Admin has full control** over what gets published
✅ **Single language submission** simplifies the process
✅ **Direct customer communication** through inquiry replies

All changes are committed and ready to push to GitHub!