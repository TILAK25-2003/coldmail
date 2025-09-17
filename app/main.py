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

# Custom CSS with enhanced typography
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Anton&family=Brush+Script+MT&family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: #0A1828;
            color: #FFFFFF;
        }
        .main-header {
            font-family: 'Anton', sans-serif;
            font-size: 5.5rem;
            font-weight: 400;
            text-align: center;
            margin-bottom: 0.3rem;
            background: linear-gradient(90deg, #178582, #BFA181);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0px 4px 15px rgba(23, 133, 130, 0.3);
            letter-spacing: 2px;
        }
        .sub-header {
            font-family: 'Brush Script MT', cursive;
            font-size: 2.2rem;
            color: #BFA181;
            text-align: center;
            margin-top: -1rem;
            margin-bottom: 2.5rem;
            text-shadow: 0px 2px 8px rgba(191, 161, 129, 0.4);
        }
        .section-header {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: #178582;
            margin-bottom: 1rem;
            border-bottom: 2px solid #BFA181;
            padding-bottom: 0.5rem;
        }
        .user-section, .generated-email-container {
            background-color: rgba(10, 24, 40, 0.9);
            padding: 1.8rem;
            border-radius: 0.8rem;
            border-left: 4px solid #178582;
            color: #FFFFFF;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            margin-bottom: 1.5rem;
        }
        .generated-email-container {
            border-left: 4px solid #BFA181;
        }
        .email-content {
            background-color: rgba(23, 133, 130, 0.1);
            padding: 1.5rem;
            border-radius: 0.5rem;
            border: 1px solid #178582;
            color: #FFFFFF;
            font-family: 'Montserrat', monospace;
            white-space: pre-wrap;
            line-height: 1.6;
            margin: 1rem 0;
            max-height: 400px;
            overflow-y: auto;
        }
        .stButton>button {
            background: linear-gradient(135deg, #178582, #0A1828);
            color: #FFFFFF;
            font-weight: 600;
            border-radius: 12px;
            padding: 12px 28px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Montserrat', sans-serif;
            box-shadow: 0 4px 8px rgba(23, 133, 130, 0.3);
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #0A1828, #178582);
            box-shadow: 0 6px 12px rgba(23, 133, 130, 0.4);
            transform: translateY(-2px);
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #0A1828;
            border-radius: 8px 8px 0px 0px;
            gap: 8px;
            padding: 12px 20px;
            border: 1px solid #178582;
            color: #BFA181;
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #178582;
            color: #0A1828;
        }
        .footer {
            text-align: center;
            color: #BFA181;
            margin-top: 3rem;
            padding: 1rem;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.9rem;
        }
        .success-message {
            background-color: rgba(23, 133, 130, 0.2);
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #178582;
            margin: 1rem 0;
        }
        .portfolio-item {
            background-color: rgba(191, 161, 129, 0.1);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.8rem;
            border: 1px solid #BFA181;
        }
        .email-textarea {
            background-color: rgba(23, 133, 130, 0.1) !important;
            color: #FFFFFF !important;
            border: 1px solid #178582 !important;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'Montserrat', monospace !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header with enhanced typography
st.markdown('<h1 class="main-header">COLDFLOW</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Crafting connections through compelling communication</p>', unsafe_allow_html=True)

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
    st.markdown('<h3 class="section-header">Extract Job Information from URL</h3>', unsafe_allow_html=True)
    job_url = st.text_input("Enter Job URL:", placeholder="https://company.com/careers/job-title", key="url_input")

    if st.button("Extract & Generate Email", key="url_btn"):
        if job_url:
            with st.spinner("Extracting job information..."):
                job_data = scraper.scrape_job_info(job_url)

                if job_data:
                    st.markdown('<div class="success-message">✅ Job information extracted successfully!</div>', unsafe_allow_html=True)
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
                                <div class="portfolio-item">
                                    <p style='margin: 0;'><strong>Item {i+1}:</strong> 
                                    <a href="{link['links']}" target="_blank" style="color:#178582; text-decoration: none; font-weight: 600;">{link['links']}</a></p>
                                    <p style='margin: 0; color: #E5E7EB;'>{link['techstack']}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    # Display the generated email properly inside the green container
st.markdown("### ✨ Generated Cold Email")
st.markdown('<div class="generated-email-container">', unsafe_allow_html=True)

# Replace newlines with HTML line breaks for proper formatting
formatted_email = email.replace('\n', '<br>')
st.markdown(f'<div class="email-content">{formatted_email}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

                        # Download button only
                        st.download_button(
                            label="📥 Download Email",
                            data=email,
                            file_name=f"cold_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                else:
                    st.error("Could not extract job information. Please try again.")
        else:
            st.warning("Please enter a job URL")

# ---------- Manual Input Tab ----------
with tab2:
    st.markdown('<h3 class="section-header">Enter Job Details Manually</h3>', unsafe_allow_html=True)
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
            st.markdown('<div class="generated-email-container">', unsafe_allow_html=True)
            
            # Display email content properly inside the container
            st.markdown(f'<div class="email-content">{email}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

            # Download button only
            st.download_button(
                label="📥 Download Email",
                data=email,
                file_name=f"cold_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="manual_download",
                use_container_width=True
            )
        else:
            st.warning("Please fill at least Job Role and Required Skills fields")

# Footer
st.markdown("---")
st.markdown(
    f"<div class='footer'>"
    "COLDFLOW • Professional Cold Email Generator • "
    f"© {datetime.now().year}</div>",
    unsafe_allow_html=True
)
