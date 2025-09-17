# main.py
import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Add the current directory to the path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from portfolio import Portfolio
    from scraper import AdvancedScraper
    from email_generator import EnhancedEmailGenerator
except ImportError as e:
    st.error(f"Import error: {e}")
    # Fallback implementations
    class Portfolio:
        def __init__(self, file_path=None):
            self.data = pd.DataFrame({
                "Techstack": ["Python, JavaScript, React", "Java, Spring Boot", "Node.js, MongoDB"],
                "Links": ["https://example.com/python", "https://example.com/java", "https://example.com/nodejs"]
            })
        
        def query_links(self, skills):
            return [
                {"links": "https://example.com/python", "techstack": "Python, JavaScript, React", "similarity": 0.8},
                {"links": "https://example.com/java", "techstack": "Java, Spring Boot", "similarity": 0.6}
            ]
    
    class AdvancedScraper:
        def scrape_job_info(self, url):
            return {
                'role': 'Software Developer',
                'experience': '2+ years',
                'skills': 'Python, JavaScript, SQL, React',
                'description': 'We are looking for a skilled professional with relevant experience and skills.',
                'company': 'Tech Company Inc.'
            }
    
    class EnhancedEmailGenerator:
        def generate_email(self, job_data, portfolio_links, user_info):
            return f"Email for {job_data.get('role', 'position')} with skills {job_data.get('skills', '')}"

def main():
    # Page configuration
    st.set_page_config(
        page_title="COLDFLOW - Professional Cold Email Generator",
        page_icon="📧",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for professional styling
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@700&family=Roboto:wght@400&display=swap" rel="stylesheet">
    <style>
    .bebas-neue-regular {
        font-family: "Bebas Neue", sans-serif;
        font-weight: 800;
        font-style: normal;
    }
    .main-header {
        font-size: 5.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.3rem;
        font-family: "Bebas Neue", sans-serif;
        letter-spacing: 2px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #374151;
        text-align: center;
        margin-top: 0rem;
        margin-bottom: 2rem;
        font-family: "Bebas Neue", sans-serif;
        font-style: italic;
        letter-spacing: 1px;
    }
    .user-section {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    .generated-email {
        background-color: #F9FAFB;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
    }
    .stButton button {
        background-color: #1B5A57;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton button:hover {
        background-color: #94B3F5;
    }
    .extracted-info {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header section
    st.markdown('<h1 class="main-header bebas-neue-regular">📧 COLDFLOW</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header bebas-neue-regular">Advanced Cold Email Generation for All Job Types</p>', unsafe_allow_html=True)
    
    # Initialize components
    portfolio = Portfolio()
    email_gen = EnhancedEmailGenerator()
    scraper = AdvancedScraper()
    
    # User information section
    with st.expander("👤 Your Professional Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("Your Full Name", value="Mohan Sharma")
            user_role = st.text_input("Your Current Role", value="Business Development Executive")
            user_company = st.text_input("Your Company", value="AtliQ Technologies")
        
        with col2:
            user_email = st.text_input("Your Email", value="mohan@atliq.com")
            user_phone = st.text_input("Your Phone", value="+91-9876543210")
            user_linkedin = st.text_input("LinkedIn Profile URL", value="")
    
    user_info = {
        'name': user_name,
        'role': user_role,
        'company': user_company,
        'email': user_email,
        'phone': user_phone,
        'linkedin': user_linkedin
    }
    
    # Main content
    tab1, tab2 = st.tabs(["🌐 Extract from Job URL", "📝 Enter Job Details Manually"])
    
    with tab1:
        st.header("Extract Job Information from URL")
        st.info("Paste any job posting URL from company career pages, LinkedIn, Indeed, Naukri, etc.")
        
        job_url = st.text_input("Enter Job URL:", placeholder="https://company.com/careers/job-title or https://linkedin.com/jobs/view/...", key="url_input")
        
        if st.button("🚀 Extract & Generate Email", key="url_btn", type="primary"):
            if job_url:
                with st.spinner("🔍 Analyzing job posting and extracting information..."):
                    job_data = scraper.scrape_job_info(job_url)
                    
                    # Check for errors
                    if 'error' in job_data:
                        st.error(f"❌ {job_data['error']}")
                        st.info("💡 Please try a different URL or use manual input below.")
                    else:
                        st.success("✅ Job information extracted successfully!")
                        
                        # Display extracted information in a structured way
                        with st.expander("📋 View Extracted Job Details", expanded=True):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**🎯 Job Role**")
                                st.info(job_data['role'])
                                
                                st.markdown("**🏢 Company**")
                                st.info(job_data['company'])
                                
                            with col2:
                                st.markdown("**📈 Experience Required**")
                                st.info(job_data['experience'])
                                
                                st.markdown("**🔧 Key Skills**")
                                st.info(job_data['skills'])
                            
                            st.markdown("**📝 Job Description**")
                            st.text_area("Description", job_data['description'], height=150, label_visibility="collapsed")
                        
                        # Get relevant portfolio links
                        skills = job_data.get('skills', '')
                        relevant_links = portfolio.query_links(skills)
                        
                        # Display relevant links
                        if relevant_links:
                            st.subheader("🔗 Recommended Portfolio Items")
                            for link in relevant_links:
                                st.markdown(f"- **[{link['techstack']}]({link['links']})** (Relevance: {link.get('similarity', 0):.2f})")
                        
                        # Generate email
                        with st.spinner("✍️ Crafting your professional cold email..."):
                            email = email_gen.generate_email(job_data, relevant_links, user_info)
                            
                            st.markdown("### ✨ Generated Professional Email")
                            st.markdown('<div class="generated-email">', unsafe_allow_html=True)
                            st.text_area("Email Content", email, height=350, label_visibility="collapsed", key="email_output_url")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Email actions
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.download_button(
                                    label="📥 Download Email",
                                    data=email,
                                    file_name=f"professional_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain",
                                    key="download_url"
                                )
                            with col2:
                                if st.button("📋 Copy to Clipboard", key="copy_url"):
                                    st.code(email, language=None)
                                    st.success("✅ Email copied to clipboard!")
                            with col3:
                                if st.button("🔄 Regenerate Email", key="regenerate_url"):
                                    st.rerun()
            else:
                st.warning("⚠️ Please enter a job URL")
    
    with tab2:
        st.header("Enter Job Details Manually")
        st.info("Fill in the details for any type of job - technical, non-technical, management, creative, etc.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            role = st.text_input("Job Role*", placeholder="e.g., Software Engineer, Marketing Manager, Sales Executive", key="manual_role")
            experience = st.selectbox("Experience Level", 
                                    ["Fresher", "0-2 years", "2-5 years", "5-8 years", "8+ years", "Senior Level"], 
                                    key="manual_exp")
        
        with col2:
            skills_input = st.text_input("Required Skills*", placeholder="e.g., Python, Marketing, Sales, Management", key="manual_skills")
            company = st.text_input("Company Name", placeholder="Company Name", key="manual_company")
        
        job_type = st.selectbox("Job Type", 
                               ["Technical", "Non-Technical", "Management", "Creative", "Sales/Marketing", "Operations", "Other"], 
                               key="job_type")
        
        description = st.text_area("Job Description", 
                                  placeholder="Paste the job description or key requirements here...", 
                                  height=150, key="manual_desc")
        
        if st.button("🚀 Generate Email", key="manual_btn", type="primary"):
            if role and skills_input:
                job_data = {
                    'role': role,
                    'experience': experience,
                    'skills': skills_input,
                    'description': description,
                    'company': company,
                    'job_type': job_type
                }
                
                relevant_links = portfolio.query_links(skills_input)
                
                # Generate email
                email = email_gen.generate_email(job_data, relevant_links, user_info)
                
                st.markdown("### ✨ Generated Professional Email")
                st.markdown('<div class="generated-email">', unsafe_allow_html=True)
                st.text_area("Email Content", email, height=350, label_visibility="collapsed", key="email_output_manual")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Email actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        label="📥 Download Email",
                        data=email,
                        file_name=f"professional_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="manual_download"
                    )
                with col2:
                    if st.button("📋 Copy to Clipboard", key="manual_copy"):
                        st.code(email, language=None)
                        st.success("✅ Email copied to clipboard!")
                with col3:
                    if st.button("🔄 Regenerate", key="manual_regenerate"):
                        st.rerun()
            else:
                st.warning("⚠️ Please fill at least Job Role and Required Skills fields")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #6B7280;'>"
        "COLDFLOW • Advanced Cold Email Generator • "
        f"© {datetime.now().year} • Supporting All Job Types</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
