# Resume Upload & Text Extraction Module - Setup Guide

## ✅ Implementation Complete!

This document guides you through the resume upload and text extraction feature for the AI Resume Analyzer and Career Guidance System.

---

## 📂 File Structure

Your project now has the following structure:

```
RACGS/
├── app.py                          # Flask backend with upload endpoint
├── requirements.txt                # Python dependencies
├── static/
│   ├── style.css                   # Existing styles
│   ├── uploads/                    # Profile photos folder
│   └── script.js                   # NEW: JavaScript for upload handling
├── templates/
│   ├── dashboard.html              # UPDATED: Added upload form and extraction display
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   └── setup_profile.html
└── uploads/                        # Resume files saved here
```

---

## 🚀 Setup Instructions

### Step 1: Install Required Dependencies

Open your terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- Flask - Web framework
- PyPDF2 - PDF text extraction
- python-docx - DOCX text extraction
- Werkzeug - File handling utilities

### Step 2: Verify File Locations

Ensure the following files are in place:
- ✅ `app.py` - Contains the /upload_resume endpoint
- ✅ `requirements.txt` - Updated with new packages
- ✅ `templates/dashboard.html` - Has upload form
- ✅ `static/script.js` - Handles frontend upload logic

### Step 3: Run the Flask Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with reloader
 * Debugger is active!
```

---

## 🧪 Testing the Feature

### Step 1: Register and Login

1. Go to http://127.0.0.1:5000/
2. Register with an email (e.g., user@example.com)
3. Set up your profile with name, phone, and job role
4. Click "Dashboard"

### Step 2: Test Resume Upload

1. On the Dashboard, find the "Upload Your Resume" section
2. Click the file input or drag a PDF/DOCX file
3. Click "Upload & Extract Text"
4. **Success!** The extracted text will appear below

### Step 3: Test Different File Types

**PDF Files:**
- Upload a PDF resume
- System extracts text from all pages

**DOCX Files:**
- Upload a Word document
- System extracts all paragraph text

### Step 4: Test Error Handling

**Try these scenarios:**
- Upload a TXT file → Shows error: "Only PDF and DOCX files are allowed"
- Upload a file >10MB → Shows error: "File size must be less than 10MB"
- Don't select a file → Upload button stays disabled
- Clear button resets the form

---

## 💻 Code Overview

### Backend (app.py)

**Upload Endpoint:**
```python
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    # Validates user session
    # Validates file type (PDF/DOCX only)
    # Saves file to uploads/ folder
    # Extracts text
    # Returns JSON response
```

**Text Extraction Functions:**
- `extract_text_from_pdf(file_path)` - Uses PyPDF2
- `extract_text_from_docx(file_path)` - Uses python-docx

### Frontend (dashboard.html + script.js)

**Upload Form:**
- File input with drag-and-drop support
- Shows selected filename
- Displays loading spinner during upload

**JavaScript Functions:**
- `uploadResume()` - Sends file via fetch API
- `clearFile()` - Resets form
- `displayExtractedText()` - Shows extracted content

---

## 🔧 Configuration Options

### Max File Size

In `app.py`, line 21:
```python
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
```

Change to different size if needed:
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

### Allowed File Types

In `app.py`, line 24:
```python
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
```

To add more types:
```python
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'doc'}
```

---

## 📝 API Response Format

### Success Response
```json
{
    "success": true,
    "message": "Resume uploaded successfully!",
    "filename": "user_email_resume.pdf",
    "extracted_text": "John Doe\nSoftware Engineer\n..."
}
```

### Error Response
```json
{
    "success": false,
    "error": "Only PDF and DOCX files are allowed"
}
```

---

## 🎨 Customization

### Change Upload Section Title

In `dashboard.html`, find:
```html
<h2 class="upload-section-title">📄 Upload Your Resume</h2>
```

Change the emoji or text as needed.

### Modify Button Colors

In `dashboard.html` CSS section:
```css
.upload-btn {
    background-color: #007bff;  /* Blue - change this hex code */
    color: white;
}
```

Color suggestions:
- Green: `#28a745`
- Red: `#dc3545`
- Purple: `#6f42c1`

### Change Text Extract Preview Length

In `static/script.js`, line ~175:
```javascript
const displayText = text.length > 2000  // Change 2000 to your limit
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'PyPDF2'"
**Solution:** Run `pip install PyPDF2`

### Issue: "No module named 'docx'"
**Solution:** Run `pip install python-docx`

### Issue: Upload button doesn't work
**Solution:** 
- Check browser console (F12) for JavaScript errors
- Verify user is logged in
- Check if file is selected

### Issue: File saved but text extraction fails
**Solution:**
- PDF might be scanned image (not extractable)
- DOCX might have special formatting
- Check Flask console for error message

### Issue: Files not saving to uploads folder
**Solution:**
- Verify `uploads/` folder exists
- Check folder permissions (Windows: right-click > Properties > Security)
- Ensure Flask has write permissions

---

## 📊 Data Storage

### Resume File Location
Files are saved in: `uploads/` folder with naming pattern:
```
user_email_resume.pdf
user_email_resume.docx
```

Example: `john_example_com_resume.pdf`

### Resume Text Storage
Extracted text is stored in the user object:
```python
users[email]['resume_text']  # Full extracted text
users[email]['resume']       # Filename
```

---

## 🔒 Security Notes

### Already Implemented:
✅ File extension validation (only PDF/DOCX)
✅ File size limit (10MB max)
✅ Secure filename generation (prevents path traversal)
✅ User session check (must be logged in)
✅ Error handling (doesn't expose full paths)

### For Production:
⚠️ Change `secret_key` in app.py
⚠️ Use a real database instead of dictionary
⚠️ Implement antivirus scanning for uploads
⚠️ Use cloud storage (S3, Azure) instead of local files
⚠️ Add user quotas (max resumes per user)

---

## 📱 Features Implemented

✅ **Frontend:**
- Upload button in dashboard
- File input with drag-and-drop
- File type validation (PDF/DOCX only)
- Show selected filename
- Loading indicator during upload
- Display extracted text

✅ **Backend:**
- Flask API endpoint `/upload_resume`
- File validation
- PDF text extraction (PyPDF2)
- DOCX text extraction (python-docx)
- JSON response format
- Error handling

✅ **Error Handling:**
- Invalid file type message
- File size exceeded message
- Network error handling
- Backend validation errors

---

## 🎯 Next Steps

After testing this module, consider adding:

1. **Resume Analysis** - Use AI to analyze extracted text
2. **Skill Extraction** - Identify skills from resume
3. **Career Recommendations** - Suggest roles based on resume
4. **Resume History** - Store multiple resume versions
5. **Resume Download** - Let users download analyzed data
6. **PDF Formatting** - Generate PDF reports of analysis

---

## 📞 Support

If you encounter issues:

1. Check the Flask console for error messages
2. Open browser DevTools (F12) for JavaScript errors
3. Verify all files are in correct locations
4. Ensure dependencies are installed: `pip list | grep -E 'Flask|PyPDF2|docx'`
5. Check file permissions in uploads folder

---

## ✨ Summary

Your resume upload and text extraction module is now complete and ready to use! The system:
- Accepts PDF and DOCX files
- Extracts text accurately
- Validates all inputs
- Handles errors gracefully
- Stores results for future use

Happy coding! 🚀
