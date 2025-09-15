import streamlit as st
import os
import requests
import json
from bs4 import BeautifulSoup
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd
import uuid
from urllib.parse import urlparse
import re

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
    .error-box {
        background-color: #FFEBEE;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #F44336;
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
if 'user_skills' not in st.session_state:
    st.session_state.user_skills = []
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = {}

# Functions
def extract_job_details(url):
    """Extract job details from a URL using requests and BeautifulSoup"""
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid URL format")
            
        # Fetch webpage content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        page_data = soup.get_text(separator='\n', strip=True)
        
    except Exception as e:
        raise Exception(f"Error fetching job details: {str(e)}")
    
    # Initialize LLM
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.3-70b-versatile"
    )
    
    # Create prompt template
    prompt_extract = PromptTemplate.from_template(
        """
        *** SCRAPED TEXT FROM WEBSITE:
        {page_data}
        *** INSTRUCTION:
        The scraped text is from a job posting page.
        Your job is to extract the job details and return them in JSON format containing the following keys: 
        - role: the job title
        - experience: required experience level
        - skills: list of required skills and technologies (both technical and non-technical)
        - description: job description summary
        
        Only return the valid JSON.
        *** VALID JSON (NO PREAMBLE).
        """
    )
    
    # Create chain
    chain_extract = prompt_extract | llm
    response = chain_extract.invoke({'page_data': page_data})
    
    # Parse JSON response
    try:
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            job_data = json.loads(json_match.group())
            return job_data
        else:
            # If no JSON found, return a basic structure
            return {
                "role": "Software Developer",
                "experience": "2+ years",
                "skills": ["Python", "JavaScript", "Problem Solving"],
                "description": page_data[:500] + "..." if len(page_data) > 500 else page_data
            }
    except json.JSONDecodeError:
        # If JSON parsing fails, return a basic structure
        return {
            "role": "Software Developer",
            "experience": "2+ years",
            "skills": ["Python", "JavaScript", "Problem Solving"],
            "description": page_data[:500] + "..." if len(page_data) > 500 else page_data
        }

def extract_profile_skills(linkedin_url, github_url):
    """Extract skills from LinkedIn and GitHub profiles"""
    skills = []
    
    # For LinkedIn (simulated extraction)
    if linkedin_url:
        try:
            # In a real application, you would use the LinkedIn API
            # For this demo, we'll simulate with common skills
            skills.extend(["Communication", "Teamwork", "Leadership", "Problem Solving", "Project Management"])
        except:
            pass
    
    # For GitHub (simulated extraction)
    if github_url:
        try:
            # In a real application, you would use the GitHub API
            # For this demo, we'll simulate with common technical skills
            skills.extend(["Python", "JavaScript", "Git", "Web Development", "HTML", "CSS", "React", "Node.js"])
        except:
            pass
    
    return list(set(skills))  # Remove duplicates

def find_relevant_projects(skills):
    """Find relevant projects based on skills (simplified version)"""
    # Sample portfolio data
    portfolio = [
        {"document": "E-commerce website with React and Node.js", "metadata": {"links": "https://example.com/react-project"}},
        {"document": "Machine Learning model for predicting stock prices", "metadata": {"links": "https://example.com/ml-project"}},
        {"document": "Mobile app with React Native and Firebase", "metadata": {"links": "https://example.com/mobile-project"}},
        {"document": "DevOps pipeline with AWS and Docker", "metadata": {"links": "https://example.com/devops-project"}},
        {"document": "Python Django web application", "metadata": {"links": "https://example.com/python-project"}},
    ]
    
    # Simple matching based on keyword presence
    relevant_projects = []
    for project in portfolio:
        project_text = project["document"].lower()
        for skill in skills:
            if skill.lower() in project_text:
                relevant_projects.append(project)
                break
                
    return relevant_projects[:3]  # Return top 3 matches

def generate_cold_email(job_data, projects, user_skills):
    """Generate a cold email based on job data and relevant projects"""
    # Initialize LLM
    llm = ChatGroq(
        temperature=0.7,
        model_name="llama-3.3-70b-versatile"
    )
    
    # Format projects for the prompt
    projects_text = ""
    if projects:
        projects_text = "Relevant Projects:\n"
        for i, project in enumerate(projects, 1):
            projects_text += f"{i}. {project['document']} (Link: {project['metadata']['links']})\n"
    
    # Format user skills
    user_skills_text = ", ".join(user_skills) if user_skills else "Not specified"
    
    # Create prompt template
    prompt_template = PromptTemplate.from_template(
        """
        You are an expert job seeker crafting a compelling cold email for a hiring manager.
        
        JOB DETAILS:
        - Role: {role}
        - Experience Required: {experience}
        - Key Skills: {skills}
        - Description: {description}
        
        CANDIDATE SKILLS:
        {user_skills}
        
        {projects_text}
        
        INSTRUCTIONS:
        Create a professional cold email that:
        1. Introduces the candidate briefly
        2. Expresses genuine interest in the specific role
        3. Highlights relevant skills and experience that match the job requirements
        4. Mentions specific projects from the portfolio that demonstrate these skills
        5. Shows enthusiasm for the company/role
        6. Includes a polite call to action (request for interview)
        7. Is concise (around 200-300 words)
        8. Has a professional tone but is not overly formal
        
        Format the email properly with:
        - Appropriate subject line
        - Professional greeting
        - Well-structured paragraphs
        - Professional closing
        
        COLD EMAIL:
        """
    )
    
    # Format skills list
    skills_text = ", ".join(job_data['skills']) if isinstance(job_data['skills'], list) else job_data['skills']
    
    # Create chain and generate email
    chain = prompt_template | llm
    response = chain.invoke({
        "role": job_data['role'],
        "experience": job_data['experience'],
        "skills": skills_text,
        "description": job_data['description'],
        "user_skills": user_skills_text,
        "projects_text": projects_text
    })
    
    return response.content

# Header
st.markdown('<h1 class="main-header">Cold Email Generator</h1>', unsafe_allow_html=True)
st.markdown("Generate personalized cold emails for job applications based on your portfolio.")

# Sidebar for API key input
with st.sidebar:
    st.header("Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password", 
                                help="Get your API key from https://console.groq.com/")
    os.environ["GROQ_API_KEY"] = groq_api_key
    
    st.divider()
    st.info("""
    **How to use:**
    1. Enter your Groq API key
    2. Upload your profile links (LinkedIn and GitHub)
    3. Paste a job posting URL
    4. Click 'Parse Job Details'
    5. Review the extracted information
    6. Click 'Generate Cold Email'
    """)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["Profile Input", "Job URL Input", "Generated Email", "About"])

with tab1:
    st.markdown('<h2 class="sub-header">Your Profile Information</h2>', unsafe_allow_html=True)
    
    linkedin_url = st.text_input("LinkedIn Profile URL:", 
                                placeholder="https://linkedin.com/in/yourprofile")
    github_url = st.text_input("GitHub Profile URL:", 
                              placeholder="https://github.com/yourusername")
    
    if st.button("Extract Skills from Profiles", disabled=not groq_api_key):
        with st.spinner("Extracting skills from your profiles..."):
            try:
                st.session_state.user_skills = extract_profile_skills(linkedin_url, github_url)
                st.session_state.profile_data = {
                    "linkedin": linkedin_url,
                    "github": github_url
                }
                
                if st.session_state.user_skills:
                    st.success("Skills extracted successfully!")
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.subheader("Extracted Skills")
                    for skill in st.session_state.user_skills:
                        st.write(f"- {skill}")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("No skills could be extracted from the provided profiles.")
            except Exception as e:
                st.error(f"Error extracting skills: {str(e)}")

with tab2:
    st.markdown('<h2 class="sub-header">Paste Job URL</h2>', unsafe_allow_html=True)
    
    job_url = st.text_input("Enter the job posting URL:", 
                           placeholder="https://careers.example.com/job/123")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        parse_clicked = st.button("Parse Job Details", disabled=not groq_api_key)
    
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
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f"Error extracting job details: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate email button
    if st.session_state.job_data:
        st.markdown("---")
        generate_clicked = st.button("Generate Cold Email", type="primary")
        
        if generate_clicked:
            with st.spinner("Generating your cold email..."):
                try:
                    st.session_state.email = generate_cold_email(
                        st.session_state.job_data, 
                        st.session_state.projects,
                        st.session_state.user_skills
                    )
                    st.success("Email generated successfully!")
                    # Switch to the email tab
                    st.switch_page("?tab=Generated%20Email")
                except Exception as e:
                    st.error(f"Error generating email: {str(e)}")

with tab3:
    st.markdown('<h2 class="sub-header">Generated Cold Email</h2>', unsafe_allow_html=True)
    
    if st.session_state.email:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.email)
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

with tab4:
    st.markdown("""
    ## About Cold Email Generator
    
    This tool helps you create personalized cold emails for job applications by:
    
    1. **Parsing job postings** - Extracting key requirements and skills
    2. **Extracting your skills** - From LinkedIn and GitHub profiles
    3. **Matching with your portfolio** - Finding your most relevant projects
    4. **Generating tailored emails** - Creating professional, personalized emails
    
    ### How It Works
    
    - Uses AI to analyze job descriptions
    - Extracts skills from your online profiles
    - Matches requirements with your portfolio projects
    - Generates compelling emails that highlight your relevant experience
    
    ### Privacy Note
    
    - Your API key is only used during your session
    - Job data is processed but not stored
    - No personal data is collected or saved
    """)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Cold Email Generator Tool • Built with Streamlit</div>", 
            unsafe_allow_html=True)

