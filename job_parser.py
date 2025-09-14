import requests
from bs4 import BeautifulSoup
import re

def extract_job_details(url):
    """Simple job description extraction"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Get text content
        text = soup.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return ' '.join(lines)
        
    except:
        return "Could not extract job details"

def extract_key_info(job_text):
    """Extract key information from job description"""
    job_lower = job_text.lower()
    
    # Extract role
    role = extract_role(job_lower)
    
    # Extract experience
    experience = extract_experience(job_lower)
    
    # Extract skills
    skills = extract_skills(job_lower)
    
    return {
        'role': role,
        'experience': experience,
        'skills': skills
    }

def extract_role(job_text):
    """Extract job role"""
    role_patterns = [
        r'looking for a (.+?)(?:developer|engineer|analyst|designer|manager)',
        r'position:\s*(.+?)\n',
        r'role:\s*(.+?)\n',
        r'job title:\s*(.+?)\n'
    ]
    
    for pattern in role_patterns:
        match = re.search(pattern, job_text, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()
    
    return "Software Developer"

def extract_experience(job_text):
    """Extract experience requirement"""
    exp_patterns = [
        r'(\d+)[+\-]?\s*years?',
        r'experience.*?(\d+)[+\-]?\s*years?',
        r'(\d+)[+\-]?\s*yr'
    ]
    
    for pattern in exp_patterns:
        match = re.search(pattern, job_text, re.IGNORECASE)
        if match:
            return f"{match.group(1)}+ years"
    
    return "Not specified"

def extract_skills(job_text):
    """Extract required skills"""
    common_skills = [
        'python', 'javascript', 'java', 'react', 'node', 'sql', 'html', 'css',
        'aws', 'docker', 'kubernetes', 'machine learning', 'data analysis',
        'typescript', 'angular', 'vue', 'django', 'flask', 'fastapi'
    ]
    
    found_skills = []
    for skill in common_skills:
        if skill in job_text:
            found_skills.append(skill.title())
    
    return found_skills[:5]  # Return top 5 skills
