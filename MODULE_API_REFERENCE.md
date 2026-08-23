# Module API Reference & Examples
## Complete Guide to Using Core Modules

---

## Table of Contents

1. [ResumeProcessor](#resumeprocessor)
2. [SkillExtractor](#skillextractor)
3. [ATSScorer](#atsscorer)
4. [SkillGapAnalyzer](#skillgapanalyzer)
5. [JobMatcher](#jobmatcher)
6. [ResumeImprover](#resumeimprover)
7. [InterviewGenerator](#interviewgenerator)
8. [RoadmapGenerator](#roadmapgenerator)
9. [CareerSimulator](#careersimulator)
10. [RecruiterView](#recruiterview)

---

## ResumeProcessor

Extract and structure resume data.

### Initialization
```python
from core import ResumeProcessor

processor = ResumeProcessor()
```

### Methods

**`extract_text(file_path: str) -> str`**
```python
text = processor.extract_text('resume.pdf')
print(text[:500])  # First 500 characters
```

**`extract_contact_info() -> Dict`**
```python
contact = processor.extract_contact_info()
# Returns: {
#   'email': 'user@example.com',
#   'phone': '555-1234',
#   'linkedin': 'linkedin.com/in/username',
#   'github': 'github.com/username'
# }
```

**`extract_sections() -> Dict[str, str]`**
```python
sections = processor.extract_sections()
# Returns sections: summary, experience, education, skills, projects
print(sections['experience'])
```

**`parse_experience(experience_text: str) -> List[Dict]`**
```python
experiences = processor.parse_experience(sections['experience'])
# Returns list of: {
#   'company': '...',
#   'position': '...',
#   'duration': '...',
#   'description': '...'
# }
```

**`process_resume(file_path: str) -> Dict`**
```python
full_data = processor.process_resume('resume.pdf')
# Complete structured resume data
```

### Example: Complete Resume Processing
```python
processor = ResumeProcessor()
data = processor.process_resume('my_resume.pdf')

print("Contact:", data['contact'])
print("Summary:", data['summary'][:200])
print("Experience:", len(data['experience']), "positions")
print("Education:", len(data['education']), "degrees")
print("Available skills:", len(data['projects']), "projects")
```

---

## SkillExtractor

Find and categorize skills.

### Initialization
```python
from core import SkillExtractor

extractor = SkillExtractor()
# Automatically loads skills_database.json
```

### Methods

**`extract_skills(text: str) -> Dict[str, List[str]]`**
```python
skills = extractor.extract_skills(resume_text)
# Returns: {
#   'programming_languages': ['Python', 'Java'],
#   'web_development': ['React', 'Node.js'],
#   'databases': ['SQL', 'MongoDB'],
#   ...
# }
```

**`get_all_skills() -> List[str]`**
```python
all_skills = extractor.get_all_skills()
print(f"Found {len(all_skills)} skills")
# ['Python', 'React', 'SQL', ...]
```

**`get_skills_by_category() -> Dict`**
```python
categories = extractor.get_skills_by_category()
for category, skills in categories.items():
    if skills:
        print(f"{category}: {', '.join(skills)}")
```

**`add_custom_skill(skill: str, category: str = 'other')`**
```python
extractor.add_custom_skill('TensorFlow', 'data_science')
extractor.add_custom_skill('Kubernetes', 'cloud_devops')
```

**`find_skill_similarity(text: str, threshold: float = 0.7)`**
```python
similar = extractor.find_skill_similarity("experience with python programming")
# Returns: [('Python', 1.0), ('Programming', 0.8), ...]
```

### Example: Skill Analysis
```python
extractor = SkillExtractor()
skills = extractor.extract_skills(resume_text)

print("=== SKILLS FOUND ===")
for category, skill_list in skills.items():
    if skill_list:
        print(f"\n{category.upper()}:")
        for skill in skill_list:
            print(f"  • {skill}")

print(f"\nTotal: {len(extractor.get_all_skills())} skills")
```

---

## ATSScorer

Calculate ATS compatibility.

### Initialization
```python
from core import ATSScorer

scorer = ATSScorer()
```

### Methods

**`calculate_ats_score(extracted_skills, projects, experience, education, text, required_skills=None) -> Dict`**
```python
result = scorer.calculate_ats_score(
    extracted_skills,
    projects=[...],
    experience=[...],
    education=[...],
    text=resume_text,
    required_skills=['Python', 'React', 'SQL']
)
# Returns: {
#   'total_score': 72.5,
#   'section_scores': {
#     'skills': 85,
#     'projects': 60,
#     'experience': 90,
#     'education': 70,
#     'formatting': 80
#   },
#   'details': {...}
# }
```

**`get_ats_score() -> float`**
```python
score = scorer.get_ats_score()
print(f"ATS Score: {score}/100")
```

**`get_scores_breakdown() -> Dict`**
```python
breakdown = scorer.get_scores_breakdown()
print(breakdown['scores'])
print(breakdown['details'])
```

### Example: ATS Scoring
```python
scorer = ATSScorer()
result = scorer.calculate_ats_score(
    skills_by_category,
    structured_data['projects'],
    structured_data['experience'],
    structured_data['education'],
    resume_text
)

print(f"Total ATS Score: {result['total_score']}/100")
print("\nSection Scores:")
for section, score in result['section_scores'].items():
    bar = '█' * int(score / 10) + '░' * (10 - int(score / 10))
    print(f"  {section:15} {bar} {score:3.0f}")
```

---

## SkillGapAnalyzer

Analyze missing skills.

### Initialization
```python
from core import SkillGapAnalyzer

analyzer = SkillGapAnalyzer()
```

### Methods

**`analyze_gap(extracted_skills: List[str], job_role: str) -> Dict`**
```python
gap = analyzer.analyze_gap(['Python', 'Git', 'SQL'], 'Full Stack Developer')
# Returns: {
#   'critical_missing': ['JavaScript', 'React'],
#   'recommended_missing': ['Docker', 'CI/CD'],
#   'bonus_missing': ['Microservices'],
#   'matched_skills': ['Python', 'Git', 'SQL'],
#   'total_gap_days': 60
# }
```

**`get_prioritized_roadmap() -> List[Dict]`**
```python
roadmap = analyzer.get_prioritized_roadmap()
for item in roadmap:
    print(f"{item['skill']} ({item['priority']}) - {item['estimated_days']} days")
    for resource in item['suggested_resources']:
        print(f"  • {resource['name']} ({resource['type']})")
```

**`get_gap_summary() -> Dict`**
```python
summary = analyzer.get_gap_summary()
print(f"Critical gaps: {summary['critical_gaps']}")
print(f"Total missing: {summary['total_missing_skills']}")
print(f"Learning time: {summary['estimated_learning_weeks']} weeks")
```

### Example: Complete Gap Analysis
```python
analyzer = SkillGapAnalyzer()
current_skills = ['Python', 'Git', 'SQL', 'HTML']
target_job = 'Full Stack Developer'

gap = analyzer.analyze_gap(current_skills, target_job)
summary = analyzer.get_gap_summary()

print("=== SKILL GAP ANALYSIS ===")
print(f"\nMatched Skills: {len(gap['matched_skills'])}")
for skill in gap['matched_skills']:
    print(f"  ✓ {skill}")

print(f"\nCritical Skills to Learn: {len(gap['critical_missing'])}")
for skill in gap['critical_missing']:
    print(f"  ! {skill}")

print(f"\nTotal Learning Time: {summary['estimated_learning_weeks']} weeks")
print(f"This is approximately {summary['estimated_learning_months']} months")
```

---

## JobMatcher

Match resume to job descriptions.

### Initialization
```python
from core import JobMatcher

matcher = JobMatcher()
```

### Methods

**`extract_skills_from_job_description(text: str) -> Dict`**
```python
job_desc = "We need Python developer with React, Docker, AWS..."
skills = matcher.extract_skills_from_job_description(job_desc)
# Returns: {
#   'required': ['Python', 'React', 'Docker', 'AWS'],
#   'nice_to_have': [],
#   'tools': [],
#   'soft_skills': []
# }
```

**`calculate_similarity(resume_skills, job_skills) -> Dict`**
```python
similarity = matcher.calculate_similarity(
    ['Python', 'React', 'Git'],
    {
        'required': ['Python', 'React', 'Docker'],
        'nice_to_have': [],
        'tools': ['Git', 'AWS']
    }
)
# Calculates match percentage and details
```

**`get_match_report(resume_skills, job_title, job_description) -> Dict`**
```python
report = matcher.get_match_report(
    my_skills=['Python', 'React', 'SQL'],
    job_title='Full Stack Developer',
    job_description="Python expert with React and Docker..."
)
# Returns complete matching report
```

### Example: Job Matching
```python
matcher = JobMatcher()
job_description = """
Full Stack Developer Required:
- Python or Node.js
- React or Vue.js
- SQL or MongoDB
- Docker
- Git
- AWS or Azure

Nice to have:
- Kubernetes
- GraphQL
- Microservices
"""

my_skills = ['Python', 'React', 'MySQL', 'Git', 'Linux']

report = matcher.get_match_report(
    my_skills,
    'Full Stack Developer - E-commerce Platform',
    job_description
)

print(f"Match Score: {report['overall_match_score']:.1f}%")
print(f"Fit Assessment: {report['fit_assessment']}")
print(f"\nMatched: {len(report['matched_skills']['required'])} critical skills")
print(f"Missing: {len(report['missing_skills']['required'])} critical skills")
print("\nRecommendations:")
for rec in report['recommendations']:
    print(f"  • {rec}")
```

---

## ResumeImprover

Get resume improvement suggestions.

### Initialization
```python
from core import ResumeImprover

improver = ResumeImprover()
```

### Methods

**`analyze_resume(text: str) -> Dict`**
```python
analysis = improver.analyze_resume(resume_text)
# Returns improvement opportunities
```

**`rewrite_bullet_point(bullet: str) -> str`**
```python
weak_bullet = "- worked on project with Python and React"
strong_bullet = improver.rewrite_bullet_point(weak_bullet)
# "Developed web application using Python and React..."
```

**`add_metrics(bullet: str) -> str`**
```python
bullet = "Improved website performance"
with_metrics = improver.add_metrics(bullet)
# "Improved website performance (40% faster example)"
```

**`get_improvement_suggestions(text: str) -> Dict`**
```python
suggestions = improver.get_improvement_suggestions(resume_text)
# Returns quick wins, medium, and major improvements
```

### Example: Improve Resume
```python
improver = ResumeImprover()
suggestions = improver.get_improvement_suggestions(resume_text)

print("=== RESUME IMPROVEMENTS ===")

print("\n🟢 QUICK WINS:")
for item in suggestions['quick_wins']:
    print(f"\n{item['title']}")
    for problem in item['items']:
        print(f"  ✗ {problem['phrase']} (found {problem['count']} times)")

print("\n🟡 MEDIUM IMPROVEMENTS:")
for item in suggestions['medium_improvements']:
    print(f"\n{item['title']}")
    for weak, strong in item['items']:
        print(f"  Replace '{weak}' → '{strong}'")

print("\n🔴 MAJOR REVISIONS:")
for item in suggestions['major_revisions']:
    print(f"\n{item['title']}")
    print(f"  {item['description']}")
    for example in item['examples']:
        print(f"    {example}")
```

---

## InterviewGenerator

Generate and evaluate interview questions.

### Initialization
```python
from core import InterviewGenerator

interview = InterviewGenerator('Full Stack Developer')
```

### Methods

**`get_question(category: str = None) -> str`**
```python
q1 = interview.get_question('behavioral')
q2 = interview.get_question('technical')
q3 = interview.get_question()  # Random category
```

**`get_multiple_questions(count: int, mix: List[str]) -> List[str]`**
```python
questions = interview.get_multiple_questions(
    count=5,
    mix=['behavioral', 'technical', 'situational']
)
for i, q in enumerate(questions, 1):
    print(f"{i}. {q}")
```

**`evaluate_response(answer: str) -> Dict`**
```python
answer = "I built a React app that helped increase productivity by 30% using..."
evaluation = interview.evaluate_response(answer)
# Returns score, feedback, strengths, improvements
```

### Example: Mock Interview
```python
interview = InterviewGenerator('Data Scientist')

# Get all questions
questions = interview.get_multiple_questions(5)

# Simulate interview
print("=== MOCK INTERVIEW ===\n")
for i, question in enumerate(questions, 1):
    print(f"Question {i}: {question}\n")
    
    # User would answer here
    answer = "My answer would be here..."
    
    # Evaluate
    eval_result = interview.evaluate_response(answer)
    print(f"Score: {eval_result['overall_score']}/100")
    print(f"Feedback: {eval_result['feedback']}\n")

# Get summary
summary = interview.get_performance_summary()
print(f"\nAverage Score: {summary['average_score']}/100")
print(f"Feedback: {summary['overall_feedback']}")
```

---

## RoadmapGenerator

Create learning roadmaps.

### Initialization
```python
from core import RoadmapGenerator

roadmap_gen = RoadmapGenerator()
```

### Methods

**`generate_learning_roadmap(skill_gaps, hours_per_week) -> List[Dict]`**
```python
roadmap = roadmap_gen.generate_learning_roadmap(
    skill_gaps=[
        {'skill': 'React', 'priority': 'CRITICAL', 'estimated_days': 20},
        {'skill': 'Docker', 'priority': 'RECOMMENDED', 'estimated_days': 15}
    ],
    hours_per_week=15
)
```

**`generate_career_timeline(target_role, skill_gaps) -> Dict`**
```python
timeline = roadmap_gen.generate_career_timeline(
    'Full Stack Developer',
    skill_gaps
)
# Shows phases with milestones
```

**`generate_weekly_plan(roadmap) -> Dict`**
```python
weekly = roadmap_gen.generate_weekly_plan(roadmap)
for week, tasks in weekly.items():
    print(f"\nWeek {week}:")
    print(f"  Hours: {tasks['total_hours']}")
    print(f"  Skills: {', '.join(tasks['skills_covered'])}")
    for task in tasks['tasks']:
        print(f"  • {task['task']} ({task['hours']} hrs)")
```

### Example: Learning Roadmap
```python
g = SkillGapAnalyzer()
gap = g.analyze_gap(['Python', 'Git'], 'Full Stack Developer')
roadmap_info = g.get_gap_summary()

rm = RoadmapGenerator()
roadmap = rm.generate_learning_roadmap(
    roadmap_info['priority_roadmap'],
    hours_per_week=20
)
timeline = rm.generate_career_timeline('Full Stack Developer', roadmap_info['priority_roadmap'])

print("=== YOUR LEARNING JOURNEY ===")
for milestone in timeline['milestones']:
    print(f"\nPhase {milestone['phase']}: {milestone['name']}")
    print(f"  Duration: {milestone['duration_weeks']} weeks")
    print(f"  Skills: {', '.join(milestone['skills'])}")
```

---

## CareerSimulator

Simulate career outcomes.

### Initialization
```python
from core import CareerSimulator

sim = CareerSimulator()
```

### Methods

**`estimate_job_readiness(...) -> Dict`**
```python
readiness = sim.estimate_job_readiness(
    missing_skills_count=8,
    ats_score=65,
    experience_years=2
)
# Returns readiness score and timeline
```

**`generate_multiple_scenarios(...) -> List[Dict]`**
```python
scenarios = sim.generate_multiple_scenarios(
    skill_gaps=[...],
    ats_score=75,
    experience_years=2
)
# Returns fast/average/slow learner scenarios
```

**`simulate_job_hunt(readiness_score, applications) -> Dict`**
```python
hunt = sim.simulate_job_hunt(readiness_score=75, applications=100)
print(f"Expected offers: {hunt['estimated_offers']}")
```

### Example: Career Simulation
```python
sim = CareerSimulator()

readiness = sim.estimate_job_readiness(5, 72, 2)
print(f"Current Readiness: {readiness['current_readiness_score']}/100")
print(f" Status: {readiness['status']}")
print(f"Weeks to Job-Ready: {readiness['estimated_weeks_to_ready']}")

scenarios = sim.generate_multiple_scenarios([], 72, 2)
print("\n=== SCENARIOS ===")
for scenario in scenarios:
    print(f"\n{scenario['name']} ({scenario['daily_hours']} hrs/day)")
    print(f"  Timeline: {scenario['total_timeline']['weeks']} weeks")
    print(f"  Readiness: {scenario['estimated_readiness_score']}/100")
    print(f"  Success Rate: {scenario['success_probability']:.0f}%")

hunt = sim.simulate_job_hunt(readiness['current_readiness_score'])
print(f"\n=== JOB SEARCH ===")
print(f"Applications: {hunt['estimated_applications']}")
print(f"Callbacks: {hunt['estimated_callbacks']}")
print(f"Interviews: {hunt['estimated_interviews']}")
print(f"Offers: {hunt['estimated_offers']}")
```

---

## RecruiterView

See from recruiter perspective.

### Initialization
```python
from core import RecruiterView

rv = RecruiterView()
```

### Methods

**`calculate_first_impression(...) -> Dict`**
```python
impression = rv.calculate_first_impression(
    resume_data, ats_score=75, skills=['Python', 'React']
)
# What recruiter thinks in 6-15 seconds
```

**`calculate_hire_probability(...) -> Dict`**
```python
prob = rv.calculate_hire_probability(
    ats_score=75,
    experience_match=0.8,
    skill_match=0.7
)
# Hiring likelihood
```

**`generate_recruiter_feedback(...) -> Dict`**
```python
feedback = rv.generate_recruiter_feedback(
    resume_data, skills, ats_score=75, hire_probability=68
)
# Complete recruiter view
```

### Example: Recruiter Analysis
```python
rv = RecruiterView()

impression = rv.calculate_first_impression(data, 78, ['Python','React','Docker'])
print(f"First Impression Score: {impression['impression_score']}/100")
print(f"Initial Reaction: {impression['initial_reaction']}")

feedback = rv.generate_recruiter_feedback(
    data, ['Python','React','Docker'], 78, 68
)
print("\n= STRENGTHS =)
for strength in feedback['strengths']:
    print(f"✓ {strength}")

print("\n=== CONCERNS ===")
for concern in feedback['concerns']:
    print(f"✗ {concern}")

print(f"\nHire Probability: {feedback['hire_probability']}")
print(f"Decision: {feedback['hiring_decision']}")
```

---

## Complete Pipeline Example

```python
from main import RACSSystem

# Initialize system
racgs = RACSSystem()

# Analyze resume
results = racgs.analyze_resume('resume.pdf', 'Full Stack Developer')

# Access each module's results
ats_result = results['ats_analysis']
skills_result = results['skills_analysis']
gaps_result = results['skill_gaps']
roadmap_result = results['learning_roadmap']
recruiter_result = results['recruiter_perspective']

# Use results
print("=== ANALYSIS COMPLETE ===")
print(f"ATS Score: {ats_result['total_score']}")
print(f"Skills Found: {len(skills_result['extracted_skills'])}")
print(f"Missing Skills: {gaps_result['total_missing_skills']}")
print(f"Learning Time: {gaps_result['estimated_learning_weeks']} weeks")
print(f"Hire Probability: {recruiter_result['hire_probability']['hire_probability_percentage']}%")
```

---

**For more information, see SYSTEM_ARCHITECTURE.md**
