# job_parser.py (enhanced with comprehensive roles and skills)
import requests
from bs4 import BeautifulSoup
import re

# Comprehensive database of roles and skills
ROLES_DATABASE = {
    # Technical Roles
    "software_development": [
        "Software Developer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
        "Mobile App Developer", "iOS Developer", "Android Developer", "Game Developer",
        "DevOps Engineer", "Site Reliability Engineer", "Systems Administrator",
        "Database Administrator", "Data Engineer", "Machine Learning Engineer",
        "AI Engineer", "Cloud Engineer", "Security Engineer", "Embedded Systems Engineer",
        "QA Engineer", "Test Automation Engineer", "Performance Engineer"
    ],
    "data_science": [
        "Data Scientist", "Data Analyst", "Business Intelligence Analyst", 
        "Data Architect", "Statistician", "Quantitative Analyst", "ML Researcher"
    ],
    "design_ux": [
        "UX Designer", "UI Designer", "Product Designer", "Graphic Designer",
        "Visual Designer", "Interaction Designer", "UX Researcher"
    ],
    "it_operations": [
        "IT Support Specialist", "Network Administrator", "Systems Analyst",
        "IT Manager", "Technical Support Engineer", "Help Desk Technician"
    ],
    
    # Non-Technical Roles
    "business": [
        "Business Analyst", "Product Manager", "Project Manager", "Program Manager",
        "Operations Manager", "Business Development Manager", "Strategy Consultant",
        "Management Consultant", "Product Owner", "Scrum Master"
    ],
    "marketing": [
        "Digital Marketing Specialist", "Content Marketer", "SEO Specialist",
        "Social Media Manager", "Marketing Manager", "Brand Manager",
        "Growth Hacker", "Email Marketing Specialist", "Content Strategist"
    ],
    "sales": [
        "Sales Representative", "Account Executive", "Sales Manager",
        "Business Development Representative", "Account Manager", "Sales Engineer"
    ],
    "customer_success": [
        "Customer Success Manager", "Account Manager", "Client Services Manager",
        "Customer Support Specialist", "Implementation Specialist"
    ],
    "hr_recruitment": [
        "HR Manager", "Recruiter", "Talent Acquisition Specialist",
        "HR Business Partner", "Compensation Analyst", "Training Specialist"
    ],
    "finance": [
        "Financial Analyst", "Accountant", "Controller", "CFO", "Financial Planner",
        "Investment Analyst", "Auditor", "Tax Specialist"
    ],
    "operations": [
        "Operations Manager", "Supply Chain Manager", "Logistics Coordinator",
        "Procurement Specialist", "Inventory Manager", "Quality Assurance Manager"
    ],
    "creative": [
        "Content Writer", "Copywriter", "Technical Writer", "Editor",
        "Video Producer", "Photographer", "Illustrator", "Animator"
    ],
    "education": [
        "Teacher", "Professor", "Instructional Designer", "Curriculum Developer",
        "Education Consultant", "Trainer", "Corporate Trainer"
    ],
    "healthcare": [
        "Nurse", "Doctor", "Physician Assistant", "Pharmacist",
        "Medical Researcher", "Healthcare Administrator", "Medical Coder"
    ],
    "legal": [
        "Lawyer", "Paralegal", "Legal Assistant", "Compliance Officer",
        "Contract Manager", "Intellectual Property Specialist"
    ],
    "other": [
        "Executive Assistant", "Office Manager", "Event Planner",
        "Real Estate Agent", "Project Coordinator", "Administrative Assistant"
    ]
}

SKILLS_DATABASE = {
    # Technical Skills
    "programming_languages": [
        "Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby", "Go", "Rust",
        "Swift", "Kotlin", "TypeScript", "SQL", "R", "Scala", "Perl", "HTML", "CSS"
    ],
    "frameworks": [
        "React", "Angular", "Vue.js", "Django", "Flask", "Spring", "Express.js",
        "Ruby on Rails", "Laravel", ".NET", "TensorFlow", "PyTorch", "Node.js"
    ],
    "databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQL Server",
        "Cassandra", "Elasticsearch", "DynamoDB", "Firebase"
    ],
    "cloud_platforms": [
        "AWS", "Azure", "Google Cloud", "Heroku", "DigitalOcean", "IBM Cloud"
    ],
    "devops_tools": [
        "Docker", "Kubernetes", "Jenkins", "Git", "CI/CD", "Terraform", "Ansible",
        "Prometheus", "Grafana", "Splunk", "New Relic"
    ],
    "data_science": [
        "Machine Learning", "Data Analysis", "Data Visualization", "Statistical Analysis",
        "Big Data", "Data Mining", "Natural Language Processing", "Computer Vision"
    ],
    
    # Non-Technical Skills
    "business_skills": [
        "Project Management", "Strategic Planning", "Business Analysis", "Financial Modeling",
        "Market Research", "Risk Management", "Process Improvement", "Supply Chain Management"
    ],
    "marketing_skills": [
        "Digital Marketing", "SEO", "Content Marketing", "Social Media Marketing",
        "Email Marketing", "Google Analytics", "PPC", "Brand Management", "Growth Marketing"
    ],
    "sales_skills": [
        "CRM", "Salesforce", "HubSpot", "Negotiation", "Lead Generation", "Account Management",
        "Sales Strategy", "Customer Relationship Management", "Pipeline Management"
    ],
    "communication_skills": [
        "Public Speaking", "Technical Writing", "Content Creation", "Presentation Skills",
        "Interpersonal Communication", "Copywriting", "Editing", "Storytelling"
    ],
    "management_skills": [
        "Team Leadership", "People Management", "Agile Methodology", "Scrum",
        "Resource Allocation", "Performance Management", "Conflict Resolution"
    ],
    "design_skills": [
        "UI/UX Design", "Graphic Design", "Adobe Creative Suite", "Figma", "Sketch",
        "Wireframing", "Prototyping", "User Research", "Visual Design"
    ],
    "analytical_skills": [
        "Data Analysis", "Problem Solving", "Critical Thinking", "Quantitative Analysis",
        "Market Analysis", "Financial Analysis", "Business Intelligence"
    ],
    "soft_skills": [
        "Time Management", "Adaptability", "Creativity", "Collaboration", "Emotional Intelligence",
        "Decision Making", "Work Ethic", "Attention to Detail", "Multitasking"
    ],
    "industry_specific": [
        "Healthcare Management", "Legal Research", "Medical Terminology", "Financial Reporting",
        "Educational Technology", "Clinical Research", "Real Estate Law", "Curriculum Development"
    ]
}

def extract_job_details(url):
    """Extract job details from a URL with comprehensive role and skill detection"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        # Get clean text
        text = soup.get_text(separator='\n', strip=True)
        
        # Extract job title using comprehensive database
        title = detect_job_title(text)
        
        # Extract skills using comprehensive database
        found_skills = detect_skills(text)
        
        # Extract experience level
        experience = extract_experience(text)
        
        # Create description snippet
        description = extract_description(text)
        
        return {
            "role": title,
            "experience": experience,
            "skills": found_skills,
            "description": description
        }
        
    except Exception as e:
        print(f"Error extracting job details: {e}")
        return {
            "role": "Professional Role",
            "experience": "Experience varies",
            "skills": ["Relevant Skills", "Industry Knowledge", "Professional Expertise"],
            "description": f"Position at {url}. Please refer to the original posting for complete details."
        }

def detect_job_title(text):
    """Detect job title from text using comprehensive database"""
    text_lower = text.lower()
    
    # Check all roles in database
    for category, roles in ROLES_DATABASE.items():
        for role in roles:
            if role.lower() in text_lower:
                return role
    
    # If no match found, try common patterns
    title_patterns = [
        r'job title[:\s-]*([^\n]{5,50})',
        r'position[:\s-]*([^\n]{5,50})',
        r'role[:\s-]*([^\n]{5,50})',
        r'<h1[^>]*>(.*?)</h1>',
        r'<title>(.*?)</title>',
        r'we are looking for a ([^\n]{5,50})',
        r'join us as ([^\n]{5,50})'
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            potential_title = match.group(1).strip()
            # Clean up the title
            potential_title = re.sub(r'[^a-zA-Z0-9\s&]', '', potential_title)
            potential_title = potential_title.strip()
            if len(potential_title) > 3 and len(potential_title) < 50:
                return potential_title
    
    return "Professional Role"

def detect_skills(text):
    """Detect skills from text using comprehensive database"""
    text_lower = text.lower()
    found_skills = []
    
    # Check all skills in database
    for category, skills in SKILLS_DATABASE.items():
        for skill in skills:
            skill_lower = skill.lower()
            # Use word boundaries to avoid partial matches
            if re.search(r'\b' + re.escape(skill_lower) + r'\b', text_lower):
                if skill not in found_skills:
                    found_skills.append(skill)
    
    # Also look for skills mentioned in requirements sections
    requirements_sections = [
        r'requirements[:\s-]*(.*?)(?=responsibilities|qualifications|$)",
        r'qualifications[:\s-]*(.*?)(?=responsibilities|requirements|$)",
        r'skills[:\s-]*(.*?)(?=responsibilities|qualifications|$)",
        r'what you.*need[:\s-]*(.*?)(?=what you|responsibilities|$)"
    ]
    
    for pattern in requirements_sections:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            # Extract potential skills from requirements text
            requirements_text = match.lower()
            for skill_category, skills in SKILLS_DATABASE.items():
                for skill in skills:
                    skill_lower = skill.lower()
                    if skill_lower in requirements_text and skill not in found_skills:
                        found_skills.append(skill)
    
    # If no skills found, return some general ones
    if not found_skills:
        found_skills = ["Communication Skills", "Problem Solving", "Team Collaboration"]
    
    return found_skills[:15]  # Limit to top 15 skills

def extract_experience(text):
    """Extract experience level from text"""
    experience_patterns = [
        r'(\d+[\+\-]*\s*years?.*experience)',
        r'experience.*(\d+[\+\-]*\s*years?)',
        r'(\d+[\+\-]*\s*years?).*experience',
        r'level[:\s-]*([^\n]{3,30})',
        r'seniority[:\s-]*([^\n]{3,30})',
        r'(entry level|junior|mid level|senior|lead|principal|executive)'
    ]
    
    for pattern in experience_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            if match.strip() and len(match.strip()) > 3:
                return match.strip()
    
    return "Experience varies"

def extract_description(text):
    """Extract job description from text"""
    # Try to find the main description content
    description_patterns = [
        r'job description[:\s-]*(.*?)(?=requirements|qualifications|responsibilities|$)',
        r'about the role[:\s-]*(.*?)(?=requirements|qualifications|responsibilities|$)',
        r'position overview[:\s-]*(.*?)(?=requirements|qualifications|responsibilities|$)',
        r'role summary[:\s-]*(.*?)(?=requirements|qualifications|responsibilities|$)'
    ]
    
    for pattern in description_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            description = match.group(1).strip()
            # Clean up the description
            description = re.sub(r'\s+', ' ', description)
            if len(description) > 50:
                if len(description) > 300:
                    description = description[:297] + "..."
                return description
    
    # Fallback: use first meaningful paragraphs
    paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 50]
    if paragraphs:
        description = ". ".join(paragraphs[:2])
        if len(description) > 300:
            description = description[:297] + "..."
        return description
    
    return "Job description not available. Please refer to the original posting."
