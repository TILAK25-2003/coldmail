import requests
from bs4 import BeautifulSoup
import re

def extract_job_details(url):
    """Simple job description extraction"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Get text content
        text = soup.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 10]
        return ' '.join(lines)
        
    except Exception as e:
        return f"Could not extract job details: {str(e)}"

def extract_key_info(job_text):
    """Extract key information from job description"""
    job_lower = job_text.lower()
    
    # Extract role
    role = extract_role(job_lower)
    
    # Extract experience
    experience = extract_experience(job_lower)
    
    # Extract skills - FIXED
    skills = extract_skills(job_text)  # Use original text for case sensitivity
    
    return {
        'role': role,
        'experience': experience,
        'skills': skills
    }

def extract_role(job_text):
    """Extract job role"""
    role_patterns = [
        r'position:\s*([^\n]+)',
        r'role:\s*([^\n]+)',
        r'job title:\s*([^\n]+)',
        r'looking for a ([^\n]+?)(?:developer|engineer|analyst|designer|manager|specialist)',
        r'hiring.*?([^\n]+?)(?:developer|engineer|analyst|designer|manager|specialist)'
    ]
    
    for pattern in role_patterns:
        match = re.search(pattern, job_text, re.IGNORECASE)
        if match:
            role = match.group(1).strip()
            # Clean up the role
            role = re.sub(r'[^a-zA-Z0-9\s]', '', role)
            return role.title()
    
    return "Software Developer"

def extract_experience(job_text):
    """Extract experience requirement"""
    exp_patterns = [
        r'(\d+)[+\-]?\s*years?',
        r'experience.*?(\d+)[+\-]?\s*years?',
        r'(\d+)[+\-]?\s*yr',
        r'(\d+)\+?\s*years?.*?experience'
    ]
    
    for pattern in exp_patterns:
        matches = re.findall(pattern, job_text, re.IGNORECASE)
        if matches:
            # Get the highest experience requirement
            years = [int(match) for match in matches if match.isdigit()]
            if years:
                return f"{max(years)}+ years"
    
    return "Not specified"

def extract_skills(job_text):
    """Extract required skills - FIXED VERSION"""
    # Comprehensive list of tech skills (case sensitive)
    tech_skills = [
        'Python', 'JavaScript', 'Java', 'React', 'Node.js', 'SQL', 'HTML', 'CSS',
        'AWS', 'Docker', 'Kubernetes', 'Machine Learning', 'Data Analysis',
        'TypeScript', 'Angular', 'Vue', 'Django', 'Flask', 'FastAPI', 'PostgreSQL',
        'MySQL', 'MongoDB', 'Git', 'GitHub', 'CI/CD', 'REST API', 'GraphQL',
        'TensorFlow', 'PyTorch', 'scikit-learn', 'Pandas', 'NumPy', 'Matplotlib',
        'Seaborn', 'Excel', 'Tableau', 'Power BI', 'Azure', 'Google Cloud',
        'Linux', 'Unix', 'Bash', 'Shell', 'C++', 'C#', '.NET', 'Spring Boot',
        'Ruby', 'Rails', 'PHP', 'Laravel', 'WordPress', 'Swift', 'Kotlin',
        'Android', 'iOS', 'React Native', 'Flutter', 'Firebase', 'Heroku',
        'Jenkins', 'Travis CI', 'JIRA', 'Agile', 'Scrum', 'DevOps'
    ]
    
    found_skills = []
    
    # Check for each skill in the job text
    for skill in tech_skills:
        # Look for exact skill name (case insensitive)
        if re.search(r'\b' + re.escape(skill) + r'\b', job_text, re.IGNORECASE):
            found_skills.append(skill)
    
    # Also look for skill patterns
    skill_patterns = {
        'React': r'react(?:\.js)?',
        'Node.js': r'node(?:\.js)?',
        'JavaScript': r'javascript|js\b',
        'TypeScript': r'typescript|ts\b',
        'SQL': r'\bsql\b',
        'AWS': r'\baws\b',
        'Machine Learning': r'machine learning|ml\b',
        'Data Analysis': r'data analysis|data analytic',
        'CI/CD': r'ci/cd|continuous integration',
        'REST API': r'rest api|restful',
        'GraphQL': r'graphql',
        'Docker': r'docker',
        'Kubernetes': r'kubernetes|k8s'
    }
    
    for skill_name, pattern in skill_patterns.items():
        if skill_name not in found_skills and re.search(pattern, job_text, re.IGNORECASE):
            found_skills.append(skill_name)
    
    # Remove duplicates and return top 8 skills
    unique_skills = list(dict.fromkeys(found_skills))
    return unique_skills[:8]

# Test function to debug skill extraction
def test_skill_extraction():
    """Test skill extraction with sample text"""
    test_text = """
    We are looking for a Python Developer with 3+ years of experience.
    Required skills: Python, Django, React, JavaScript, SQL, AWS.
    Nice to have: Docker, Kubernetes, Machine Learning.
    """
    
    skills = extract_skills(test_text)
    print("Extracted skills:", skills)
    return skills

if __name__ == "__main__":
    test_skill_extraction()
