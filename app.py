import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# ==================== JOB PARSER FUNCTIONS ====================
def extract_job_details(url):
    """Extract job details from URL with error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
            element.decompose()
        
        # Get text content
        text = soup.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 10]
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
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Common job board domains
    job_boards = ['linkedin', 'indeed', 'glassdoor', 'monster', 'careerbuilder', 'ziprecruiter', 'angel', 'wellfound']
    
    # Extract domain name without TLD
    domain_parts = domain.split('.')
    if len(domain_parts) >= 2:
        main_domain = domain_parts[-2]
    else:
        main_domain = domain_parts[0] if domain_parts else "company"
    
    # If it's not a job board, use the domain name
    if main_domain not in job_boards:
        return main_domain.title()
    
    # For job boards, try to extract company name from text
    company_patterns = [
        r'at\s+([A-Z][a-zA-Z0-9&\s\.]+)(?:\s+|$|,)',
        r'company:\s*([^\n]+)',
        r'employer:\s*([^\n]+)',
        r'([A-Z][a-zA-Z0-9&\s\.]+)\s+is hiring',
        r'hiring at\s+([A-Z][a-zA-Z0-9&\s\.]+)',
        r'about\s+([A-Z][a-zA-Z0-9&\s\.]+)'
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, job_text, re.IGNORECASE)
        if match:
            company = match.group(1).strip()
            company = re.sub(r'[^a-zA-Z0-9\s&\.]', '', company)
            if 2 <= len(company.split()) <= 4 and len(company) < 30:
                return company.title()
    
    return main_domain.title()

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
    return list(dict.fromkeys(found_skills))[:15]

# ==================== PORTFOLIO MATCHER FUNCTIONS ====================
def find_relevant_projects(job_text, portfolio_projects):
    """Find relevant portfolio projects based on job description"""
    if not job_text or not portfolio_projects:
        return []
    
    job_lower = job_text.lower()
    relevant_projects = []
    
    for project in portfolio_projects:
        relevance_score = 0
        
        # Check project skills
        for skill in project.get('skills', []):
            if skill.lower() in job_lower:
                relevance_score += 2
        
        # Check project description
        project_desc = project.get('description', '').lower()
        if any(word in job_lower for word in project_desc.split()[:10]):
            relevance_score += 1
        
        # Check project name
        project_name = project.get('name', '').lower()
        if any(word in job_lower for word in project_name.split()):
            relevance_score += 1
        
        if relevance_score > 0:
            project_with_score = project.copy()
            project_with_score['relevance_score'] = relevance_score
            relevant_projects.append(project_with_score)
    
    # Sort by relevance score
    relevant_projects.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    return relevant_projects[:3]

# ==================== EMAIL GENERATOR FUNCTIONS ====================
def generate_cold_email(your_name, company_name, hiring_manager, job_role, job_skills, relevant_projects, job_description, your_email, your_phone):
    """Generate a comprehensive cold email"""
    
    # Skills categorization
    tech_skills = [skill for skill in job_skills if skill in [
        'Python', 'JavaScript', 'Java', 'React', 'Node.js', 'SQL', 'HTML', 'CSS',
        'AWS', 'Docker', 'Kubernetes', 'Machine Learning', 'Data Analysis'
    ]]
    
    soft_skills = [skill for skill in job_skills if skill in [
        'Communication', 'Leadership', 'Teamwork', 'Problem Solving', 'Project Management'
    ]]
    
    # Projects section
    projects_text = ""
    if relevant_projects:
        projects_text = "I have successfully delivered projects that demonstrate these skills:\n"
        for proj in relevant_projects[:2]:
            projects_text += f"• {proj['name']}: {proj['description']}\n"
    else:
        projects_text = "My experience includes working on various projects that have honed my skills in these areas."
    
    email = f"""Subject: Application for {job_role} Position at {company_name}

Dear {hiring_manager},

I am writing to express my enthusiastic interest in the {job_role} position at {company_name}. After reviewing your job description, I am confident that my skills and experience align perfectly with your requirements.

Your posting emphasizes the need for expertise in {', '.join(tech_skills[:3]) if tech_skills else 'key technical areas'} as well as strong {', '.join(soft_skills[:2]) if soft_skills else 'professional'} skills. 

{projects_text}

Some key strengths I would bring to {company_name} include:

• Technical Proficiency: {', '.join(tech_skills[:5]) if tech_skills else 'Relevant technical expertise'}
• Professional Skills: {', '.join(soft_skills[:3]) if soft_skills else 'Strong professional capabilities'}
• Proven track record of delivering results in similar roles

I am particularly impressed by {company_name}'s work in the industry and would be thrilled to contribute to your team's success.

I would welcome the opportunity to discuss how my skills and experience can benefit {company_name}. Thank you for considering my application.

Best regards,
{your_name}
Email: {your_email}
Phone: {your_phone}
LinkedIn: linkedin.com/in/{your_name.replace(' ', '').lower()}

P.S. I have attached my resume for your review and would be happy to provide references upon request.
"""

    return email

# ==================== MAIN APP FUNCTIONS ====================
def is_valid_url(url):
    """Simple URL validation"""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

def display_results():
    """Display extracted job information"""
    key_info = st.session_state.key_info
    relevant_projects = st.session_state.relevant_projects
    company_name = st.session_state.company_name
    
    st.subheader("🔍 Extracted Job Information")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Role:** {key_info.get('role', 'Not specified')}")
    with col2:
        st.info(f"**Experience:** {key_info.get('experience', 'Not specified')}")
    with col3:
        st.info(f"**Company:** {company_name}")
    
    st.subheader("🛠️ Required Skills")
    # FIXED: Skills display with fallback
    skills = key_info.get('skills', [])
    if skills:
        st.info(f"**Skills:** {', '.join(skills)}")
    else:
        st.warning("No skills detected. The job posting might not contain common tech skills.")
    
    st.subheader("🎯 Relevant Projects")
    if relevant_projects:
        for project in relevant_projects:
            with st.expander(f"📁 {project['name']}"):
                st.write(f"**Description:** {project['description']}")
                st.write(f"**Skills:** {', '.join(project['skills'])}")
    else:
        st.info("No relevant projects found. Consider adding more projects to your portfolio.")

def generate_email(your_name, company_name, hiring_manager, your_email, your_phone):
    """Generate and display cold email"""
    key_info = st.session_state.key_info
    relevant_projects = st.session_state.relevant_projects
    job_text = st.session_state.job_text
    
    email = generate_cold_email(
        your_name=your_name,
        company_name=company_name,
        hiring_manager=hiring_manager,
        job_role=key_info.get('role', ''),
        job_skills=key_info.get('skills', []),
        relevant_projects=relevant_projects,
        job_description=job_text[:1000],
        your_email=your_email,
        your_phone=your_phone
    )
    
    st.subheader("📝 Generated Cold Email")
    st.text_area("Email Content", email, height=400)
    
    if st.button("📋 Copy to Clipboard"):
        st.code(email, language=None)
        st.success("Email copied to clipboard!")

# ==================== MAIN APP ====================
def main():
    st.set_page_config(page_title="ColdMail Generator", page_icon="✉️", layout="wide")
    
    st.title("✉️ ColdMail Generator")
    st.write("Paste job URL → Get key info → Generate personalized email")
    
    # Your portfolio - replace with your actual projects
    MY_PORTFOLIO = [
        {
            'name': 'E-commerce Website',
            'description': 'Built a full-stack e-commerce platform with React and Node.js',
            'skills': ['React', 'Node.js', 'MongoDB', 'JavaScript', 'E-commerce'],
            'url': 'https://github.com/yourusername/ecommerce'
        },
        {
            'name': 'Data Analysis Tool',
            'description': 'Developed a Python tool for data analysis and visualization',
            'skills': ['Python', 'Pandas', 'Matplotlib', 'Data Analysis', 'Visualization'],
            'url': 'https://github.com/yourusername/data-tool'
        }
    ]
    
    # Input section
    job_url = st.text_input("Job Posting URL:", placeholder="https://linkedin.com/job/123 or https://indeed.com/job/abc")
    
    if st.button("Analyze Job", type="primary"):
        if not job_url:
            st.warning("Please enter a job URL")
        elif not is_valid_url(job_url):
            st.error("❌ Invalid URL format. Please enter a valid web address (e.g., https://example.com)")
        else:
            with st.spinner("🔍 Analyzing job posting..."):
                try:
                    # Extract job details
                    job_text = extract_job_details(job_url)
                    
                    if "error" in job_text.lower():
                        st.error(f"❌ {job_text}")
                    else:
                        # Extract key information
                        key_info = extract_key_info(job_text)
                        company_name = extract_company_name(job_url, job_text)
                        
                        # Find relevant projects
                        relevant_projects = find_relevant_projects(job_text, MY_PORTFOLIO)
                        
                        # Store in session state
                        st.session_state.key_info = key_info
                        st.session_state.relevant_projects = relevant_projects
                        st.session_state.job_text = job_text
                        st.session_state.company_name = company_name
                        st.session_state.job_url = job_url
                        
                        st.success("✅ Analysis complete!")
                        
                except Exception as e:
                    st.error(f"❌ Error analyzing job: {str(e)}")
    
    # Show results if available
    if 'key_info' in st.session_state:
        display_results()
        
        # Email generation section
        st.markdown("---")
        st.subheader("📧 Generate Cold Email")
        
        col1, col2 = st.columns(2)
        with col1:
            your_name = st.text_input("Your Name:", "John Doe")
        with col2:
            company_name = st.text_input("Company Name:", st.session_state.company_name)
        
        hiring_manager = st.text_input("Hiring Manager (optional):", "Hiring Team")
        your_email = st.text_input("Your Email:", "johndoe@email.com")
       
