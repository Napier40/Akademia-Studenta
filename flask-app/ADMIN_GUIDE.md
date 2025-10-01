# Admin Panel Guide

## 🎯 Overview

The admin panel allows you to manage blog posts, comments, and contact inquiries through a user-friendly web interface.

---

## 🔐 Accessing the Admin Panel

### Login URL
```
http://localhost:5001/admin/login
```

### Default Credentials
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **IMPORTANT:** Change these credentials in production!

---

## 📝 Managing Blog Posts

### Creating a New Post

1. **Navigate to Admin Panel**
   - Go to `/admin/login` and login
   - Click "Blog Posts" in the sidebar
   - Click "New Post" button

2. **Fill in the Form**
   
   **English Content:**
   - Title (English) - Required, 5-200 characters
   - Excerpt (English) - Optional, brief summary
   - Content (English) - Required, minimum 50 characters
   - Category (English) - Optional

   **Polish Content:**
   - Title (Polish) - Required, 5-200 characters
   - Excerpt (Polish) - Optional, brief summary
   - Content (Polish) - Required, minimum 50 characters
   - Category (Polish) - Optional

   **Additional Settings:**
   - Featured Image URL - Optional, link to an image
   - Status - Choose from:
     * **Draft** - Not visible to public
     * **Published** - Visible to everyone
     * **Archived** - Hidden but not deleted

3. **Save the Post**
   - Click "Save Post" button
   - The slug (URL) is automatically generated from the English title

### Editing a Post

1. Go to "Blog Posts" in admin panel
2. Click the pencil icon (✏️) next to the post
3. Make your changes
4. Click "Save Post"

### Deleting a Post

1. Go to "Blog Posts" in admin panel
2. Click the trash icon (🗑️) next to the post
3. Confirm deletion in the modal

---

## 💬 Managing Comments

### Viewing Comments

1. Click "Comments" in the sidebar
2. Filter by status:
   - **All** - Show all comments
   - **Pending** - Awaiting moderation
   - **Approved** - Visible on website
   - **Rejected** - Hidden from website

### Moderating Comments

**Approve a Comment:**
- Click the green checkmark (✓) button
- Comment becomes visible on the website

**Reject a Comment:**
- Click the yellow X button
- Comment is hidden from the website

**Delete a Comment:**
- Click the red trash icon (🗑️)
- Comment is permanently deleted

---

## 📧 Managing Contact Inquiries

### Viewing Inquiries

1. Click "Inquiries" in the sidebar
2. Filter by status:
   - **New** - Unread inquiries
   - **In Progress** - Being handled
   - **Resolved** - Completed

### Marking as Resolved

1. Find the inquiry in the list
2. Click the green checkmark button
3. Status changes to "Resolved"

---

## 📊 Dashboard

The dashboard shows:
- **Total Posts** - All blog posts
- **Published Posts** - Live posts
- **Pending Comments** - Comments awaiting moderation
- **New Inquiries** - Unread contact messages

### Quick Actions
- View recent posts
- Moderate pending comments directly
- Quick links to create new content

---

## 🎨 Admin Panel Features

### Navigation
- **Dashboard** - Overview and statistics
- **Blog Posts** - Manage all posts
- **Comments** - Moderate comments
- **Inquiries** - Handle contact messages
- **View Website** - Opens main site in new tab
- **Logout** - End admin session

### Security
- Session-based authentication
- CSRF protection on all forms
- Admin-only access to management pages

---

## 💡 Tips & Best Practices

### Writing Blog Posts

1. **Use Clear Titles**
   - Make titles descriptive and engaging
   - Keep them under 60 characters for SEO

2. **Write Good Excerpts**
   - Summarize the post in 1-2 sentences
   - This appears in blog listings

3. **Add Categories**
   - Use consistent category names
   - Examples: "News", "Guides", "Tips"

4. **Use Featured Images**
   - Add relevant images from free sources:
     * Unsplash.com
     * Pexels.com
     * Pixabay.com

5. **Draft First, Publish Later**
   - Save as "Draft" while writing
   - Review and edit before publishing
   - Change to "Published" when ready

### Managing Comments

1. **Review Regularly**
   - Check pending comments daily
   - Respond to questions when possible

2. **Moderate Fairly**
   - Approve constructive comments
   - Reject spam or offensive content

3. **Engage with Users**
   - Anonymous comments are allowed
   - Encourage discussion

### Handling Inquiries

1. **Respond Promptly**
   - Check new inquiries daily
   - Reply via email

2. **Track Status**
   - Mark as "Resolved" when done
   - Keep records organized

---

## 🔧 Technical Details

### File Structure
```
flask-app/
├── admin.py                    # Admin routes and logic
├── forms.py                    # BlogPostForm definition
├── templates/admin/
│   ├── base.html              # Admin layout
│   ├── login.html             # Login page
│   ├── dashboard.html         # Dashboard
│   ├── posts.html             # Post listing
│   ├── post_form.html         # Create/edit post
│   ├── comments.html          # Comment management
│   └── inquiries.html         # Inquiry management
```

### Routes
- `/admin/login` - Admin login
- `/admin` - Dashboard
- `/admin/posts` - List posts
- `/admin/posts/new` - Create post
- `/admin/posts/<id>/edit` - Edit post
- `/admin/posts/<id>/delete` - Delete post
- `/admin/comments` - Manage comments
- `/admin/inquiries` - Manage inquiries
- `/admin/logout` - Logout

### Authentication
- Simple session-based auth
- Decorator: `@admin_required`
- Session key: `is_admin`

---

## 🚀 Quick Start Workflow

### Daily Routine

1. **Login to Admin Panel**
   ```
   http://localhost:5001/admin/login
   ```

2. **Check Dashboard**
   - Review statistics
   - Check pending items

3. **Moderate Comments**
   - Approve/reject new comments
   - Delete spam

4. **Handle Inquiries**
   - Read new messages
   - Mark as resolved when done

5. **Create Content**
   - Write new blog posts
   - Publish when ready

---

## 🔒 Security Recommendations

### For Production

1. **Change Default Password**
   - Edit `admin.py`
   - Use strong password
   - Consider environment variables

2. **Use HTTPS**
   - Enable SSL certificate
   - Redirect HTTP to HTTPS

3. **Implement Proper Auth**
   - Use Flask-Login
   - Add password hashing
   - Implement user roles

4. **Add Rate Limiting**
   - Prevent brute force attacks
   - Use Flask-Limiter

5. **Enable Logging**
   - Track admin actions
   - Monitor for suspicious activity

---

## 🆘 Troubleshooting

### Can't Login
- Check username and password
- Clear browser cookies
- Check browser console for errors

### Posts Not Showing
- Verify status is "Published"
- Check published_at date
- Refresh the main website

### Comments Not Appearing
- Check comment status (must be "Approved")
- Verify post exists
- Check database connection

### Images Not Loading
- Verify image URL is correct
- Check image is publicly accessible
- Try different image source

---

## 📚 Additional Resources

### Markdown Formatting
Blog posts support basic HTML and line breaks:
- Use `\n\n` for paragraphs
- Use `**bold**` for emphasis
- Use lists with `-` or `*`

### Image Sources
Free image websites:
- https://unsplash.com
- https://pexels.com
- https://pixabay.com
- https://placeholder.com (for testing)

---

## ✅ Checklist for New Posts

Before publishing a post:
- [ ] English title is clear and descriptive
- [ ] Polish title is translated correctly
- [ ] Both content versions are complete
- [ ] Excerpts are written (optional but recommended)
- [ ] Category is set
- [ ] Featured image is added (optional)
- [ ] Content is proofread
- [ ] Status is set to "Published"
- [ ] Preview on website looks good

---

**Last Updated:** 2025-10-01
**Version:** 1.0
**Status:** Production Ready