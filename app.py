import streamlit as st
from job_parser import extract_job_details
from portfolio_matcher import find_relevant_projects
from email_generator import generate_cold_email

# Your portfolio - replace with your actual projects
MY_PORTFOLIO = [
    {
        'name': 'E-commerce Website',
        'description': 'Full-stack e-commerce platform with React and Node.js handling user authentication and payments',
        'skills': ['React', 'Node.js', 'MongoDB', 'JavaScript', 'Express'],
        'url': 'https://github.com/yourusername/ecommerce'
    },
    {
        'name': 'Data Analysis Dashboard',
        'description': 'Interactive dashboard for data visualization using Python and Plotly',
        'skills': ['Python', 'Pandas', 'Plotly', 'Data Analysis', 'SQL'],
        'url': 'https://github.com/yourusername/data-dashboard'
    },
    {
        'name': 'Machine Learning Model',
        'description': 'Predictive model for customer classification using scikit-learn',
        'skills': ['Python', 'scikit-learn', 'Machine Learning', 'Pandas'],
        'url': 'https://github.com/yourusername/ml-model'
    }
]

def main():
    st.set_page_config(page_title="ColdMail Assistant", page_icon="✉️")
    
    st.title("✉️ ColdMail Assistant")
    st.write("Analyze job postings and generate personalized cold emails")
    
    # Initialize session state
    if 'job_details' not in st.session_state:
        st.session_state.job_details = None
    if 'relevant_projects' not in st.session_state:
        st.session_state.relevant_projects = None
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        job_url = st.text_input("Job Posting URL:", placeholder="https://linkedin.com/job/123")
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔍 Analyze Job", use_container_width=True):
            if job_url:
                analyze_job_posting(job_url)
            else:
                st.warning("Please enter a job URL")
    
    # Display results if available
    if st.session_state.job_details and st.session_state.relevant_projects:
        display_results()
        
        # Email generation section
        st.markdown("---")
        st.subheader("📧 Generate Cold Email")
        
        applicant_info = st.text_input("Your Name:", placeholder="John Doe")
        company_info = st.text_input("Company Name:", placeholder="Tech Company Inc.")
        
        if st.button("✨ Generate Email", type="primary"):
            if applicant_info and company_info:
                generate_email(applicant_info, company_info)
            else:
                st.warning("Please enter your name and company name")

def analyze_job_posting(job_url):
    """Analyze the job posting and find relevant projects"""
    with st.spinner("Analyzing job posting..."):
        try:
            # Extract job details
            job_details = extract_job_details(job_url)
            st.session_state.job_details = job_details
            
            # Find relevant projects
            relevant_projects = find_relevant_projects(job_details['description'], MY_PORTFOLIO)
            st.session_state.relevant_projects = relevant_projects
            
            st.success("✅ Analysis complete!")
            
        except Exception as e:
            st.error(f"Error analyzing job: {str(e)}")

def display_results():
    """Display job analysis results"""
    job_details = st.session_state.job_details
    relevant_projects = st.session_state.relevant_projects
    
    st.subheader("📋 Job Analysis")
    st.write(f"**Position:** {job_details['title']}")
    
    with st.expander("View Job Description"):
        st.text(job_details['description'][:1000] + "..." if len(job_details['description']) > 1000 else job_details['description'])
    
    st.subheader("🎯 Relevant Portfolio Projects")
    
    if relevant_projects:
        for i, project in enumerate(relevant_projects, 1):
            with st.expander(f"Project {i}: {project['name']}"):
                st.write(f"**Description:** {project['description']}")
                st.write(f"**Skills:** {', '.join(project['skills'])}")
                if project.get('url'):
                    st.write(f"**URL:** {project['url']}")
    else:
        st.info("No relevant projects found. Consider adding more projects to your portfolio.")

def generate_email(applicant_name, company_name):
    """Generate and display cold email"""
    with st.spinner("Generating email..."):
        try:
            job_details = st.session_state.job_details
            relevant_projects = st.session_state.relevant_pro
