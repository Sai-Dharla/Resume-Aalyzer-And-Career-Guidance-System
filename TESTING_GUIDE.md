# 🚀 Testing & Troubleshooting Guide

## ✅ What Was Fixed

Your Flask resume upload module now has these improvements:

### **Fix #1: Text No Longer Disappears**
- ✅ Uses `event.preventDefault()` to prevent page reload
- ✅ Uses Fetch API instead of form submission
- ✅ JavaScript doesn't trigger page reload
- ✅ Extracted text stays visible indefinitely

### **Fix #2: Upload Moved to "My Resumes" Page**
- ✅ Created new `my_resumes.html` page
- ✅ Dashboard cleaned up (now only shows welcome message)
- ✅ Users click "My Resumes" in sidebar to access uploads
- ✅ Better organization and separation

### **Fix #3: Improved Frontend Behavior**
- ✅ Shows selected file name with file size
- ✅ Loading indicator (spinner) while processing
- ✅ Text formatting preserved with `white-space: pre-wrap`
- ✅ Auto-scroll to extracted text
- ✅ No auto-clear (text stays visible!)

---

## 🧪 Step-by-Step Testing

### **Step 1: Prepare Your Environment**

```bash
# Navigate to project folder
cd c:\Users\saida\Downloads\RACGS

# Make sure dependencies are installed
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask, PyPDF2, python-docx, Werkzeug
```

### **Step 2: Start Flask Application**

```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with reloader
 * Debugger is active!
```

### **Step 3: Open Browser**

Navigate to:
```
http://127.0.0.1:5000/
```

### **Step 4: Register New User**

1. Click "Register"
2. Enter email: `test@example.com`
3. Click "Register"

**Expected:**
```
✅ Registration successful! Please login.
```

### **Step 5: Login**

1. Enter email: `test@example.com`
2. Click "Login"

**Expected:**
```
Redirected to Profile Setup page
```

### **Step 6: Setup Profile**

1. Name: `John Doe`
2. Phone: `555-1234`
3. Job Role: `Software Engineer`
4. Click "Complete Profile"

**Expected:**
```
✅ Profile setup complete!
Redirected to Dashboard
```

### **Step 7: Go to "My Resumes" Page**

1. **Option A:** Click "My Resumes" in sidebar
2. **Option B:** Click "View Resumes" button on Dashboard

**Expected:**
```
See upload form with:
- File input
- "Upload & Extract Text" button
- "Clear Selection" button
```

### **Step 8: Select a File**

1. Click file input
2. Select a PDF or DOCX file from your computer
3. Watch for file name to appear

**Expected:**
```
✅ File name displays: "resume.pdf (245 KB)"
✅ Upload button becomes enabled
```

### **Step 9: Click Upload Button**

1. Click "Upload & Extract Text"
2. Watch for loading indicator

**Expected:**
```
Button shows: "⏳ Processing..."
With animated spinner
```

### **Step 10: View Extracted Text** ⭐ KEY TEST

1. Wait 1-3 seconds for extraction
2. See success message
3. See extracted text appear
4. **Text stays visible!** (This is the fix!)

**Expected:**
```
✅ Success message: "Resume uploaded successfully!"
✅ Extracted text displays in the box
✅ Text stays visible
✅ Page did NOT reload! (Check URL - still http://127.0.0.1:5000/my_resumes)
✅ Text formatting is preserved
```

### **Step 11: Test Upload Another File**

1. Select a different file (or same file)
2. Click upload again
3. Previous text is replaced with new text
4. **System works smoothly**

**Expected:**
```
✅ New text replaces old text
✅ No errors
✅ File name updates
✅ Loading indicator shows again
```

---

## ✨ Detailed Verification Checklist

### Frontend Behavior
- [ ] File input accepts PDF files
- [ ] File input accepts DOCX files
- [ ] File input rejects other file types
- [ ] Selected file name displays with size
- [ ] Upload button is disabled until file selected
- [ ] Loading spinner appears during upload
- [ ] Spinner animation is smooth

### Text Display
- [ ] Extracted text appears in the right box
- [ ] Text formatting is preserved (line breaks, spaces)
- [ ] Text doesn't get cut off
- [ ] Text area has scrollbar if needed
- [ ] Text is readable and formatted well
- [ ] Success message displays

### Critical Fixes
- [ ] **Page does NOT reload after upload** (Check URL!)
- [ ] **Text stays visible** (doesn't disappear!)
- [ ] Page scroll position preserved
- [ ] No error messages in browser console (F12)
- [ ] No 404 errors
- [ ] No JavaScript errors

### User Actions
- [ ] Clear button works (resets form)
- [ ] Can upload multiple files in sequence
- [ ] Sidebar navigation works
- [ ] Dashboard link works
- [ ] Profile link works
- [ ] Logout works

---

## 🔍 How to Debug

### **Check Browser Console**

1. Press `F12` to open Developer Tools
2. Click "Console" tab
3. Look for error messages
4. Should see: `"Page loaded successfully"`

### **Check Flask Console**

1. Look at terminal where Flask is running
2. Should see:
   ```
   127.0.0.1 - - [2024-01-01 12:00:00] "POST /upload_resume HTTP/1.1" 200
   ```

### **Verify Request/Response**

1. Press `F12` → Network tab
2. Upload a file
3. Look for `upload_resume` request
4. Click it to see:
   - Request: POST to `/upload_resume`
   - Response: JSON with `success: true`
   - Status: 200

### **Check if Text is in HTML**

1. Press `F12` → Elements tab
2. Find `<div id="extractedText">`
3. See if text is inside it
4. It should contain extracted resume text

---

## 🐛 Troubleshooting

### **Issue: Text disappears after upload**

**Diagnostic:**
- Check if page reloads (look at URL)
- Check browser console for errors

**Solution:**
- Verify `event.preventDefault()` is in code
- Check that fetch API is being used
- NOT a form submission

---

### **Issue: Upload button doesn't work**

**Diagnostic:**
1. Select a file → button should enable
2. Click button → nothing happens?

**Solution:**
- Press F12 and check console for JavaScript errors
- Make sure my_resumes.html is loaded
- Check if the JavaScript code is executing

---

### **Issue: "Page not found" error**

**Diagnostic:**
- URL shows 404 error
- "My Resumes" link doesn't work

**Solution:**
- Check `@app.route('/my_resumes')` exists in app.py
- Restart Flask: `python app.py`
- Clear browser cache (Ctrl+Shift+Delete)

---

### **Issue: Extracted text formatting is wrong**

**Diagnostic:**
- Text appears on one line
- Line breaks are lost
- Spaces are lost

**Solution:**
- Check CSS has `white-space: pre-wrap;`
- Make sure it's in `.extracted-text-content` class
- Force-reload page (Ctrl+F5)

---

### **Issue: File upload fails with error**

**Diagnostic:**
- Error message appears
- File doesn't upload

**Possible Solutions:**
1. **"Only PDF and DOCX files allowed"**
   - Make sure file extension is .pdf or .docx
   - Try a different PDF/DOCX file

2. **"File size must be less than 10MB"**
   - File is too large
   - Compress or use smaller file

3. **"User not logged in"**
   - User session expired
   - Login again

4. **"Error processing file"**
   - PDF might be scanned (not extractable)
   - DOCX might be corrupted
   - Try a different file

---

### **Issue: Flask console shows error**

**Common Errors:**

1. **ModuleNotFoundError: PyPDF2**
   ```bash
   pip install PyPDF2
   ```

2. **ModuleNotFoundError: docx**
   ```bash
   pip install python-docx
   ```

3. **Port 5000 already in use**
   ```bash
   python app.py --port 5001
   ```

---

## 📊 File Size for Testing

Good test files:
- **Small:** 50KB - 100KB
- **Medium:** 100KB - 500KB
- **Large:** 500KB - 5MB

Don't use files larger than 10MB (will be rejected).

---

## 🎯 Key Success Indicators

When everything works correctly, you should see:

✅ **URL stays at** `http://127.0.0.1:5000/my_resumes`
✅ **Page doesn't blink or reload**
✅ **Text appears instantly** (1-3 seconds)
✅ **Text stays visible** indefinitely
✅ **No error messages** anywhere
✅ **Can upload multiple files** in sequence
✅ **File name displays** with size
✅ **Loading spinner shows** during extraction
✅ **Success message appears**
✅ **Text formatting is preserved**

If all these are true: **Everything is working perfectly!** 🎉

---

## 🔍 File Locations

Keep these in mind while troubleshooting:

```
Files to Check:
├── app.py                           (Routes, upload endpoint)
├── templates/
│   ├── dashboard.html               (Cleaned up, links to my_resumes)
│   ├── my_resumes.html              (NEW - upload form here!)
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   └── setup_profile.html
├── static/
│   ├── script.js                    (Global scripts only)
│   ├── style.css
│   └── uploads/                     (Profile photos)
├── uploads/                         (Resume files saved here)
└── requirements.txt                 (Dependencies)
```

---

## 📱 Testing on Mobile

To test on mobile device:

1. Find your computer's IP address:
   ```bash
   ipconfig
   # Look for "IPv4 Address" like 192.168.1.100
   ```

2. On mobile, visit:
   ```
   http://192.168.1.100:5000/
   ```

3. Test upload with mobile experience
4. Everything should work the same!

---

## 🎪 Test Scenarios

### **Scenario 1: Normal Happy Path**
1. Register
2. Setup profile
3. Go to Dashboard
4. Click "My Resumes"
5. Upload PDF
6. See extracted text
7. **Result:** ✅ SUCCESS

### **Scenario 2: Multiple Uploads**
1. Upload first file
2. See text
3. Upload second file
4. See new text (replaces old)
5. **Result:** ✅ SUCCESS

### **Scenario 3: Error Handling**
1. Try uploading TXT file
2. See error message
3. Try uploading large file
4. See size error
5. Upload valid file after errors
6. Works normally
7. **Result:** ✅ SUCCESS

### **Scenario 4: Session Timeout**
1. Upload file (succeeds)
2. Logout
3. Try accessing `/my_resumes` without login
4. Redirects to login
5. **Result:** ✅ SUCCESS (security works)

---

## 🎊 Final Check

Run through this quick check:

```
□ Flask running without errors
□ Can register user
□ Can login
□ Can setup profile
□ Dashboard loads
□ Can click "My Resumes"
□ Upload form appears
□ Can select file
□ Upload works
□ Text appears
□ Text stays visible
□ No page reload
□ Text formatting good
□ Can upload again
□ Clear button works
□ Logout works
```

**If all checked:** Your system is ready! 🚀

---

## 💡 Quick Tips

1. **Always check browser console (F12)** for errors first
2. **Always check Flask console** for backend errors
3. **Hard refresh the page** (Ctrl+F5) if styling won't update
4. **Clear cookies** if login issues persist
5. **Restart Flask** if routes don't work after changes

---

## 📞 Getting Help

1. Check this guide first for your issue
2. Look at browser console (F12) → Console tab
3. Look at Flask console output
4. Check file locations are correct
5. Verify all dependencies installed

---

**Now you're ready to test!** Good luck! 🎉
