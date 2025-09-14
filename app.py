import streamlit as st
from job_parser import extract_job_details, extract_key_info
from portfolio_matcher import find_relevant_projects
from email_generator import generate_cold_email

# Your portfolio
MY_PORTFOLIO = [
    {
        'name': 'E-commerce Website',
        'description': 'Built a full-stack e-commerce platform with React and Node.js',
        'skills': ['React', 'Node.js', 'MongoDB', 'JavaScript', 'HTML', 'CSS'],
        'url': 'https://github.com/yourusername/ecommerce'
    },
    {
        'name': 'Data Analysis Tool',
        'description': 'Developed a Python tool for data analysis and visualization',
        'skills': ['Python', 'Pandas', 'Matplotlib', 'Data Analysis', 'SQL'],
        'url': 'https://github.com/yourusername/data-tool'
    }
]

def main():
    st.title("✉️ ColdMail Generator")
    st.write("Paste job URL → Get key info → Generate personalized email")
    
    job_url = st.text_input("Job Posting URL:", placeholder="https://linkedin.com/job/123")
    
    if st.button("Analyze Job") and job_url:
        with st.spinner("Extracting job details and company information..."):
            result = extract_job_details(job_url)
            key_info = extract_key_info(result['job_text'])
            relevant_projects = find_relevant_projects(result['job_text'], MY_PORTFOLIO)
            
            # Store in session state
            st.session_state.key_info = key_info
            st.session_state.relevant_projects = relevant_projects
            st.session_state.company_name = result['company_name']
            st.session_state.job_text = result['job_text']
            
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
            # Use detected company name as default
            company_name = st.text_input("Company Name:", st.session_state.company_name)
        
        hiring_manager = st.text_input("Hiring Manager (optional):", "Hiring Team")
        
        if st.button("Generate Email"):
            generate_email(your_name, company_name, hiring_manager)

def display_results():
    """Display extracted job information"""
    key_info = st.session_state.key_info
    
    st.subheader("🔍 Extracted Job Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Role:** {key_info.get('role', 'Not specified')}")
    with col2:
        st.info(f"**Experience:** {key_info.get('experience', 'Not specified')}")
    
    st.subheader("🛠️ Technical Skills")
    tech_skills = key_info.get('technical_skills', [])
    if tech_skills:
        st.write(", ".join(tech_skills))
    else:
        st.write("No technical skills detected")
    
    st.subheader("💼 Soft Skills")
    soft_skills = key_info.get('soft_skills', [])
    if soft_skills:
        st.write(", ".join(soft_skills))
    else:
        st.write("No soft skills detected")
    
    st.subheader("🎯 Relevant Projects")
    relevant_projects = st.session_state.relevant_projects
    if relevant_projects:
        for project in relevant_projects:
            st.write(f"**{project['name']}** - {project['description']}")
    else:
        st.write("No relevant projects found")

def generate_email(your_name, company_name, hiring_manager):
    """Generate and display cold email"""
    key_info = st.session_state.key_info
    relevant_projects = st.session_state.relevant_projects
    
    email = generate_cold_email(
        your_name=your_name,
        company_name=company_name,
        hiring_manager=hiring_manager,
        job_role=key_info.get('role', ''),
        technical_skills=key_info.get('technical_skills', []),
        soft_skills=key_info.get('soft_skills', []),
        relevant_projects=relevant_projects,
        experience_required=key_info.get('experience', '')
    )
    
    st.subheader("📝 Generated Cold Email")
    st.text_area("Email Content", email, height=400)
    st.success("✅ Email generated! Copy and customize as needed.")

if __name__ == "__main__":
    main()
