# 🗄️ Database Setup & Migration Guide

## Overview

Your Flask application has been upgraded to use **SQLite** for persistent data storage. All user data, profile information, and resumes are now saved to a database file instead of being lost on restart.

---

## 📋 What Changed

### Old System (In-Memory)
- ❌ Data stored in Python dictionary
- ❌ All data lost when app restarts
- ❌ Passwords not encrypted
- ❌ No resume history tracking

### New System (SQLite Database)
- ✅ Persistent SQLite database (file-based)
- ✅ All data saved permanently
- ✅ Passwords hashed with werkzeug security
- ✅ Multiple resume tracking per user
- ✅ Timestamp tracking for each upload
- ✅ Easy to backup and migrate

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install New Dependencies

```bash
cd c:\Users\saida\Downloads\RACGS
pip install -r requirements.txt
```

This will install:
- `Flask` - Web framework
- `Flask-SQLAlchemy` - Database ORM (NEW!)
- `PyPDF2` - PDF text extraction
- `python-docx` - DOCX text extraction
- `Werkzeug` - Security utilities

**Expected output:**
```
Successfully installed Flask-SQLAlchemy
```

### Step 2: Run the App (Database Auto-Initializes)

```bash
python app.py
```

**Expected output:**
```
✅ Database initialized successfully!
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

The database will automatically create:
- `app.db` file in your project folder
- `users` table
- `resumes` table

### Step 3: Register a New Account

1. Go to: http://127.0.0.1:5000/
2. Click "Register"
3. Enter email: `test@example.com`
4. Enter password: `password123` (at least 6 characters)
5. Confirm password: `password123`
6. Click "Register"

### Step 4: Login and Upload Resume

1. Click "Login"
2. Enter same email and password
3. Complete your profile
4. Go to "My Resumes"
5. Upload a PDF or DOCX file
6. ✅ Resume is now saved in database!

### Step 5: Verify Data is Persistent

1. Refresh the page (F5)
2. Resume list still shows! ✅
3. Upload another resume
4. Close the app (Ctrl+C)
5. Run `python app.py` again
6. Login and go to "My Resumes"
7. Both resumes still there! ✅

---

## 📁 Database File Location

```
c:\Users\saida\Downloads\RACGS\app.db
```

**This file contains:**
- User account information (email, hashed password, name, phone, job role)
- Resume upload history
- Extracted resume text
- Upload timestamps
- File sizes

**⚠️ Important:** Do NOT delete `app.db` unless you want to lose all data!

---

## 🔐 Password Security

Passwords are now **hashed** for security:

```python
# Registration
new_user = User(email=email)
new_user.set_password(password)  # Automatically hashed!
db.session.add(new_user)
db.session.commit()

# Login
user = User.query.filter_by(email=email).first()
if user and user.check_password(password):  # Safe comparison
    # Login successful
```

**What this means:**
- Raw passwords are NEVER stored
- Even if database is compromised, passwords are protected
- Uses `werkzeug.security.generate_password_hash()`

---

## 📚 Database Schema

### Users Table

```
CREATE TABLE users (
    id              INTEGER PRIMARY KEY,
    email           VARCHAR(120) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    name            VARCHAR(120),
    phone           VARCHAR(20),
    job_role        VARCHAR(120),
    profile_photo   VARCHAR(255),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Resumes Table

```
CREATE TABLE resumes (
    id                  INTEGER PRIMARY KEY,
    user_id             INTEGER FOREIGN KEY REFERENCES users(id),
    file_name           VARCHAR(255) NOT NULL,
    original_file_name  VARCHAR(255),
    extracted_text      TEXT NOT NULL,
    file_size           INTEGER,
    upload_date         DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Key Points:**
- `user_id` links resumes to users (one user can have many resumes)
- `original_file_name` is what user uploaded (e.g., "my_resume.pdf")
- `file_name` is secure server filename (e.g., "user_1_resume_12345.pdf")
- `extracted_text` stores the full resume content from PDF/DOCX

---

## 📝 Code Changes Summary

### app.py Changes

**Before:**
```python
users = {}  # In-memory dictionary
session['email'] = email  # Just store email
```

**After:**
```python
db = SQLAlchemy(app)  # Database connection

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    resumes = db.relationship('Resume', backref='user', lazy=True)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    extracted_text = db.Column(db.Text, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

session['user_id'] = user.id  # Store user ID instead
```

### Authentication Changes

**Before:**
```python
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    if email not in users:  # Check dictionary
        flash('Not registered')
    session['email'] = email
```

**After:**
```python
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email'].lower()
    password = request.form['password']
    
    user = User.query.filter_by(email=email).first()  # Query database
    
    if user and user.check_password(password):  # Verify hashed password
        session['user_id'] = user.id
        session['email'] = user.email
```

### Resume Storage

**Before:**
```python
users[email]['resume'] = filename  # Lost on restart!
users[email]['resume_text'] = extracted_text
```

**After:**
```python
resume = Resume(
    user_id=user.id,
    file_name=resume_filename,
    extracted_text=extracted_text,
    file_size=file_size,
    upload_date=datetime.utcnow()
)
db.session.add(resume)
db.session.commit()  # Saved to database!
```

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError: No module named 'flask_sqlalchemy'

**Solution:**
```bash
pip install Flask-SQLAlchemy
```

---

### Issue: "database is locked" error

**Cause:** Multiple instances of the app trying to access database at once

**Solution:**
```bash
# Close all instances of the app
# Python process might still be running
# Check Task Manager and kill python.exe if needed
```

---

### Issue: Database file is corrupt or won't open

**Solution:** Delete and recreate:
```bash
# CAREFUL: This will DELETE all data!
del app.db

# Then restart the app
python app.py
```

---

### Issue: Can't login after upgrade

**Cause:** Old user accounts from in-memory system don't exist in database

**Solution:** Register new account (email/password required now)

---

### Issue: Want to backup database

**Solution:**
```bash
# Simply copy the file
copy c:\Users\saida\Downloads\RACGS\app.db c:\Users\saida\Downloads\RACGS\app_backup.db
```

---

## 🔄 Migrating from Old System (If Needed)

### Option 1: Start Fresh (Recommended)

```bash
# Just delete app.db and register new accounts
del app.db
python app.py
# Then register accounts and upload resumes
```

### Option 2: Manual Migration

If you need to preserve old data from dictionary, you'd need to:
1. Export data from old system
2. Create Python script to import into database
3. Run migration script

(This is beyond the scope of this guide - contact support if needed)

---

## 📊 Verifying Database Works

### Method 1: Using Python

```bash
# Start Python interactive shell
python

# Then in Python:
from app import app, db, User, Resume

with app.app_context():
    # Count users
    user_count = User.query.count()
    print(f"Users: {user_count}")
    
    # List all users
    users = User.query.all()
    for user in users:
        print(f"  - {user.email}")
    
    # Count resumes
    resume_count = Resume.query.count()
    print(f"Resumes: {resume_count}")

# Exit
exit()
```

### Method 2: Using SQLite Browser (GUI)

1. Download: https://sqlitebrowser.org/
2. Open `app.db`
3. View tables and data in GUI
4. Makes it easy to inspect database

---

## 🎯 Key Differences for Users

### Before Database
- Login page only has email field
- Data disappears on app restart
- Same email can register multiple times
- No password security
- Can only see current session's resume

### After Database
- Login page has email AND password
- Data persists permanently
- Each email can only register once
- Passwords hashed and encrypted
- Can see all your uploaded resumes
- Can view/delete individual resumes
- Access resume history anytime

---

## 🚀 Next Steps

1. ✅ Install dependencies (`pip install -r requirements.txt`)
2. ✅ Run app (`python app.py`)
3. ✅ Database auto-initializes (`✅ Database initialized successfully!`)
4. ✅ Test by registering and uploading resumes
5. ✅ Verify data persists after refresh/restart

---

## 📞 Quick Reference

| Task | How To |
|------|--------|
| Start app | `python app.py` |
| Access app | http://127.0.0.1:5000/ |
| Database file | `app.db` in project folder |
| View data | Use SQLite Browser on `app.db` |
| Backup data | Copy `app.db` file |
| Delete all data | Delete `app.db`, restart app |
| Install dependencies | `pip install -r requirements.txt` |
| Check database | `python -c "from app import db, User; print(db.inspect(User))"` |

---

## ✨ Summary

Your application now uses SQLite for **permanent, secure data storage**. All resumes and user data are saved to `app.db` and will persist even after closing the application.

**Key improvements:**
- 🔐 Secure password hashing
- 💾 Persistent data storage
- 📋 Multiple resume tracking
- 📅 Timestamp tracking
- 🔗 User-resume relationships
- ⚡ Fast database queries

**Ready to use!** Register an account and start uploading resumes. 🚀
