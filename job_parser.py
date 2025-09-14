import requests
from bs4 import BeautifulSoup
import re

def extract_job_details(url):
    """Extract job description from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Get text content
        text = soup.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 5]
        return ' '.join(lines)
        
    except Exception as e:
        return f"Could not extract job details: {str(e)}"

def extract_key_info(job_text):
    """Extract key information from job description"""
    # Extract role
    role = extract_role(job_text)
    
    # Extract experience
    experience = extract_experience(job_text)
    
    # Extract ALL skills (technical + non-technical)
    skills = extract_all_skills(job_text)
    
    return {
        'role': role,
        'experience': experience,
        'skills': skills
    }

def extract_role(job_text):
    """Extract job role/title"""
    role_patterns = [
        r'position:\s*([^\n]+?)(?:\n|\.|$)',
        r'role:\s*([^\n]+?)(?:\n|\.|$)',
        r'job title:\s*([^\n]+?)(?:\n|\.|$)',
        r'looking for (?:a|an)?\s*([^\n]+?)(?:developer|engineer|analyst|designer|manager|specialist|coordinator|director)',
        r'hiring.*?([^\n]+?)(?:developer|engineer|analyst|designer|manager|specialist|coordinator|director)',
        r'title:\s*([^\n]+)'
    ]
    
    for pattern in role_patterns:
        match = re.search(pattern, job_text, re.IGNORECASE)
        if match:
            role = match.group(1).strip()
            # Clean up the role
            role = re.sub(r'[^a-zA-Z0-9\s\-/]', '', role)
            return role.title()
    
    return "Professional Role"

def extract_experience(job_text):
    """Extract experience requirement"""
    exp_patterns = [
        r'(\d+)[+\-]?\s*years?',
        r'experience.*?(\d+)[+\-]?\s*years?',
        r'(\d+)[+\-]?\s*yr',
        r'(\d+)\+?\s*years?.*?experience',
        r'minimum.*?(\d+).*?years',
        r'at least.*?(\d+).*?years'
    ]
    
    years_found = []
    for pattern in exp_patterns:
        matches = re.findall(pattern, job_text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]  # Handle capture groups
            if match.isdigit():
                years_found.append(int(match))
    
    if years_found:
        return f"{max(years_found)}+ years"
    
    return "Experience not specified"

def extract_all_skills(job_text):
    """Extract ALL skills (technical + non-technical + soft skills)"""
    # Technical skills
    technical_skills = extract_technical_skills(job_text)
    
    # Non-technical and soft skills
    soft_skills = extract_soft_skills(job_text)
    
    # Combine and remove duplicates
    all_skills = list(set(technical_skills + soft_skills))
    
    # Sort for better readability (technical first, then soft skills)
    return sorted(all_skills, key=lambda x: (x not in technical_skills, x))

def extract_technical_skills(job_text):
    """Extract technical skills"""
    # Comprehensive list of technical skills
    tech_skills_list = [
        # Programming Languages
        'Python', 'JavaScript', 'Java', 'TypeScript', 'C++', 'C#', 'Ruby', 'PHP', 'Go', 'Rust',
        'Swift', 'Kotlin', 'SQL', 'R', 'MATLAB', 'Scala', 'Perl', 'HTML', 'CSS', 'SASS', 'LESS',
        
        # Frameworks & Libraries
        'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring', 'Express',
        'Ruby on Rails', 'Laravel', 'jQuery', 'Bootstrap', 'TensorFlow', 'PyTorch', 'Keras',
        'scikit-learn', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn',
        
        # Databases
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'SQL Server', 'Cassandra',
        'Elasticsearch', 'DynamoDB', 'Firebase',
        
        # Tools & Platforms
        'Git', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'Google Cloud', 'Heroku', 'Jenkins',
        'Travis CI', 'CircleCI', 'JIRA', 'Confluence', 'Slack', 'Trello', 'Asana',
        'Tableau', 'Power BI', 'Excel', 'Word', 'PowerPoint', 'Outlook',
        
        # methodologies
        'Agile', 'Scrum', 'Kanban', 'Waterfall', 'DevOps', 'CI/CD', 'TDD', 'BDD',
        
        # Other technical
        'REST API', 'GraphQL', 'Microservices', 'Machine Learning', 'AI', 'Data Analysis',
        'Data Visualization', 'Big Data', 'Cloud Computing', 'Cybersecurity', 'Networking',
        'Linux', 'Unix', 'Windows Server', 'Shell Scripting', 'Bash'
    ]
    
    found_tech_skills = []
    
    # Check for exact matches
    for skill in tech_skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', job_text, re.IGNORECASE):
            found_tech_skills.append(skill)
    
    return found_tech_skills

def extract_soft_skills(job_text):
    """Extract soft skills and non-technical skills"""
    soft_skills_list = [
        # Communication
        'Communication', 'Verbal Communication', 'Written Communication', 'Presentation',
        'Public Speaking', 'Storytelling', 'Technical Writing',
        
        # Leadership
        'Leadership', 'Team Management', 'Project Management', 'Mentoring', 'Coaching',
        'Decision Making', 'Strategic Thinking', 'Delegation',
        
        # Collaboration
        'Teamwork', 'Collaboration', 'Cross-functional Collaboration', 'Stakeholder Management',
        'Relationship Building', 'Networking',
        
        # Problem-solving
        'Problem Solving', 'Critical Thinking', 'Analytical Thinking', 'Creativity',
        'Innovation', 'Troubleshooting', 'Research', 'Analysis',
        
        # Personal skills
        'Time Management', 'Organization', 'Multitasking', 'Adaptability', 'Flexibility',
        'Work Ethic', 'Professionalism', 'Reliability', 'Attention to Detail',
        'Self-motivation', 'Initiative', 'Curiosity', 'Continuous Learning',
        
        # Business skills
        'Business Acumen', 'Customer Service', 'Client Management', 'Sales', 'Marketing',
        'Negotiation', 'Conflict Resolution', 'Emotional Intelligence',
        
        # Other
        'Remote Work', 'Agile Methodology', 'Scrum Master', 'Product Management',
        'Quality Assurance', 'Testing', 'Documentation'
    ]
    
    found_soft_skills = []
    
    # Check for soft skills
    for skill in soft_skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', job_text, re.IGNORECASE):
            found_soft_skills.append(skill)
    
    # Extract skills from common phrases
    skill_phrases = {
        'Communication': r'communication skills|excellent communicator',
        'Teamwork': r'team player|work well in teams|collaborative spirit',
        'Problem Solving': r'problem-solving|solve problems|analytical skills',
        'Leadership': r'leadership skills|ability to lead',
        'Time Management': r'time management|meet deadlines|organizational skills',
        'Adaptability': r'adaptable|ability to adapt|fast-paced environment'
    }
    
    for skill, pattern in skill_phrases.items():
        if skill not in found_soft_skills and re.search(pattern, job_text, re.IGNORECASE):
            found_soft_skills.append(skill)
    
    return found_soft_skills

def debug_skill_extraction(job_text):
    """Debug function to see what skills are being extracted"""
    print("=== SKILL EXTRACTION DEBUG ===")
    print("Technical skills:", extract_technical_skills(job_text))
    print("Soft skills:", extract_soft_skills(job_text))
    print("All skills:", extract_all_skills(job_text))
    print("==============================")

# Test with sample job description
if __name__ == "__main__":
    sample_job = """
    We're hiring a Senior Software Engineer with 5+ years of experience in Python and JavaScript.
    Required skills: React, Node.js, AWS, Docker, excellent communication skills, teamwork.
    Must have strong problem-solving abilities and leadership experience.
    Nice to have: Kubernetes, Machine Learning, project management.
    """
    
    debug_skill_extraction(sample_job)
