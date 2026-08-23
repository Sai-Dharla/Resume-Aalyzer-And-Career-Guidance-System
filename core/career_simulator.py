"""
Career Simulator Module
Simulates job readiness timeline and multiple scenarios
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class CareerSimulator:
    """Simulate job readiness and career outcomes"""
    
    def __init__(self):
        """Initialize career simulator"""
        self.scenarios = []
        self.current_scenario = None
    
    def estimate_job_readiness(self, missing_skills_count: int,
                              ats_score: float,
                              experience_years: int) -> Dict:
        """
        Estimate timeline to job readiness
        
        Args:
            missing_skills_count: Number of missing skills
            ats_score: Current ATS score (0-100)
            experience_years: Years of relevant experience
            
        Returns:
            Job readiness estimate
        """
        # Calculate base readiness factors
        skill_factor = max(0, 100 - missing_skills_count * 5)  # 5 points per missing skill
        ats_factor = ats_score
        experience_factor = min(100, experience_years * 15)   # 15 points per year
        
        # Calculate current readiness level
        current_readiness = (skill_factor * 0.5 + ats_factor * 0.3 + experience_factor * 0.2)
        current_readiness = max(0, min(100, current_readiness))
        
        # Estimate weeks to readiness (80% benchmark)
        if current_readiness >= 80:
            weeks_to_ready = 0
            status = 'READY'
        elif current_readiness >= 60:
            weeks_to_ready = 4
            status = 'NEARLY READY'
        elif current_readiness >= 40:
            weeks_to_ready = 12
            status = 'IN PROGRESS'
        else:
            weeks_to_ready = 24
            status = 'NEEDS WORK'
        
        return {
            'current_readiness_score': round(current_readiness, 2),
            'status': status,
            'estimated_weeks_to_ready': weeks_to_ready,
            'estimated_months_to_ready': round(weeks_to_ready / 4.3, 1),
            'readiness_factors': {
                'skills_alignment': skill_factor,
                'ats_score': ats_factor,
                'experience_level': experience_factor
            }
        }
    
    def generate_multiple_scenarios(self, skill_gaps: List[Dict],
                                   ats_score: float,
                                   experience_years: int) -> List[Dict]:
        """
        Generate multiple job readiness scenarios
        
        Args:
            skill_gaps: List of skill gaps
            ats_score: Current ATS score
            experience_years: Experience years
            
        Returns:
            List of scenarios (fast/average/slow learner)
        """
        scenarios = {}
        missing_count = len(skill_gaps)
        
        # Scenario 1: Fast Learner (4-5 hours/day, dedicated)
        scenarios['fast_learner'] = {
            'name': 'Fast Learner',
            'description': 'Dedicated, with 4-5 hours daily',
            'daily_hours': 4.5,
            'hours_per_week': 30,
            'learning_days_per_skill': 12,
            'total_timeline': {
                'days': missing_count * 12,
                'weeks': round(missing_count * 12 / 7),
                'months': round((missing_count * 12 / 7) / 4.3, 1)
            },
            'milestones': self._generate_scenario_milestones('fast', missing_count),
            'estimated_readiness_score': min(100, ats_score + 25),
            'success_probability': min(95, 70 + (experience_years * 5))
        }
        
        # Scenario 2: Average Learner (2-3 hours/day, moderate)
        scenarios['average_learner'] = {
            'name': 'Average Learner',
            'description': 'Part-time learning, 2-3 hours daily',
            'daily_hours': 2.5,
            'hours_per_week': 15,
            'learning_days_per_skill': 20,
            'total_timeline': {
                'days': missing_count * 20,
                'weeks': round(missing_count * 20 / 7),
                'months': round((missing_count * 20 / 7) / 4.3, 1)
            },
            'milestones': self._generate_scenario_milestones('average', missing_count),
            'estimated_readiness_score': min(100, ats_score + 15),
            'success_probability': min(85, 65 + (experience_years * 4))
        }
        
        # Scenario 3: Slow Learner (1-2 hours/day, part-time)
        scenarios['slow_learner'] = {
            'name': 'Slow Learner',
            'description': 'Slow pace, 1-2 hours daily',
            'daily_hours': 1.5,
            'hours_per_week': 10,
            'learning_days_per_skill': 30,
            'total_timeline': {
                'days': missing_count * 30,
                'weeks': round(missing_count * 30 / 7),
                'months': round((missing_count * 30 / 7) / 4.3, 1)
            },
            'milestones': self._generate_scenario_milestones('slow', missing_count),
            'estimated_readiness_score': min(100, ats_score + 8),
            'success_probability': min(75, 60 + (experience_years * 3))
        }
        
        self.scenarios = list(scenarios.values())
        return self.scenarios
    
    def _generate_scenario_milestones(self, pace: str, skill_count: int) -> List[Dict]:
        """Generate milestones for scenario"""
        multipliers = {
            'fast': 0.5,
            'average': 1.0,
            'slow': 1.5
        }
        
        multiplier = multipliers.get(pace, 1.0)
        milestone_interval = max(1, int(skill_count / 3 * multiplier))
        
        milestones = []
        for i in range(1, 4):
            weeks = i * int(skill_count * multiplier * 20 / 7 / 3)
            milestones.append({
                'phase': i,
                'name': f'Phase {i}: {"Basics" if i == 1 else "Intermediate" if i == 2 else "Advanced"}',
                'weeks': weeks,
                'description': f'Complete {i * milestone_interval} skills'
            })
        
        return milestones
    
    def simulate_job_hunt(self, readiness_score: float,
                         applications: int = 100) -> Dict:
        """
        Simulate job search outcomes
        
        Args:
            readiness_score: Job readiness score (0-100)
            applications: Number of applications
            
        Returns:
            Job search simulation results
        """
        # Probability calculations based on readiness
        base_callback_rate = 0.02  # 2% base
        
        if readiness_score >= 85:
            callback_rate = 0.15  # 15%
            avg_interviews = 8
            offer_rate = 0.4
        elif readiness_score >= 70:
            callback_rate = 0.10  # 10%
            avg_interviews = 5
            offer_rate = 0.25
        elif readiness_score >= 60:
            callback_rate = 0.06  # 6%
            avg_interviews = 3
            offer_rate = 0.15
        else:
            callback_rate = 0.03  # 3%
            avg_interviews = 1
            offer_rate = 0.05
        
        estimated_callbacks = int(applications * callback_rate)
        estimated_interviews = int(estimated_callbacks * (avg_interviews / estimated_callbacks)) if estimated_callbacks > 0 else 0
        estimated_offers = int(estimated_interviews * offer_rate)
        
        return {
            'estimated_applications': applications,
            'callback_rate': f'{callback_rate * 100:.1f}%',
            'estimated_callbacks': estimated_callbacks,
            'estimated_interviews': estimated_interviews,
            'offer_rate': f'{offer_rate * 100:.1f}%',
            'estimated_offers': max(1, estimated_offers),
            'recommendation': self._job_hunt_recommendation(estimated_offers, applications)
        }
    
    def _job_hunt_recommendation(self, offers: int, applications: int) -> str:
        """Generate recommendation for job hunt"""
        if offers >= 1:
            return 'You likely have competitive offers. Negotiate and choose the best opportunity!'
        elif offers == 0 and applications >= 100:
            return 'Improve resume quality and interview skills for better outcomes.'
        else:
            return 'Continue improving and apply to more positions.'
    
    def calculate_salary_trajectory(self, starting_salary: float,
                                   years_projection: int = 5) -> List[Dict]:
        """
        Project salary growth trajectory
        
        Args:
            starting_salary: Current/expected starting salary
            years_projection: Years to project
            
        Returns:
            Projected salary trajectory
        """
        trajectory = []
        
        for year in range(years_projection + 1):
            # Typical progression: 8-10% annual increase
            salary = starting_salary * (1.09 ** year)
            
            trajectory.append({
                'year': year,
                'projected_salary': round(salary, 2),
                'annual_increase': round(salary - (starting_salary * (1.09 ** (year - 1)))) if year > 0 else 0,
                'role_progression': self._get_role_by_year(year)
            })
        
        return trajectory
    
    def _get_role_by_year(self, year: int) -> str:
        """Get expected role progression"""
        progressions = {
            0: 'Entry Level / Junior',
            1: 'Junior',
            2: 'Mid-Level',
            3: 'Mid-Level / Senior',
            4: 'Senior',
            5: 'Senior / Lead'
        }
        return progressions.get(min(year, 5), 'Lead / Manager')
    
    def get_scenario_comparison(self) -> Dict:
        """Get comparison of all scenarios"""
        if not self.scenarios:
            return {}
        
        comparison = {
            'scenarios': self.scenarios,
            'best_scenario': max(self.scenarios, key=lambda x: x['estimated_readiness_score']),
            'fastest_path': min(self.scenarios, 
                               key=lambda x: x['total_timeline']['weeks']),
            'most_realistic': self.scenarios[1] if len(self.scenarios) > 1 else self.scenarios[0]
        }
        
        return comparison
