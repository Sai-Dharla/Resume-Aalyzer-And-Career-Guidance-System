"""
Flask Resume Analyzer and Career Guidance System
With SQLite Database for Persistent Data Storage
"""

import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import smtplib
import random
import time
import traceback
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
from datetime import datetime
import json
from sqlalchemy import inspect, text

# ===================  APP CONFIGURATION  ===================

app = Flask(__name__)

# Secret key for session management - must be set via environment variable
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise ValueError("SECRET_KEY environment variable is required. Set it before running the application.")

# Database configuration
# Using SQLite (simple file-based database)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Serializer for generating timed tokens
serializer = URLSafeTimedSerializer(app.secret_key)


def send_otp_email(to_email: str, otp: str) -> bool:
    # Get SMTP credentials from environment variables
    sender_email = os.environ.get('GMAIL_SMTP_USER')
    app_password = os.environ.get('GMAIL_SMTP_PASS')
    
    # If credentials are not configured, log and return False gracefully
    if not sender_email or not app_password:
        app.logger.warning('Email OTP requested but GMAIL_SMTP_USER/GMAIL_SMTP_PASS not configured')
        return False

    msg = MIMEText(f'Your OTP is: {otp}')
    msg['Subject'] = 'RACGS OTP'
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # Verbose SMTP conversation to stdout for debugging
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print('Email sent successfully')
        app.logger.info('OTP email sent successfully to %s', to_email)
        return True
    except Exception as e:
        # Print and log full exception and traceback for debugging
        print('SMTP ERROR:', str(e))
        tb = traceback.format_exc()
        print(tb)
        app.logger.error('SMTP ERROR when sending to %s: %s', to_email, str(e))
        app.logger.error(tb)
        return False


# ===================  DATABASE MODELS  ===================

class User(db.Model):
    """User model - stores user account information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    job_role = db.Column(db.String(120))
    profile_photo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to resumes
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and store password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Resume(db.Model):
    """Resume model - stores uploaded resumes and extracted text"""
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    original_file_name = db.Column(db.String(255))  # Original name (e.g., "my_resume.pdf")
    extracted_text = db.Column(db.Text, nullable=False)
    file_size = db.Column(db.Integer)  # File size in bytes
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Resume {self.file_name}>'


# ===================  HELPER FUNCTIONS  ===================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


def analyze_resume(text):
    """
    Analyze resume text using keyword-based logic
    Returns score, skills found, missing skills, and suggestions
    """
    import re

    # normalize text
    text_lower = (text or '').lower()
    def normalize(s: str) -> str:
        return re.sub(r'[^a-z0-9 ]', ' ', (s or '').lower()).strip()

    # Important skills (critical set influences penalties)
    important_skills = [
        'python', 'java', 'sql', 'machine learning', 'html', 'css', 'javascript'
    ]

    # Keywords
    project_keywords = ['project', 'projects', 'developed', 'built', 'created', 'implemented', 'designed', 'portfolio', 'github', 'repository']
    experience_keywords = ['experience', 'internship', 'work', 'job', 'employment', 'position', 'role']
    formatting_keywords = ['skills', 'summary', 'objective', 'contact', 'email', 'phone', 'linkedin', 'github', 'portfolio']

    # Detect basic sections
    word_count = len(text.split())
    has_projects = any(k in text_lower for k in project_keywords)
    has_experience = any(k in text_lower for k in experience_keywords)
    has_formatting = any(k in text_lower for k in formatting_keywords)

    # Extract skills found using stricter matching (word-boundary or contained tokens)
    resume_tokens = set(normalize(text_lower).split())
    skills_found = []
    for skill in important_skills:
        sk_norm = normalize(skill)
        # exact token or phrase present
        if sk_norm in text_lower or all(tok in resume_tokens for tok in sk_norm.split()):
            skills_found.append(skill.title())

    # Missing skills list
    missing_skills = [s.title() for s in important_skills if s.title() not in skills_found]

    # Measurable achievements detection (numbers or impact verbs)
    measurable = bool(re.search(r'\b\d{1,3}%?\b', text)) or bool(re.search(r'increased|decreased|improved|reduced|boosted|result|raised|cut|grew|achieved', text_lower))

    # Projects scoring (20%) - require description + tech + measurable result for full points
    project_has_description = has_projects
    project_has_tech = any(sk.lower() in text_lower for sk in important_skills) or 'github' in text_lower or 'portfolio' in text_lower
    project_has_result = measurable
    project_score = 0
    if project_has_description and project_has_tech and project_has_result:
        project_score = 20
    elif (project_has_description and project_has_tech) or (project_has_description and project_has_result):
        project_score = 10

    # Experience scoring (20%) - award based on presence and relevance
    experience_score = 0
    if has_experience:
        # check for years of experience mention
        if re.search(r'\b\d+\s+years?\b', text_lower):
            experience_score = 20
        else:
            experience_score = 10

    # Quality scoring (20%) - require proper sections and measurable achievements
    quality_score = 0
    quality_components = 0
    if has_formatting:
        quality_components += 1
    if measurable:
        quality_components += 1
    # check for strong verbs / quantified results
    if re.search(r'\b(achieved|reduced|increased|improved|designed|launched)\b', text_lower):
        quality_components += 1

    if quality_components == 3:
        quality_score = 20
    elif quality_components == 2:
        quality_score = 12
    elif quality_components == 1:
        quality_score = 6

    # Skills scoring (40%) - stricter: proportion of important skills found
    total_important = len(important_skills)
    matched_count = len(skills_found)
    skills_score = int((matched_count / total_important) * 40)

    # Base total
    total = skills_score + project_score + experience_score + quality_score

    # Penalties
    penalties = 0
    # Missing critical skills: choose first 3 as critical
    critical_skills = important_skills[:3]
    for cs in critical_skills:
        if cs.title() not in skills_found:
            penalties += 15

    # No measurable achievements penalty
    if not measurable:
        penalties += 10

    # No relevant experience penalty
    if not has_experience:
        penalties += 20

    total = total - penalties

    # Word count bonus or penalty
    if word_count < 120:
        total -= 5
    elif word_count > 800:
        total += 3

    # Ensure final score boundaries and rounding
    final_score = max(0, min(100, int(total)))

    # Suggestions based on findings
    suggestions = []
    if missing_skills:
        suggestions.append(f"Consider adding or improving these skills: {', '.join(missing_skills[:5])}.")
    if not project_has_description:
        suggestions.append('Add detailed project descriptions including technologies used.')
    if not project_has_result:
        suggestions.append('Include measurable results for projects (percentages, numbers).')
    if not has_experience:
        suggestions.append('Add relevant work experience or internships; quantify responsibilities.')
    if measurable is False:
        suggestions.append('Add measurable achievements (numbers, percentages, impact).')

    return {
        'score': final_score,
        'skills_found': skills_found,
        'missing_skills': missing_skills,
        'suggestions': suggestions
    }


# Job matching configuration
JOB_ROLES = {
    'software engineer': ['python', 'java', 'c++', 'git', 'sql', 'javascript', 'html', 'css', 'docker', 'rest api'],
    'data scientist': ['python', 'r', 'sql', 'machine learning', 'statistics', 'pandas', 'numpy', 'sklearn', 'data visualization'],
    'frontend developer': ['html', 'css', 'javascript', 'react', 'vue', 'angular', 'responsive design', 'ui/ux'],
    'backend developer': ['python', 'java', 'node', 'sql', 'database', 'api', 'docker', 'kubernetes', 'microservices'],
    'devops engineer': ['linux', 'docker', 'kubernetes', 'ci/cd', 'aws', 'azure', 'terraform', 'monitoring']
}


def extract_skills_from_text(text):
    """Extract normalized skills found in resume text."""
    text_lower = text.lower()
    found = set()

    for role_skills in JOB_ROLES.values():
        for skill in role_skills:
            # simple containment check; can be replaced with token matching or regex
            if skill in text_lower:
                found.add(skill)

    return sorted(found)


def compute_job_match(resume_skills, target_role):
    """Compute match percentage and missing skills for a target role."""
    import re

    def normalize(s: str) -> str:
        if not s:
            return ''
        # lowercase, strip, collapse spaces
        s2 = re.sub(r'[^a-z0-9 ]', '', s.lower())
        s2 = re.sub(r'\s+', ' ', s2).strip()
        return s2

    # common abbreviation mapping to handle simple cases like 'ml' -> 'machine learning'
    ABBREVIATIONS = {
        'machine learning': ['ml', 'machinelearning'],
        'javascript': ['js'],
        'c++': ['cpp'],
        'c#': ['csharp'],
        'data science': ['ds']
    }

    role_key = (target_role or '').strip().lower()
    if not role_key or role_key not in JOB_ROLES:
        return None

    required_skills = JOB_ROLES[role_key]

    # Normalize resume_skills entries to strings
    resume_set = [normalize(str(s)) for s in (resume_skills or [])]

    matched = []
    missing = []

    for req in required_skills:
        req_norm = normalize(str(req))
        is_matched = False

        # direct substring matching (partial allowed)
        for r in resume_set:
            if not r:
                continue
            if req_norm in r or r in req_norm:
                is_matched = True
                break

        # check abbreviation list for this required skill
        if not is_matched and req_norm in ABBREVIATIONS:
            aliases = ABBREVIATIONS.get(req_norm, [])
            for alias in aliases:
                if alias in resume_set:
                    is_matched = True
                    break

        if is_matched:
            matched.append(req)
        else:
            missing.append(req)

    total_required = len(required_skills) or 1
    match_pct = int((len(matched) / total_required) * 100)

    return {
        'role': role_key,
        'match_pct': match_pct,
        'matched_skills': matched,
        'missing_skills': missing,
        'required_skills': required_skills
    }


def generate_roadmap(missing_skills):
    """
    Generate a learning roadmap for missing skills.
    
    Args:
        missing_skills (list): List of skills to generate roadmap for
    
    Returns:
        list: Ordered roadmap items for each matched missing skill
    """
    try:
        # Load roadmap data from JSON file
        with open('roadmap_data.json', 'r') as f:
            roadmap_data = json.load(f)

        # Simple rule-based ranking: core skills first, then medium, then low.
        priority_rank = {
            'high': 0,
            'medium': 1,
            'low': 2
        }

        core_skills = {
            'python',
            'sql',
            'javascript',
            'api'
        }

        # Build roadmap cards for each missing skill
        roadmap = []

        for skill in missing_skills:
            skill_lower = skill.lower()

            # Check if skill exists in roadmap data
            if skill_lower in roadmap_data:
                details = roadmap_data[skill_lower]

                # Use JSON priority when available; otherwise infer from simple rules.
                priority = str(details.get('priority', '')).strip().lower()
                if priority not in priority_rank:
                    priority = 'high' if skill_lower in core_skills else 'medium'

                roadmap.append({
                    'skill': skill,
                    'title': details.get('title', f'Learn {skill.title()}'),
                    'duration': details.get('duration', 'N/A'),
                    'resources': details.get('resources', []),
                    'project': details.get('project', 'No project specified yet.'),
                    'priority': priority.title()
                })

        roadmap.sort(
            key=lambda item: (
                priority_rank.get(str(item.get('priority', 'Low')).lower(), 2),
                item.get('skill', '').lower()
            )
        )

        return roadmap
    
    except FileNotFoundError:
        print("ERROR: roadmap_data.json not found!")
        return []
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON in roadmap_data.json!")
        return []
    except Exception as e:
        print(f"ERROR generating roadmap: {str(e)}")
        return []


def generate_ai_feedback(resume_skills, missing_skills, job_role):
    """
    Generate simple AI-style feedback using rule-based scoring.

    Args:
        resume_skills (list): Skills found in resume
        missing_skills (list): Skills missing for selected role
        job_role (str): Target job role

    Returns:
        dict: summary, strengths, weaknesses, suggestions
    """
    resume_skills = resume_skills or []
    missing_skills = missing_skills or []
    total_gap = len(missing_skills)

    if total_gap >= 6:
        summary = "You need strong improvement"
    elif total_gap >= 3:
        summary = "You are on track"
    else:
        summary = "You are job ready"

    strengths = [skill.title() for skill in resume_skills[:5]]
    weaknesses = [skill.title() for skill in missing_skills[:5]]

    core_first = {'python', 'sql', 'javascript', 'api', 'git'}
    first_priority = [skill for skill in missing_skills if skill in core_first]
    second_priority = [skill for skill in missing_skills if skill not in core_first]
    ordered_learning = first_priority + second_priority

    suggestions = []
    if ordered_learning:
        suggestions.append(f"Start with: {', '.join(skill.title() for skill in ordered_learning[:3])}")
    if job_role:
        suggestions.append(f"Focus your projects on real {job_role.title()} tasks.")
    if total_gap > 0:
        suggestions.append("Practice consistently and update your resume after each project.")
    else:
        suggestions.append("Maintain your edge by building advanced portfolio projects.")

    return {
        'summary': summary,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'suggestions': suggestions
    }


def generate_daily_plan(roadmap):
    """
    Convert roadmap items into a day-by-day learning planner.

    Args:
        roadmap (list): Output list from generate_roadmap()

    Returns:
        list: Daily task items with day number and task metadata
    """
    daily_plan = []
    day = 1

    for item in roadmap:
        skill = item.get('skill', 'Skill')
        resources = item.get('resources', [])
        project = item.get('project', 'Build a mini project')

        # Day 1 for each skill starts with basics.
        daily_plan.append({
            'day': day,
            'week': ((day - 1) // 7) + 1,
            'skill': skill,
            'task': f"Learn {skill.title()} basics",
            'type': 'learn'
        })
        day += 1

        # Add up to two resource-focused practice days to keep the plan concise.
        for resource in resources[:2]:
            daily_plan.append({
                'day': day,
                'week': ((day - 1) // 7) + 1,
                'skill': skill,
                'task': f"Study: {resource}",
                'type': 'resource'
            })
            day += 1

        # End each skill block with a practical task.
        daily_plan.append({
            'day': day,
            'week': ((day - 1) // 7) + 1,
            'skill': skill,
            'task': f"Practice: {project}",
            'type': 'project'
        })
        day += 1

    return daily_plan


def init_db():
    """Initialize the database - create all tables"""
    with app.app_context():
        db.create_all()

        # Beginner-friendly schema upgrade path for existing DB files.
        inspector = inspect(db.engine)
        if 'users' in inspector.get_table_names():
            user_columns = [col['name'] for col in inspector.get_columns('users')]
            if 'username' not in user_columns:
                db.session.execute(text('ALTER TABLE users ADD COLUMN username VARCHAR(80)'))
                db.session.commit()

        print("✅ Database initialized successfully!")


# ===================  ROUTES  ===================

@app.route('/')
def home():
    """Redirect to login page"""
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup route"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()
        
        # Validate inputs
        if not username or not email or not password:
            flash('Username, email, and password are required.', 'danger')
            return redirect(url_for('signup'))

        if len(username) < 3:
            flash('Username must be at least 3 characters long.', 'danger')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('signup'))
        
        # Check if email or username already registered
        existing_user = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Email already registered. Please login instead.', 'danger')
            return redirect(url_for('signup'))
        if existing_username:
            flash('Username already taken. Please choose another one.', 'danger')
            return redirect(url_for('signup'))
        
        # Create new user with hashed password
        try:
            new_user = User(username=username, email=email, name=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error during signup. Please try again.', 'danger')
            return redirect(url_for('signup'))
    
    return render_template('signup.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Backward-compatible registration route."""
    return redirect(url_for('signup'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check password
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['email'] = user.email
            session['username'] = user.username or user.name or user.email
            
            # Check if profile is complete
            if not user.name or not user.job_role:
                return redirect(url_for('setup_profile'))
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/setup_profile', methods=['GET', 'POST'])
def setup_profile():
    """Setup user profile after registration"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user.name = request.form.get('name', '').strip()
        user.phone = request.form.get('phone', '').strip()
        user.job_role = request.form.get('job_role', '').strip()
        
        try:
            db.session.commit()
            flash('Profile setup complete!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error saving profile. Please try again.', 'danger')
    
    return render_template('setup_profile.html', user=user)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile page - view and edit profile"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user.name = request.form.get('name', '').strip()
        user.phone = request.form.get('phone', '').strip()
        user.job_role = request.form.get('job_role', '').strip()
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'danger')
    
    # Determine profile image path (prefer session value)
    user_profile_image = None
    if session.get('profile_image'):
        user_profile_image = session.get('profile_image')
    elif user.profile_photo:
        # previous DB shape stored filename or 'profile_pics/...'
        # try to normalize to 'uploads/...' for url_for('static')
        if user.profile_photo.startswith('uploads/'):
            user_profile_image = user.profile_photo
        else:
            user_profile_image = f"uploads/{user.profile_photo}"

    return render_template('profile.html', user=user, user_profile_image=user_profile_image)


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if not email:
            flash('Please provide an email address.', 'warning')
            return redirect(url_for('forgot_password'))

        user = User.query.filter_by(email=email).first()

        # Generate 6-digit OTP
        otp = f"{random.randint(0, 999999):06d}"

        # Attempt to send OTP via SMTP. Only store OTP in session if send succeeds.
        sent = send_otp_email(email, otp)
        if sent:
            session['reset_otp'] = otp
            session['reset_otp_time'] = int(time.time())
            session['reset_email'] = email
            flash('An OTP has been sent to your email. Please check your inbox.', 'info')
            return redirect(url_for('verify_otp'))
        else:
            flash('Could not send OTP via SMTP. Please contact support or try again later.', 'danger')
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
        # token valid
        return render_template('reset_password.html', token=token, error=None)
    except SignatureExpired:
        flash('Reset link has expired. Please request a new one.', 'warning')
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash('Invalid reset link.', 'danger')
        return redirect(url_for('forgot_password'))


@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp_entered = request.form.get('otp', '').strip()
        stored_otp = session.get('reset_otp')
        otp_time = session.get('reset_otp_time')
        email = session.get('reset_email')

        if not stored_otp or not otp_time or not email:
            flash('No OTP request found. Please request a new OTP.', 'warning')
            return redirect(url_for('forgot_password'))

        # Check expiry (10 minutes)
        if int(time.time()) - int(otp_time) > 10 * 60:
            session.pop('reset_otp', None)
            session.pop('reset_otp_time', None)
            session.pop('reset_email', None)
            flash('OTP expired. Please request a new one.', 'warning')
            return redirect(url_for('forgot_password'))

        if otp_entered == stored_otp:
            # OTP valid - generate token and redirect to reset form
            token = serializer.dumps(email, salt='password-reset-salt')
            # Clear OTP from session
            session.pop('reset_otp', None)
            session.pop('reset_otp_time', None)
            session.pop('reset_email', None)
            return redirect(url_for('reset_password', token=token))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            return render_template('verify_otp.html')

    return render_template('verify_otp.html')


@app.route('/update-password', methods=['POST'])
def update_password():
    token = request.form.get('token', '')
    password = request.form.get('password', '').strip()
    confirm = request.form.get('confirm_password', '').strip()

    if not token or not password:
        flash('Invalid request.', 'danger')
        return redirect(url_for('forgot_password'))

    if password != confirm:
        flash('Passwords do not match.', 'warning')
        return render_template('reset_password.html', token=token, error='Passwords do not match')

    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        flash('Reset link has expired. Please request a new one.', 'warning')
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash('Invalid reset link.', 'danger')
        return redirect(url_for('forgot_password'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('forgot_password'))

    try:
        user.set_password(password)
        db.session.commit()
        flash('Password updated successfully. You can now login.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        db.session.rollback()
        flash('Error saving password. Please try again.', 'danger')
        return redirect(url_for('forgot_password'))


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    # Get count of user's resumes
    resume_count = Resume.query.filter_by(user_id=user.id).count()

    # Dashboard analytics inputs - prefer session (set after analysis)
    missing_skills = session.get('missing_skills', [])
    total_missing_skills = len(missing_skills)

    # If analysis values are not present in session but the user has a resume,
    # compute analysis from the latest stored resume so dashboard shows existing data.
    if not session.get('ats_score') and resume_count > 0:
        latest_resume = Resume.query.filter_by(user_id=user.id).order_by(Resume.upload_date.desc()).first()
        if latest_resume and latest_resume.extracted_text:
            try:
                analysis = analyze_resume(latest_resume.extracted_text)
                # Persist key results into session for subsequent requests
                session['ats_score'] = analysis.get('score', None)
                session['resume_skills'] = analysis.get('skills_found', [])
                session['missing_skills'] = analysis.get('missing_skills', [])
                session['app_readiness'] = analysis.get('score', None)
                # compute job match only if a target role is already selected
                target_role = session.get('target_role')
                if target_role:
                    jm = compute_job_match(session.get('resume_skills', []), target_role)
                    # store numeric match percent and full detail separately
                    session['job_match'] = jm.get('match_pct') if jm else None
                    session['job_match_detail'] = jm
            except Exception:
                # If analysis fails, continue and render page without those metrics
                pass

    # Build skill requirement counts from roadmap so frontend can map localStorage progress.
    skill_requirements = {}
    try:
        with open('roadmap_data.json', 'r') as f:
            roadmap_data = json.load(f)

        for skill in missing_skills:
            skill_key = skill.lower()
            details = roadmap_data.get(skill_key, {})
            resources_count = len(details.get('resources', []))
            projects_count = len(details.get('projects', []))

            # Backward compatible with singular "project" field.
            if projects_count == 0 and details.get('project'):
                projects_count = 1

            skill_requirements[skill_key.replace(' ', '-')] = {
                'resources': resources_count,
                'projects': projects_count,
                'total': resources_count + projects_count
            }
    except Exception:
        # Keep dashboard usable even if roadmap_data.json is unavailable.
        skill_requirements = {}
        
        return render_template(
            'dashboard.html',
            user=user,
            resume_count=resume_count,
            missing_skills=missing_skills,
            total_missing_skills=total_missing_skills,
            skill_requirements=skill_requirements,
            target_role=session.get('target_role', None)
        )

    return render_template(
        'dashboard.html',
        user=user,
        resume_count=resume_count,
        missing_skills=missing_skills,
        total_missing_skills=total_missing_skills,
        skill_requirements=skill_requirements,
        # Ensure these variables exist even if the analysis step wasn't run yet
        ats_score=session.get('ats_score', 0),
        app_readiness=session.get('app_readiness', 0),
        job_match=session.get('job_match', None),
        target_role=session.get('target_role', None)
    )


@app.route('/my_resumes')
def my_resumes():
    """My Resumes page - view and manage uploaded resumes"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    # Get all resumes for this user, sorted by upload date (newest first)
    resumes = Resume.query.filter_by(user_id=user.id).order_by(Resume.upload_date.desc()).all()
    
    return render_template('my_resumes.html', user=user, resumes=resumes)


@app.route('/job-match', methods=['GET', 'POST'])
def job_match_page():
    """Dedicated Job Match page with role selection and results."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))

    selected_role = request.form.get('job_role', '').strip().lower() if request.method == 'POST' else ''
    job_match_result = None

    if request.method == 'POST':
        if not selected_role:
            flash('Please select a job role.', 'warning')
        elif selected_role not in JOB_ROLES:
            flash('Unknown job role selected.', 'danger')
        else:
            latest_resume = Resume.query.filter_by(user_id=user.id).order_by(Resume.upload_date.desc()).first()
            if not latest_resume:
                flash('No resume found. Upload a resume first to run Job Match.', 'warning')
            else:
                resume_skills = extract_skills_from_text(latest_resume.extracted_text)
                job_match_result = compute_job_match(resume_skills, selected_role)
                if job_match_result:
                    session['missing_skills'] = job_match_result['missing_skills']
                    session['target_role'] = selected_role
                    session['resume_skills'] = resume_skills

    return render_template(
        'job_match.html',
        user=user,
        job_roles=sorted(JOB_ROLES.keys()),
        selected_role=selected_role,
        job_match_result=job_match_result
    )


@app.route('/analyze-job-match', methods=['POST'])
def analyze_job_match():
    """API endpoint for dynamic job matching via AJAX."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401

    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    # Get job role from request body
    data = request.get_json()
    selected_role = data.get('job_role', '').strip().lower() if data else ''

    # Validate role
    if not selected_role:
        return jsonify({'success': False, 'error': 'Please select a job role'}), 400

    if selected_role not in JOB_ROLES:
        return jsonify({'success': False, 'error': 'Unknown job role'}), 400

    # Get latest resume for user
    latest_resume = Resume.query.filter_by(user_id=user.id).order_by(Resume.upload_date.desc()).first()
    if not latest_resume:
        return jsonify({'success': False, 'error': 'No resume found. Upload a resume first'}), 400

    try:
        # Extract skills and compute match
        resume_skills = extract_skills_from_text(latest_resume.extracted_text)
        job_match_result = compute_job_match(resume_skills, selected_role)

        if not job_match_result:
            return jsonify({'success': False, 'error': 'Could not compute match'}), 500

        # Store missing skills in session for career path
        session['missing_skills'] = job_match_result['missing_skills']
        session['target_role'] = selected_role
        session['resume_skills'] = resume_skills

        # Return JSON response
        return jsonify({
            'success': True,
            'role': job_match_result['role'],
            'score': job_match_result['match_pct'],
            'matched': job_match_result['matched_skills'],
            'missing': job_match_result['missing_skills']
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500

    return render_template(
        'job_match.html',
        user=user,
        job_roles=sorted(JOB_ROLES.keys()),
        selected_role=selected_role,
        job_match_result=job_match_result
    )


@app.route('/job_match', methods=['POST'])
def job_match():
    """Create/update job match results from sidebar role picker"""
    if 'user_id' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    role = request.form.get('job_role', '').strip().lower()
    if not role:
        flash('Please select a job role.', 'warning')
        return redirect(request.referrer or url_for('dashboard'))

    if role not in JOB_ROLES:
        flash('Unknown job role.', 'danger')
        return redirect(request.referrer or url_for('dashboard'))

    resume = Resume.query.filter_by(user_id=user.id).order_by(Resume.upload_date.desc()).first()
    if not resume:
        flash('No resume available. Upload a resume first.', 'warning')
        return redirect(request.referrer or url_for('dashboard'))

    resume_skills = extract_skills_from_text(resume.extracted_text)
    match = compute_job_match(resume_skills, role)
    # store numeric percent for quick access, and keep full detail in a separate key
    session['job_match'] = match.get('match_pct') if match else None
    session['job_match_detail'] = match
    session['job_match_time'] = datetime.utcnow().isoformat()

    flash(f"Job match updated for '{role.title()}' ({match['match_pct']}%).", 'success')
    return redirect(request.referrer or url_for('dashboard'))


@app.context_processor
def inject_job_match_context():
    # Expose job match detail and numeric percent separately to avoid
    # accidentally rendering the full dict in places that expect a number.
    return {
        'job_match_detail': session.get('job_match_detail'),
        'job_match_percent': session.get('job_match'),
        'job_roles': JOB_ROLES,
    }


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    """
    Handle resume file upload and text extraction
    Accepts PDF and DOCX files
    Stores file and extracted text in database
    """
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401
    
    # Get user from database
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    # Check if file is in request
    if 'resume_file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['resume_file']
    
    # Check if file has a filename
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Check if file type is allowed
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Only PDF and DOCX files are allowed'}), 400
    
    try:
        # Create secure filename
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        resume_filename = secure_filename(f"user_{user.id}_resume_{datetime.utcnow().timestamp()}.{file_ext}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        
        # Save file to disk
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        # Extract text based on file type
        if file_ext == 'pdf':
            extracted_text = extract_text_from_pdf(file_path)
        else:  # docx
            extracted_text = extract_text_from_docx(file_path)
        
        # Create resume record in database
        resume = Resume(
            user_id=user.id,
            file_name=resume_filename,
            original_file_name=file.filename,
            extracted_text=extracted_text,
            file_size=file_size
        )
        
        db.session.add(resume)
        db.session.commit()
        
        # Return success response
        return jsonify({
            'success': True,
            'message': 'Resume uploaded and extracted successfully!',
            'resume_id': resume.id,
            'extracted_text': extracted_text,
            'file_name': file.filename,
            'file_size': f"{file_size / 1024 / 1024:.2f} MB" if file_size >= 1024*1024 else f"{file_size / 1024:.2f} KB"
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Error processing file: {str(e)}'}), 500


@app.route('/resume/<int:resume_id>', methods=['GET', 'POST'])
def view_resume(resume_id):
    """View a specific resume's extracted text and run job match"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    resume = Resume.query.get(resume_id)
    
    # Check if resume exists and belongs to current user
    if not resume or resume.user_id != session['user_id']:
        flash('Resume not found.', 'danger')
        return redirect(url_for('my_resumes'))
    
    user = User.query.get(session['user_id'])

    job_match_result = None
    selected_role = None

    if request.method == 'POST':
        selected_role = request.form.get('job_role', '').strip().lower()

        if not selected_role:
            flash('Please select a job role to match.', 'warning')
        elif selected_role not in JOB_ROLES:
            flash('Unknown job role selected.', 'danger')
        else:
            resume_skills = extract_skills_from_text(resume.extracted_text)
            job_match_result = compute_job_match(resume_skills, selected_role)
            if not job_match_result:
                flash('Could not compute job match for selected role.', 'danger')

    return render_template('resume_detail.html', user=user, resume=resume,
                           job_match=job_match_result, selected_role=selected_role,
                           resume_skills=extract_skills_from_text(resume.extracted_text),
                           JOB_ROLES=JOB_ROLES)


@app.route('/delete_resume/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    """Delete a resume"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401
    
    resume = Resume.query.get(resume_id)
    
    # Check if resume exists and belongs to current user
    if not resume or resume.user_id != session['user_id']:
        return jsonify({'success': False, 'error': 'Resume not found'}), 404
    
    try:
        # Delete file from disk
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete from database
        db.session.delete(resume)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Resume deleted successfully!'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Error deleting resume: {str(e)}'}), 500


# Allowed image extensions for profile photos
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_image_file(filename):
    """Check if image file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


@app.route('/upload_profile_image', methods=['POST'])
def upload_profile_image():
    """Upload profile image via AJAX"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    # Check if file is in request
    if 'profile_image' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['profile_image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Check if file type is allowed
    if not allowed_image_file(file.filename):
        return jsonify({'success': False, 'error': 'Only JPG, PNG, and GIF files are allowed'}), 400
    
    # Check file size (max 5MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > 5 * 1024 * 1024:  # 5MB
        return jsonify({'success': False, 'error': 'File size must be less than 5MB'}), 400
    
    try:
        # Create profile pics folder if it doesn't exist
        profile_pics_folder = os.path.join('static', 'uploads', 'profile_pics')
        if not os.path.exists(profile_pics_folder):
            os.makedirs(profile_pics_folder)
        
        # Generate unique filename
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"user_{user.id}_profile_{datetime.utcnow().timestamp()}.{file_ext}"
        file_path = os.path.join(profile_pics_folder, unique_filename)
        
        # Save file to disk
        file.save(file_path)
        
        # Update user profile image in database
        user.profile_photo = f"profile_pics/{unique_filename}"
        db.session.commit()
        
        # Return success response with image URL
        image_url = url_for('static', filename=f'uploads/profile_pics/{unique_filename}', _external=False)
        
        return jsonify({
            'success': True,
            'message': 'Profile image uploaded successfully!',
            'image_url': image_url,
            'filename': unique_filename
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Error uploading image: {str(e)}'}), 500


@app.route('/upload-profile', methods=['POST'])
def upload_profile():
    """Handle profile uploads from frontend (field name: 'profile').

    Saves image to static/uploads/, updates both DB and session, and
    returns JSON with `image_url` for immediate client-side update.
    """
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401

    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    # Expecting file under 'profile'
    if 'profile' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400

    file = request.files['profile']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400

    # Validate extension
    if not allowed_image_file(file.filename):
        return jsonify({'success': False, 'error': 'Only JPG, PNG, and GIF files are allowed'}), 400

    # Check file size (max 5MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > 5 * 1024 * 1024:
        return jsonify({'success': False, 'error': 'File size must be less than 5MB'}), 400

    try:
        profile_folder = os.path.join('static', 'uploads')
        if not os.path.exists(profile_folder):
            os.makedirs(profile_folder)

        file_ext = file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"user_{user.id}_profile.{file_ext}")
        save_path = os.path.join(profile_folder, filename)

        # Save file
        file.save(save_path)

        # Store relative path in session and DB for persistence
        session['profile_image'] = f"uploads/{filename}"
        user.profile_photo = f"{filename}"
        db.session.commit()

        image_url = url_for('static', filename=session['profile_image'])

        return jsonify({'success': True, 'message': 'Profile image uploaded', 'image_url': image_url}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Error uploading image: {str(e)}'}), 500


@app.route('/analyze_resume/<int:resume_id>')
def analyze_resume_route(resume_id):
    """Analyze a resume and return AI-like analysis results"""
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    
    resume = Resume.query.get(resume_id)
    
    # Check if resume exists and belongs to current user
    if not resume or resume.user_id != session['user_id']:
        return jsonify({'error': 'Resume not found'}), 404
    
    try:
        # Analyze the resume text
        analysis = analyze_resume(resume.extracted_text)
        # Persist key results into session so dashboard can read them
        session['ats_score'] = analysis.get('score', 0)
        # store detected skills and missing skills
        session['resume_skills'] = analysis.get('skills_found', [])
        session['missing_skills'] = analysis.get('missing_skills', [])

        # If target role is already selected in session, compute job match
        target_role = session.get('target_role')
        job_match_result = None
        if target_role:
            job_match_result = compute_job_match(session.get('resume_skills', []), target_role)
            # Persist numeric percent and full detail for other views
            session['job_match'] = job_match_result.get('match_pct') if job_match_result else None
            session['job_match_detail'] = job_match_result

        # Optionally update an application readiness metric (reuse ATS score)
        session['app_readiness'] = analysis.get('score', 0)

        # Return analysis results as JSON including persisted values
        return jsonify({
            'resume_id': resume.id,
            'file_name': resume.original_file_name,
            'analysis': analysis,
            'ats_score': session.get('ats_score'),
            'job_match': session.get('job_match'),
            'job_match_detail': job_match_result,
            'target_role': target_role
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing resume: {str(e)}'}), 500


@app.route('/career-path')
def career_path():
    """Career Path page - shows skill roadmap based on missing skills."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))

    # Get missing skills and target role from session
    missing_skills = session.get('missing_skills', [])
    target_role = session.get('target_role', '')
    resume_skills = session.get('resume_skills', [])

    # Fallback: if resume skills not in session, derive from latest resume
    if not resume_skills:
        latest_resume = Resume.query.filter_by(user_id=user.id).order_by(Resume.upload_date.desc()).first()
        if latest_resume:
            resume_skills = extract_skills_from_text(latest_resume.extracted_text)

    # Generate roadmap from session missing skills.
    # If missing_skills is empty, this returns an empty list and template shows the prepared-state message.
    roadmap = generate_roadmap(missing_skills)
    ai_feedback = generate_ai_feedback(resume_skills, missing_skills, target_role)
    
    return render_template(
        'career_path.html',
        user=user,
        missing_skills=missing_skills,
        target_role=target_role,
        roadmap=roadmap,
        ai_feedback=ai_feedback
    )


@app.route('/planner')
def planner():
    """Daily Planner page - converts roadmap to day-wise tasks."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))

    missing_skills = session.get('missing_skills', [])
    target_role = session.get('target_role', '')

    roadmap = generate_roadmap(missing_skills)
    daily_plan = generate_daily_plan(roadmap)

    weekly_plan = {}
    for item in daily_plan:
        week_no = item.get('week', ((item.get('day', 1) - 1) // 7) + 1)
        if week_no not in weekly_plan:
            weekly_plan[week_no] = []
        weekly_plan[week_no].append(item)

    return render_template(
        'planner.html',
        user=user,
        target_role=target_role,
        daily_plan=daily_plan,
        total_days=len(daily_plan),
        weekly_plan=weekly_plan,
        total_weeks=len(weekly_plan)
    )


@app.route('/skill-builder')
def skill_builder():
    """Skill Builder page - shows skill detail or all available skills."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))

    # Get skill name from URL query parameter
    skill = request.args.get('skill', '').lower().strip()

    # Load roadmap data
    try:
        with open('roadmap_data.json', 'r') as f:
            roadmap_data = json.load(f)
    except Exception as e:
        flash('Error loading skill data.', 'danger')
        return redirect(url_for('career_path'))

    # If no skill is provided, show all available skills in a listing/grid view
    if not skill:
        all_skills = []
        for skill_name, details in roadmap_data.items():
            all_skills.append({
                'name': skill_name,
                'title': details.get('title', f'Learn {skill_name.title()}'),
                'duration': details.get('duration', 'N/A'),
                'project': details.get('project', 'No project specified yet.')
            })

        all_skills.sort(key=lambda item: item['name'])

        return render_template(
            'skill_builder.html',
            user=user,
            skill='',
            all_skills=all_skills
        )

    # Get skill details
    if skill not in roadmap_data:
        flash(f'Skill "{skill}" not found in roadmap.', 'danger')
        return redirect(url_for('career_path'))

    skill_details = roadmap_data[skill]

    # Add a default level so template remains robust with simple roadmap JSON
    skill_details.setdefault('level', 'Beginner-friendly')

    # Backward-compatible shape for template (expects projects list)
    if 'projects' not in skill_details:
        skill_details['projects'] = [skill_details.get('project', 'No project specified yet.')]

    return render_template(
        'skill_builder.html',
        user=user,
        skill=skill,
        skill_details=skill_details,
        all_skills=[]
    )


@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


# ===================  ERROR HANDLERS  ===================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


# ===================  INITIALIZATION  ===================

if __name__ == '__main__':
    # Initialize database before running
    init_db()
    
    # Start Flask development server
    app.run(debug=True)
