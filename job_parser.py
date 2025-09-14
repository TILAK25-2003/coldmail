import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def extract_job_details(url):
    """Extract job description and company info from URL"""
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
        job_text = ' '.join(lines)
        
        # Extract company name from URL and page
        company_name = extract_company_name(url, soup)
        
        return {
            'job_text': job_text,
            'company_name': company_name,
            'url': url
        }
        
    except Exception as e:
        return {
            'job_text': f"Could not extract job details: {str(e)}",
            'company_name': "Unknown Company",
            'url': url
        }

def extract_company_name(url, soup):
    """Extract company name from URL and page content"""
    # Try to get company name from URL first
    domain = urlparse(url).netloc
    company_from_url = domain.replace('www.', '').split('.')[0].title()
    
    # Try to extract from page title and meta tags
    possible_names = set()
    
    # From title tag
    if soup.title:
        title_text = soup.title.get_text()
        possible_names.update(extract_possible_company_names(title_text))
    
    # From meta tags
    meta_tags = soup.find_all('meta', attrs={'name': ['og:site_name', 'application-name', 'apple-mobile-web-app-title']})
    for meta in meta_tags:
        if meta.get('content'):
            possible_names.update(extract_possible_company_names(meta.get('content')))
    
    # From h1 and strong tags (often contain company names)
    for tag in soup.find_all(['h1', 'h2', 'strong', 'b']):
        text = tag.get_text().strip()
        if len(text) < 50:  # Company names are usually short
            possible_names.update(extract_possible_company_names(text))
    
    # Filter out garbage and choose the best name
    valid_names = [name for name in possible_names if 2 <= len(name) <= 30 and name != company_from_url]
    
    if valid_names:
        # Prefer longer names (more likely to be actual company names)
        return max(valid_names, key=len)
    
    return company_from_url

def extract_possible_company_names(text):
    """Extract possible company names from text"""
    names = set()
    
    # Look for patterns like "Company Name" or "Company Name Careers"
    patterns = [
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)(?:\s+(?:Careers|Jobs|Hiring|Career))',
        r'Careers at\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'Welcome to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+[-–]+\s+Careers',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        names.update(matches)
    
    # Also add any capitalized words that might be company names
    words = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+', text)
    names.update(words)
    
    return names

def extract_key_info(job_text):
    """Extract all types of skills from job description"""
    # Extract technical skills
    technical_skills = extract_technical_skills(job_text)
    
    # Extract soft skills
    soft_skills = extract_soft_skills(job_text)
    
    # Extract role
    role = extract_role(job_text)
    
    # Extract experience
    experience = extract_experience(job_text)
    
    # Extract tools and technologies
    tools = extract_tools(job_text)
    
    return {
        'role': role,
        'experience': experience,
        'technical_skills': technical_skills,
        'soft_skills': soft_skills,
        'tools': tools,
        'all_skills': technical_skills + soft_skills + tools
    }

def extract_technical_skills(job_text):
    """Extract technical skills"""
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
        'Jenkins', 'Travis CI', 'JIRA', 'Agile', 'Scrum', 'DevOps', 'NoSQL',
        'Redis', 'Kafka', 'RabbitMQ', 'Elasticsearch', 'Spark', 'Hadoop'
    ]
    
    return find_skills_in_text(job_text, tech_skills)

def extract_soft_skills(job_text):
    """Extract soft skills"""
    soft_skills = [
        'Communication', 'Leadership', 'Teamwork', 'Problem Solving', 'Creativity',
        'Time Management', 'Adaptability', 'Critical Thinking', 'Collaboration',
        'Interpersonal Skills', 'Presentation', 'Negotiation', 'Conflict Resolution',
        'Emotional Intelligence', 'Decision Making', 'Strategic Thinking', 'Innovation',
        'Attention to Detail', 'Organization', 'Multitasking', 'Customer Service',
        'Mentoring', 'Coaching', 'Training', 'Public Speaking', 'Writing',
        'Analytical Thinking', 'Research', 'Planning', 'Coordination', 'Flexibility',
        'Resilience', 'Motivation', 'Initiative', 'Accountability', 'Professionalism',
        'Networking', 'Relationship Building', 'Persuasion', 'Influence', 'Diplomacy'
    ]
    
    return find_skills_in_text(job_text, soft_skills)

def extract_tools(job_text):
    """Extract tools and technologies"""
    tools = [
        'JIRA', 'Confluence', 'Slack', 'Teams', 'Zoom', 'Trello', 'Asana',
        'Salesforce', 'HubSpot', 'Google Workspace', 'Microsoft Office',
        'Google Analytics', 'Adobe Creative Suite', 'Figma', 'Sketch',
        'Visual Studio', 'VS Code', 'IntelliJ', 'Eclipse', 'Xcode',
        'Android Studio', 'Postman', 'Swagger', 'Splunk', 'Datadog',
        'New Relic', 'Sentry', 'GitLab', 'Bitbucket', 'Jenkins',
        'CircleCI', 'GitHub Actions', 'Terraform', 'Ansible', 'Chef',
        'Puppet', 'Nagios', 'Prometheus', 'Grafana', 'Kibana'
    ]
    
    return find_skills_in_text(job_text, tools)

def find_skills_in_text(text, skills_list):
    """Find skills from list in text"""
    found_skills = []
    text_lower = text.lower()
    
    for skill in skills_list:
        # Check for exact match with word boundaries
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            found_skills.append(skill)
    
    return list(set(found_skills))[:10]  # Remove duplicates and limit

def extract_role(job_text):
    """Extract job role"""
    role_patterns = [
        r'position:\s*([^\n]+?)(?=\n|\.|$)',
        r'role:\s*([^\n]+?)(?=\n|\.|$)',
        r'job title:\s*([^\n]+?)(?=\n|\.|$)',
        r'looking for (?:a|an)?\s*([^\n]+?)(?=\n|\.|$)',
        r'hiring.*?([^\n]+?)(?:developer|engineer|analyst|designer|manager|specialist|lead|architect)',
        r'join.*?as.*?([^\n]+?)(?=\n|\.|$)'
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
        r'at least.*?(\d+).*?years'
    ]
    
    for pattern in exp_patterns:
        matches = re.findall(pattern, job_text, re.IGNORECASE)
        if matches:
            years = [int(match) for match in matches if isinstance(match, str) and match.isdigit()]
            if years:
                return f"{max(years)}+ years"
    
    return "Not specified"
