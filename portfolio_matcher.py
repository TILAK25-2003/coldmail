import re
from typing import List, Dict

def find_relevant_projects(job_description: str, portfolio_projects: List[Dict]) -> List[Dict]:
    """
    Find portfolio projects relevant to the job description
    """
    if not job_description or not portfolio_projects:
        return []
    
    relevant_projects = []
    job_text = job_description.lower()
    
    for project in portfolio_projects:
        relevance_score = calculate_relevance_score(job_text, project)
        if relevance_score > 0:  # Only include projects with some relevance
            project_with_score = project.copy()
            project_with_score['relevance_score'] = relevance_score
            relevant_projects.append(project_with_score)
    
    # Sort by relevance score descending
    relevant_projects.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    return relevant_projects

def calculate_relevance_score(job_text: str, project: Dict) -> float:
    """
    Calculate relevance score between job description and project
    """
    score = 0.0
    
    # Check project skills
    project_skills = [skill.lower() for skill in project.get('skills', [])]
    for skill in project_skills:
        if skill in job_text:
            score += 2.0  # Higher weight for explicit skills
    
    # Check project description
    project_desc = project.get('description', '').lower()
    desc_keywords = extract_keywords(project_desc)
    
    # Check project name
    project_name = project.get('name', '').lower()
    name_keywords = extract_keywords(project_name)
    
    # Combine all project keywords
    all_project_keywords = set(project_skills + desc_keywords + name_keywords)
    
    # Check for keyword matches
    for keyword in all_project_keywords:
        if len(keyword) > 3 and keyword in job_text:
            score += 1.0
    
    # Bonus for multiple occurrences
    for keyword in all_project_keywords:
        occurrences = job_text.count(keyword)
        if occurrences > 1:
            score += (occurrences - 1) * 0.5
    
    return score

def extract_keywords(text: str) -> List[str]:
    """
    Extract meaningful keywords from text
    """
    # Remove common stop words and short words
    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'a', 'an'}
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    return [word for word in words if word not in stop_words]

# Sample portfolio data for testing
SAMPLE_PORTFOLIO = [
    {
        'name': 'E-commerce Website',
        'description': 'Full-stack e-commerce platform with React and Node.js handling user authentication and payment processing',
        'skills': ['React', 'Node.js', 'MongoDB', 'JavaScript', 'Express', 'HTML', 'CSS'],
        'url': 'https://github.com/example/ecommerce'
    },
    {
        'name': 'Data Analysis Tool',
        'description': 'Python-based data analysis and visualization tool using Pandas and Matplotlib for business insights',
        'skills': ['Python', 'Pandas', 'Matplotlib', 'Data Analysis', 'Data Visualization', 'SQL'],
        'url': 'https://github.com/example/data-tool'
    },
    {
        'name': 'Machine Learning Model',
        'description': 'Predictive machine learning model for customer classification using scikit-learn',
        'skills': ['Python', 'scikit-learn', 'Machine Learning', 'Pandas', 'NumPy', 'Data Science'],
        'url': 'https://github.com/example/ml-model'
    },
    {
        'name': 'Mobile Application',
        'description': 'Cross-platform mobile app built with React Native featuring real-time updates',
        'skills': ['React Native', 'JavaScript', 'Mobile Development', 'iOS', 'Android', 'Firebase'],
        'url': 'https://github.com/example/mobile-app'
    }
]
