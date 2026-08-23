# Code Reference - Resume Upload Module

## 📋 Quick Reference

This document provides code snippets and summaries for the resume upload and text extraction module.

---

## 1️⃣ requirements.txt

**Location:** `c:\Users\saida\Downloads\RACGS\requirements.txt`

**Content:**
```
Flask
PyPDF2
python-docx
Werkzeug
```

**What it does:**
- Flask: Web framework for creating the API
- PyPDF2: PDF text extraction library
- python-docx: Microsoft Word (.docx) text extraction
- Werkzeug: Secure file upload handling

---

## 2️⃣ Backend: app.py (Key Sections)

**Location:** `c:\Users\saida\Downloads\RACGS\app.py`

### Imports & Configuration:
```python
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max
```

### Text Extraction Function (PDF):
```python
def extract_text_from_pdf(file_path):
    """Extract text from PDF file using PyPDF2"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
```

### Text Extraction Function (DOCX):
```python
def extract_text_from_docx(file_path):
    """Extract text from DOCX file using python-docx"""
    try:
        text = ""
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")
```

### Upload Endpoint:
```python
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    """Handle resume file upload and text extraction"""
    # Validation checks:
    # 1. User is logged in
    # 2. File is provided
    # 3. File type is PDF or DOCX
    # 4. File size < 10MB
    
    # Process:
    # 1. Save file to uploads/ folder
    # 2. Extract text based on file type
    # 3. Store in user profile
    # 4. Return JSON response
```

---

## 3️⃣ Frontend: dashboard.html (Resume Section)

**Location:** `c:\Users\saida\Downloads\RACGS\templates\dashboard.html`

### Form Structure:
```html
<div class="upload-container">
    <h2 class="upload-section-title">📄 Upload Your Resume</h2>
    
    <!-- Message Display for Errors/Success -->
    <div id="uploadMessage" class="message"></div>
    
    <!-- File Info Display -->
    <div id="fileInfo" class="file-info" style="display: none;">
        <strong>Selected File:</strong> <span id="selectedFileName"></span>
    </div>

    <!-- File Input -->
    <div class="file-input-group">
        <label for="resumeFile">Choose Resume File (PDF or DOCX)</label>
        <input 
            type="file" 
            id="resumeFile" 
            accept=".pdf,.docx"
        >
    </div>

    <!-- Buttons -->
    <div class="upload-btn-group">
        <button id="uploadBtn" class="upload-btn" onclick="uploadResume()" disabled>
            Upload & Extract Text
        </button>
        <button id="clearBtn" class="clear-btn" onclick="clearFile()">
            Clear Selection
        </button>
    </div>

    <!-- Extracted Text Display -->
    <div id="extractedTextContainer" class="extracted-text-container">
        <div class="extracted-text-title">✅ Extracted Resume Text</div>
        <div id="extractedText" class="extracted-text-content"></div>
    </div>
</div>
```

### Styling: See dashboard.html for complete CSS

---

## 4️⃣ Frontend: script.js

**Location:** `c:\Users\saida\Downloads\RACGS\static\script.js`

### File Selection Handler:
```javascript
resumeFileInput.addEventListener('change', function() {
    if (this.files && this.files[0]) {
        const fileName = this.files[0].name;
        // Enable upload button
        uploadBtn.disabled = false;
        // Display filename
        fileInfo.classList.add('show');
    }
});
```

### Upload Function:
```javascript
function uploadResume() {
    // Validate file selection
    // Create FormData
    // Send via fetch to /upload_resume
    // Handle response
    // Display extracted text
    
    fetch('/upload_resume', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('✅ Resume uploaded successfully!', 'success');
            displayExtractedText(data.extracted_text);
        } else {
            showMessage(`❌ ${data.error}`, 'error');
        }
    })
    .catch(error => {
        showMessage(`❌ Error uploading file: ${error.message}`, 'error');
    });
}
```

### Helper Functions:
```javascript
function clearFile() {
    // Reset file input
    // Disable upload button
    // Hide file info
    // Clear messages
    // Hide extracted text
}

function displayExtractedText(text) {
    // Show extracted text container
    // Limit to 2000 chars for preview
    // Scroll to results
}

function showMessage(message, type) {
    // Display success or error message
}
```

---

## 🔄 Data Flow Diagram

```
User Action
    ↓
Select PDF/DOCX file
    ↓
JavaScript validates file type
    ↓
Click "Upload & Extract Text"
    ↓
fetch('/upload_resume') sends FormData
    ↓
Flask receives POST request
    ↓
Server validates:
  - User logged in? ✓
  - File type allowed? ✓
  - File size < 10MB? ✓
    ↓
Save file to /uploads folder
    ↓
Extract text:
  - If PDF → use PyPDF2
  - If DOCX → use python-docx
    ↓
Store results in user profile
    ↓
Return JSON response
    ↓
JavaScript displays extracted text
    ↓
User sees results on dashboard
```

---

## 🧪 Testing Endpoints

### Test Upload Endpoint:

**Using curl:**
```bash
curl -X POST -F "resume_file=@resume.pdf" http://localhost:5000/upload_resume
```

**Using Python:**
```python
import requests
from pathlib import Path

with open('resume.pdf', 'rb') as f:
    files = {'resume_file': f}
    response = requests.post('http://localhost:5000/upload_resume', files=files)
    print(response.json())
```

---

## 📊 File Structure with Full Paths

```
c:\Users\saida\Downloads\RACGS\
├── app.py                                    # Main Flask application
├── requirements.txt                          # Python dependencies
├── SETUP_GUIDE.md                           # Setup instructions
├── CODE_REFERENCE.md                        # This file
├── templates/
│   ├── dashboard.html                       # UPDATED: Resume upload form
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   └── setup_profile.html
├── static/
│   ├── script.js                            # NEW: Frontend upload logic
│   ├── style.css                            # Existing styles
│   └── uploads/                             # Profile photos folder
├── uploads/                                 # Resume files saved here
└── .venv/                                   # Python virtual environment
```

---

## 📝 Variable Reference

### Session Variables:
```python
session['email']  # Current logged-in user's email
```

### User Data Structure:
```python
users[email] = {
    'name': 'John Doe',
    'phone': '555-1234',
    'job_role': 'Software Engineer',
    'profile_photo': 'filename.jpg',
    'resume': 'email_resume.pdf',
    'resume_text': 'Full extracted text...'
}
```

### Flask Configuration:
```python
app.config['UPLOAD_FOLDER']        # = 'uploads'
app.config['MAX_CONTENT_LENGTH']   # = 10485760 bytes (10MB)
ALLOWED_EXTENSIONS                 # = {'pdf', 'docx'}
```

### API Request Format:
```
POST /upload_resume
Content-Type: multipart/form-data
Body: 
  resume_file: <binary PDF/DOCX data>
```

### API Response Format:
```json
{
    "success": true/false,
    "message": "Resume uploaded successfully!",
    "filename": "user_email_resume.pdf",
    "extracted_text": "John Doe...",
    "error": "Error message if failed"
}
```

---

## 🎯 Key Functions Summary

| Location | Function | Purpose |
|----------|----------|---------|
| app.py | `allowed_file()` | Check if file extension is allowed |
| app.py | `extract_text_from_pdf()` | Extract text from PDF using PyPDF2 |
| app.py | `extract_text_from_docx()` | Extract text from DOCX using python-docx |
| app.py | `upload_resume()` | Main API endpoint for file upload |
| script.js | `uploadResume()` | Send file to backend |
| script.js | `clearFile()` | Reset upload form |
| script.js | `displayExtractedText()` | Show extracted text in UI |
| script.js | `showMessage()` | Display success/error messages |

---

## ✅ Verification Checklist

Before testing, verify:

- [ ] `app.py` contains `/upload_resume` endpoint
- [ ] `requirements.txt` has: Flask, PyPDF2, python-docx, Werkzeug
- [ ] `dashboard.html` has upload form with id="resumeFile"
- [ ] `script.js` exists in `static/` folder
- [ ] `uploads/` folder exists and is writable
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Flask runs without errors: `python app.py`
- [ ] Can access http://127.0.0.1:5000/
- [ ] Upload button is disabled until file is selected
- [ ] Can select and upload PDF files
- [ ] Can select and upload DOCX files
- [ ] Extracted text displays correctly

---

## 🚀 Performance Notes

- **PDF Extraction**: Fast for text-based PDFs, slow for scanned images
- **DOCX Extraction**: Fast and reliable
- **File Size**: Supports up to 10MB (configurable)
- **Text Truncation**: Preview limited to 2000 characters
- **Response Time**: ~1-3 seconds for typical resume

---

## 📚 Resource Links

- Flask Documentation: https://flask.palletsprojects.com/
- PyPDF2 Documentation: https://github.com/py-pdf/PyPDF2
- python-docx Documentation: https://python-docx.readthedocs.io/
- Werkzeug Documentation: https://werkzeug.palletsprojects.com/

---

**Last Updated:** 2026-03-21
