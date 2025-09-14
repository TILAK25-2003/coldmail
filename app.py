import streamlit as st
from job_parser import extract_job_details, extract_key_info
from portfolio_matcher import find_relevant_projects
from email_generator import generate_cold_email

# Your portfolio - replace with your actual projects
MY_PORTFOLIO = [
    {
        'name': 'E-commerce Website',
        'description': 'Built a full-stack e-commerce platform with React and Node.js',
        'skills': ['React', 'Node.js', 'MongoDB', 'JavaScript'],
        'url': 'https://github.com/yourusername/ecommerce'
    },
    {
        'name': 'Data Analysis Tool',
        'description': 'Developed a Python tool for data analysis and visualization',
        'skills': ['Python', 'Pandas', 'Matplotlib', 'Data Analysis'],
        'url': 'https://github.com/yourusername/data-tool'
    }
]

def main():
    st.title("✉️ ColdMail Generator")
    st.write("Paste job URL → Get key info → Generate email")
    
    job_url = st.text_input("Job Posting URL:", placeholder="https://example.com/job")
    
    if st.button("Analyze Job") and job_url:
        with st.spinner("Extracting job details..."):
            job_text = extract_job_details(job_url)
            key_info = extract_key_info(job_text)
            relevant_projects = find_relevant_projects(job_text, MY_PORTFOLIO)
            
            # Store in session state
            st.session_state.key_info = key_info
            st.session_state.relevant_projects = relevant_projects
            st.session_state.job_text = job_text
            
    # Show results if available
    if 'key_info' in st.session_state:
        display_results()
        
        # Email generation
        st.markdown("---")
        st.subheader("📧 Generate Cold Email")
        
        col1, col2 = st.columns(2)
        with col1:
            your_name = st.text_input("Your Name:", "John Doe")
        with col2:
            company_name = st.text_input("Company Name:", "Tech Company")
        
        hiring_manager = st.text_input("Hiring Manager (optional):", "Hiring Team")
        
        if st.button("Generate Email"):
            generate_email(your_name, company_name, hiring_manager)

def display_results():
    """Display extracted job information"""
    key_info = st.session_state.key_info
    relevant_projects = st.session_state.relevant_projects
    
    st.subheader("🔍 Extracted Job Information")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Role:** {key_info.get('role', 'Not specified')}")
    with col2:
        st.info(f"**Experience:** {key_info.get('experience', 'Not specified')}")
    with col3:
        st.info(f"**Skills:** {', '.join(key_info.get('skills', []))}")
    
    st.subheader("🎯 Relevant Projects")
    for project in relevant_projects:
        st.write(f"**{project['name']}** - {project['description']}")

def generate_email(your_name, company_name, hiring_manager):
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
        job_description=job_text[:500]  # First 500 chars
    )
    
    st.subheader("📝 Generated Cold Email")
    st.text_area("Email Content", email, height=300)
    st.button("Copy to Clipboard")

if __name__ == "__main__":
    main()
