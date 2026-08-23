"""
Resume Processor Module
Handles resume text extraction and structured data conversion
Supports PDF and DOCX formats
"""

import os
from PyPDF2 import PdfReader
from docx import Document
import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class ResumeProcessor:
    """Process resumes and extract structured information"""
    
    def __init__(self):
        """Initialize resume processor"""
        self.text = ""
        self.structured_data = {
            'contact': {},
            'summary': '',
            'skills': [],
            'experience': [],
            'education': [],
            'projects': []
        }
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text from PDF
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """
        Extract text from DOCX file
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text from DOCX
        """
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting DOCX text: {str(e)}")
            return ""
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from resume file (PDF or DOCX)
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Extracted text
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            self.text = self.extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            self.text = self.extract_text_from_docx(file_path)
        else:
            logger.error(f"Unsupported file format: {file_ext}")
            self.text = ""
        
        return self.text
    
    def extract_contact_info(self) -> Dict:
        """
        Extract contact information from resume text
        
        Returns:
            Dictionary with email, phone, LinkedIn, GitHub
        """
        contact = {}
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.text)
        contact['email'] = emails[0] if emails else "Not found"
        
        # Extract phone
        phone_pattern = r'\b(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
        phones = re.findall(phone_pattern, self.text)
        contact['phone'] = phones[0][2] if phones else "Not found"
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
        linkedin = re.findall(linkedin_pattern, self.text, re.IGNORECASE)
        contact['linkedin'] = linkedin[0] if linkedin else "Not found"
        
        # Extract GitHub
        github_pattern = r'github\.com/[\w\-]+'
        github = re.findall(github_pattern, self.text, re.IGNORECASE)
        contact['github'] = github[0] if github else "Not found"
        
        self.structured_data['contact'] = contact
        return contact
    
    def extract_sections(self) -> Dict[str, str]:
        """
        Extract main sections from resume
        
        Returns:
            Dictionary with resume sections
        """
        sections = {
            'summary': '',
            'experience': '',
            'education': '',
            'skills': '',
            'projects': ''
        }
        
        text_lower = self.text.lower()
        lines = self.text.split('\n')
        
        # Define section keywords
        section_keywords = {
            'summary': ['summary', 'objective', 'professional summary', 'about'],
            'experience': ['experience', 'work experience', 'employment'],
            'education': ['education', 'educational', 'degree', 'university'],
            'skills': ['skills', 'technical skills', 'core competencies'],
            'projects': ['projects', 'portfolio', 'achievements']
        }
        
        # Find section start indices
        section_starts = {}
        for section, keywords in section_keywords.items():
            for i, line in enumerate(lines):
                if any(keyword in line.lower() for keyword in keywords):
                    section_starts[section] = i
                    break
        
        # Extract section content
        sorted_sections = sorted(section_starts.items(), key=lambda x: x[1])
        for idx, (section, start_line) in enumerate(sorted_sections):
            if idx < len(sorted_sections) - 1:
                end_line = sorted_sections[idx + 1][1]
                sections[section] = '\n'.join(lines[start_line:end_line])
            else:
                sections[section] = '\n'.join(lines[start_line:])
        
        return sections
    
    def parse_experience(self, experience_text: str) -> List[Dict]:
        """
        Parse experience section into structured format
        
        Args:
            experience_text: Raw experience section text
            
        Returns:
            List of experience entries
        """
        experiences = []
        
        # Split by common job separators
        job_blocks = re.split(r'\n(?=[A-Z])', experience_text)
        
        for block in job_blocks:
            if len(block.strip()) > 10:
                lines = block.strip().split('\n')
                experience = {
                    'company': lines[0] if lines else '',
                    'position': lines[1] if len(lines) > 1 else '',
                    'duration': '',
                    'description': '\n'.join(lines[2:]) if len(lines) > 2 else ''
                }
                
                # Try to extract duration (dates)
                date_pattern = r'(\d{1,2}/\d{4}|\d{4})\s*[-–]\s*(\d{1,2}/\d{4}|Present|\d{4})'
                dates = re.findall(date_pattern, block)
                if dates:
                    experience['duration'] = f"{dates[0][0]} - {dates[0][1]}"
                
                experiences.append(experience)
        
        return experiences
    
    def parse_education(self, education_text: str) -> List[Dict]:
        """
        Parse education section into structured format
        
        Args:
            education_text: Raw education section text
            
        Returns:
            List of education entries
        """
        educations = []
        
        # Split by common degree separators
        degree_blocks = re.split(r'\n(?=[A-Z])', education_text)
        
        for block in degree_blocks:
            if len(block.strip()) > 5:
                lines = block.strip().split('\n')
                education = {
                    'degree': '',
                    'field': '',
                    'institution': lines[0] if lines else '',
                    'year': ''
                }
                
                # Extract degree info from subsequent lines
                for line in lines[1:]:
                    if any(d in line.lower() for d in ['bachelor', 'master', 'phd', 'bs', 'ms', 'diploma']):
                        education['degree'] = line
                    # Extract year
                    year_match = re.search(r'\b(20\d{2})\b', line)
                    if year_match:
                        education['year'] = year_match.group(1)
                
                educations.append(education)
        
        return educations
    
    def process_resume(self, file_path: str) -> Dict:
        """
        Complete resume processing pipeline
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Structured resume data
        """
        # Extract text
        self.extract_text(file_path)
        
        if not self.text:
            return self.structured_data
        
        # Extract structured information
        self.extract_contact_info()
        
        sections = self.extract_sections()
        
        # Parse specific sections
        if sections['experience']:
            self.structured_data['experience'] = self.parse_experience(sections['experience'])
        
        if sections['education']:
            self.structured_data['education'] = self.parse_education(sections['education'])
        
        if sections['summary']:
            self.structured_data['summary'] = sections['summary'][:500]  # First 500 chars
        
        # Skills will be extracted by SkillExtractor
        self.structured_data['raw_text'] = self.text
        
        return self.structured_data
    
    def get_text(self) -> str:
        """Get extracted text"""
        return self.text
    
    def get_structured_data(self) -> Dict:
        """Get structured resume data"""
        return self.structured_data
