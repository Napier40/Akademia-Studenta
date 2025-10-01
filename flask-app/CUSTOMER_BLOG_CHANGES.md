# Customer Blog Submission Changes

## Overview
The blog submission system has been redesigned to allow customers to submit posts directly from the blog page in a single language (English OR Polish), not bilingual.

## Key Changes

### 1. Blog Page Integration
- **Collapsible submission form** added directly to the blog page
- Click "Submit Your Post" button to reveal the form
- No separate page needed - everything happens on `/blog`

### 2. Single Language Submission
- Customers choose ONE language: English OR Polish
- No need to provide translations
- Admin can add translations later if needed

### 3. Form Fields
**Required:**
- Language selection (EN/PL)
- Title
- Content (minimum 50 characters)

**Optional:**
- Category
- Author name
- Author email

### 4. Submission Flow
1. Customer fills form on blog page
2. Post submitted with status: `pending`
3. Admin sees post on dashboard with:
   - "Customer" badge
   - Language indicator (EN/PL)
   - Customer name (if provided)
4. Admin can:
   - **Approve** - Publishes immediately
   - **Edit** - Modify before publishing
   - **Reject** - Removes from pending

### 5. Admin Dashboard Improvements
- Pending customer posts clearly marked
- Shows submission language
- Shows customer name if provided
- Quick approve/edit/reject actions

### 6. Customer Inquiry Replies
- Admin can now reply directly to customer inquiries
- Reply form integrated into inquiry view
- Track reply status and timestamp
- New status: "replied"

## Database Changes

### BlogPost Model - New Fields:
- `is_customer_post` - Boolean flag for customer submissions
- `customer_language` - Language submitted in ('en' or 'pl')
- `customer_name` - Optional customer name
- `customer_email` - Optional customer email

### ContactInquiry Model - New Fields:
- `admin_reply` - Admin's reply text
- `replied_at` - Timestamp of reply

## Migration Instructions

1. **Update database schema:**
   ```bash
   cd flask-app
   python update_db.py
   ```

2. **Restart the application:**
   ```bash
   python app.py
   ```

3. **Test the new features:**
   - Visit `/blog` and click "Submit Your Post"
   - Fill the form in one language
   - Login to admin panel
   - Check pending posts on dashboard
   - Try replying to inquiries

## Admin Workflow

### Moderating Customer Posts:
1. Login to admin panel
2. Dashboard shows pending customer posts
3. For each post you can:
   - **Approve**: Publishes immediately as-is
   - **Edit**: Modify content, add translation, then publish
   - **Reject**: Removes from pending queue

### Replying to Customers:
1. Go to Admin → Inquiries
2. Click on an inquiry to expand
3. Type your reply in the text area
4. Click "Send Reply"
5. Status automatically changes to "replied"

## Technical Details

### Customer Post Storage:
- If submitted in English:
  - `title_en`, `content_en`, `category_en` = customer input
  - `title_pl`, `content_pl`, `category_pl` = empty (admin can fill later)
  
- If submitted in Polish:
  - `title_pl`, `content_pl`, `category_pl` = customer input
  - `title_en`, `content_en`, `category_en` = empty (admin can fill later)

### Status Values:
- `pending` - Awaiting admin review
- `published` - Live on website
- `draft` - Admin-created draft
- `archived` - Removed from public view

## Benefits

1. **Easier for customers** - No translation required
2. **Better moderation** - Admin reviews before publishing
3. **Flexible workflow** - Edit or approve as-is
4. **Clear tracking** - Know which posts are customer submissions
5. **Direct communication** - Reply to inquiries from admin panel

## Notes

- Customer posts are NOT visible until approved
- Admin can edit customer posts before publishing
- Language indicator helps admin know which translation is needed
- Customer contact info is optional but helpful for follow-up