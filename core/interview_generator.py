"""
Interview Generator Module
Generates mock interview questions and evaluates responses
"""

from typing import List, Dict, Tuple
import random
import logging

logger = logging.getLogger(__name__)


class InterviewGenerator:
    """Generate and evaluate mock interview questions"""
    
    # Question bank by category
    QUESTION_BANK = {
        'behavioral': [
            'Tell me about a time you successfully completed a project under pressure.',
            'Describe a situation where you had to work with a difficult team member.',
            'Share an example of how you handled failure or setback.',
            'Tell me about a time you took initiative and led a project.',
            'Describe a time you learned something new to solve a problem.',
            'Tell me about your greatest professional achievement.',
            'How do you handle feedback and criticism?',
            'Describe your approach to solving complex problems.',
            'Tell me about a time you improved a process or system.'
        ],
        'technical': [
            'Explain the difference between supervised and unsupervised learning.',
            'How would you optimize a slow database query?',
            'Describe the difference between SQL and NoSQL databases.',
            'Explain RESTful API principles.',
            'What is the difference between Git merge and rebase?',
            'How does Docker improve development workflows?',
            'Explain the concept of microservices.',
            'What are the key differences between Python and JavaScript?',
            'Describe your approach to writing testable code.'
        ],
        'role_specific_developer': [
            'How do you approach code reviews?',
            'What design patterns are you most familiar with?',
            'How do you debug production issues?',
            'What is your experience with version control?',
            'How do you ensure code quality in your projects?',
            'Tell me about your experience with different frameworks.'
        ],
        'role_specific_data_scientist': [
            'How do you approach feature engineering?',
            'Explain overfitting and how to prevent it.',
            'How do you handle imbalanced datasets?',
            'Describe a project where you improved model performance.',
            'How do you evaluate model performance?',
            'Tell me about your experience with big data tools.'
        ],
        'situational': [
            'What would you do if you disagreed with a decision made by your manager?',
            'How do you prioritize when given multiple urgent tasks?',
            'Describe how you would approach learning a completely new technology needed for a project.',
            'Tell me how you would handle missing deadlines.',
            'What would you do if you found a senior colleague making a mistake?'
        ]
    }
    
    # Evaluation criteria
    EVALUATION_CRITERIA = {
        'clarity': {
            'weight': 0.20,
            'description': 'How clear and well-structured is the answer?'
        },
        'relevance': {
            'weight': 0.25,
            'description': 'Does the answer directly address the question?'
        },
        'structure': {
            'weight': 0.20,
            'description': 'Does the answer follow STAR or clear structure?'
        },
        'depth': {
            'weight': 0.20,
            'description': 'Does the answer provide sufficient detail?'
        },
        'keywords': {
            'weight': 0.15,
            'description': 'Does answer include relevant technical keywords?'
        }
    }
    
    def __init__(self, job_role: str = 'Software Developer'):
        """
        Initialize interview generator
        
        Args:
            job_role: Target job role
        """
        self.job_role = job_role
        self.current_question = None
        self.question_history = []
        self.responses = []
    
    def get_question(self, category: str = None) -> str:
        """
        Get interview question
        
        Args:
            category: Category of question (behavioral, technical, etc.)
            
        Returns:
            Interview question
        """
        if category is None:
            # Mix of question types
            weights = [0.4, 0.4, 0.2]  # behavioral, technical, situational
            categories = ['behavioral', 'technical', 'situational']
            category = random.choices(categories, weights=weights)[0]
        
        # Get role-specific questions if available
        role_key = f'role_specific_{self.job_role.lower().replace(" ", "_")}'
        
        if category == 'technical' and role_key in self.QUESTION_BANK:
            questions = self.QUESTION_BANK[role_key]
        else:
            questions = self.QUESTION_BANK.get(category, self.QUESTION_BANK['behavioral'])
        
        self.current_question = random.choice(questions)
        return self.current_question
    
    def get_multiple_questions(self, count: int = 5, 
                              mix: List[str] = None) -> List[str]:
        """
        Get multiple interview questions
        
        Args:
            count: Number of questions
            mix: Mix of question types (e.g., ['behavioral', 'technical'])
            
        Returns:
            List of interview questions
        """
        questions = []
        
        if mix is None:
            mix = ['behavioral', 'technical', 'situational']
        
        for _ in range(count):
            category = random.choice(mix)
            questions.append(self.get_question(category))
        
        return questions
    
    def evaluate_response(self, answer: str) -> Dict:
        """
        Evaluate interview response
        
        Args:
            answer: Candidate's response to the question
            
        Returns:
            Evaluation scores and feedback
        """
        evaluation = {
            'overall_score': 0,
            'criteria_scores': {},
            'feedback': [],
            'strengths': [],
            'improvements': []
        }
        
        # Evaluate clarity (word count, sentence structure)
        clarity_score = self._evaluate_clarity(answer)
        evaluation['criteria_scores']['clarity'] = clarity_score
        
        # Evaluate relevance (checks for keywords matching question)
        relevance_score = self._evaluate_relevance(answer, self.current_question)
        evaluation['criteria_scores']['relevance'] = relevance_score
        
        # Evaluate structure (STAR framework check)
        structure_score = self._evaluate_structure(answer)
        evaluation['criteria_scores']['structure'] = structure_score
        
        # Evaluate depth (answer length and details)
        depth_score = self._evaluate_depth(answer)
        evaluation['criteria_scores']['depth'] = depth_score
        
        # Evaluate keywords (technical keywords if technical question)
        keywords_score = self._evaluate_keywords(answer)
        evaluation['criteria_scores']['keywords'] = keywords_score
        
        # Calculate weighted overall score
        overall = sum(
            score * self.EVALUATION_CRITERIA[criterion]['weight']
            for criterion, score in evaluation['criteria_scores'].items()
        )
        evaluation['overall_score'] = round(overall, 2)
        
        # Generate feedback
        evaluation.update(self._generate_feedback(evaluation, answer))
        
        self.responses.append({
            'question': self.current_question,
            'answer': answer,
            'evaluation': evaluation
        })
        
        return evaluation
    
    def _evaluate_clarity(self, answer: str) -> float:
        """Evaluate clarity of response (0-100)"""
        score = 50  # Base score
        
        # Check sentence structure
        sentences = [s.strip() for s in answer.split('.') if s.strip()]
        if len(sentences) >= 3:
            score += 20
        elif len(sentences) >= 2:
            score += 10
        
        # Check for jargon and filler words
        filler_words = ['um', 'uh', 'like', 'you know', 'basically', 'literally']
        filler_count = sum(1 for word in filler_words if word in answer.lower())
        
        if filler_count == 0:
            score += 30
        elif filler_count <= 2:
            score += 15
        
        return min(100, score)
    
    def _evaluate_relevance(self, answer: str, question: str) -> float:
        """Evaluate relevance to question (0-100)"""
        score = 50  # Base score
        
        answer_lower = answer.lower()
        question_lower = question.lower()
        
        # Extract key words from question
        key_words = [w for w in question_lower.split() if len(w) > 4]
        
        matches = sum(1 for word in key_words if word in answer_lower)
        match_percentage = (matches / len(key_words) * 100) if key_words else 0
        
        if match_percentage >= 80:
            score += 50
        elif match_percentage >= 60:
            score += 35
        elif match_percentage >= 40:
            score += 15
        
        return min(100, score)
    
    def _evaluate_structure(self, answer: str) -> float:
        """Evaluate structure (STAR framework) (0-100)"""
        score = 50  # Base score
        
        answer_lower = answer.lower()
        
        # Check for STAR elements
        situation_words = ['was', 'worked', 'faced', 'encountered', 'in my']
        task_words = ['needed to', 'had to', 'responsible', 'task']
        action_words = ['did', 'implemented', 'developed', 'created', 'solved']
        result_words = ['resulted', 'achieved', 'improved', 'increased', 'learned']
        
        has_situation = any(word in answer_lower for word in situation_words)
        has_task = any(word in answer_lower for word in task_words)
        has_action = any(word in answer_lower for word in action_words)
        has_result = any(word in answer_lower for word in result_words)
        
        star_elements = sum([has_situation, has_task, has_action, has_result])
        
        if star_elements == 4:
            score += 50
        elif star_elements == 3:
            score += 35
        elif star_elements == 2:
            score += 15
        
        return min(100, score)
    
    def _evaluate_depth(self, answer: str) -> float:
        """Evaluate depth of answer (0-100)"""
        score = 50  # Base score
        
        word_count = len(answer.split())
        
        if word_count >= 150:
            score += 50
        elif word_count >= 100:
            score += 35
        elif word_count >= 50:
            score += 15
        
        # Check for specific examples
        if 'for example' in answer.lower() or 'specifically' in answer.lower():
            score += 10
        
        return min(100, score)
    
    def _evaluate_keywords(self, answer: str) -> float:
        """Evaluate presence of technical keywords (0-100)"""
        score = 50  # Base score
        
        # Common technical keywords
        tech_keywords = [
            'algorithm', 'database', 'api', 'framework', 'performance',
            'optimization', 'testing', 'debugging', 'deployment', 'scalability'
        ]
        
        answer_lower = answer.lower()
        keyword_count = sum(1 for keyword in tech_keywords if keyword in answer_lower)
        
        if keyword_count >= 3:
            score += 50
        elif keyword_count >= 2:
            score += 30
        elif keyword_count >= 1:
            score += 15
        
        return min(100, score)
    
    def _generate_feedback(self, evaluation: Dict, answer: str) -> Dict:
        """Generate detailed feedback"""
        feedback = {
            'feedback': [],
            'strengths': [],
            'improvements': []
        }
        
        # Feedback based on scores
        if evaluation['overall_score'] >= 80:
            feedback['feedback'].append('Excellent response! Well-structured and comprehensive.')
            feedback['strengths'].append('Clear communication of your experience')
        
        elif evaluation['overall_score'] >= 60:
            feedback['feedback'].append('Good response with room for improvement.')
        
        else:
            feedback['feedback'].append('Response needs significant improvement.')
        
        # Specific improvements
        if evaluation['criteria_scores']['clarity'] < 60:
            feedback['improvements'].append('Work on clarity. Try to use shorter sentences.')
        
        if evaluation['criteria_scores']['structure'] < 60:
            feedback['improvements'].append('Try using STAR framework (Situation-Task-Action-Result)')
        
        if evaluation['criteria_scores']['depth'] < 60:
            feedback['improvements'].append('Add more specific examples and details')
        
        if evaluation['criteria_scores']['keywords'] < 50:
            feedback['improvements'].append('Include more relevant technical keywords')
        
        return feedback
    
    def get_interview_session(self, num_questions: int = 5) -> List[Dict]:
        """
        Get complete interview session
        
        Args:
            num_questions: Number of questions for interview
            
        Returns:
            List of questions
        """
        questions = []
        question_set = set()
        
        attempts = 0
        max_attempts = 50
        
        while len(questions) < num_questions and attempts < max_attempts:
            q = self.get_question()
            if q not in question_set:
                questions.append(q)
                question_set.add(q)
            attempts += 1
        
        return questions
    
    def get_performance_summary(self) -> Dict:
        """Get interview performance summary"""
        if not self.responses:
            return {}
        
        total_score = sum(r['evaluation']['overall_score'] for r in self.responses)
        avg_score = total_score / len(self.responses)
        
        return {
            'total_questions': len(self.responses),
            'average_score': round(avg_score, 2),
            'responses': self.responses,
            'overall_feedback': self._generate_overall_feedback(avg_score)
        }
    
    def _generate_overall_feedback(self, avg_score: float) -> str:
        """Generate overall feedback based on average score"""
        if avg_score >= 80:
            return 'Excellent performance! You are well-prepared for this role.'
        elif avg_score >= 65:
            return 'Good performance. Focus on depth and technical details.'
        elif avg_score >= 50:
            return 'Average performance. Practice structuring answers with STAR framework.'
        else:
            return 'Below average. Significant practice needed on technical and communication skills.'
