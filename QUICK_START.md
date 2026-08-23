# 🚀 Quick Start Guide - Resume Upload Module

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (1 min)
```bash
cd c:\Users\saida\Downloads\RACGS
pip install -r requirements.txt
```

### Step 2: Run Flask App (1 min)
```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Step 3: Open in Browser (1 min)
Visit: **http://127.0.0.1:5000/**

### Step 4: Register & Login (1 min)
1. Click "Register"
2. Enter any email (e.g., `test@example.com`)
3. Click "Register"
4. Login with same email

### Step 5: Complete Profile (1 min)
1. Enter Name: "John Doe"
2. Enter Phone: "555-1234"
3. Enter Job Role: "Software Engineer"
4. Click "Complete Profile"

---

## ✅ Test Resume Upload

### On Dashboard:

1. **Find the Upload Section**
   - Look for "📄 Upload Your Resume" at the top

2. **Select a PDF or DOCX File**
   - Click the file input
   - Or drag-and-drop a file

3. **Watch for File Name**
   - Selected filename appears below input
   - Upload button becomes enabled

4. **Click Upload Button**
   - Button shows "Processing..." with spinner
   - Takes 1-3 seconds to extract text

5. **See Results!**
   - Success message appears
   - Extracted text displays in preview box
   - Form clears automatically after 2 seconds

---

## 📁 File Organization

```
RACGS/
├── app.py                    ← Backend with upload endpoint
├── requirements.txt          ← Dependencies to install
├── templates/
│   └── dashboard.html        ← Upload form here
├── static/
│   └── script.js             ← Upload JavaScript
└── uploads/                  ← Saved resume files go here
```

---

## 🧪 Test with Sample Files

### Using a Test PDF:
```bash
# Create simple test PDF with Python
python -c "
from reportlab.pdfgen import canvas
c = canvas.Canvas('test_resume.pdf')
c.drawString(100, 750, 'John Doe')
c.drawString(100, 730, 'Software Engineer')
c.drawString(100, 710, 'Skills: Python, Flask, JavaScript')
c.save()
"
```

### Using a Test DOCX:
```bash
# Create simple test DOCX with Python
python -c "
from docx import Document
doc = Document()
doc.add_paragraph('John Doe')
doc.add_paragraph('Software Engineer')
doc.add_paragraph('Skills: Python, Flask, JavaScript')
doc.save('test_resume.docx')
"
```

---

## 📊 What Gets Saved

### File Location:
```
uploads/test_example_com_resume.pdf
```

### User Profile:
```python
users['test@example.com'] = {
    'name': 'John Doe',
    'phone': '555-1234',
    'job_role': 'Software Engineer',
    'resume': 'test_example_com_resume.pdf',
    'resume_text': 'John Doe\nSoftware Engineer\n...'
}
```

---

## 🎯 Key Features to Try

### 1. File Type Validation
```
Try uploading: .txt file
Result: "Only PDF and DOCX files are allowed"
```

### 2. File Size Check
```
Try uploading: File > 10MB
Result: "File size must be less than 10MB"
```

### 3. Drag & Drop
```
Drag a PDF directly onto the file input
Result: File automatically selected
```

### 4. Clear Form
```
Click "Clear Selection" button
Result: Form resets completely
```

---

## 🔧 Customization (Optional)

### Change Upload Button Color
**File:** `templates/dashboard.html`
```css
.upload-btn {
    background-color: #28a745;  /* Green */
}
```

### Change Max File Size
**File:** `app.py` (line 21)
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

### Change Upload Folder
**File:** `app.py` (line 15)
```python
UPLOAD_FOLDER = 'my_resumes'  # New folder name
```

---

## ❌ Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError: PyPDF2 | Run `pip install PyPDF2` |
| ModuleNotFoundError: docx | Run `pip install python-docx` |
| Port 5000 already in use | Run `python app.py --port 5001` |
| Upload button disabled | Select a file first |
| "User not logged in" | Login or register first |
| Empty extracted text | PDF might be scanned image |

---

## 📱 Browser Compatibility

✅ Chrome/Edge - Fully supported
✅ Firefox - Fully supported
✅ Safari - Fully supported
✅ Mobile browsers - Responsive design

---

## 🎓 Code Locations

### If you need to modify:

| What | Where | What to Change |
|------|-------|-----------------|
| Upload button appearance | `dashboard.html` (CSS) | `.upload-btn` class |
| Upload endpoint | `app.py` | `/upload_resume` function |
| Text extraction | `app.py` | `extract_text_from_*()` functions |
| File validation | `app.py` | `allowed_file()` function |
| Form behavior | `static/script.js` | `uploadResume()` function |
| Error messages | `static/script.js` or `app.py` | Error strings |

---

## ✨ What Happens Behind the Scenes

```
1. User selects file
   ↓
2. JavaScript validates file type & size
   ↓
3. User clicks "Upload & Extract Text"
   ↓
4. JavaScript sends FormData to /upload_resume
   ↓
5. Flask receives POST request
   ↓
6. Server validates user session & file
   ↓
7. File saved to uploads/ folder
   ↓
8. Text extraction:
   - If PDF: PyPDF2 reads all pages
   - If DOCX: python-docx reads paragraphs
   ↓
9. Server returns JSON response
   ↓
10. JavaScript displays extracted text
    ↓
11. User sees results!
```

---

## 🎉 You're All Set!

Next steps:
1. Install dependencies: `pip install -r requirements.txt`
2. Run app: `python app.py`
3. Visit: http://127.0.0.1:5000/
4. Register & test upload

---

## 📞 Need Help?

1. **Check requirements installed:**
   ```bash
   pip list | grep -E 'Flask|PyPDF2|docx'
   ```

2. **Check Flask runs:**
   ```bash
   python app.py
   ```

3. **Check files exist:**
   ```bash
   dir c:\Users\saida\Downloads\RACGS\static\script.js
   dir c:\Users\saida\Downloads\RACGS\templates\dashboard.html
   ```

4. **View Flask console logs:**
   - Check output when starting Flask
   - Upload file and watch for errors

---

**Happy testing!** 🚀
