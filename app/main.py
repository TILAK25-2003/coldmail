# main.py
import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from portfolio import Portfolio
    from scraper import SimpleScraper
    from email_generator import EmailGenerator
except ImportError:
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
                'description': 'We are looking for a skilled professional with relevant experience and skills.',
                'company': 'Tech Company Inc.'
            }

    class EmailGenerator:
        def generate_email(self, job_data, portfolio_links, user_info):
            return f"Email for {job_data.get('role', 'position')} with skills {job_data.get('skills', '')}"

# Page config
st.set_page_config(
    page_title="COLDFLOW - Professional Cold Email Generator",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with new color theme
st.markdown(
    """
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0A1828;
            color: #FFFFFF;
        }
        .main-header {
            font-size: 4rem;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 0.3rem;
            font-weight: bold;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #BFA181;
            text-align: center;
            margin-top: 0rem;
            margin-bottom: 2rem;
        }
        .user-section, .generated-email {
            background-color: #0A1828;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #178582;
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #178582;
            color: #FFFFFF;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #BFA181;
            color: #0A1828;
        }
        .copy-btn {
            padding: 8px 15px;
            border-radius: 5px;
            background: #6C63FF;
            color: #fff;
            border: none;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<h1 class="main-header">📧 COLDFLOW</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Smooth cold email generation for job applications</p>', unsafe_allow_html=True)

# Initialize components
portfolio = Portfolio()
email_gen = EmailGenerator()
scraper = SimpleScraper()

# User info
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

# Tabs
tab1, tab2 = st.tabs(["🌐 Extract from URL", "📝 Manual Input"])

# ---------- URL Tab ----------
with tab1:
    st.header("Extract Job Information from URL")
    job_url = st.text_input("Enter Job URL:", placeholder="https://company.com/careers/job-title")

    if st.button("Extract & Generate Email", key="url_btn"):
        if job_url:
            with st.spinner("Extracting job information..."):
                job_data = scraper.scrape_job_info(job_url)

                if job_data:
                    st.success("✅ Job information extracted successfully!")
                    st.markdown("---")
                    st.markdown("### 📋 Extracted Job Details")

                    job_col1, job_col2 = st.columns([1, 2])
                    with job_col1:
                        st.markdown(
                            f"""
                            <div class="user-section">
                                <h3 style='color: #BFA181; margin-top: 0;'>{job_data.get('role', 'Not specified')}</h3>
                                <p><strong>🏢 Company:</strong> {job_data.get('company', 'Not specified')}</p>
                                <p><strong>📊 Experience:</strong> {job_data.get('experience', 'Not specified')}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    with job_col2:
                        st.markdown(
                            f"""
                            <div class="user-section">
                                <p><strong>🛠️ Required Skills:</strong></p>
                                <p>{job_data.get('skills', 'Not specified')}</p>
                                <p><strong>📝 Description:</strong></p>
                                <p>{job_data.get('description', 'Not specified')}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # Portfolio links
                    skills = job_data.get('skills', '')
                    relevant_links = portfolio.query_links(skills)

                    if relevant_links:
                        st.markdown("### 🔗 Relevant Portfolio Items")
                        for i, link in enumerate(relevant_links):
                            st.markdown(
                                f"""
                                <div class="user-section" style="margin-bottom:0.5rem;">
                                    <p style='margin: 0;'><strong>Item {i+1}:</strong> 
                                    <a href="{link['links']}" target="_blank" style="color:#178582;">{link['links']}</a></p>
                                    <p style='margin: 0; color: #E5E7EB;'>{link['techstack']}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    # Generate email
                    with st.spinner("Crafting your perfect cold email..."):
                        email = email_gen.generate_email(job_data, relevant_links, user_info)

                        st.markdown("### ✨ Generated Cold Email")
                        st.markdown('<div class="generated-email">', unsafe_allow_html=True)
                        st.text_area("Email Content", email, height=300, label_visibility="collapsed", key="email_output_url")
                        st.markdown('</div>', unsafe_allow_html=True)

                        # Actions
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                label="Download Email",
                                data=email,
                                file_name=f"cold_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain"
                            )
                        with col2:
                            st.markdown(
                                f"""
                                <button class="copy-btn" onclick="navigator.clipboard.writeText(`{email}`)">
                                    📋 Copy to Clipboard
                                </button>
                                """,
                                unsafe_allow_html=True
                            )
                else:
                    st.error("Could not extract job information. Please try again.")
        else:
            st.warning("Please enter a job URL")

# ---------- Manual Input Tab ----------
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
            email = email_gen.generate_email(job_data, relevant_links, user_info)

            st.markdown("### ✨ Generated Cold Email")
            st.markdown('<div class="generated-email">', unsafe_allow_html=True)
            st.text_area("Email Content", email, height=300, label_visibility="collapsed", key="email_output_manual")
            st.markdown('</div>', unsafe_allow_html=True)

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
                st.markdown(
                    f"""
                    <button class="copy-btn" onclick="navigator.clipboard.writeText(`{email}`)">
                        📋 Copy to Clipboard
                    </button>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("Please fill at least Job Role and Required Skills fields")

# Footer
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #FFFFFF;'>"
    "COLDFLOW • Professional Cold Email Generator • "
    f"© {datetime.now().year}</div>",
    unsafe_allow_html=True
)


