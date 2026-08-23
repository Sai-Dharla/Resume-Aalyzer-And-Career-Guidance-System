"""
Job Matcher Module
Compares resume skills with job descriptions using similarity scoring
"""

from typing import List, Dict, Tuple
import re
import logging

logger = logging.getLogger(__name__)


class JobMatcher:
    """Match resumes against job descriptions"""
    
    def __init__(self):
        """Initialize job matcher"""
        self.resume_data = {}
        self.job_description = ""
        self.similarity_scores = {}
    
    def extract_skills_from_job_description(self, job_description: str) -> Dict[str, List[str]]:
        """
        Extract skills mentioned in job description
        
        Args:
            job_description: Job description text
            
        Returns:
            Dictionary of extracted skills by category
        """
        extracted = {
            'required': [],
            'nice_to_have': [],
            'tools': [],
            'soft_skills': []
        }
        
        text_lower = job_description.lower()
        
        # Define skill patterns
        required_keywords = ['required', 'must have', 'essential', 'mandatory']
        nice_keywords = ['nice to have', 'preferred', 'beneficial']
        
        # Extract required skills
        for keyword in required_keywords:
            pattern = rf'{keyword}:?\s*(.+?)(?:nice to have|preferred|$)'
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            for match in matches:
                skills = self._parse_skill_list(match)
                extracted['required'].extend(skills)
        
        # Extract nice-to-have skills
        for keyword in nice_keywords:
            pattern = rf'{keyword}:?\s*(.+?)(?:required|$)'
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            for match in matches:
                skills = self._parse_skill_list(match)
                extracted['nice_to_have'].extend(skills)
        
        # Extract explicitly mentioned technical skills
        technical_skills = [
            'Python', 'Java', 'JavaScript', 'React', 'Angular', 'Vue',
            'Node.js', 'Express', 'Django', 'Flask', 'SQL', 'MongoDB',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'Git', 'REST API',
            'GraphQL', 'Linux', 'CI/CD', 'Jenkins', 'Terraform'
        ]
        
        for skill in technical_skills:
            if skill.lower() in text_lower:
                extracted['tools'].append(skill)
        
        # Remove duplicates
        for key in extracted:
            extracted[key] = list(set(extracted[key]))
        
        return extracted
    
    def _parse_skill_list(self, text: str) -> List[str]:
        """Parse comma/bullet separated skill list"""
        # Split by common delimiters
        items = re.split(r'[,\n•∙·-]', text)
        skills = []
        
        for item in items:
            skill = item.strip()
            # Clean up common prefixes/suffixes
            skill = re.sub(r'^(and|or|\/)\s+', '', skill)
            skill = re.sub(r'\s+(and|or)$', '', skill)
            
            if len(skill) > 2 and len(skill) < 100:  # Reasonable skill length
                skills.append(skill)
        
        return skills
    
    def calculate_similarity(self, resume_skills: List[str], 
                            job_skills: Dict[str, List[str]]) -> Dict:
        """
        Calculate similarity between resume and job
        
        Args:
            resume_skills: Skills extracted from resume
            job_skills: Skills extracted from job description
            
        Returns:
            Similarity scores and matching details
        """
        resume_lower = [s.lower() for s in resume_skills]
        
        # Calculate matches for each category
        required_matches = self._find_matches(resume_lower, job_skills.get('required', []))
        nice_matches = self._find_matches(resume_lower, job_skills.get('nice_to_have', []))
        tool_matches = self._find_matches(resume_lower, job_skills.get('tools', []))
        
        total_required = len(job_skills.get('required', []))
        total_nice = len(job_skills.get('nice_to_have', []))
        total_tools = len(job_skills.get('tools', []))
        
        # Calculate percentages
        required_percentage = (len(required_matches) / total_required * 100) if total_required > 0 else 0
        nice_percentage = (len(nice_matches) / total_nice * 100) if total_nice > 0 else 0
        tools_percentage = (len(tool_matches) / total_tools * 100) if total_tools > 0 else 0
        
        # Calculate overall score (70% required, 20% nice, 10% tools)
        overall_score = (
            (required_percentage * 0.7) +
            (nice_percentage * 0.2) +
            (tools_percentage * 0.1)
        )
        
        self.similarity_scores = {
            'overall_score': round(overall_score, 2),
            'required_match_percentage': round(required_percentage, 2),
            'nice_match_percentage': round(nice_percentage, 2),
            'tools_match_percentage': round(tools_percentage, 2),
            'matches': {
                'required': required_matches,
                'nice_to_have': nice_matches,
                'tools': tool_matches
            },
            'missing': {
                'required': [s for s in job_skills.get('required', []) 
                            if not self._skill_matched(s, resume_lower)],
                'nice_to_have': [s for s in job_skills.get('nice_to_have', []) 
                                if not self._skill_matched(s, resume_lower)],
                'tools': [s for s in job_skills.get('tools', []) 
                         if not self._skill_matched(s, resume_lower)]
            }
        }
        
        return self.similarity_scores
    
    def _find_matches(self, resume_skills: List[str], 
                     job_skills: List[str]) -> List[str]:
        """Find matching skills between resume and job"""
        matches = []
        
        for job_skill in job_skills:
            if self._skill_matched(job_skill, resume_skills):
                matches.append(job_skill)
        
        return matches
    
    def _skill_matched(self, skill: str, skill_list: List[str]) -> bool:
        """Check if skill matches any in the list"""
        skill_lower = skill.lower()
        
        for item in skill_list:
            item_lower = item.lower()
            # Exact substring match
            if skill_lower in item_lower or item_lower in skill_lower:
                return True
        
        return False
    
    def get_match_report(self, resume_skills: List[str],
                        job_title: str,
                        job_description: str) -> Dict:
        """
        Generate comprehensive job match report
        
        Args:
            resume_skills: Skills from resume
            job_title: Job title
            job_description: Job description text
            
        Returns:
            Detailed match report
        """
        self.job_description = job_description
        
        # Extract job skills
        job_skills = self.extract_skills_from_job_description(job_description)
        
        # Calculate similarity
        scores = self.calculate_similarity(resume_skills, job_skills)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(scores, resume_skills)
        
        # Generate fit assessment
        fit_assessment = self._assess_fit(scores['overall_score'])
        
        report = {
            'job_title': job_title,
            'overall_match_score': scores['overall_score'],
            'fit_assessment': fit_assessment,
            'detailed_scores': {
                'required_skills_match': scores['required_match_percentage'],
                'nice_to_have_match': scores['nice_match_percentage'],
                'tools_match': scores['tools_match_percentage']
            },
            'matched_skills': {
                'required': scores['matches']['required'],
                'nice_to_have': scores['matches']['nice_to_have'],
                'tools': scores['matches']['tools']
            },
            'missing_skills': {
                'required': scores['missing']['required'],
                'nice_to_have': scores['missing']['nice_to_have'],
                'tools': scores['missing']['tools']
            },
            'recommendations': recommendations,
            'total_matched': sum(len(v) for v in scores['matches'].values()),
            'total_missing': sum(len(v) for v in scores['missing'].values())
        }
        
        return report
    
    def _generate_recommendations(self, scores: Dict, 
                                 resume_skills: List[str]) -> List[str]:
        """Generate recommendations based on match scores"""
        recommendations = []
        
        overall = scores['overall_score']
        
        if overall >= 80:
            recommendations.append("Excellent match! You meet most job requirements.")
            recommendations.append("Consider highlighting matching skills in your resume cover letter.")
        elif overall >= 60:
            recommendations.append("Good match! You have most required skills.")
            recommendations.append("Focus on learning the missing critical skills.")
        elif overall >= 40:
            recommendations.append("Moderate match. You have some relevant skills.")
            recommendations.append("Consider learning the missing required skills first.")
        else:
            recommendations.append("Limited match. You may need significant skill development.")
            recommendations.append("This role might not be ideal right now. Consider adjacent roles.")
        
        # Specific recommendations for missing critical skills
        if scores['missing'].get('required'):
            missing_count = len(scores['missing']['required'])
            if missing_count <= 3:
                skills_str = ', '.join(scores['missing']['required'][:3])
                recommendations.append(f"Priority: Learn {skills_str}")
            else:
                recommendations.append(f"Priority: Learn {missing_count} critical skills first")
        
        return recommendations
    
    def _assess_fit(self, score: float) -> str:
        """Assess job fit based on score"""
        if score >= 85:
            return "Excellent Fit"
        elif score >= 70:
            return "Good Fit"
        elif score >= 50:
            return "Moderate Fit"
        elif score >= 30:
            return "Poor Fit"
        else:
            return "Not a Good Fit"
