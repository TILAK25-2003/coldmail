import streamlit as st
from job_parser import extract_job_details, extract_key_info, extract_company_name
from portfolio_matcher import find_relevant_projects
from email_generator import generate_cold_email
import validators

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

def main():
    st.set_page_config(page_title="ColdMail Generator", page_icon="✉️", layout="wide")
    
    st.title("✉️ ColdMail Generator")
    st.write("Paste job URL → Get key info → Generate personalized email")
    
    # Input section
    job_url = st.text_input("Job Posting URL:", placeholder="https://linkedin.com/job/123 or https://indeed.com/job/abc")
    
    if st.button("Analyze Job", type="primary"):
        if not job_url:
            st.warning("Please enter a job URL")
        elif not validators.url(job_url):
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
            # Pre-fill company name if detected
            company_name = st.text_input("Company Name:", st.session_state.company_name)
        
        hiring_manager = st.text_input("Hiring Manager (optional):", "Hiring Team")
        your_email = st.text_input("Your Email:", "johndoe@email.com")
        your_phone = st.text_input("Your Phone (optional):", "+1 (555) 123-4567")
        
        if st.button("✨ Generate Email", type="primary"):
            generate_email(your_name, company_name, hiring_manager, your_email, your_phone)

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
    skills = key_info.get('skills', [])
    if skills:
        st.write(", ".join(skills))
    else:
        st.warning("No skills detected in the job posting")
    
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
    
    # Copy to clipboard button
    if st.button("📋 Copy to Clipboard"):
        st.code(email, language=None)
        st.success("Email copied to clipboard!")

if __name__ == "__main__":
    main()
