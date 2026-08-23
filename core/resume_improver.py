"""
Resume Improver Module
Provides suggestions for resume enhancement and rephrasing
"""

from typing import List, Dict
import re
import logging

logger = logging.getLogger(__name__)


class ResumeImprover:
    """Improve resume content and structure"""
    
    # Action verbs and weak phrases mapping
    STRONG_VERBS = [
        'Developed', 'Designed', 'Built', 'Created', 'Implemented',
        'Managed', 'Led', 'Directed', 'Coordinated', 'Organized',
        'Optimized', 'Improved', 'Enhanced', 'Increased', 'Reduced',
        'Streamlined', 'Automated', 'Integrated', 'Deployed', 'Launched'
    ]
    
    WEAK_VERBS = {
        'worked on': 'Developed',
        'helped with': 'Contributed to',
        'did': 'Implemented',
        'made': 'Created',
        'was responsible for': 'Managed',
        'was involved in': 'Participated in',
        'handled': 'Managed',
        'took part in': 'Led',
        'was in charge of': 'Directed'
    }
    
    WEAK_PHRASES = [
        'I believe', 'I think', 'I feel', 'In my opinion',
        'very', 'really', 'quite', 'somewhat', 'kind of',
        'a lot', 'lots of', 'multiple', 'several'
    ]
    
    METRICS_KEYWORDS = [
        'Increased', 'Reduced', 'Improved', 'Optimized', 'Decreased',
        'Accelerated', 'Maximized', 'Minimized', 'Enhanced'
    ]
    
    def __init__(self):
        """Initialize resume improver"""
        self.improvements = []
        self.rewritten_content = []
    
    def analyze_resume(self, text: str) -> Dict:
        """
        Analyze resume for improvement opportunities
        
        Args:
            text: Resume text to analyze
            
        Returns:
            Dictionary with analysis and suggestions
        """
        analysis = {
            'weak_phrases_found': [],
            'weak_verbs_found': [],
            'missing_metrics': [],
            'formatting_issues': [],
            'suggestions': []
        }
        
        text_lower = text.lower()
        lines = text.split('\n')
        
        # Check for weak phrases
        for phrase in self.WEAK_PHRASES:
            if phrase in text_lower:
                count = text_lower.count(phrase)
                analysis['weak_phrases_found'].append({
                    'phrase': phrase,
                    'count': count
                })
        
        # Check for weak verbs
        for weak, strong in self.WEAK_VERBS.items():
            if weak in text_lower:
                count = text_lower.count(weak)
                analysis['weak_verbs_found'].append({
                    'weak': weak,
                    'strong': strong,
                    'count': count
                })
        
        # Check for missing action verbs in bullet points
        bullet_lines = [line for line in lines if line.strip().startswith(('-', '•', '*'))]
        for line in bullet_lines:
            if not any(verb.lower() in line.lower() for verb in self.STRONG_VERBS):
                analysis['missing_metrics'].append({
                    'line': line.strip(),
                    'issue': 'Could start with a strong action verb'
                })
        
        # Check for missing metrics/numbers
        for line in bullet_lines:
            line_lower = line.lower()
            has_number = bool(re.search(r'\d+', line))
            has_metric_verb = any(verb in line for verb in self.METRICS_KEYWORDS)
            
            if has_metric_verb and not has_number:
                analysis['missing_metrics'].append({
                    'line': line.strip(),
                    'issue': 'Could add specific metrics/numbers'
                })
        
        # Generate suggestions
        if analysis['weak_phrases_found']:
            count = sum(item['count'] for item in analysis['weak_phrases_found'])
            analysis['suggestions'].append(
                f"Remove {count} weak/filler phrases to improve clarity"
            )
        
        if analysis['weak_verbs_found']:
            analysis['suggestions'].append(
                "Replace weak verbs with strong action verbs"
            )
        
        if len(analysis['missing_metrics']) > 3:
            analysis['suggestions'].append(
                "Add measurable results/metrics to your bullet points"
            )
        
        return analysis
    
    def rewrite_bullet_point(self, bullet: str) -> str:
        """
        Rewrite a bullet point with improvements
        
        Args:
            bullet: Original bullet point
            
        Returns:
            Improved bullet point
        """
        improved = bullet.strip()
        
        # Remove weak phrases
        for phrase in self.WEAK_PHRASES:
            improved = re.sub(rf'\b{phrase}\b', '', improved, flags=re.IGNORECASE)
        
        # Replace weak verbs
        for weak, strong in self.WEAK_VERBS.items():
            if weak.lower() in improved.lower():
                improved = re.sub(
                    rf'\b{re.escape(weak)}\b',
                    strong,
                    improved,
                    flags=re.IGNORECASE
                )
                break
        
        # Add strong verb if missing
        if not any(verb.lower() in improved.lower() for verb in self.STRONG_VERBS):
            improved = 'Implemented ' + improved.lower()
        
        # Clean up multiple spaces
        improved = re.sub(r'\s+', ' ', improved).strip()
        
        # Ensure starts with capital letter
        if improved:
            improved = improved[0].upper() + improved[1:]
        
        return improved
    
    def add_metrics(self, bullet: str) -> str:
        """
        Suggest metrics for a bullet point
        
        Args:
            bullet: Original bullet point
            
        Returns:
            Suggestion for adding metrics
        """
        suggestion = bullet.strip()
        
        # Check if metrics already present
        if re.search(r'\d+%|\$\d+|X[0-9.]+', suggestion):
            return suggestion
        
        # Find appropriate metric suggestions based on content
        keywords_metrics = {
            'improved': '(50% improvement example)',
            'increased': '(X% or X units)',
            'reduced': '(X% reduction)',
            'optimized': '(X% faster)',
            'saved': '($X or X hours)',
            'developed': '(X features)',
            'processed': '(X thousand items)'
        }
        
        for keyword, metric in keywords_metrics.items():
            if keyword in suggestion.lower():
                suggestion += f" {metric}"
                break
        
        return suggestion
    
    def get_improvement_suggestions(self, text: str) -> Dict:
        """
        Get comprehensive improvement suggestions
        
        Args:
            text: Resume text
            
        Returns:
            List of actionable suggestions
        """
        analysis = self.analyze_resume(text)
        
        suggestions = {
            'quick_wins': [],
            'medium_improvements': [],
            'major_revisions': []
        }
        
        # Quick wins (easy immediate improvements)
        if analysis['weak_phrases_found']:
            suggestions['quick_wins'].append({
                'title': 'Remove Weak Phrases',
                'items': analysis['weak_phrases_found'],
                'impact': 'Improves clarity and professionalism'
            })
        
        # Medium improvements
        if analysis['weak_verbs_found']:
            suggestions['medium_improvements'].append({
                'title': 'Strengthen Action Verbs',
                'items': analysis['weak_verbs_found'],
                'impact': 'Makes achievements sound more impactful'
            })
        
        # Major revisions needed
        if len(analysis['missing_metrics']) > 5:
            suggestions['major_revisions'].append({
                'title': 'Add Quantifiable Results',
                'description': 'Include metrics, percentages, or numbers to demonstrate impact',
                'examples': [
                    'Instead of: "Improved performance"',
                    'Write: "Improved performance by 40% through optimization"'
                ],
                'impact': 'Significantly increases ATS score and recruiter attention'
            })
        
        return suggestions
    
    def generate_improved_resume(self, text: str) -> str:
        """
        Generate improved version of resume
        
        Args:
            text: Original resume text
            
        Returns:
            Improved resume text
        """
        lines = text.split('\n')
        improved_lines = []
        
        for line in lines:
            if line.strip().startswith(('-', '•', '*')):
                improved = self.rewrite_bullet_point(line)
                improved_lines.append(improved)
            else:
                improved_lines.append(line)
        
        return '\n'.join(improved_lines)
    
    def check_formatting_issue(self, text: str) -> Dict:
        """
        Check for formatting issues
        
        Args:
            text: Resume text
            
        Returns:
            List of formatting issues
        """
        issues = {
            'length': '',
            'structure': [],
            'consistency': []
        }
        
        lines = text.split('\n')
        word_count = len(text.split())
        
        # Check length
        if word_count > 800:
            issues['length'] = 'Resume might be too long. Consider condensing to 1 page.'
        elif word_count < 100:
            issues['length'] = 'Resume is too short. Add more details about your experience.'
        
        # Check structure
        sections_found = []
        for section in ['experience', 'education', 'skills', 'projects']:
            if section in text.lower():
                sections_found.append(section)
        
        if len(sections_found) < 3:
            issues['structure'].append('Missing important resume sections')
        
        # Check consistency
        bullet_styles = set()
        for line in lines:
            if line.strip().startswith(('-', '•', '*')):
                bullet_styles.add(line.strip()[0])
        
        if len(bullet_styles) > 1:
            issues['consistency'].append('Inconsistent bullet point styles')
        
        return issues
