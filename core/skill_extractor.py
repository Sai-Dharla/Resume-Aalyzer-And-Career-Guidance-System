"""
Skill Extractor Module
Matches resume text against predefined skills database
Identifies technical and soft skills
"""

import json
import os
import re
from typing import List, Dict, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SkillExtractor:
    """Extract and match skills from resume"""
    
    def __init__(self, skills_db_path: str = None):
        """
        Initialize skill extractor with skills database
        
        Args:
            skills_db_path: Path to skills database JSON file
        """
        self.skills_db = {}
        self.extracted_skills = []
        
        if skills_db_path is None:
            # Default path relative to this module
            skills_db_path = os.path.join(
                os.path.dirname(__file__),
                '../data/skills_database.json'
            )
        
        self.load_skills_database(skills_db_path)
    
    def load_skills_database(self, file_path: str):
        """
        Load skills database from JSON file
        
        Args:
            file_path: Path to skills database JSON
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    self.skills_db = json.load(f)
            else:
                logger.warning(f"Skills database not found at {file_path}")
                self.load_default_skills_database()
        except Exception as e:
            logger.error(f"Error loading skills database: {str(e)}")
            self.load_default_skills_database()
    
    def load_default_skills_database(self):
        """Load default skills database if file not available"""
        self.skills_db = {
            'programming_languages': [
                'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby',
                'Go', 'Rust', 'TypeScript', 'R', 'MATLAB', 'Kotlin', 'Swift'
            ],
            'web_development': [
                'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js',
                'Express', 'Flask', 'Django', 'ASP.NET', 'Spring'
            ],
            'databases': [
                'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis',
                'Oracle', 'SQLite', 'Cassandra', 'Elasticsearch'
            ],
            'cloud_devops': [
                'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes',
                'CI/CD', 'Jenkins', 'GitLab CI', 'Terraform', 'CloudFormation'
            ],
            'data_science': [
                'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch',
                'Pandas', 'NumPy', 'Scikit-learn', 'Data Analysis', 'Statistics'
            ],
            'soft_skills': [
                'Communication', 'Leadership', 'Problem Solving', 'Teamwork',
                'Project Management', 'Analytical', 'Critical Thinking'
            ]
        }
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills from text by matching against skills database
        
        Args:
            text: Resume text to analyze
            
        Returns:
            Dictionary with skills grouped by category
        """
        extracted = {
            'programming_languages': [],
            'web_development': [],
            'databases': [],
            'cloud_devops': [],
            'data_science': [],
            'soft_skills': [],
            'other': []
        }
        
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Search for skills in each category
        for category, skills in self.skills_db.items():
            if category in extracted:
                for skill in skills:
                    # Create pattern for skill matching
                    pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                    if re.search(pattern, text_lower):
                        extracted[category].append(skill)
        
        self.extracted_skills = extracted
        return extracted
    
    def get_all_skills(self) -> List[str]:
        """
        Get flat list of all extracted skills
        
        Returns:
            List of all extracted skills
        """
        all_skills = []
        for category, skills in self.extracted_skills.items():
            all_skills.extend(skills)
        return list(set(all_skills))  # Remove duplicates
    
    def get_skills_by_category(self) -> Dict[str, List[str]]:
        """
        Get extracted skills organized by category
        
        Returns:
            Dictionary with skills grouped by category
        """
        return self.extracted_skills
    
    def get_skill_categories(self) -> List[str]:
        """
        Get list of available skill categories
        
        Returns:
            List of skill categories
        """
        return list(self.skills_db.keys())
    
    def add_custom_skill(self, skill: str, category: str = 'other'):
        """
        Add custom skill to database
        
        Args:
            skill: Skill name to add
            category: Skill category
        """
        if category not in self.skills_db:
            self.skills_db[category] = []
        
        if skill not in self.skills_db[category]:
            self.skills_db[category].append(skill)
    
    def find_skill_similarity(self, text: str, threshold: float = 0.7) -> List[Tuple[str, float]]:
        """
        Find skills with partial/fuzzy matching
        
        Args:
            text: Text to search in
            threshold: Similarity threshold (0-1)
            
        Returns:
            List of (skill, similarity_score) tuples
        """
        similar_skills = []
        text_lower = text.lower()
        words = text_lower.split()
        
        for category, skills in self.skills_db.items():
            for skill in skills:
                skill_lower = skill.lower()
                # Simple substring matching (more sophisticated matching could use difflib)
                if skill_lower in text_lower:
                    similar_skills.append((skill, 1.0))
                else:
                    # Check for partial matches
                    skill_words = skill_lower.split()
                    matches = sum(1 for word in skill_words if word in text_lower)
                    if matches > 0:
                        similarity = matches / len(skill_words)
                        if similarity >= threshold:
                            similar_skills.append((skill, similarity))
        
        # Remove duplicates and sort by similarity
        seen = set()
        result = []
        for skill, score in sorted(similar_skills, key=lambda x: x[1], reverse=True):
            if skill not in seen:
                result.append((skill, score))
                seen.add(skill)
        
        return result
