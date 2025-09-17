import streamlit as st
import os
import sys
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page config
st.set_page_config(page_title="Email Generator", page_icon="📧", layout="wide")

# Custom CSS for theme + button styling
st.markdown(
    """
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0A1828;
            color: #FFFFFF;
        }
        .main-title {
            font-size: 3rem;
            font-weight: bold;
            color: #178582;
            text-align: center;
            margin-bottom: -10px;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #BFA181;
            text-align: center;
            margin-bottom: 30px;
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

# Title + subtitle (restored ColdFlow design)
st.markdown("<div class='main-title'>ColdFlow</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Cold Email Generator for Technical & Non-Technical Careers</div>", unsafe_allow_html=True)

# User inputs
career_type = st.selectbox("Select Career Type", ["Technical", "Non-Technical"])
name = st.text_input("Your Name")
receiver = st.text_input("Receiver's Name / Company")
role = st.text_input("Job Role")
skills = st.text_area("Skills / Experience (comma separated)")
portfolio = st.text_area("Portfolio Projects / Links")
extra_notes = st.text_area("Additional Notes (optional)")

# Email generation
if st.button("Generate Email"):
    email_content = f"""
Dear {receiver},

I hope this message finds you well.

My name is {name}, and I am interested in the {role} position. With experience in {skills}, I believe I can contribute effectively to your team. 

Some of my relevant work includes:
{portfolio}

{extra_notes}

Looking forward to hearing from you.

Best regards,  
{name}
    """

    st.markdown("### ✉️ Generated Email:")
    st.text_area("Generated Email", email_content, height=250)

    # Copy to clipboard button (JS injection)
    st.markdown(
        f"""
        <button class="copy-btn" onclick="navigator.clipboard.writeText(`{email_content}`)">
            📋 Copy to Clipboard
        </button>
        """,
        unsafe_allow_html=True
    )

