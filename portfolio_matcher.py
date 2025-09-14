# portfolio_matcher.py
import re
from typing import List, Dict

def find_relevant_projects(job_description: str, portfolio_projects: List[Dict]) -> List[Dict]:
    """
    Find portfolio projects relevant to the job description
    """
    relevant_projects = []
    
    for project in portfolio_projects:
        if is_project_relevant(job_description, project):
            relevant_projects.append(project)
    
    return relevant_projects

def is_project_relevant(job_description: str, project: Dict) -> bool:
    """
    Check if a project is relevant to the job description
    """
    # Simple keyword matching - you can enhance this with NLP later
    job_text = job_description.lower()
    project_skills = project.get('skills', [])
    project_description = project.get('description', '').lower()
    
    # Check if any project skills are mentioned in job description
    for skill in project_skills:
        if skill.lower() in job_text:
            return True
    
    # Check if project description contains job-related terms
    job_keywords = extract_keywords(job_text)
    for keyword in job_keywords:
        if keyword in project_description:
            return True
    
    return False

def extract_keywords(text: str) -> List[str]:
    """
    Extract potential keywords from job description
    """
    # Simple keyword extraction - can be enhanced
    keywords = re.findall(r'\b[a-z]{4,}\b', text.lower())
    return list(set(keywords))  # Remove duplicates

# Sample portfolio data structure
SAMPLE_PORTFOLIO = [
    {
        'name': 'E-commerce Website',
        'description': 'Full-stack e-commerce platform with React and Node.js',
        'skills': ['React', 'Node.js', 'MongoDB', 'JavaScript'],
        'url': 'https://github.com/username/ecommerce'
    },
    {
        'name': 'Data Analysis Tool',
        'description': 'Python tool for data analysis and visualization',
        'skills': ['Python', 'Pandas', 'Matplotlib', 'Data Analysis'],
        'url': 'https://github.com/username/data-tool'
    }
]
