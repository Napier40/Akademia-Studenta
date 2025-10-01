# Admin Panel Access Guide

## 🎯 How to Access the Admin Panel

### Method 1: Direct URL
Simply navigate to:
```
http://localhost:5001/admin/login
```

### Method 2: Navigation Menu Icon
Look for the **person icon** (👤) in the top navigation bar:
- Click the person icon
- You'll be redirected to the admin login page

### Method 3: After Login
Once logged in as admin, you'll see:
- **"Admin"** link with a shield icon (🛡️) in the navigation bar
- Click it to go directly to the admin dashboard

---

## 🔐 Login Credentials

**Default credentials:**
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **IMPORTANT:** Change these in production!

---

## 📍 Navigation Menu Behavior

### When NOT Logged In
- You'll see a **person icon** (👤) in the navigation bar
- Clicking it takes you to `/admin/login`

### When Logged In as Admin
- The person icon changes to **"Admin"** text with a shield icon (🛡️)
- Clicking it takes you to `/admin` (dashboard)
- You can access admin features from any page

---

## 🎨 Admin Panel Features

Once logged in, you can:

### 1. **Dashboard** (`/admin`)
- View statistics (total posts, comments, inquiries)
- See recent blog posts
- Moderate pending comments
- Quick access to all features

### 2. **Blog Posts** (`/admin/posts`)
- View all blog posts
- Create new posts
- Edit existing posts
- Delete posts
- See post statistics (views, status)

### 3. **Create New Post** (`/admin/posts/new`)
- Write bilingual content (English & Polish)
- Add title, excerpt, content
- Set category
- Add featured image URL
- Choose status (Draft/Published/Archived)
- Auto-generated URL slug

### 4. **Comments** (`/admin/comments`)
- View all comments
- Filter by status (All/Pending/Approved/Rejected)
- Approve comments
- Reject comments
- Delete comments

### 5. **Inquiries** (`/admin/inquiries`)
- View contact form submissions
- Filter by status (All/New/In Progress/Resolved)
- Mark inquiries as resolved
- See contact details and messages

---

## 📝 Creating Your First Blog Post

### Step-by-Step Guide

1. **Login to Admin Panel**
   - Click the person icon in navigation
   - Or go to `http://localhost:5001/admin/login`
   - Enter username: `admin`, password: `admin123`

2. **Navigate to Blog Posts**
   - Click "Blog Posts" in the sidebar
   - Or click "New Post" button on dashboard

3. **Click "New Post"**
   - Green button in top right corner

4. **Fill in English Content** (Left Column)
   - **Title (English):** Your post title
   - **Excerpt (English):** Brief summary (optional)
   - **Content (English):** Full post content
   - **Category (English):** e.g., "News", "Guides", "Tips"

5. **Fill in Polish Content** (Right Column)
   - **Title (Polish):** Polish translation
   - **Excerpt (Polish):** Polish summary (optional)
   - **Content (Polish):** Polish content
   - **Category (Polish):** Polish category name

6. **Add Optional Settings**
   - **Featured Image URL:** Link to an image
   - **Status:** Choose "Published" to make it live

7. **Save the Post**
   - Click "Save Post" button
   - You'll be redirected to the posts list

8. **View Your Post**
   - Click "View Website" in admin sidebar
   - Navigate to Blog page
   - Your post should appear!

---

## 💡 Quick Tips

### For Blog Posts
- **Draft First:** Save as "Draft" while writing
- **Use Good Images:** Get free images from:
  - https://unsplash.com
  - https://pexels.com
  - https://pixabay.com
- **Keep Titles Short:** Under 60 characters for SEO
- **Write Excerpts:** They appear in blog listings

### For Comments
- **Check Daily:** Review pending comments regularly
- **Be Fair:** Approve constructive feedback
- **Delete Spam:** Remove obvious spam quickly

### For Inquiries
- **Respond Promptly:** Check new inquiries daily
- **Mark Resolved:** Keep your inbox organized

---

## 🔄 Workflow Example

### Daily Admin Routine

1. **Login** → Click person icon or go to `/admin/login`
2. **Check Dashboard** → See what needs attention
3. **Moderate Comments** → Approve/reject new comments
4. **Review Inquiries** → Read and respond to messages
5. **Create Content** → Write new blog posts
6. **Logout** → Click "Logout" in sidebar

---

## 🎯 Where to Find Things

### Main Navigation (Public Site)
- **Home** → Homepage
- **Services** → Services page
- **Blog** → Blog listing
- **Contact** → Contact form
- **👤 / Admin** → Admin login/dashboard
- **EN/PL** → Language switcher

### Admin Sidebar
- **Dashboard** → Overview and stats
- **Blog Posts** → Manage posts
- **Comments** → Moderate comments
- **Inquiries** → Handle messages
- **View Website** → Open public site
- **Logout** → End session

---

## 🚀 Getting Started Checklist

- [ ] Login to admin panel
- [ ] Explore the dashboard
- [ ] Create your first blog post
- [ ] Publish the post
- [ ] View it on the public blog page
- [ ] Test commenting on your post
- [ ] Moderate the comment in admin panel
- [ ] Check contact form submissions

---

## 🆘 Troubleshooting

### Can't See Admin Link
- **Not logged in:** You'll see a person icon instead
- **Click the icon:** It will take you to login page
- **After login:** The icon changes to "Admin" text

### Can't Login
- Check username: `admin`
- Check password: `admin123`
- Clear browser cookies
- Try incognito/private mode

### Post Not Showing on Blog
- Check status is "Published" (not Draft)
- Refresh the blog page
- Check the post has content in both languages

### Admin Link Not Working
- Make sure you're logged in
- Check the URL is correct
- Clear browser cache

---

## 📚 Additional Resources

- **ADMIN_GUIDE.md** - Complete admin panel documentation
- **VSCODE_SETUP.md** - Development setup
- **IMPLEMENTATION_SUMMARY.md** - Technical details

---

## ✅ Summary

**To access admin panel:**
1. Click the **person icon** (👤) in navigation
2. Login with `admin` / `admin123`
3. Start managing your content!

**After login:**
- Person icon becomes **"Admin"** link
- Click it anytime to return to dashboard
- Manage posts, comments, and inquiries

---

**Last Updated:** 2025-10-01
**Version:** 1.0
**Status:** Ready to Use