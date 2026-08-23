# Resume Analyzer and Career Guidance System (RACGS)
## Complete Modular Architecture Documentation

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Core Modules](#core-modules)
4. [Features](#features)
5. [Installation](#installation)
6. [Usage](#usage)
7. [API Reference](#api-reference)
8. [Data Files](#data-files)
9. [Examples](#examples)
10. [Best Practices](#best-practices)

---

## 🎯 System Overview

**RACGS** is a comprehensive Python-based system for analyzing resumes, identifying skill gaps, generating personalized learning roadmaps, and providing career guidance. The system is built with a **modular, beginner-friendly architecture** that separates concerns into independent, reusable components.

### Key Characteristics
- ✅ **Modular Design**: Each feature is a separate, independent module
- ✅ **Beginner-Friendly**: Clear code structure with extensive comments
- ✅ **Comprehensive**: 12+ major features covering everything from resume analysis to career simulation
- ✅ **Extensible**: Easy to add new modules or customize existing ones
- ✅ **Production-Ready**: Proper error handling and logging throughout

---

## 🏗️ Architecture

### Directory Structure

```
RACGS/
├── core/                          # Core business logic
│   ├── __init__.py               # Module exports
│   ├── resume_processor.py        # Text extraction & parsing
│   ├── skill_extractor.py         # Skill detection
│   ├── ats_scorer.py              # ATS scoring
│   ├── skill_gap_analyzer.py      # Gap analysis
│   ├── job_matcher.py             # Job matching
│   ├── resume_improver.py         # Resume enhancement
│   ├── interview_generator.py     # Mock interviews
│   ├── roadmap_generator.py       # Learning roadmaps
│   ├── career_simulator.py        # Career timeline
│   └── recruiter_view.py          # Recruiter perspective
│
├── data/                          # Data files
│   ├── skills_database.json       # Comprehensive skill list
│   └── job_roles.json             # Job role definitions
│
├── web/                           # Flask web application
│   ├── app.py                     # Main Flask app
│   ├── models.py                  # SQLAlchemy models
│   ├── routes.py                  # Flask routes
│   └── utils.py                   # Utilities
│
├── templates/                     # Jinja2 templates
├── static/                        # CSS, JS, images
├── main.py                        # CLI entry point
├── requirements.txt               # Dependencies
└── README.md                      # Documentation
```

### Module Dependencies

```
Resume Input
    ↓
ResumeProcessor (extract text)
    ↓
├─→ SkillExtractor (find skills)
│       ↓
│   ATSScorer (score compatibility)
│       ↓
│   SkillGapAnalyzer (identify gaps)
│       ↓
│   RoadmapGenerator (create learning path)
│       ↓
│   CareerSimulator (estimate readiness)
│
├─→ ResumeImprover (suggest improvements)
│
├─→ JobMatcher (compare with jobs)
│
├─→ InterviewGenerator (generate questions)
│
└─→ RecruiterView (hiring perspective)
```

---

## 📦 Core Modules

### 1. **ResumeProcessor** (`core/resume_processor.py`)

Extracts and structures resume information from PDF and DOCX files.

**Key Methods:**
- `extract_text(file_path)` - Extract text from resume
- `extract_contact_info()` - Parse contact information
- `extract_sections()` - Identify and extract resume sections
- `process_resume(file_path)` - Complete processing pipeline

**Output Structure:**
```python
{
    'contact': {'email': '...', 'phone': '...', 'linkedin': '...'},
    'summary': '...',
    'skills': [],
    'experience': [{'company': '...', 'position': '...', 'duration': '...'}],
    'education': [{'degree': '...', 'institution': '...', 'year': '...'}],
    'projects': []
}
```

### 2. **SkillExtractor** (`core/skill_extractor.py`)

Matches resume text against predefined skills database.

**Key Methods:**
- `extract_skills(text)` - Find skills in text
- `get_all_skills()` - Flat list of extracted skills
- `get_skills_by_category()` - Skills organized by category
- `add_custom_skill(skill, category)` - Add custom skills

**Skill Categories:**
- Programming Languages
- Web Development
- Databases
- Cloud & DevOps
- Data Science
- Mobile Development
- Tools & Frameworks
- Soft Skills
- Specializations

### 3. **ATSScorer** (`core/ats_scorer.py`)

Calculates ATS (Applicant Tracking System) compatibility scores.

**Scoring Breakdown:**
- Skills: 30%
- Projects: 20%
- Experience: 25%
- Education: 15%
- Formatting: 10%

**Key Methods:**
- `score_skills_section(skills)` - Skills score
- `score_projects_section(projects)` - Projects score
- `score_experience_section(experience)` - Experience score
- `score_education_section(education)` - Education score
- `score_formatting(text)` - Formatting score
- `calculate_ats_score(...)` - Complete ATS score

### 4. **SkillGapAnalyzer** (`core/skill_gap_analyzer.py`)

Identifies missing skills and creates prioritized learning paths.

**Key Methods:**
- `analyze_gap(extracted_skills, job_role)` - Gap analysis
- `get_prioritized_roadmap()` - Skills to learn
- `get_gap_summary()` - Summary report

**Output:**
```python
{
    'critical_gaps': 5,
    'recommended_gaps': 3,
    'bonus_gaps': 2,
    'total_missing_skills': 10,
    'estimated_learning_weeks': 16,
    'priority_roadmap': [...]
}
```

### 5. **JobMatcher** (`core/job_matcher.py`)

Compares resume skills with job requirements.

**Key Methods:**
- `extract_skills_from_job_description(text)` - Parse job requirements
- `calculate_similarity(resume_skills, job_skills)` - Match score
- `get_match_report(...)` - Complete matching report

**Match Report:**
```python
{
    'overall_match_score': 75.5,
    'fit_assessment': 'Good Fit',
    'matched_skills': [...],
    'missing_skills': [...],
    'recommendations': [...]
}
```

### 6. **ResumeImprover** (`core/resume_improver.py`)

Analyzes and suggests resume improvements.

**Key Methods:**
- `analyze_resume(text)` - Find improvement opportunities
- `rewrite_bullet_point(bullet)` - Improve bullet points
- `add_metrics(bullet)` - Suggest metrics
- `get_improvement_suggestions(text)` - Actionable suggestions

### 7. **InterviewGenerator** (`core/interview_generator.py`)

Generates mock interview questions and evaluates responses.

**Question Categories:**
- Behavioral (40%)
- Technical (40%)
- Situational (20%)
- Role-specific variations

**Key Methods:**
- `get_question(category)` - Single question
- `get_multiple_questions(count)` - Multiple questions
- `evaluate_response(answer)` - Score response
- `get_performance_summary()` - Interview performance

**Evaluation Criteria:**
- Clarity (20%)
- Relevance (25%)
- Structure (20%)
- Depth (20%)
- Keywords (15%)

### 8. **RoadmapGenerator** (`core/roadmap_generator.py`)

Creates personalized learning paths and milestones.

**Key Methods:**
- `generate_learning_roadmap(skill_gaps, hours_per_week)` - Create roadmap
- `generate_career_timeline(target_role, skill_gaps)` - Timeline with milestones
- `generate_weekly_plan(roadmap)` - Weekly breakdown
- `adjust_roadmap_for_pace(pace)` - Customize for learning speed

### 9. **CareerSimulator** (`core/career_simulator.py`)

Simulates career outcomes and job readiness.

**Key Methods:**
- `estimate_job_readiness(...)` - Timeline estimate
- `generate_multiple_scenarios(...)` - Fast/average/slow learner scenarios
- `simulate_job_hunt(readiness_score)` - Job search simulation
- `calculate_salary_trajectory(...)` - Salary projection

### 10. **RecruiterView** (`core/recruiter_view.py`)

Analyzes resume from recruiter perspective.

**Key Methods:**
- `calculate_first_impression(...)` - 6-15 second review analysis
- `calculate_hire_probability(...)` - Hiring likelihood
- `analyze_strengths_from_recruiter_view(...)` - Key strengths
- `analyze_concerns_from_recruiter_view(...)` - Red flags
- `generate_recruiter_feedback(...)` - Complete feedback

---

## ✨ Features

### 1. Resume Processing
Extract and structure resume data from PDF and DOCX files.

### 2. Skill Analysis
Identify technical and soft skills with categorization.

### 3. ATS Scoring
Calculate resume compatibility with ATS systems (0-100 score).

### 4. Skill Gap Analysis
Identify missing skills and estimate learning time.

### 5. Resume Enhancement
Suggest improvements for stronger impact.

### 6. Job Matching
Compare resume against job descriptions (similarity % + matched/missing skills).

### 7. Mock Interviews
Generate questions, evaluate responses, provide feedback.

### 8. Learning Roadmaps
Create week-by-week learning plans with milestones.

### 9. Career Timeline
Project job readiness with multiple learning pace scenarios.

### 10. Job Search Simulation
Estimate interview callbacks, offers, and success rates.

### 11. Salary Projection
Project salary growth over time.

### 12. Recruiter Perspective
Show what hiring managers see: strengths, concerns, hire probability.

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Steps

```bash
# 1. Navigate to project directory
cd RACGS

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. (Optional) Download NLTK data for NLP
python -m nltk.downloader punkt stopwords averaged_perceptron_tagger
```

---

## 📖 Usage

### CLI Usage

```bash
# Basic analysis
python main.py resume.pdf

# With target job role
python main.py resume.pdf --job "Full Stack Developer"

# Custom output path
python main.py resume.pdf --job "Data Scientist" --output my_report.json
```

### Python API Usage

```python
from core import ResumeProcessor, SkillExtractor, ATSScorer, SkillGapAnalyzer

# Initialize modules
processor = ResumeProcessor()
extractor = SkillExtractor()
scorer = ATSScorer()
gap_analyzer = SkillGapAnalyzer()

# Process resume
resume_data = processor.process_resume('resume.pdf')
resume_text = processor.get_text()

# Extract skills
skills = extractor.extract_skills(resume_text)
all_skills = extractor.get_all_skills()

# Calculate ATS score
ats_result = scorer.calculate_ats_score(
    skills,
    resume_data['projects'],
    resume_data['experience'],
    resume_data['education'],
    resume_text
)

# Analyze skill gaps
gap_analysis = gap_analyzer.analyze_gap(all_skills, 'Software Developer')
gap_summary = gap_analyzer.get_gap_summary()

print(f"ATS Score: {ats_result['total_score']}/100")
print(f"Missing Skills: {gap_summary['total_missing_skills']}")
print(f"Learning Time: {gap_summary['estimated_learning_weeks']} weeks")
```

### Flask Web Usage

```bash
python web/app.py
# Visit http://localhost:5000
```

---

## 📚 API Reference

### Complete Module Reference

See individual module files for complete documentation:
- `core/resume_processor.py` - Resume extraction
- `core/skill_extractor.py` - Skill matching
- `core/ats_scorer.py` - ATS calculations
- `core/skill_gap_analyzer.py` - Gap analysis
- `core/job_matcher.py` - Job matching
- `core/resume_improver.py` - Improvements
- `core/interview_generator.py` - Interview prep
- `core/roadmap_generator.py` - Learning paths
- `core/career_simulator.py` - Career timeline
- `core/recruiter_view.py` - Recruiter analysis

---

## 📁 Data Files

### `data/skills_database.json`
Comprehensive list of 100+ skills across 10 categories.

```json
{
  "programming_languages": ["Python", "Java", ...],
  "web_development": ["React", "Node.js", ...],
  "databases": ["SQL", "MongoDB", ...],
  ...
}
```

### `data/job_roles.json`
12+ predefined job roles with required, recommended, and bonus skills.

```json
{
  "Full Stack Developer": {
    "critical": ["JavaScript", "React", ...],
    "recommended": ["Docker", "Git", ...],
    "bonus": ["GraphQL", "Kubernetes", ...],
    "salary_range": "$80k-$120k",
    "learning_time": 20
  },
  ...
}
```

---

## 💡 Examples

### Example 1: Complete Resume Analysis

```python
from main import RACSSystem

# Initialize system
racgs = RACSSystem()

# Analyze resume
results = racgs.analyze_resume('resume.pdf', 'Full Stack Developer')

# Print summary
racgs.print_summary()

# Save report
racgs.generate_report()
```

### Example 2: Skill Gap Analysis

```python
from core import SkillGapAnalyzer

analyzer = SkillGapAnalyzer()
current_skills = ['Python', 'HTML', 'CSS', 'Git']
gap_analysis = analyzer.analyze_gap(current_skills, 'Full Stack Developer')

roadmap = analyzer.get_prioritized_roadmap()
print("Skills to learn (prioritized):")
for skill in roadmap:
    print(f"- {skill['skill']} ({skill['priority']}) - {skill['estimated_days']} days")
```

### Example 3: Job Matching

```python
from core import JobMatcher

matcher = JobMatcher()
resume_skills = ['Python', 'Django', 'SQL', 'React']
job_desc = "We're looking for a candidate with Python, Django, Node.js..."

report = matcher.get_match_report(resume_skills, 'Full Stack Dev', job_desc)
print(f"Match Score: {report['overall_match_score']}%")
print(f"Missing: {report['missing_skills']}")
```

### Example 4: Mock Interview

```python
from core import InterviewGenerator

interview = InterviewGenerator('Full Stack Developer')

# Get questions
questions = interview.get_multiple_questions(5)
for q in questions:
    print(f"Q: {q}")

# Evaluate response
answer = "I built a web app using React and Node.js..."
evaluation = interview.evaluate_response(answer)
print(f"Score: {evaluation['overall_score']}/100")
print(f"Feedback: {evaluation['feedback']}")
```

---

## 🎯 Best Practices

### 1. Always Validate Input
```python
if not os.path.exists(resume_path):
    print("Resume file not found!")
    return
```

### 2. Use Logging
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Processing resume...")
```

### 3. Handle Errors Gracefully
```python
try:
    text = processor.extract_text(file_path)
except Exception as e:
    logger.error(f"Extraction failed: {str(e)}")
    return None
```

### 4. Modularize Your Code
```python
# Good: Each module has single responsibility
gap_analyzer = SkillGapAnalyzer()
roadmap_gen = RoadmapGenerator()

# Bad: Mixing concerns
# Don't put job matching logic in skill extractor
```

### 5. Use Configuration Files
```python
# Store settings in JSON/YAML files
CONFIG_PATH = 'config.json'
with open(CONFIG_PATH) as f:
    config = json.load(f)
```

### 6. Document Custom Modules
```python
class MyCustomModule:
    """
    Description of what this module does.
    
    Attributes:
        param1: Description
        param2: Description
    """
    
    def my_method(self, arg1: str) -> Dict:
        """
        What this method does.
        
        Args:
            arg1: Description of arg1
            
        Returns:
            Description of return value
        """
        pass
```

---

## 🔄 Extension Guide

### Adding a New Module

1. Create file in `core/` directory
2. Import in `core/__init__.py`
3. Implement required methods
4. Add data files if needed
5. Document module

### Example: Custom Certification Module

```python
# core/certification_matcher.py
from typing import List, Dict

class CertificationMatcher:
    """Match certifications with job requirements"""
    
    def __init__(self):
        self.certifications = {}
    
    def find_relevant_certifications(self, job_role: str) -> List[str]:
        """Find certifications for job role"""
        pass
```

---

## 📞 Support & Troubleshooting

### Common Issues

**Issue**: PDF extraction returns empty text
- **Solution**: Ensure PDF is not scanned image-only. Rerun OCR if needed.

**Issue**: Skills not being recognized
- **Solution**: Add to `data/skills_database.json` or use custom categories

**Issue**: Job role not found
- **Solution**: Add to `data/job_roles.json` or use fuzzy matching

---

## 📝 License & Attribution

This system is built with beginner-friendly Python code and comprehensive documentation for easy understanding and extension.

**Built with:**
- PyPDF2 for PDF processing
- python-docx for DOCX processing
- scikit-learn for similarity calculations
- Flask for web interface
- SQLAlchemy for database ORM

---

## 🎓 Learning Resources

- [Python Documentation](https://docs.python.org/3/)
- [PyPDF2 Guide](https://github.com/py-pdf/PyPDF2)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)

---

**Last Updated**: March 2024  
**Version**: 1.0.0  
**Status**: Production Ready  
