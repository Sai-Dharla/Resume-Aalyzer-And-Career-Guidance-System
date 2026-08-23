"""
Roadmap Generator Module
Creates personalized learning and career roadmaps
"""

from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class RoadmapGenerator:
    """Generate personalized learning and career roadmaps"""
    
    # Default learning hours per week
    DEFAULT_HOURS_PER_WEEK = 15
    
    def __init__(self):
        """Initialize roadmap generator"""
        self.roadmap = []
        self.total_duration = 0
    
    def generate_learning_roadmap(self, skill_gaps: List[Dict],
                                 hours_per_week: int = None) -> List[Dict]:
        """
        Generate learning roadmap for missing skills
        
        Args:
            skill_gaps: List of skill gap dictionaries with priority
            hours_per_week: Hours available per week for learning
            
        Returns:
            Detailed learning roadmap
        """
        if hours_per_week is None:
            hours_per_week = self.DEFAULT_HOURS_PER_WEEK
        
        roadmap = []
        current_week = 1
        tasks_this_week = 0
        hours_used = 0
        
        # Organize by priority - critical first
        priority_order = ['CRITICAL', 'RECOMMENDED', 'BONUS']
        organized_gaps = []
        
        for priority in priority_order:
            organized_gaps.extend([g for g in skill_gaps if g.get('priority') == priority])
        
        for skill_gap in organized_gaps:
            skill = skill_gap.get('skill', 'Unnamed Skill')
            priority = skill_gap.get('priority', 'BONUS')
            estimated_days = skill_gap.get('estimated_days', 20)
            resources = skill_gap.get('suggested_resources', [])
            
            # Calculate weeks needed
            hours_needed = (estimated_days * 2)  # Assume 2 hours per day
            weeks_needed = (hours_needed + hours_per_week - 1) // hours_per_week  # Ceiling division
            
            # Task sequence for this skill
            tasks = self._generate_skill_tasks(skill, resources, weeks_needed)
            
            for task_idx, task in enumerate(tasks):
                task_week = 1 + (task_idx * (weeks_needed // max(len(tasks), 1)))
                
                roadmap_item = {
                    'week': current_week + task_week,
                    'skill': skill,
                    'priority': priority,
                    'task': task['task'],
                    'task_type': task['type'],
                    'duration_hours': task.get('hours', 2),
                    'resources': task.get('resources', []),
                    'milestone': task_idx == len(tasks) - 1,
                    'notes': task.get('notes', '')
                }
                
                roadmap.append(roadmap_item)
            
            current_week += weeks_needed
        
        self.roadmap = roadmap
        self.total_duration = current_week - 1
        return roadmap
    
    def _generate_skill_tasks(self, skill: str, resources: List[Dict],
                             weeks_available: int) -> List[Dict]:
        """Generate learning tasks for a skill"""
        tasks = [
            {
                'task': f'Learn {skill} fundamentals',
                'type': 'learning',
                'hours': 6,
                'resources': resources[:2] if resources else []
            },
            {
                'task': f'Complete {skill} hands-on exercises',
                'type': 'practice',
                'hours': 4,
                'notes': 'Follow tutorials and build mini projects'
            },
            {
                'task': f'Build a project using {skill}',
                'type': 'project',
                'hours': 8,
                'notes': 'Create a portfolio-worthy project'
            },
            {
                'task': f'Master advanced {skill} concepts',
                'type': 'advanced',
                'hours': 4,
                'notes': 'Dive deep into advanced topics'
            },
            {
                'task': f'{skill} - Code review and optimization',
                'type': 'review',
                'hours': 2,
                'notes': 'Review your code and optimize'
            }
        ]
        
        # Limit tasks based on available weeks
        max_tasks = min(len(tasks), max(2, weeks_available // 2))
        return tasks[:max_tasks]
    
    def generate_career_timeline(self, target_role: str,
                                skill_gaps: List[Dict]) -> Dict:
        """
        Generate career growth timeline
        
        Args:
            target_role: Target job role
            skill_gaps: List of skill gaps
            
        Returns:
            Career timeline with milestones
        """
        timeline = {
            'target_role': target_role,
            'current_phase': 'Skill Development',
            'milestones': [],
            'estimated_completion_weeks': 0
        }
        
        # Phase 1: Critical Skills
        critical_gaps = [g for g in skill_gaps if g.get('priority') == 'CRITICAL']
        if critical_gaps:
            critical_weeks = sum(g.get('estimated_days', 20) / 7 for g in critical_gaps)
            timeline['milestones'].append({
                'phase': 1,
                'name': 'Master Critical Skills',
                'duration_weeks': int(critical_weeks),
                'skills': [g['skill'] for g in critical_gaps],
                'description': 'Build foundation with essential skills',
                'success_criteria': 'Complete all critical skill projects'
            })
            timeline['estimated_completion_weeks'] += int(critical_weeks)
        
        # Phase 2: Recommended Skills
        recommended_gaps = [g for g in skill_gaps if g.get('priority') == 'RECOMMENDED']
        if recommended_gaps:
            recommended_weeks = sum(g.get('estimated_days', 20) / 7 for g in recommended_gaps)
            timeline['milestones'].append({
                'phase': 2,
                'name': 'Develop Recommended Skills',
                'duration_weeks': int(recommended_weeks),
                'skills': [g['skill'] for g in recommended_gaps],
                'description': 'Strengthen profile with additional skills',
                'success_criteria': 'Complete recommended skill projects'
            })
            timeline['estimated_completion_weeks'] += int(recommended_weeks)
        
        # Phase 3: Bonus Skills & Portfolio
        timeline['milestones'].append({
            'phase': 3,
            'name': 'Build Portfolio & Apply',
            'duration_weeks': 4,
            'description': 'Create portfolio projects and start applying to jobs',
            'success_criteria': 'Complete 2-3 portfolio projects',
            'activities': [
                'Build complex end-to-end project',
                'Contribute to open source',
                'Create GitHub portfolio',
                'Practice interviews'
            ]
        })
        timeline['estimated_completion_weeks'] += 4
        
        return timeline
    
    def generate_weekly_plan(self, roadmap: List[Dict],
                            start_week: int = 1) -> Dict:
        """
        Generate weekly breakdown of roadmap
        
        Args:
            roadmap: Learning roadmap
            start_week: Starting week number
            
        Returns:
            Weekly breakdown
        """
        weekly_plan = {}
        
        for item in roadmap:
            week = item['week'] + start_week - 1
            
            if week not in weekly_plan:
                weekly_plan[week] = {
                    'week': week,
                    'tasks': [],
                    'total_hours': 0,
                    'skills_covered': set()
                }
            
            weekly_plan[week]['tasks'].append({
                'skill': item['skill'],
                'task': item['task'],
                'type': item['task_type'],
                'hours': item['duration_hours']
            })
            
            weekly_plan[week]['total_hours'] += item['duration_hours']
            weekly_plan[week]['skills_covered'].add(item['skill'])
        
        # Convert sets to lists for JSON serialization
        for week in weekly_plan:
            weekly_plan[week]['skills_covered'] = list(weekly_plan[week]['skills_covered'])
        
        return Dict(sorted(weekly_plan.items()))
    
    def adjust_roadmap_for_pace(self, current_pace: str) -> List[Dict]:
        """
        Adjust roadmap based on pace (fast/normal/slow learner)
        
        Args:
            current_pace: 'fast', 'normal', or 'slow'
            
        Returns:
            Adjusted roadmap
        """
        pace_multipliers = {
            'fast': 0.7,      # 30% faster
            'normal': 1.0,
            'slow': 1.5       # 50% slower
        }
        
        multiplier = pace_multipliers.get(current_pace.lower(), 1.0)
        adjusted = []
        
        for item in self.roadmap:
            adjusted_item = item.copy()
            adjusted_item['duration_hours'] = int(item['duration_hours'] / multiplier)
            adjusted.append(adjusted_item)
        
        return adjusted
    
    def mark_task_complete(self, week: int, task_index: int) -> float:
        """
        Mark task as complete and calculate progress
        
        Args:
            week: Week number
            task_index: Task index in week
            
        Returns:
            Progress percentage
        """
        # Find and mark task
        for item in self.roadmap:
            if item['week'] == week and item.get('task'):
                item['completed'] = True
                break
        
        # Calculate progress
        completed = sum(1 for item in self.roadmap if item.get('completed'))
        total = len(self.roadmap)
        
        progress = (completed / total * 100) if total > 0 else 0
        return round(progress, 2)
    
    def get_next_milestone(self) -> Dict:
        """Get next milestone in roadmap"""
        for item in self.roadmap:
            if item.get('milestone') and not item.get('completed'):
                return item
        
        # If no incomplete milestones found, return next uncompleted task
        for item in self.roadmap:
            if not item.get('completed'):
                return item
        
        return {'message': 'Roadmap completed!'}
    
    def get_roadmap_summary(self) -> Dict:
        """Get summary of roadmap"""
        return {
            'total_items': len(self.roadmap),
            'total_duration_weeks': self.total_duration,
            'total_duration_months': round(self.total_duration / 4.3, 1),
            'items_completed': sum(1 for item in self.roadmap if item.get('completed')),
            'progress_percentage': round(
                sum(1 for item in self.roadmap if item.get('completed')) / 
                max(1, len(self.roadmap)) * 100, 2
            ),
            'next_milestone': self.get_next_milestone()
        }
