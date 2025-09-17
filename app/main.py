# main.py
import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime
import json

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from portfolio import Portfolio
    from scraper import SimpleScraper
    from email_generator import EmailGenerator
except ImportError:
    # Fallback implementations
    class Portfolio:
        def query_links(self, skills):
            return [{"links": "https://example.com/python", "techstack": "Python, React", "similarity": 0.9}]
    class SimpleScraper:
        def scrape_job_info(self, url):
            return {
                "role": "Software Developer",
                "experience": "2+ years",
                "skills": "Python, React, SQL",
                "description": "We are hiring engineers with strong fullstack skills.",
                "company": "Tech Corp"
            }
    class EmailGenerator:
        def generate_email(self, job_data, portfolio_links, user_info):
            return f"Cold email for {job_data.get('role')} with skills {job_data.get('skills')}."

def main():
    # Page setup
    st.set_page_config(
        page_title="COLDFLOW - Cold Email Generator",
        page_icon="📧",
        layout="wide"
    )

    # Custom fonts + gradient CSS with clipboard functionality
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@700&family=Roboto:wght@400&display=swap" rel="stylesheet">
    <style>
    body {
        margin: 0;
        font-family: "Roboto", sans-serif;
        background: linear-gradient(135deg, #0A1828 0%, #178582 50%, #0A1828 100%);
        color: white;
    }
    .hero {
        padding: 4rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, #0A1828, #178582);
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 5rem;
        font-family: "Bebas Neue", sans-serif;
        letter-spacing: 2px;
        color: #BFA181; /* Gold */
        margin-bottom: 0.5rem;
    }
    .hero p {
        font-size: 1.3rem;
        font-style: italic;
        color: #F0F0F0;
        margin-top: 0;
    }
    .stTabs [role="tablist"] button {
        background: #0A1828;
        color: #FFFFFF;
        border-radius: 6px;
    }
    .stTabs [role="tablist"] button[data-baseweb="tab"]:hover {
        background: #178582;
        color: #FFFFFF;
    }
    .stButton button {
        background-color: #BFA181;
        color: #0A1828;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #178582;
        color: #FFFFFF;
    }
    .card {
        background-color: rgba(10, 24, 40, 0.85);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #BFA181;
    }
    .generated-email {
        background: rgba(23,133,130,0.15);
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #BFA181;
        color: #FFFFFF;
    }
    .copy-btn {
        background-color: #178582 !important;
        color: white !important;
        margin-top: 10px;
    }
    .copy-btn:hover {
        background-color: #0A1828 !important;
        border: 1px solid #BFA181 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Add JavaScript for clipboard functionality
    st.markdown("""
    <script>
    function copyToClipboard(text) {
        // Create a temporary textarea element
        var textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            var successful = document.execCommand('copy');
            var msg = successful ? 'successful' : 'unsuccessful';
            alert('Email copied to clipboard successfully!');
        } catch (err) {
            console.error('Could not copy text: ', err);
            alert('Failed to copy to clipboard. Please try again.');
        }
        
        document.body.removeChild(textArea);
    }
    </script>
    """, unsafe_allow_html=True)

    # Hero header
    st.markdown("""
    <div class="hero">
        <h1>📧 COLDFLOW</h1>
        <p>Generate personalized cold emails effortlessly — stand out in job applications.</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize modules
    portfolio = Portfolio()
    scraper = SimpleScraper()
    email_gen = EmailGenerator()

    # User info
    with st.expander("👤 Your Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name", "Mohan Sharma")
            role = st.text_input("Your Role", "Business Development Executive")
            company = st.text_input("Your Company", "AtliQ Technologies")
        with col2:
            email = st.text_input("Your Email", "mohan@atliq.com")
            phone = st.text_input("Your Phone", "+91-9876543210")
            linkedin = st.text_input("LinkedIn Profile (optional)", "")
    user_info = {"name": name, "role": role, "company": company, "email": email, "phone": phone, "linkedin": linkedin}

    # Tabs
    tab1, tab2 = st.tabs(["🌐 Extract from URL", "📝 Manual Input"])

    # Store email text in session state
    if 'email_text' not in st.session_state:
        st.session_state.email_text = ""

    with tab1:
        st.header("Extract Job Information from URL")
        job_url = st.text_input("Job URL", placeholder="https://company.com/job/software-dev", key="url_input")
        if st.button("Extract & Generate Email", key="url_btn"):
            if job_url:
                job_data = scraper.scrape_job_info(job_url)
                st.success("✅ Extracted job info!")
                st.markdown(f"""
                <div class="card">
                    <h3 style='color:#BFA181'>{job_data.get("role")}</h3>
                    <p><b>🏢 Company:</b> {job_data.get("company")}</p>
                    <p><b>📊 Experience:</b> {job_data.get("experience")}</p>
                    <p><b>🛠 Skills:</b> {job_data.get("skills")}</p>
                    <p><b>📝 Description:</b> {job_data.get("description")}</p>
                </div>
                """, unsafe_allow_html=True)

                links = portfolio.query_links(job_data.get("skills"))
                if links:
                    st.markdown("### 🔗 Relevant Portfolio Items")
                    for i, l in enumerate(links):
                        st.markdown(f"""
                        <div class="card">
                            <p><strong>Item {i+1}:</strong> <a href="{l['links']}" target="_blank" style="color:#BFA181;">{l['links']}</a></p>
                            <p style="color:#E0E0E0;">{l['techstack']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                st.session_state.email_text = email_gen.generate_email(job_data, links, user_info)
                st.markdown("### ✨ Generated Email")
                st.markdown(f"<div class='generated-email'><pre>{st.session_state.email_text}</pre></div>", unsafe_allow_html=True)
                
                # Add copy to clipboard functionality
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download Email",
                        data=st.session_state.email_text,
                        file_name=f"cold_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                with col2:
                    # Use JavaScript to copy to clipboard - fixed escaping
                    safe_text = st.session_state.email_text.replace("`", "\\`").replace("${", "\\${")
                    st.markdown(f"""
                    <button onclick="copyToClipboard(`{safe_text}`)" 
                            style="background-color: #178582; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 8px; cursor: pointer; width: 100%;">
                        📋 Copy to Clipboard
                    </button>
                    """, unsafe_allow_html=True)

    with tab2:
        st.header("Enter Job Details Manually")
        col1, col2 = st.columns(2)
        with col1:
            role_manual = st.text_input("Job Role*", key="m_role")
            exp_manual = st.text_input("Experience", key="m_exp")
        with col2:
            skills_manual = st.text_input("Skills*", key="m_skills")
            company_manual = st.text_input("Company", key="m_company")
        desc_manual = st.text_area("Job Description", key="m_desc")
        if st.button("Generate Email", key="manual_btn"):
            if role_manual and skills_manual:
                job_data = {"role": role_manual, "experience": exp_manual, "skills": skills_manual, "description": desc_manual, "company": company_manual}
                links = portfolio.query_links(skills_manual)
                st.session_state.email_text = email_gen.generate_email(job_data, links, user_info)
                st.markdown("### ✨ Generated Email")
                st.markdown(f"<div class='generated-email'><pre>{st.session_state.email_text}</pre></div>", unsafe_allow_html=True)
                
                # Add copy to clipboard functionality
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download Email",
                        data=st.session_state.email_text,
                        file_name=f"cold_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="manual_download"
                    )
                with col2:
                    # Use JavaScript to copy to clipboard - fixed escaping
                    safe_text = st.session_state.email_text.replace("`", "\\`").replace("${", "\\${")
                    st.markdown(f"""
                    <button onclick="copyToClipboard(`{safe_text}`)" 
                            style="background-color: #178582; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 8px; cursor: pointer; width: 100%;">
                        📋 Copy to Clipboard
                    </button>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Fill at least Role & Skills")

    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align:center;color:#BFA181'>© {datetime.now().year} COLDFLOW — Built for professionals</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
