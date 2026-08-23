"""
ATS (Applicant Tracking System) Scorer Module
Calculates resume compatibility score and section-wise scoring
"""

from typing import Dict, List
import logging
import re

logger = logging.getLogger(__name__)


class ATSScorer:
    """Calculate ATS score and detailed section analysis"""
    
    # Scoring weights
    WEIGHTS = {
        'skills': 0.30,
        'projects': 0.20,
        'experience': 0.25,
        'education': 0.15,
        'formatting': 0.10
    }
    
    def __init__(self):
        """Initialize ATS scorer"""
        self.scores = {
            'skills': 0,
            'projects': 0,
            'experience': 0,
            'education': 0,
            'formatting': 0,
            'total': 0
        }
        self.details = {}
    
    def score_skills_section(self, extracted_skills: Dict[str, List[str]], 
                            required_skills: List[str] = None) -> float:
        """
        Score skills section (30% weight)
        
        Args:
            extracted_skills: Dictionary of extracted skills by category
            required_skills: List of required skills for comparison
            
        Returns:
            Skills score (0-100)
        """
        score = 0
        total_skills = sum(len(skills) for skills in extracted_skills.values())
        
        # Base score from skill count
        if total_skills > 0:
            score += min(50, total_skills * 2)  # Max 50 points from skill count
        
        # Bonus if skills are diverse (multiple categories)
        categories_with_skills = sum(1 for skills in extracted_skills.values() if skills)
        if categories_with_skills >= 3:
            score += 30
        elif categories_with_skills >= 2:
            score += 15
        
        # Match against required skills if provided
        if required_skills:
            all_extracted = []
            for skills in extracted_skills.values():
                all_extracted.extend(skills)
            
            matches = sum(1 for req in required_skills 
                         if any(req.lower() in skill.lower() for skill in all_extracted))
            match_percentage = (matches / len(required_skills)) * 100 if required_skills else 0
            
            if match_percentage >= 80:
                score += 20
            elif match_percentage >= 60:
                score += 15
            elif match_percentage >= 40:
                score += 10
        
        score = min(100, score)  # Cap at 100
        self.scores['skills'] = score
        self.details['skills'] = {
            'total_skills': total_skills,
            'categories': categories_with_skills,
            'score': score
        }
        return score
    
    def score_projects_section(self, projects: List[Dict]) -> float:
        """
        Score projects section (20% weight)
        
        Args:
            projects: List of project entries
            
        Returns:
            Projects score (0-100)
        """
        score = 0
        
        if not projects:
            self.scores['projects'] = 0
            self.details['projects'] = {'count': 0, 'score': 0}
            return 0
        
        # Score based on number of projects
        project_count = len(projects)
        score += min(40, project_count * 15)  # Max 40 points
        
        # Check quality indicators
        quality_indicators = ['github', 'deployed', 'live', 'production', 'open source']
        quality_count = 0
        
        for project in projects:
            project_text = str(project).lower()
            for indicator in quality_indicators:
                if indicator in project_text:
                    quality_count += 1
                    break
        
        if quality_count > 0:
            score += (quality_count / max(1, project_count)) * 30  # Max 30 bonus points
        
        # Check for measurable results/metrics
        metric_keywords = ['increased', 'reduced', 'improved', 'optimized', '%', 'x faster']
        metrics_found = 0
        
        for project in projects:
            project_text = str(project).lower()
            for keyword in metric_keywords:
                if keyword in project_text:
                    metrics_found += 1
                    break
        
        if metrics_found > 0:
            score += (metrics_found / max(1, project_count)) * 30  # Max 30 bonus points
        
        score = min(100, score)
        self.scores['projects'] = score
        self.details['projects'] = {
            'count': project_count,
            'quality_count': quality_count,
            'metrics_found': metrics_found,
            'score': score
        }
        return score
    
    def score_experience_section(self, experience: List[Dict]) -> float:
        """
        Score experience section (25% weight)
        
        Args:
            experience: List of experience entries
            
        Returns:
            Experience score (0-100)
        """
        score = 0
        
        if not experience:
            self.scores['experience'] = 0
            self.details['experience'] = {'count': 0, 'years': 0, 'score': 0}
            return 0
        
        # Score based on number of positions
        exp_count = len(experience)
        score += min(30, exp_count * 15)  # Max 30 points
        
        # Calculate years of experience
        total_years = 0
        for exp in experience:
            years = self._calculate_years_of_experience(exp.get('duration', ''))
            total_years += years
        
        # Score based on years
        if total_years >= 5:
            score += 40
        elif total_years >= 3:
            score += 30
        elif total_years >= 1:
            score += 20
        else:
            score += 10
        
        # Check for achievement indicators
        achievement_keywords = ['led', 'managed', 'developed', 'increased', 'reduced',
                               'optimized', 'led team', 'delivered']
        achievements = 0
        
        for exp in experience:
            exp_text = str(exp).lower()
            for keyword in achievement_keywords:
                if keyword in exp_text:
                    achievements += 1
                    break
        
        if achievements > 0:
            score += (achievements / max(1, exp_count)) * 30
        
        score = min(100, score)
        self.scores['experience'] = score
        self.details['experience'] = {
            'count': exp_count,
            'years': total_years,
            'achievements': achievements,
            'score': score
        }
        return score
    
    def score_education_section(self, education: List[Dict]) -> float:
        """
        Score education section (15% weight)
        
        Args:
            education: List of education entries
            
        Returns:
            Education score (0-100)
        """
        score = 50  # Base score for having education
        
        if not education:
            self.scores['education'] = 30
            self.details['education'] = {'count': 0, 'highest_degree': 'None', 'score': 30}
            return 30
        
        # Score based on degree level
        degree_scores = {
            'phd': 100,
            'master': 90,
            'bachelor': 75,
            'associate': 60,
            'diploma': 40
        }
        
        highest_score = 50
        highest_degree = 'Other'
        
        for edu in education:
            degree_text = str(edu.get('degree', '')).lower()
            for degree, degree_score in degree_scores.items():
                if degree in degree_text:
                    if degree_score > highest_score:
                        highest_score = degree_score
                        highest_degree = degree.title()
                    break
        
        score += highest_score
        
        # Bonus for certifications/specialized degrees
        if 'specialization' in str(education).lower():
            score += 15
        
        score = min(100, score)
        self.scores['education'] = score
        self.details['education'] = {
            'count': len(education),
            'highest_degree': highest_degree,
            'score': score
        }
        return score
    
    def score_formatting(self, text: str) -> float:
        """
        Score formatting (10% weight)
        
        Args:
            text: Resume text
            
        Returns:
            Formatting score (0-100)
        """
        score = 50  # Base score
        
        # Check for proper structure
        section_keywords = ['experience', 'education', 'skills', 'projects']
        sections_found = sum(1 for keyword in section_keywords 
                            if keyword in text.lower())
        
        if sections_found >= 3:
            score += 30
        elif sections_found >= 2:
            score += 15
        
        # Check for contact information
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            score += 10
        
        # Check for proper formatting (not too long)
        lines = text.split('\n')
        if len(lines) < 500:  # Reasonable resume length
            score += 10
        
        score = min(100, score)
        self.scores['formatting'] = score
        self.details['formatting'] = {
            'sections_found': sections_found,
            'has_contact': bool(re.search(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
            'score': score
        }
        return score
    
    def calculate_ats_score(self, extracted_skills: Dict[str, List[str]],
                           projects: List[Dict],
                           experience: List[Dict],
                           education: List[Dict],
                           text: str,
                           required_skills: List[str] = None) -> Dict:
        """
        Calculate complete ATS score
        
        Args:
            extracted_skills: Extracted skills
            projects: Project entries
            experience: Experience entries
            education: Education entries
            text: Full resume text
            required_skills: Optional list of required skills
            
        Returns:
            Dictionary with detailed ATS scores
        """
        # Calculate section scores
        self.score_skills_section(extracted_skills, required_skills)
        self.score_projects_section(projects)
        self.score_experience_section(experience)
        self.score_education_section(education)
        self.score_formatting(text)
        
        # Calculate weighted total
        total_score = (
            self.scores['skills'] * self.WEIGHTS['skills'] +
            self.scores['projects'] * self.WEIGHTS['projects'] +
            self.scores['experience'] * self.WEIGHTS['experience'] +
            self.scores['education'] * self.WEIGHTS['education'] +
            self.scores['formatting'] * self.WEIGHTS['formatting']
        )
        
        self.scores['total'] = round(total_score, 2)
        
        return {
            'total_score': self.scores['total'],
            'section_scores': {
                'skills': self.scores['skills'],
                'projects': self.scores['projects'],
                'experience': self.scores['experience'],
                'education': self.scores['education'],
                'formatting': self.scores['formatting']
            },
            'details': self.details
        }
    
    @staticmethod
    def _calculate_years_of_experience(duration_str: str) -> float:
        """Calculate years from duration string"""
        import re
        from datetime import datetime
        
        # Try to find year patterns
        years = re.findall(r'\b(20\d{2})\b', duration_str)
        
        if len(years) >= 2:
            try:
                return float(years[-1]) - float(years[0])
            except:
                pass
        
        # If no years found, return 0
        return 0
    
    def get_ats_score(self) -> float:
        """Get current ATS score"""
        return self.scores['total']
    
    def get_scores_breakdown(self) -> Dict:
        """Get complete scores breakdown"""
        return {
            'scores': self.scores,
            'details': self.details
        }
