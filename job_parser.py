import requests
from bs4 import BeautifulSoup
import re
import tldextract
from urllib.parse import urlparse

def extract_job_details(url):
    """Extract job details from URL with error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Check if content is HTML
        if 'text/html' not in response.headers.get('content-type', '').lower():
            return "Error: URL does not contain HTML content"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
            element.decompose()
        
        # Get text content from main content areas
        content_selectors = [
            'main', 'article', 'section', 
            '[class*="job"]', '[class*="description"]', '[class*="content"]',
            '#content', '.content', '#main', '.main'
        ]
        
        text_content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            for element in elements:
                text_content += element.get_text() + "\n"
        
        if not text_content.strip():
            text_content = soup.get_text()
        
        # Clean up text
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)
        
        if len(cleaned_text) < 100:
            return "Error: Insufficient content extracted from URL"
            
        return cleaned_text
        
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to access URL - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def extract_company_name(url, job_text):
    """Extract company name from URL and job text"""
    # Try to extract from URL first
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Common job board domains
    job_boards = ['linkedin', 'indeed', 'glassdoor', 'monster', 'careerbuilder', 'ziprecruiter']
    
    if any(job_board in domain for job_board in job_boards):
        # For job boards, try to extract company name from text
        company_patterns = [
            r'at\s+([A-Z][a-zA-Z0-9&\s\.]+)(?:\s+|$|,)',
            r'company:\s*([^\n]+)',
            r'employer:\s*([^\n]+)',
            r'([A-Z][a-zA-Z0-9&\s\.]+)\s+is hiring',
            r'hiring at\s+([A-Z][a-zA-Z0-9&\s\.]+)'
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, job_text, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if len(company.split()) <= 5:  # Reasonable company name length
                    return company.title()
    
    # Extract from domain name as fallback
    extracted = tldextract.extract(url)
    if extracted.domain and extracted.domain not in job_boards:
        return extracted.domain.title()
    
    return "The Company"

def extract_key_info(job_text):
    """Extract key information from job description"""
    # Extract role
    role = extract_role(job_text)
    
    # Extract experience
    experience = extract_experience(job_text)
    
    # Extract all types of skills
    skills = extract_all_skills(job_text)
    
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
        r'looking for a ([^\n]+?)(?:developer|engineer|analyst|designer|manager|specialist|coordinator)',
        r'hiring.*?([^\n]+?)(?:developer|engineer|analyst|designer|manager|specialist|coordinator)',
        r'job.*?([^\n]+?)(?:developer|engineer|analyst|designer|manager|specialist|coordinator)'
    ]
    
    for pattern in role_patterns:
        match = re.search(pattern, job_text, re.IGNORECASE)
        if match:
            role = match.group(1).strip()
            # Clean up the role
            role = re.sub(r'[^a-zA-Z0-9\s\-]', '', role)
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
        r'(\d+).*?years.*?experience'
    ]
    
    for pattern in exp_patterns:
        matches = re.findall(pattern, job_text, re.IGNORECASE)
        if matches:
            years = [int(match) for match in matches if isinstance(match, str) and match.isdigit()]
            if years:
                return f"{max(years)}+ years"
    
    return "Not specified"

def extract_all_skills(job_text):
    """Extract both technical and non-technical skills"""
    # Technical skills
    tech_skills = [
        'Python', 'JavaScript', 'Java', 'React', 'Node.js', 'SQL', 'HTML', 'CSS',
        'AWS', 'Docker', 'Kubernetes', 'Machine Learning', 'Data Analysis',
        'TypeScript', 'Angular', 'Vue', 'Django', 'Flask', 'FastAPI', 'PostgreSQL',
        'MySQL', 'MongoDB', 'Git', 'GitHub', 'CI/CD', 'REST API', 'GraphQL',
        'TensorFlow', 'PyTorch', 'scikit-learn', 'Pandas', 'NumPy', 'Matplotlib',
        'Seaborn', 'Excel', 'Tableau', 'Power BI', 'Azure', 'Google Cloud',
        'Linux', 'Unix', 'Bash', 'Shell', 'C++', 'C#', '.NET', 'Spring Boot',
        'Ruby', 'Rails', 'PHP', 'Laravel', 'WordPress', 'Swift', 'Kotlin',
        'Android', 'iOS', 'React Native', 'Flutter', 'Firebase', 'Heroku'
    ]
    
    # Non-technical skills
    soft_skills = [
        'Communication', 'Leadership', 'Teamwork', 'Problem Solving', 'Time Management',
        'Adaptability', 'Creativity', 'Critical Thinking', 'Project Management',
        'Agile', 'Scrum', 'Collaboration', 'Presentation', 'Negotiation',
        'Customer Service', 'Analytical Skills', 'Strategic Planning', 'Mentoring',
        'Public Speaking', 'Writing', 'Research', 'Decision Making', 'Innovation',
        'Conflict Resolution', 'Emotional Intelligence', 'Networking', 'Sales',
        'Marketing', 'Budgeting', 'Training', 'Coaching', 'Multitasking'
    ]
    
    # Tools and methodologies
    tools = [
        'JIRA', 'Confluence', 'Slack', 'Trello', 'Asana', 'Microsoft Office',
        'Google Workspace', 'Zoom', 'Teams', 'Salesforce', 'HubSpot', 'WordPress',
        'Shopify', 'Google Analytics', 'Adobe Creative Suite', 'Figma', 'Sketch'
    ]
    
    all_skills = tech_skills + soft_skills + tools
    found_skills = []
    
    # Check for each skill in the job text (case insensitive)
    for skill in all_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', job_text, re.IGNORECASE):
            found_skills.append(skill)
    
    # Remove duplicates and return
    return list(dict.fromkeys(found_skills))[:15]  # Limit to 15 most relevant skills
