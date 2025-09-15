import streamlit as st
import time
from scraper import JobScraper
from email_generator import EmailGenerator

# Set page configuration
st.set_page_config(
    page_title="Cold Email Generator",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'job_details' not in st.session_state:
    st.session_state.job_details = None
if 'email_generated' not in st.session_state:
    st.session_state.email_generated = False
if 'user_context' not in st.session_state:
    st.session_state.user_context = {
        "name": "",
        "background": "",
        "skills": ""
    }

# Custom CSS for better styling
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
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #4CAF50;
    }
    .error-box {
        background-color: #FFEBEE;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #F44336;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #2196F3;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #0D47A1;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">✉️ Cold Email Generator</h1>', unsafe_allow_html=True)
st.markdown("Generate personalized cold emails for job applications using AI")

# Sidebar for user input
with st.sidebar:
    st.markdown("### 🔑 API Configuration")
    st.info("Make sure to set your GROQ_API_KEY in the .env file")
    
    st.markdown("### 👤 Your Information")
    name = st.text_input("Your Name", value=st.session_state.user_context["name"])
    background = st.text_area("Your Background/Experience", value=st.session_state.user_context["background"])
    skills = st.text_area("Your Key Skills", value=st.session_state.user_context["skills"])
    
    if name or background or skills:
        st.session_state.user_context = {
            "name": name,
            "background": background,
            "skills": skills
        }

# Main content
tab1, tab2 = st.tabs(["📝 Generate Email", "ℹ️ How It Works"])

with tab1:
    st.markdown('<div class="sub-header">Enter Job URL</div>', unsafe_allow_html=True)
    
    job_url = st.text_input("Paste the job posting URL here:", placeholder="https://example.com/jobs/software-engineer")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        generate_btn = st.button("🚀 Generate Email", use_container_width=True)
    
    if generate_btn and job_url:
        with st.spinner("Analyzing job posting and generating email..."):
            # Initialize scraper and extract job details
            scraper = JobScraper()
            job_details, error = scraper.extract_job_details(job_url)
            
            if error:
                st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)
            else:
                st.session_state.job_details = job_details
                
                # Display extracted job details
                st.markdown(f'<div class="success-box">✅ Successfully extracted job details!</div>', unsafe_allow_html=True)
                
                with st.expander("View Extracted Job Details"):
                    st.json(job_details)
                
                # Generate email
                email_gen = EmailGenerator()
                email_content = email_gen.generate_email(job_details, st.session_state.user_context)
                
                if email_content.startswith("Error"):
                    st.markdown(f'<div class="error-box">❌ {email_content}</div>', unsafe_allow_html=True)
                else:
                    st.session_state.email_generated = True
                    st.session_state.email_content = email_content
                    
                    # Display the generated email
                    st.markdown("### 📧 Generated Email")
                    st.text_area("Email Content", email_content, height=300)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Email",
                        data=email_content,
                        file_name="cold_email.txt",
                        mime="text/plain"
                    )

with tab2:
    st.markdown("""
    ## How to Use the Cold Email Generator
    
    1. **Get a Groq API Key**: 
        - Sign up at [GroqCloud](https://console.groq.com/)
        - Create an API key from your dashboard
        - Create a `.env` file in the project directory and add:
          ```
          GROQ_API_KEY=your_api_key_here
          ```
    
    2. **Enter Your Information**:
        - Fill in your name, background, and skills in the sidebar
        - This helps personalize the generated email
    
    3. **Paste Job URL**:
        - Copy the URL of the job posting you're interested in
        - Paste it into the input field on the main tab
    
    4. **Generate Email**:
        - Click the "Generate Email" button
        - The system will analyze the job posting and create a personalized email
    
    5. **Review and Download**:
        - Review the generated email
        - Make any necessary adjustments
        - Download or copy the email for your use
    
    ## Supported Job Platforms
    
    This tool works best with job postings that have clear text content. It may have limitations with:
    - Job platforms that require login
    - PDF job descriptions
    - Complex JavaScript-rendered pages
    
    For best results, use direct links to job postings on company career pages.
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Cold Email Generator powered by Groq Cloud | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)

