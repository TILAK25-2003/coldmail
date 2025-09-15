import streamlit as st
import os
import re
import traceback

try:
    from job_parser import extract_job_details
    from portfolio_matcher import find_relevant_projects
    from email_generator import generate_cold_email
    from profile_analyzer import extract_skills_from_profiles
except ImportError as e:
    st.error(f"Import Error: {e}. Please make sure all dependencies are installed.")
    st.stop()

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
    .warning-box {
        background-color: #FFF8E1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #FFC107;
        margin-top: 1rem;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        width: 100%;
    }
    .tab-container {
        padding: 1rem;
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

# Header
st.markdown('<h1 class="main-header">Cold Email Generator</h1>', unsafe_allow_html=True)
st.markdown("Generate personalized cold emails for job applications based on your portfolio and profiles.")

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
    2. Add your LinkedIn and/or GitHub profiles
    3. Paste a job posting URL
    4. Click 'Parse Job Details'
    5. Review the extracted information
    6. Click 'Generate Cold Email'
    """)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["Profile Input", "Job URL Input", "Generated Email", "About"])

with tab1:
    st.markdown('<h2 class="sub-header">Add Your Profiles</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        linkedin_url = st.text_input("LinkedIn Profile URL:", 
                                    placeholder="https://linkedin.com/in/yourprofile")
    
    with col2:
        github_url = st.text_input("GitHub Profile URL:", 
                                  placeholder="https://github.com/yourusername")
    
    analyze_clicked = st.button("Analyze Profiles", disabled=not groq_api_key)
    
    if analyze_clicked and (linkedin_url or github_url):
        with st.spinner("Analyzing profiles..."):
            try:
                profile_urls = []
                if linkedin_url:
                    if not linkedin_url.startswith(('http://', 'https://')):
                        linkedin_url = 'https://' + linkedin_url
                    profile_urls.append(("linkedin", linkedin_url))
                if github_url:
                    if not github_url.startswith(('http://', 'https://')):
                        github_url = 'https://' + github_url
                    profile_urls.append(("github", github_url))
                
                st.session_state.profile_data = extract_skills_from_profiles(profile_urls)
                st.session_state.user_skills = st.session_state.profile_data.get('skills', [])
                
                st.success("Profiles analyzed successfully!")
                
                # Display profile data
                if st.session_state.user_skills:
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.subheader("Skills Extracted from Your Profiles")
                    for skill in st.session_state.user_skills:
                        st.write(f"- {skill}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error analyzing profiles: {str(e)}")
                st.error("Please check if the URLs are valid and accessible.")
    
    # Manual skills input as fallback
    st.markdown("---")
    st.markdown("### Or Add Skills Manually")
    manual_skills = st.text_area("Enter your skills (comma-separated):", 
                                placeholder="Python, JavaScript, Project Management, Communication")
    
    if manual_skills:
        manual_skills_list = [skill.strip() for skill in manual_skills.split(",") if skill.strip()]
        if manual_skills_list:
            # Combine with profile skills if any
            all_skills = list(set(st.session_state.user_skills + manual_skills_list))
            st.session_state.user_skills = all_skills
            
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.subheader("Your Combined Skills")
            for skill in all_skills:
                st.write(f"- {skill}")
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<h2 class="sub-header">Paste Job URL</h2>', unsafe_allow_html=True)
    
    job_url = st.text_input("Enter the job posting URL:", 
                           placeholder="https://careers.example.com/job/123")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        parse_clicked = st.button("Parse Job Details", disabled=not groq_api_key)
    
    if parse_clicked and job_url:
        # Validate URL format
        url_pattern = re.compile(
            r'^(https?://)?'  # http:// or https://
            r'(([A-Z0-9-]+\.)+[A-Z]{2,63})'  # domain
            r'(:[0-9]{1,5})?'  # optional port
            r'(/.*)?$', re.IGNORECASE)
        
        if not url_pattern.match(job_url):
            st.error("Please enter a valid URL starting with http:// or https://")
        else:
            with st.spinner("Extracting job details..."):
                try:
                    if not job_url.startswith(('http://', 'https://')):
                        job_url = 'https://' + job_url
                    
                    st.session_state.job_data = extract_job_details(job_url)
                    
                    # If we have user skills, find relevant projects
                    if st.session_state.user_skills:
                        st.session_state.projects = find_relevant_projects(
                            st.session_state.job_data['skills'],
                            st.session_state.user_skills
                        )
                    
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
                    
                    # Display matched projects if available
                    if st.session_state.projects:
                        st.markdown('<div class="info-box">', unsafe_allow_html=True)
                        st.subheader("Relevant Projects from Your Portfolio")
                        for project in st.session_state.projects:
                            st.write(f"- {project['document']} - [View Project]({project['metadata']['links']})")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Show skill match analysis
                    if st.session_state.user_skills and st.session_state.job_data.get('skills'):
                        job_skills = st.session_state.job_data['skills']
                        user_skills = st.session_state.user_skills
                        
                        matched_skills = set(job_skills) & set(user_skills)
                        missing_skills = set(job_skills) - set(user_skills)
                        
                        st.markdown('<div class="info-box">', unsafe_allow_html=True)
                        st.subheader("Skills Match Analysis")
                        
                        st.write("**Skills You Have:**")
                        for skill in matched_skills:
                            st.write(f"- ✅ {skill}")
                        
                        if missing_skills:
                            st.write("**Skills You Might Need to Develop:**")
                            for skill in missing_skills:
                                st.write(f"- ⚠️ {skill}")
                        
                        match_percentage = len(matched_skills) / len(job_skills) * 100 if job_skills else 0
                        st.write(f"**Match Percentage:** {match_percentage:.1f}%")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error extracting job details: {str(e)}")
                    st.error("Please check if the URL is valid and accessible.")
    
    # Generate email button
    if st.session_state.job_data:
        st.markdown("---")
        generate_clicked = st.button("Generate Cold Email", type="primary")
        
        if generate_clicked:
            with st.spinner("Generating your cold email..."):
                try:
                    st.session_state.email = generate_cold_email(
                        st.session_state.job_data, 
                        st.session_state.projects if st.session_state.projects else [],
                        st.session_state.profile_data
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
        
        # Regenerate button with options
        st.markdown("---")
        st.subheader("Customize Email")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tone = st.selectbox("Email Tone", 
                               ["Professional", "Enthusiastic", "Conservative", "Creative"])
        
        with col2:
            length = st.selectbox("Email Length", 
                                 ["Concise", "Medium", "Detailed"])
        
        with col3:
            focus = st.selectbox("Primary Focus", 
                                ["Skills", "Experience", "Projects", "Culture Fit"])
        
        regenerate_clicked = st.button("Regenerate with New Settings", type="secondary")
        
        if regenerate_clicked:
            with st.spinner("Regenerating email..."):
                try:
                    st.session_state.email = generate_cold_email(
                        st.session_state.job_data, 
                        st.session_state.projects if st.session_state.projects else [],
                        st.session_state.profile_data,
                        tone=tone,
                        length=length,
                        focus=focus
                    )
                    st.success("Email regenerated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error regenerating email: {str(e)}")
    else:
        st.info("No email generated yet. Please parse a job URL first.")

with tab4:
    st.markdown("""
    ## About Cold Email Generator
    
    This tool helps you create personalized cold emails for job applications by:
    
    1. **Analyzing your profiles** - Extracting skills from LinkedIn and GitHub
    2. **Parsing job postings** - Extracting key requirements and skills
    3. **Matching with your skills** - Finding your most relevant qualifications
    4. **Generating tailored emails** - Creating professional, personalized emails
    
    ### How It Works
    
    - Uses AI to analyze job descriptions and your profiles
    - Matches requirements with your skills and experience
    - Generates compelling emails that highlight your relevant experience
    
    ### Privacy Note
    
    - Your API key is only used during your session
    - Job data and profile information is processed but not stored
    - No personal data is collected or saved
    """)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Cold Email Generator Tool • Built with Streamlit</div>", 
            unsafe_allow_html=True)
