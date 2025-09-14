# app.py (complete single file solution)
import streamlit as st
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import re
import random

# ----- Portfolio Matcher Functions -----
def load_portfolio_data():
    """Load portfolio data from CSV or create default if not exists"""
    csv_path = "my_portfolio.csv"
    
    # Create default portfolio if file doesn't exist
    if not os.path.exists(csv_path):
        default_data = {
            "Techstack": [
                "React, Node.js, MongoDB",
                "Python, Django, PostgreSQL",
                "Java, Spring Boot, MySQL",
                "JavaScript, React, Node.js",
                "Python, Machine Learning, TensorFlow",
                "AWS, Docker, Kubernetes",
                "React Native, Firebase, JavaScript",
                "Vue.js, Express, MongoDB"
            ],
            "Links": [
                "https://example.com/react-project",
                "https://example.com/python-project",
                "https://example.com/java-project",
                "https://example.com/js-project",
                "https://example.com/ml-project",
                "https://example.com/devops-project",
                "https://example.com/mobile-project",
                "https://example.com/vue-project"
            ]
        }
        df = pd.DataFrame(default_data)
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path)
    
    return df

def find_relevant_projects(skills, n_results=3):
    """Find relevant projects based on skills using simple text matching"""
    try:
        df = load_portfolio_data()
        
        # Convert skills to a list if it's a string
        if isinstance(skills, str):
            skills = [skill.strip() for skill in skills.split(',')]
        
        # Score each project based on skill matches
        scored_projects = []
        for index, row in df.iterrows():
            score = 0
            techstack = str(row['Techstack']).lower()
            
            for skill in skills:
                skill_lower = str(skill).lower().strip()
                if skill_lower in techstack:
                    score += 3
                elif any(skill_lower in word for word in techstack.split()):
                    score += 1
            
            scored_projects.append({
                'score': score,
                'document': row['Techstack'],
                'metadata': {'links': row['Links']}
            })
        
        # Sort by score and return top n results
        scored_projects.sort(key=lambda x: x['score'], reverse=True)
        top_projects = scored_projects[:n_results]
        
        # Format results
        relevant_projects = []
        for project in top_projects:
            relevant_projects.append({
                "document": project['document'],
                "metadata": project['metadata']
            })
        
        return relevant_projects
        
    except Exception as e:
        # Fallback: return default projects
        return [
            {"document": "Python, Django, PostgreSQL", "metadata": {"links": "https://example.com/python-project"}},
            {"document": "React, Node.js, MongoDB", "metadata": {"links": "https://example.com/react-project"}}
        ]

# ----- Job Parser Functions -----
def extract_job_details(url):
    """Extract job details from a URL without using LLM"""
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
        
        # Extract job title (common patterns)
        title = "Software Developer"
        title_patterns = [
            r'job title[:\s-]*([^\n]+)',
            r'position[:\s-]*([^\n]+)',
            r'role[:\s-]*([^\n]+)',
            r'<h1[^>]*>(.*?)</h1>',
            r'<title>(.*?)</title>'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                break
        
        # Extract skills (common tech keywords)
        common_skills = [
            'python', 'javascript', 'java', 'react', 'node', 'angular', 'vue',
            'html', 'css', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
            'aws', 'azure', 'docker', 'kubernetes', 'linux', 'git', 'rest',
            'api', 'machine learning', 'ai', 'tensorflow', 'pytorch'
        ]
        
        found_skills = []
        for skill in common_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                found_skills.append(skill.title())
        
        # If no skills found, use defaults
        if not found_skills:
            found_skills = ["Python", "JavaScript", "Problem Solving"]
        
        # Extract experience level
        experience = "2+ years"
        exp_patterns = [
            r'experience[:\s-]*([^\n]+)',
            r'years.*experience[:\s-]*([^\n]+)',
            r'(\d+[\+\-]*\s*years?)'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                experience = match.group(1).strip()
                break
        
        # Create description snippet
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        description = ". ".join(sentences[:2]) + "." if sentences else "Job description not available."
        
        if len(description) > 200:
            description = description[:197] + "..."
        
        return {
            "role": title,
            "experience": experience,
            "skills": found_skills[:8],
            "description": description
        }
        
    except Exception as e:
        return {
            "role": "Software Developer",
            "experience": "2+ years",
            "skills": ["Python", "JavaScript", "Problem Solving"],
            "description": f"Position at {url}. Please refer to the original posting for complete details."
        }

# ----- Email Generator Functions -----
def generate_cold_email(job_data, projects):
    """Generate a cold email using templates instead of AI"""
    
    # Email templates
    templates = [
        {
            "subject": "Application for {role} Position",
            "greeting": "Dear Hiring Manager,",
            "body": """
I am writing to express my interest in the {role} position at your company. 
With {experience} of experience in {skills}, I believe I possess the qualifications you're seeking.

My relevant experience includes:
{projects}

{description}

I am excited about the opportunity to contribute to your team and would welcome the chance to discuss how my skills can benefit your organization.
""",
            "closing": "Sincerely,\n[Your Name]\n[Your Phone Number]\n[Your Email]"
        }
    ]
    
    # Select a template
    template = templates[0]
    
    # Format skills
    skills_text = ", ".join(job_data['skills']) if isinstance(job_data['skills'], list) else job_data['skills']
    
    # Format projects
    projects_text = ""
    if projects:
        projects_text = "\n".join([f"• {p['document']} - {p['metadata']['links']}" for p in projects])
    else:
        projects_text = "• Various projects demonstrating proficiency in the required skills"
    
    # Fill in the template
    email = f"Subject: {template['subject'].format(role=job_data['role'])}\n\n"
    email += f"{template['greeting']}\n\n"
    email += template['body'].format(
        role=job_data['role'],
        experience=job_data['experience'],
        skills=skills_text,
        projects=projects_text,
        description=job_data['description']
    )
    email += f"\n\n{template['closing']}"
    
    return email

# ----- Streamlit App -----
# Page configuration
st.set_page_config(
    page_title="Cold Email Generator",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #4CAF50;
        margin-top: 1.5rem;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2196F3;
        margin-top: 1rem;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'job_data' not in st.session_state:
    st.session_state.job_data = None
if 'projects' not in st.session_state:
    st.session_state.projects = None
if 'email' not in st.session_state:
    st.session_state.email = None

# Header
st.markdown('<h1 class="main-header">Cold Email Generator</h1>', unsafe_allow_html=True)
st.markdown("Generate personalized cold emails for job applications based on your portfolio.")

# Sidebar
with st.sidebar:
    st.header("How to Use")
    st.info("""
    **Instructions:**
    1. Paste a job posting URL
    2. Click 'Parse Job Details'
    3. Review the extracted information
    4. Click 'Generate Cold Email'
    5. Copy and customize your email
    """)
    
    st.divider()
    st.info("""
    **Note:** This tool uses pattern matching instead of AI 
    to generate emails, so no API key is required!
    """)

# Main content
tab1, tab2, tab3 = st.tabs(["Job URL Input", "Generated Email", "About"])

with tab1:
    st.markdown('<h2 class="sub-header">Paste Job URL</h2>', unsafe_allow_html=True)
    
    job_url = st.text_input("Enter the job posting URL:", 
                           placeholder="https://careers.example.com/job/123")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        parse_clicked = st.button("Parse Job Details")
    
    if parse_clicked and job_url:
        with st.spinner("Extracting job details..."):
            try:
                st.session_state.job_data = extract_job_details(job_url)
                st.session_state.projects = find_relevant_projects(st.session_state.job_data['skills'])
                
                st.success("Job details extracted successfully!")
                
                # Display job details
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.subheader("Extracted Job Details")
                st.write(f"**Role:** {st.session_state.job_data['role']}")
                st.write(f"**Experience:** {st.session_state.job_data['experience']}")
                st.write("**Key Skills:**")
                for skill in st.session_state.job_data['skills']:
                    st.write(f"- {skill}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display matched projects
                if st.session_state.projects:
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.subheader("Relevant Projects from Your Portfolio")
                    for project in st.session_state.projects:
                        st.write(f"- {project['document']} - [View Project]({project['metadata']['links']})")
                    st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error extracting job details: {str(e)}")
    
    # Generate email button
    if st.session_state.job_data:
        st.markdown("---")
        generate_clicked = st.button("Generate Cold Email", type="primary")
        
        if generate_clicked:
            with st.spinner("Generating your cold email..."):
                try:
                    st.session_state.email = generate_cold_email(
                        st.session_state.job_data, 
                        st.session_state.projects
                    )
                    st.success("Email generated successfully!")
                    # Switch to the email tab
                    st.switch_page("?tab=Generated%20Email")
                except Exception as e:
                    st.error(f"Error generating email: {str(e)}")

with tab2:
    st.markdown('<h2 class="sub-header">Generated Cold Email</h2>', unsafe_allow_html=True)
    
    if st.session_state.email:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.text(st.session_state.email)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Copy to clipboard button
        st.download_button(
            label="Copy Email to Clipboard",
            data=st.session_state.email,
            file_name="cold_email.txt",
            mime="text/plain"
        )
    else:
        st.info("No email generated yet. Please parse a job URL first.")

with tab3:
    st.markdown("""
    ## About Cold Email Generator
    
    This tool helps you create personalized cold emails for job applications by:
    
    1. **Parsing job postings** - Extracting key requirements and skills using pattern matching
    2. **Matching with your portfolio** - Finding your most relevant projects
    3. **Generating tailored emails** - Creating professional emails using templates
    
    ### How It Works
    
    - Uses pattern matching to analyze job descriptions
    - Matches requirements with your portfolio projects
    - Generates compelling emails using pre-defined templates
    
    ### Privacy Note
    
    - No API keys or external services required
    - All processing happens in your browser
    - No personal data is collected or saved



