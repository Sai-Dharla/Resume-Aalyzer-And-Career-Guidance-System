"""
Main Entry Point for Resume Analyzer and Career Guidance System (RACGS)
Demonstrates complete usage of all core modules
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core import (
    ResumeProcessor, SkillExtractor, ATSScorer, SkillGapAnalyzer,
    JobMatcher, ResumeImprover, InterviewGenerator, RoadmapGenerator,
    CareerSimulator, RecruiterView
)
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RACSSystem:
    """Complete Resume Analyzer and Career Guidance System"""
    
    def __init__(self):
        """Initialize RACGS system with all modules"""
        self.resume_processor = ResumeProcessor()
        self.skill_extractor = SkillExtractor()
        self.ats_scorer = ATSScorer()
        self.skill_gap_analyzer = SkillGapAnalyzer()
        self.job_matcher = JobMatcher()
        self.resume_improver = ResumeImprover()
        self.interview_generator = InterviewGenerator()
        self.roadmap_generator = RoadmapGenerator()
        self.career_simulator = CareerSimulator()
        self.recruiter_view = RecruiterView()
        
        self.analysis_results = {}
    
    def analyze_resume(self, resume_path: str, target_job: str = None) -> Dict:
        """
        Complete resume analysis pipeline
        
        Args:
            resume_path: Path to resume file
            target_job: Target job role for analysis
            
        Returns:
            Complete analysis report
        """
        logger.info(f"Starting resume analysis for: {resume_path}")
        
        # Step 1: Extract resume text
        logger.info("Step 1: Extracting resume text...")
        resume_text = self.resume_processor.extract_text(resume_path)
        
        if not resume_text:
            logger.error("Failed to extract resume text")
            return {}
        
        # Step 2: Process and structure data
        logger.info("Step 2: Processing and structuring resume data...")
        structured_data = self.resume_processor.process_resume(resume_path)
        
        # Step 3: Extract skills
        logger.info("Step 3: Extracting skills...")
        skills_by_category = self.skill_extractor.extract_skills(resume_text)
        all_skills = self.skill_extractor.get_all_skills()
        
        logger.info(f"Found {len(all_skills)} unique skills")
        
        # Step 4: Calculate ATS Score
        logger.info("Step 4: Calculating ATS score...")
        ats_result = self.ats_scorer.calculate_ats_score(
            skills_by_category,
            structured_data.get('projects', []),
            structured_data.get('experience', []),
            structured_data.get('education', []),
            resume_text,
            required_skills=None if not target_job else 
                self.skill_gap_analyzer.get_skill_requirements(target_job).get('critical', [])
        )
        ats_score = ats_result['total_score']
        logger.info(f"ATS Score: {ats_score}/100")
        
        # Step 5: Skill Gap Analysis
        logger.info("Step 5: Analyzing skill gaps...")
        gap_analysis = self.skill_gap_analyzer.analyze_gap(all_skills, target_job or 'Software Developer')
        gap_report = self.skill_gap_analyzer.get_gap_summary()
        
        # Step 6: Resume Improvement
        logger.info("Step 6: Analyzing resume improvements...")
        improvement_analysis = self.resume_improver.analyze_resume(resume_text)
        improvement_suggestions = self.resume_improver.get_improvement_suggestions(resume_text)
        
        # Step 7: Generate Interview Questions
        logger.info("Step 7: Generating interview questions...")
        interview_questions = self.interview_generator.get_multiple_questions(
            count=5,
            mix=['behavioral', 'technical']
        )
        self.interview_generator.job_role = target_job or 'Software Developer'
        
        # Step 8: Generate Learning Roadmap
        logger.info("Step 8: Generating learning roadmap...")
        roadmap = self.roadmap_generator.generate_learning_roadmap(
            gap_report['priority_roadmap'],
            hours_per_week=15
        )
        career_timeline = self.roadmap_generator.generate_career_timeline(
            target_job or 'Software Developer',
            gap_report['priority_roadmap']
        )
        
        # Step 9: Career Simulation
        logger.info("Step 9: Running career simulations...")
        job_readiness = self.career_simulator.estimate_job_readiness(
            gap_report['total_missing_skills'],
            ats_score,
            len(structured_data.get('experience', []))
        )
        scenarios = self.career_simulator.generate_multiple_scenarios(
            gap_report['priority_roadmap'],
            ats_score,
            len(structured_data.get('experience', []))
        )
        
        # Step 10: Recruiter View Analysis
        logger.info("Step 10: Generating recruiter perspective...")
        first_impression = self.recruiter_view.calculate_first_impression(
            structured_data, ats_score, all_skills
        )
        experience_match = min(1.0, len(structured_data.get('experience', [])) / 3)
        skill_match = min(1.0, len(all_skills) / 10)
        hire_assessment = self.recruiter_view.calculate_hire_probability(
            ats_score, experience_match, skill_match
        )
        recruiter_feedback = self.recruiter_view.generate_recruiter_feedback(
            structured_data, all_skills, ats_score,
            hire_assessment['hire_probability_percentage'],
            self.skill_gap_analyzer.get_skill_requirements(target_job or 'Software Developer').get('critical', [])
        )
        
        # Compile complete report
        self.analysis_results = {
            'resume_data': structured_data,
            'skills_analysis': {
                'extracted_skills': all_skills,
                'by_category': skills_by_category
            },
            'ats_analysis': ats_result,
            'skill_gaps': gap_report,
            'improvements_needed': improvement_suggestions,
            'interview_preparation': {
                'sample_questions': interview_questions,
                'target_job': target_job or 'Software Developer'
            },
            'learning_roadmap': {
                'detailed_roadmap': roadmap,
                'career_timeline': career_timeline,
                'summary': self.roadmap_generator.get_roadmap_summary()
            },
            'job_readiness': job_readiness,
            'career_scenarios': scenarios,
            'recruiter_perspective': {
                'first_impression': first_impression,
                'hire_probability': hire_assessment,
                'feedback': recruiter_feedback
            }
        }
        
        logger.info("Resume analysis complete!")
        return self.analysis_results
    
    def generate_report(self, output_path: str = 'analysis_report.json'):
        """Generate JSON report of analysis"""
        with open(output_path, 'w') as f:
            # Convert non-serializable objects
            report_data = json.dumps(self.analysis_results, indent=2, default=str)
            f.write(report_data)
        logger.info(f"Report saved to: {output_path}")
    
    def print_summary(self):
        """Print summary of analysis"""
        if not self.analysis_results:
            print("No analysis results available")
            return
        
        print("\n" + "="*60)
        print("RESUME ANALYSIS SUMMARY")
        print("="*60)
        
        # ATS Score
        ats = self.analysis_results.get('ats_analysis', {})
        print(f"\nATS SCORE: {ats.get('total_score', 'N/A')}/100")
        print(f"  Skills: {ats.get('section_scores', {}).get('skills', 'N/A')}/100")
        print(f"  Experience: {ats.get('section_scores', {}).get('experience', 'N/A')}/100")
        print(f"  Education: {ats.get('section_scores', {}).get('education', 'N/A')}/100")
        
        # Skills
        skills_analysis = self.analysis_results.get('skills_analysis', {})
        print(f"\nTOTAL SKILLS FOUND: {len(skills_analysis.get('extracted_skills', []))}")
        
        # Skill Gaps
        gaps = self.analysis_results.get('skill_gaps', {})
        print(f"\nSKILL GAPS:")
        print(f"  Critical: {gaps.get('critical_gaps', 0)}")
        print(f"  Recommended: {gaps.get('recommended_gaps', 0)}")
        print(f"  Bonus: {gaps.get('bonus_gaps', 0)}")
        print(f"  Estimated Learning Time: {gaps.get('estimated_learning_weeks', 0)} weeks")
        
        # Job Readiness
        readiness = self.analysis_results.get('job_readiness', {})
        print(f"\nJOB READINESS:")
        print(f"  Current Score: {readiness.get('current_readiness_score', 'N/A')}/100")
        print(f"  Status: {readiness.get('status', 'N/A')}")
        print(f"  Weeks to Ready: {readiness.get('estimated_weeks_to_ready', 'N/A')}")
        
        # Recruiter View
        recruiter = self.analysis_results.get('recruiter_perspective', {})
        hire_prob = recruiter.get('hire_probability', {})
        print(f"\nRECRUITER VIEW:")
        print(f"  Hire Probability: {hire_prob.get('hire_probability_percentage', 'N/A')}%")
        print(f"  Hiring Decision: {hire_prob.get('hiring_decision', 'N/A')}")
        print(f"  First Impression: {recruiter.get('first_impression', {}).get('impression_score', 'N/A')}/100")
        
        print("\n" + "="*60 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Resume Analyzer & Career Guidance System')
    parser.add_argument('resume_path', help='Path to resume file (PDF or DOCX)')
    parser.add_argument('--job', default='Software Developer', help='Target job role')
    parser.add_argument('--output', default='analysis_report.json', help='Output report path')
    
    args = parser.parse_args()
    
    # Initialize system
    racgs = RACSSystem()
    
    # Analyze resume
    results = racgs.analyze_resume(args.resume_path, args.job)
    
    # Print summary
    racgs.print_summary()
    
    # Generate report
    racgs.generate_report(args.output)
    
    print(f"✓ Full analysis report saved to: {args.output}")


if __name__ == '__main__':
    # For testing, create a simple demo
    print("Resume Analyzer and Career Guidance System (RACGS)")
    print("=" * 60)
    print("\nUsage: python main.py <resume_path> --job 'Target Job Role'")
    print("\nExample: python main.py resume.pdf --job 'Full Stack Developer'")
    print("\n" + "="*60)
