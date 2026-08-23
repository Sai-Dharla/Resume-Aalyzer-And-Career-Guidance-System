"""
Recruiter View Module
Provides recruiter perspective and hiring analysis
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class RecruiterView:
    """Analyze resume from recruiter's perspective"""
    
    def __init__(self):
        """Initialize recruiter view"""
        self.first_impression = {}
        self.hire_probability = 0
    
    def calculate_first_impression(self, resume_data: Dict,
                                  ats_score: float,
                                  skills: List[str]) -> Dict:
        """
        Calculate first impression metrics (6-15 seconds review)
        
        Args:
            resume_data: Processed resume data
            ats_score: ATS score from analysis
            skills: Extracted skills
            
        Returns:
            First impression assessment
        """
        impression = {
            'time_to_review_seconds': 8,
            'elements_reviewed': [],
            'initial_reaction': '',
            'key_takeaway': '',
            'concerns': [],
            'positives': [],
            'impression_score': 0
        }
        
        score = 50  # Base score
        
        # Check contact information
        contact = resume_data.get('contact', {})
        if contact.get('email') and contact['email'] != 'Not found':
            impression['positives'].append('Professional email provided')
            score += 10
            impression['elements_reviewed'].append('Contact Info')
        else:
            impression['concerns'].append('Missing email address')
            score -= 10
        
        # Check experience
        experience = resume_data.get('experience', [])
        if len(experience) >= 2:
            impression['positives'].append('Relevant work experience')
            score += 15
        elif len(experience) == 1:
            impression['positives'].append('Some work experience')
            score += 5
        else:
            impression['concerns'].append('Limited work experience')
            score -= 5
        impression['elements_reviewed'].append('Experience')
        
        # Check education
        education = resume_data.get('education', [])
        if education:
            impression['positives'].append('Educational background listed')
            score += 10
        impression['elements_reviewed'].append('Education')
        
        # Check skills
        if len(skills) >= 5:
            impression['positives'].append('Strong skill set')
            score += 15
        elif len(skills) >= 2:
            score += 5
        impression['elements_reviewed'].append('Technical Skills')
        
        # Check projects
        projects = resume_data.get('projects', [])
        if projects:
            impression['positives'].append('Portfolio projects included')
            score += 10
        impression['elements_reviewed'].append('Projects')
        
        # ATS Score impact
        if ats_score >= 80:
            impression['positives'].append('High ATS compatibility')
            score += 10
        elif ats_score >= 60:
            score += 5
        else:
            impression['concerns'].append('Low ATS score - may not pass screening')
            score -= 10
        
        # Determine reaction
        if score >= 80:
            impression['initial_reaction'] = 'Strong interest - Move to interviews'
            impression['key_takeaway'] = 'Well-qualified candidate with relevant experience'
        elif score >= 60:
            impression['initial_reaction'] = 'Moderate interest - Review full resume carefully'
            impression['key_takeaway'] = 'Promising candidate with room for improvement'
        else:
            impression['initial_reaction'] = 'Doubtful - May not meet minimum requirements'
            impression['key_takeaway'] = 'Resume needs significant improvement'
        
        impression['impression_score'] = max(0, min(100, score))
        self.first_impression = impression
        
        return impression
    
    def calculate_hire_probability(self, ats_score: float,
                                 experience_match: float,
                                 skill_match: float,
                                 culture_fit: float = 0.5) -> Dict:
        """
        Calculate probability of hiring
        
        Args:
            ats_score: ATS score (0-100)
            experience_match: Experience alignment (0-1.0)
            skill_match: Required skills match (0-1.0)
            culture_fit: Estimated culture fit (0-1.0)
            
        Returns:
            Hire probability and reasoning
        """
        # Weighted calculation
        weights = {
            'ats': 0.25,
            'experience': 0.30,
            'skills': 0.35,
            'culture': 0.10
        }
        
        probability = (
            (ats_score / 100) * weights['ats'] +
            experience_match * weights['experience'] +
            skill_match * weights['skills'] +
            culture_fit * weights['culture']
        ) * 100
        
        probability = min(100, max(0, probability))
        
        self.hire_probability = probability
        
        # Generate assessment
        assessment = {
            'hire_probability_percentage': round(probability, 2),
            'hiring_decision': self._get_hiring_decision(probability),
            'confidence_level': self._get_confidence_level(probability),
            'component_scores': {
                'ats_score': round((ats_score / 100) * 100, 2),
                'experience_alignment': round(experience_match * 100, 2),
                'skill_match': round(skill_match * 100, 2),
                'culture_fit_estimate': round(culture_fit * 100, 2)
            }
        }
        
        return assessment
    
    def _get_hiring_decision(self, probability: float) -> str:
        """Get hiring recommendation"""
        if probability >= 80:
            return 'STRONG YES - Recommend immediate interview'
        elif probability >= 65:
            return 'YES - Recommend for interview round'
        elif probability >= 50:
            return 'MAYBE - Consider for interviews'
        elif probability >= 35:
            return 'WEAK - Only if few candidates available'
        else:
            return 'NO - Not recommended'
    
    def _get_confidence_level(self, probability: float) -> str:
        """Get confidence in hiring decision"""
        if probability >= 85:
            return 'Very High'
        elif probability >= 70:
            return 'High'
        elif probability >= 55:
            return 'Medium'
        elif probability >= 40:
            return 'Low'
        else:
            return 'Very Low'
    
    def analyze_strengths_from_recruiter_view(self, resume_data: Dict,
                                             skills: List[str],
                                             ats_score: float) -> List[str]:
        """
        Analyze strengths from recruiter perspective
        
        Args:
            resume_data: Resume data
            skills: Extracted skills
            ats_score: ATS score
            
        Returns:
            List of strengths
        """
        strengths = []
        
        # Experience strengths
        experience = resume_data.get('experience', [])
        if len(experience) >= 2:
            total_years = sum(self._get_years_from_duration(exp.get('duration', '')) 
                             for exp in experience)
            if total_years >= 3:
                strengths.append(f'Significant {total_years:.0f}+ years of relevant experience')
            else:
                strengths.append('Relevant work experience')
        
        # Skill strengths
        if len(skills) >= 8:
            strengths.append('Diverse and comprehensive skill set')
        elif len(skills) >= 5:
            strengths.append('Strong technical skills')
        
        # Specialty skills
        premium_skills = ['Leadership', 'Management', 'Architecture', 'Machine Learning']
        matched_premium = [s for s in skills if any(p in s for p in premium_skills)]
        if matched_premium:
            strengths.append(f'Advanced skills: {", ".join(matched_premium)}')
        
        # ATS strengths
        if ats_score >= 85:
            strengths.append('Excellent ATS compatibility and formatting')
        elif ats_score >= 70:
            strengths.append('Good ATS score and document quality')
        
        # Achievement indicators
        for exp in experience:
            description = exp.get('description', '').lower()
            achievement_words = ['led', 'managed', 'increased', 'improved', 'launched']
            if any(word in description for word in achievement_words):
                strengths.append('Demonstrated achievement and impact in previous roles')
                break
        
        return strengths
    
    def analyze_concerns_from_recruiter_view(self, resume_data: Dict,
                                            skills: List[str],
                                            ats_score: float,
                                            required_skills: List[str] = None) -> List[str]:
        """
        Analyze concerns from recruiter perspective
        
        Args:
            resume_data: Resume data
            skills: Extracted skills
            ats_score: ATS score
            required_skills: Required skills for role
            
        Returns:
            List of concerns
        """
        concerns = []
        
        # Experience concerns
        experience = resume_data.get('experience', [])
        if not experience:
            concerns.append('No work experience listed')
        elif len(experience) == 1:
            concerns.append('Limited work experience - may need more time to adjust')
        
        # Skill gaps
        if required_skills:
            missing = [s for s in required_skills 
                      if not any(s.lower() in skill.lower() for skill in skills)]
            if missing:
                concerns.append(f'Missing key skills: {", ".join(missing[:3])}')
        
        # ATS concerns
        if ats_score < 60:
            concerns.append('Low ATS score - may not pass automated screening')
        
        # Formatting/structure
        education = resume_data.get('education', [])
        if not education:
            concerns.append('Education background not clearly specified')
        
        # Skill depth
        if len(skills) < 5:
            concerns.append('Limited technical skills listed')
        
        return concerns
    
    def generate_recruiter_feedback(self, resume_data: Dict,
                                   skills: List[str],
                                   ats_score: float,
                                   hire_probability: float,
                                   required_skills: List[str] = None) -> Dict:
        """
        Generate complete recruiter feedback
        
        Args:
            resume_data: Resume data
            skills: Extracted skills
            ats_score: ATS score
            hire_probability: Hire probability percentage
            required_skills: Required skills
            
        Returns:
            Complete recruiter feedback
        """
        strengths = self.analyze_strengths_from_recruiter_view(resume_data, skills, ats_score)
        concerns = self.analyze_concerns_from_recruiter_view(resume_data, skills, ats_score, required_skills)
        interview_readiness = self._assess_interview_readiness(ats_score, len(skills))
        
        return {
            'overall_impression': self.first_impression.get('initial_reaction', ''),
            'hire_probability': f'{hire_probability:.1f}%',
            'hiring_decision': self._get_hiring_decision(hire_probability),
            'strengths': strengths,
            'concerns': concerns,
            'interview_readiness': interview_readiness,
            'recommendation': self._get_recommendation(hire_probability, concerns),
            'next_steps': self._get_next_steps(hire_probability)
        }
    
    def _assess_interview_readiness(self, ats_score: float, skill_count: int) -> str:
        """Assess how ready candidate is for interviews"""
        if ats_score >= 80 and skill_count >= 5:
            return 'Highly ready - Schedule interviews'
        elif ats_score >= 70 and skill_count >= 3:
            return 'Moderately ready - Can proceed to interviews'
        else:
            return 'Needs improvement - Recommend resume revision first'
    
    def _get_recommendation(self, probability: float, concerns: List[str]) -> str:
        """Get overall recommendation"""
        if probability >= 80 and len(concerns) <= 2:
            return 'Recommend for immediate interview'
        elif probability >= 60:
            return 'Recommend to hiring team for consideration'
        else:
            return 'Recommend for skill development before reapplication'
    
    def _get_next_steps(self, probability: float) -> List[str]:
        """Get recommended next steps"""
        steps = []
        
        if probability >= 75:
            steps = [
                'Schedule phone screening',
                'Prepare for technical interview',
                'Prepare for cultural fit assessment'
            ]
        elif probability >= 50:
            steps = [
                'Review resume for improvement',
                'Assess skill gaps',
                'Schedule initial call if interested'
            ]
        else:
            steps = [
                'Recommend skill development',
                'Suggest resume rewrite',
                'Encourage reapplication after 3-6 months'
            ]
        
        return steps
    
    @staticmethod
    def _get_years_from_duration(duration_str: str) -> float:
        """Extract years from duration string"""
        import re
        years = re.findall(r'\b(20\d{2})\b', duration_str)
        if len(years) >= 2:
            try:
                return float(years[-1]) - float(years[0])
            except:
                pass
        return 0
