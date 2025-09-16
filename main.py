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
    from scraper import SimpleScraper
    from email_generator import EmailGenerator
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
    
    class SimpleScraper:
        def scrape_job_info(self, url):
            return {
                'role': 'Software Developer',
                'experience': '2+ years',
                'skills': 'Python, JavaScript, SQL, React',
                'description': 'We are looking for a skilled professional with relevant experience and skills.'
            }
    
    class EmailGenerator:
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
        margin-bottom: 0.3rem; /* Reduced from 1rem */
        font-family: "Bebas Neue", sans-serif;
        letter-spacing: 2px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #374151;
        text-align: center;
        margin-top: 0rem;      /* Add this line to remove any top margin */
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
    </style>
    """, unsafe_allow_html=True)

    # Header section
    st.markdown('<h1 class="main-header bebas-neue-regular">📧 COLDFLOW</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header bebas-neue-regular">Smooth cold email generation for job applications</p>', unsafe_allow_html=True)
    
    # Initialize components
    portfolio = Portfolio()
    email_gen = EmailGenerator()
    scraper = SimpleScraper()
    
    # User information section
    with st.expander("👤 Your Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("Your Name", value="Mohan Sharma")
            user_role = st.text_input("Your Role", value="Business Development Executive")
            user_company = st.text_input("Your Company", value="AtliQ Technologies")
        
        with col2:
            user_email = st.text_input("Your Email", value="mohan@atliq.com")
            user_phone = st.text_input("Your Phone", value="+91-9876543210")
            user_linkedin = st.text_input("LinkedIn Profile (optional)", value="")
    
    user_info = {
        'name': user_name,
        'role': user_role,
        'company': user_company,
        'email': user_email,
        'phone': user_phone,
        'linkedin': user_linkedin
    }
    
    # Main content
    tab1, tab2 = st.tabs(["🌐 Extract from URL", "📝 Manual Input"])
    
    with tab1:
        st.header("Extract Job Information from URL")
        job_url = st.text_input("Enter Job URL:", placeholder="https://company.com/careers/job-title")
        
        if st.button("Extract & Generate Email", key="url_btn"):
            if job_url:
                with st.spinner("Extracting job information..."):
                    job_data = scraper.scrape_job_info(job_url)
                    
                    if job_data:
                        st.success("Job information extracted successfully!")
                        with st.expander("View Extracted Job Details"):
                            st.json(job_data)
                        
                        # Get relevant portfolio links
                        skills = job_data.get('skills', '')
                        relevant_links = portfolio.query_links(skills)
                        
                        # Generate email
                        with st.spinner("Crafting your perfect cold email..."):
                            email = email_gen.generate_email(job_data, relevant_links, user_info)
                            
                            st.markdown("### ✨ Generated Cold Email")
                            st.markdown('<div class="generated-email">', unsafe_allow_html=True)
                            st.text_area("Email Content", email, height=300, label_visibility="collapsed")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Email actions
                            col1, col2 = st.columns(2)
                            with col1:
                                st.download_button(
                                    label="Download Email",
                                    data=email,
                                    file_name=f"cold_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain"
                                )
                            with col2:
                                if st.button("Copy to Clipboard"):
                                    st.code(email, language=None)
                                    st.success("Email copied to clipboard!")
                    else:
                        st.error("Could not extract job information. Please try a different URL or use manual input.")
            else:
                st.warning("Please enter a job URL")
    
    with tab2:
        st.header("Enter Job Details Manually")
        
        col1, col2 = st.columns(2)
        
        with col1:
            role = st.text_input("Job Role*", key="manual_role")
            experience = st.text_input("Experience Level", key="manual_exp")
        
        with col2:
            skills_input = st.text_input("Required Skills*", key="manual_skills")
            company = st.text_input("Company Name", key="manual_company")
        
        description = st.text_area("Job Description", height=150, key="manual_desc")
        
        if st.button("Generate Email", key="manual_btn"):
            if role and skills_input:
                job_data = {
                    'role': role,
                    'experience': experience,
                    'skills': skills_input,
                    'description': description,
                    'company': company
                }
                
                relevant_links = portfolio.query_links(skills_input)
                
                # Generate email
                email = email_gen.generate_email(job_data, relevant_links, user_info)
                
                st.markdown("### ✨ Generated Cold Email")
                st.markdown('<div class="generated-email">', unsafe_allow_html=True)
                st.text_area("Email Content", email, height=300, label_visibility="collapsed")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Email actions
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download Email",
                        data=email,
                        file_name=f"cold_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="manual_download"
                    )
                with col2:
                    if st.button("Copy to Clipboard", key="manual_copy"):
                        st.code(email, language=None)
                        st.success("Email copied to clipboard!")
            else:
                st.warning("Please fill at least Job Role and Required Skills fields")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #6B7280;'>"
        "COLDFLOW • Professional Cold Email Generator • "
        f"© {datetime.now().year}</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()