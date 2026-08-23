"""
Skill Gap Analyzer Module
Identifies missing skills and creates prioritized learning paths
"""

from typing import List, Dict, Tuple
import json
import os
import logging

logger = logging.getLogger(__name__)


class SkillGapAnalyzer:
    """Analyze skill gaps and create learning recommendations"""
    
    def __init__(self, job_roles_db_path: str = None):
        """
        Initialize skill gap analyzer
        
        Args:
            job_roles_db_path: Path to job roles database
        """
        self.job_roles_db = {}
        self.skill_gaps = []
        self.learning_time = {}
        
        if job_roles_db_path is None:
            job_roles_db_path = os.path.join(
                os.path.dirname(__file__),
                '../data/job_roles.json'
            )
        
        self.load_job_roles_database(job_roles_db_path)
    
    def load_job_roles_database(self, file_path: str):
        """Load job roles database"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    self.job_roles_db = json.load(f)
            else:
                logger.warning(f"Job roles database not found at {file_path}")
                self.load_default_job_roles()
        except Exception as e:
            logger.error(f"Error loading job roles: {str(e)}")
            self.load_default_job_roles()
    
    def load_default_job_roles(self):
        """Load default job roles if database unavailable"""
        self.job_roles_db = {
            'Junior Software Developer': {
                'critical': ['Python/Java', 'Git', 'SQL', 'OOP'],
                'recommended': ['HTML/CSS', 'JavaScript', 'Unit Testing'],
                'bonus': ['Docker', 'CI/CD', 'AWS']
            },
            'Full Stack Developer': {
                'critical': ['JavaScript', 'React/Vue', 'Node.js', 'SQL', 'REST API'],
                'recommended': ['Docker', 'Git', 'NoSQL', 'Authentication'],
                'bonus': ['GraphQL', 'Microservices', 'AWS']
            },
            'Data Scientist': {
                'critical': ['Python', 'pandas', 'NumPy', 'Statistics', 'Machine Learning'],
                'recommended': ['SQL', 'Data Visualization', 'Scikit-learn'],
                'bonus': ['TensorFlow', 'Deep Learning', 'Big Data']
            },
            'Cloud Architect': {
                'critical': ['AWS/Azure', 'Docker', 'Kubernetes', 'Networking'],
                'recommended': ['Terraform', 'CI/CD', 'Linux', 'Security'],
                'bonus': ['Multi-cloud', 'Serverless', 'Advanced Networking']
            },
            'DevOps Engineer': {
                'critical': ['Linux', 'Docker', 'Kubernetes', 'CI/CD', 'Git'],
                'recommended': ['Terraform', 'Ansible', 'Monitoring', 'Python'],
                'bonus': ['Advanced AWS', 'ArgoCD', 'Performance Tuning']
            }
        }
    
    def get_skill_requirements(self, job_role: str) -> Dict[str, List[str]]:
        """
        Get skill requirements for specific job role
        
        Args:
            job_role: Target job role
            
        Returns:
            Dictionary of required skills by category
        """
        if job_role in self.job_roles_db:
            return self.job_roles_db[job_role]
        
        # Try fuzzy matching
        for role in self.job_roles_db.keys():
            if job_role.lower() in role.lower() or role.lower() in job_role.lower():
                return self.job_roles_db[role]
        
        logger.warning(f"Job role '{job_role}' not found in database")
        return {'critical': [], 'recommended': [], 'bonus': []}
    
    def analyze_gap(self, extracted_skills: List[str], 
                   job_role: str) -> Dict:
        """
        Analyze skill gap between current skills and target role
        
        Args:
            extracted_skills: List of skills extracted from resume
            job_role: Target job role
            
        Returns:
            Dictionary with gap analysis
        """
        requirements = self.get_skill_requirements(job_role)
        
        # Normalize skill names for comparison
        current_skills_lower = [s.lower() for s in extracted_skills]
        
        gap_analysis = {
            'critical_missing': [],
            'recommended_missing': [],
            'bonus_missing': [],
            'matched_skills': [],
            'total_gap_days': 0
        }
        
        # Check critical skills
        for skill in requirements.get('critical', []):
            if not self._skill_matched(skill, current_skills_lower):
                gap_analysis['critical_missing'].append(skill)
            else:
                gap_analysis['matched_skills'].append(skill)
        
        # Check recommended skills
        for skill in requirements.get('recommended', []):
            if not self._skill_matched(skill, current_skills_lower):
                gap_analysis['recommended_missing'].append(skill)
            else:
                gap_analysis['matched_skills'].append(skill)
        
        # Check bonus skills
        for skill in requirements.get('bonus', []):
            if not self._skill_matched(skill, current_skills_lower):
                gap_analysis['bonus_missing'].append(skill)
            else:
                gap_analysis['matched_skills'].append(skill)
        
        self.skill_gaps = gap_analysis
        self._calculate_learning_time()
        
        return gap_analysis
    
    def _skill_matched(self, required_skill: str, extracted_skills_lower: List[str]) -> bool:
        """Check if required skill is in extracted skills"""
        required_lower = required_skill.lower()
        
        for extracted in extracted_skills_lower:
            if required_lower in extracted or extracted in required_lower:
                return True
        
        return False
    
    def _calculate_learning_time(self):
        """Calculate learning time for missing skills"""
        # Default learning times (in days) for skill categories
        learning_times = {
            'programming_languages': 30,
            'database': 20,
            'cloud': 25,
            'devops': 30,
            'data_science': 45,
            'web_framework': 25,
            'tool': 15,
            'default': 20
        }
        
        self.learning_time = {
            'critical': 0,
            'recommended': 0,
            'bonus': 0,
            'breakdown': {}
        }
        
        # Calculate time for critical skills
        for skill in self.skill_gaps.get('critical_missing', []):
            days = self._estimate_skill_learning_time(skill, learning_times)
            self.learning_time['critical'] += days
            self.learning_time['breakdown'][skill] = days
        
        # Calculate time for recommended skills
        for skill in self.skill_gaps.get('recommended_missing', []):
            days = self._estimate_skill_learning_time(skill, learning_times)
            self.learning_time['recommended'] += days
            self.learning_time['breakdown'][skill] = days
        
        # Calculate time for bonus skills
        for skill in self.skill_gaps.get('bonus_missing', []):
            days = self._estimate_skill_learning_time(skill, learning_times)
            self.learning_time['bonus'] += days
            self.learning_time['breakdown'][skill] = days
    
    def _estimate_skill_learning_time(self, skill: str, learning_times: Dict) -> int:
        """Estimate learning time for a skill"""
        skill_lower = skill.lower()
        
        for category, days in learning_times.items():
            if category != 'default' and category in skill_lower:
                return days
        
        return learning_times['default']
    
    def get_prioritized_roadmap(self) -> List[Dict]:
        """
        Get prioritized list of skills to learn
        
        Returns:
            List of skills sorted by priority and learning time
        """
        roadmap = []
        priority_order = ['critical', 'recommended', 'bonus']
        
        for priority in priority_order:
            for skill in self.skill_gaps.get(f'{priority}_missing', []):
                learning_days = self.learning_time['breakdown'].get(skill, 20)
                roadmap.append({
                    'skill': skill,
                    'priority': priority.upper(),
                    'estimated_days': learning_days,
                    'importance': self._get_importance_score(priority),
                    'suggested_resources': self._get_resources_for_skill(skill)
                })
        
        return roadmap
    
    def _get_importance_score(self, priority: str) -> int:
        """Get importance score for priority level"""
        scores = {
            'critical': 10,
            'recommended': 7,
            'bonus': 5
        }
        return scores.get(priority, 5)
    
    def _get_resources_for_skill(self, skill: str) -> List[Dict]:
        """Get learning resources for skill"""
        resources_map = {
            'python': [
                {'name': 'Python Official Docs', 'type': 'documentation'},
                {'name': 'Real Python Tutorials', 'type': 'tutorial'},
                {'name': 'Codecademy Python Course', 'type': 'course'}
            ],
            'javascript': [
                {'name': 'MDN Web Docs', 'type': 'documentation'},
                {'name': 'Eloquent JavaScript', 'type': 'book'},
                {'name': 'freeCodeCamp JavaScript', 'type': 'tutorial'}
            ],
            'react': [
                {'name': 'React Official Docs', 'type': 'documentation'},
                {'name': 'React Tutorial - Todo App', 'type': 'tutorial'},
                {'name': 'Scrimba React Course', 'type': 'course'}
            ],
            'sql': [
                {'name': 'SQL Tutorial W3Schools', 'type': 'tutorial'},
                {'name': 'PostgreSQL Documentation', 'type': 'documentation'},
                {'name': 'Mode Analytics SQL Tutorial', 'type': 'tutorial'}
            ],
            'docker': [
                {'name': 'Docker Official Docs', 'type': 'documentation'},
                {'name': 'Docker Tutorial for Beginners', 'type': 'tutorial'},
                {'name': 'Play with Docker', 'type': 'interactive'}
            ]
        }
        
        skill_lower = skill.lower()
        for key in resources_map.keys():
            if key in skill_lower:
                return resources_map[key]
        
        # Return generic resources
        return [
            {'name': f'{skill} Official Documentation', 'type': 'documentation'},
            {'name': f'Free courses on {skill}', 'type': 'course'},
            {'name': f'{skill} YouTube tutorials', 'type': 'video'}
        ]
    
    def get_gap_summary(self) -> Dict:
        """Get summary of skill gaps"""
        critical_count = len(self.skill_gaps.get('critical_missing', []))
        recommended_count = len(self.skill_gaps.get('recommended_missing', []))
        bonus_count = len(self.skill_gaps.get('bonus_missing', []))
        total_days = sum(self.learning_time.get('breakdown', {}).values())
        
        return {
            'critical_gaps': critical_count,
            'recommended_gaps': recommended_count,
            'bonus_gaps': bonus_count,
            'total_missing_skills': critical_count + recommended_count + bonus_count,
            'estimated_learning_time_days': total_days,
            'estimated_learning_weeks': total_days / 7,
            'matched_skills_count': len(self.skill_gaps.get('matched_skills', [])),
            'priority_roadmap': self.get_prioritized_roadmap()
        }
