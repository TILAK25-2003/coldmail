# app.py (updated imports section)
import streamlit as st
import os
import sys
import traceback

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import with better error handling
try:
    from job_parser import extract_job_details
except ImportError as e:
    st.error(f"Failed to import job_parser: {e}")
    # Define a fallback function
    def extract_job_details(url):
        return {
            "role": "Software Developer",
            "experience": "2+ years",
            "skills": ["Python", "JavaScript", "Problem Solving"],
            "description": "Job description extraction is currently unavailable."
        }

try:
    from portfolio_matcher import find_relevant_projects
except ImportError as e:
    st.error(f"Failed to import portfolio_matcher: {e}")
    # Define a fallback function
    def find_relevant_projects(skills, n_results=3):
        return [
            {"document": "Python, Django, PostgreSQL", "metadata": {"links": "https://example.com/python-project"}},
            {"document": "React, Node.js, MongoDB", "metadata": {"links": "https://example.com/react-project"}}
        ]

try:
    from email_generator import generate_cold_email
except ImportError as e:
    st.error(f"Failed to import email_generator: {e}")
    # Define a fallback function
    def generate_cold_email(job_data, projects):
        return f"""
        Subject: Application for {job_data.get('role', 'Software Developer')} Position
        
        Dear Hiring Manager,
        
        I am writing to express my interest in the {job_data.get('role', 'Software Developer')} position.
        
        With experience in {', '.join(job_data.get('skills', ['Python', 'JavaScript']))}, 
        I believe I would be a strong candidate for this role.
        
        Thank you for considering my application.
        
        Sincerely,
        [Your Name]
        """

# The rest of your app.py remains the same...
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
    2. Paste a job posting URL
    3. Click 'Parse Job Details'
    4. Review the extracted information
    5. Click 'Generate Cold Email'
    """)

# Main content
tab1, tab2, tab3 = st.tabs(["Job URL Input", "Generated Email", "About"])

with tab1:
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

with tab3:
    st.markdown("""
    ## About Cold Email Generator
    
    This tool helps you create personalized cold emails for job applications by:
    
    1. **Parsing job postings** - Extracting key requirements and skills
    2. **Matching with your portfolio** - Finding your most relevant projects
    3. **Generating tailored emails** - Creating professional, personalized emails
    
    ### How It Works
    
    - Uses AI to analyze job descriptions
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

