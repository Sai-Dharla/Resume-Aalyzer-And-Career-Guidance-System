# 🔄 Migration Guide: From In-Memory to Database

## Complete Upgrade Instructions

This guide walks you through upgrading your Flask app from in-memory storage to SQLite database.

---

## ⏱️ Estimated Time: 10 Minutes

---

## 📋 What You're Upgrading

| Feature | Before | After |
|---------|--------|-------|
| User storage | Python dictionary | SQLite database |
| Data persistence | ❌ Lost on restart | ✅ Permanent |
| Multiple accounts | ❌ All share same data | ✅ Separate profiles |
| Passwords | ❌ Plain text | ✅ Hashed/encrypted |
| Resume tracking | ❌ One per user | ✅ Multiple per user |
| Resume history | ❌ None | ✅ Upload timestamps |
| Security | ❌ Basic | ✅ Industry standard |

---

## 🚀 Step-by-Step Migration

### STEP 1: Update requirements.txt ✅ DONE

The requirements have been updated to include:
```
Flask-SQLAlchemy
```

**Verify in file:** `c:\Users\saida\Downloads\RACGS\requirements.txt`

---

### STEP 2: Update app.py ✅ DONE

**Changes made:**
1. Added SQLAlchemy imports
2. Created `User` model with hashed passwords
3. Created `Resume` model with relationships
4. Updated all routes to use database queries
5. Updated authentication to verify passwords
6. Updated upload to store in database
7. Added resume viewing and deletion
8. Added error handlers

**Files modified:**
- `app.py` - Complete rewrite of auth and storage logic

---

### STEP 3: Update Login/Register Pages ✅ DONE

**register.html changes:**
- Added password field
- Added confirm password field
- Password validation (min 6 characters)

**login.html changes:**
- Added password field

**Files modified:**
- `templates/register.html`
- `templates/login.html`

---

### STEP 4: Update My Resumes Page ✅ DONE

**my_resumes.html changes:**
- Added resume list from database
- Shows upload date and file size
- View button for each resume
- Delete button for each resume
- Empty state when no resumes
- Resume count badge

**Files modified:**
- `templates/my_resumes.html`

---

### STEP 5: Create Resume Detail Page ✅ DONE

**resume_detail.html (NEW):**
- View full extracted text of a resume
- Shows resume metadata (date, size, etc.)
- Delete option
- Full-text display with formatting preserved

**Files created:**
- `templates/resume_detail.html`

---

## 📥 Installation Instructions

### 1. Install New Dependencies

```bash
# Navigate to project folder
cd c:\Users\saida\Downloads\RACGS

# Install updated requirements
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-SQLAlchemy-X.X.X
```

---

### 2. Initialize Database

```bash
# Simply run the app - it auto-initializes!
python app.py
```

**Expected output:**
```
✅ Database initialized successfully!
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

This creates:
- `app.db` - SQLite database file
- `users` table - Stores user accounts
- `resumes` table - Stores uploaded resumes

---

### 3. Verify Installation

Open your browser to:
```
http://127.0.0.1:5000/
```

You should see the login page. ✅

---

## 🧪 Testing the Upgrade

### Test 1: Register with Password

1. Click "Register"
2. Enter:
   - Email: `test@example.com`
   - Password: `password123`
   - Confirm: `password123`
3. Click "Register"
4. ✅ Should see success message

### Test 2: Password Validation

1. Try registering with:
   - Password: `123` (too short)
2. ✅ Should see error "min 6 characters"

### Test 3: Login

1. Click "Login"
2. Enter email and password from Test 1
3. ✅ Should login successfully

### Test 4: Upload Resume

1. Go to "My Resumes"
2. Upload a PDF or DOCX file
3. ✅ See extracted text
4. ✅ Resume appears in list

### Test 5: Data Persistence

1. Refresh page (F5)
2. ✅ Resume still in list
3. Close app (Ctrl+C)
4. Run `python app.py` again
5. Login
6. Go to "My Resumes"
7. ✅ Resume still there!

### Test 6: Multiple Resumes

1. Upload second resume
2. ✅ Both appear in list
3. Click "View" on each
4. ✅ Can see each resume's text

### Test 7: Delete Resume

1. Click "Delete" on a resume
2. Confirm deletion
3. ✅ Resume removed from list

---

## 🔑 Key Changes for Users

### Old Workflow
```
1. Visit app
2. Register with email only
3. Upload resume
4. Close app
5. ❌ All data gone
```

### New Workflow
```
1. Visit app
2. Register with email + password
3. Login with email + password
4. Upload resume (can upload multiple!)
5. Close app
6. ✅ Login again, all resumes still there
7. Can view/delete any resume anytime
```

---

## ⚙️ Configuration Settings

### Database Location

Change in `app.py` line ~24:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "app.db")}'
```

To use different location:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/path/to/my_database.db'
```

### Password Requirements

Change in `app.py` register route (~61):
```python
if len(password) < 6:  # Change 6 to desired minimum
```

### Max File Size

Change in `app.py` line ~32:
```python
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
```

To 50MB:
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

---

## 🔒 Security Improvements

### Password Hashing

User passwords are hashed using `werkzeug.security`:

```python
def set_password(self, password):
    """Hash and store password - NEVER stores plain password"""
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    """Verify password without storing it"""
    return check_password_hash(self.password_hash, password)
```

### Email Uniqueness

Only one account per email - prevents multiple registrations:
```python
email = db.Column(db.String(120), unique=True, nullable=False)
```

### User Isolation

Users can only see their own resumes:
```python
@app.route('/resume/<int:resume_id>')
def view_resume(resume_id):
    resume = Resume.query.get(resume_id)
    
    # Check ownership
    if resume.user_id != session['user_id']:
        return "Access denied"
```

---

## 📊 Database Inspection

### View Database Contents (Python)

```bash
python

# In Python:
from app import app, db, User, Resume

with app.app_context():
    # List all users
    users = User.query.all()
    for u in users:
        print(f"User: {u.email} - Resumes: {len(u.resumes)}")
    
    # List all resumes
    resumes = Resume.query.all()
    for r in resumes:
        print(f"Resume: {r.original_file_name} - User ID: {r.user_id}")

exit()
```

### View Database (SQLite Browser)

1. Download: https://sqlitebrowser.org/
2. Open `app.db` file
3. Browse tables and data
4. View all records

---

## 🆘 Common Issues & Solutions

### Issue: "ModuleNotFoundError: flask_sqlalchemy"
```bash
pip install Flask-SQLAlchemy
```

### Issue: Database locked
- Close all app instances
- Kill any lingering python.exe processes
- Restart app

### Issue: Can't login after upgrade
- Old accounts don't exist in database
- Register new account instead

### Issue: Want to delete all data
```bash
# WARNING: Permanent deletion!
del app.db

# App will create new database on restart
python app.py
```

### Issue: Want to move database
```python
# Change in app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new/path/app.db'
```

---

## 📁 File Structure After Upgrade

```
RACGS/
├── app.py                          ← Updated with SQLAlchemy
├── app.db                          ← NEW: SQLite database file
├── requirements.txt                ← Updated with Flask-SQLAlchemy
├── DATABASE_SETUP.md               ← NEW: Setup guide
├── MIGRATION_GUIDE.md              ← This file
├── templates/
│   ├── register.html               ← Updated: Added password fields
│   ├── login.html                  ← Updated: Added password field
│   ├── my_resumes.html             ← Updated: Shows resume list
│   ├── resume_detail.html          ← NEW: View individual resume
│   ├── dashboard.html
│   ├── profile.html
│   └── setup_profile.html
├── static/
│   ├── style.css
│   ├── script.js
│   └── uploads/
└── uploads/                        ← Resume files stored here
```

---

## 🚨 Important Notes

### ⚠️ Data Backup
```bash
# Before making changes, backup your current state
# (If you were using old system)
# Copy entire project folder as backup:
copy c:\Users\saida\Downloads\RACGS c:\Users\saida\Downloads\RACGS_backup
```

### ⚠️ Database File
```
DO NOT:
- Delete app.db (unless you want to lose data)
- Share app.db over untrusted networks
- Edit app.db manually with text editor

DO:
- Backup app.db regularly
- Keep app.db in same folder as app.py
- Let the app manage database
```

### ✅ Production Checklist

- [ ] Changed secret key in app.py (line ~21)
- [ ] Set debug=False for production
- [ ] Backed up app.db
- [ ] Tested all features
- [ ] Verified resumes persist
- [ ] Tested password hashing

---

## 📞 Quick Troubleshooting

**App won't start?**
```bash
# Check for syntax errors
python -m py_compile app.py

# Check dependencies
pip list | grep -i flask
```

**Database corrupted?**
```bash
# Delete and recreate
del app.db
python app.py  # Creates new database
```

**Want to check data?**
```bash
# Download SQLite Browser and open app.db
# Or use Python shell (see above)
```

---

## ✨ Summary

You've successfully upgraded from in-memory storage to a robust SQLite database system with:

✅ Persistent data storage
✅ Secure password hashing
✅ Multiple resume support
✅ User account isolation
✅ Timestamp tracking
✅ Easy data management

**Start using it** with `python app.py` and register an account! 🚀

---

## 📚 Additional Resources

- [Flask-SQLAlchemy Docs](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/security/)

Happy coding! 💻
