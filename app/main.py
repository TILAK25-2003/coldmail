import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page config
st.set_page_config(page_title="COLDFLOW - Email Generator", page_icon="📧", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0A1828, #178582);
            color: #FFFFFF;
        }
        .gradient-text {
            font-size: 42px;
            font-weight: bold;
            background: linear-gradient(90deg, #178582, #BFA181, #0A1828);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 20px;
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
            padding: 10px 20px;
            border-radius: 8px;
            background: #6C63FF;
            color: #fff;
            border: none;
            font-weight: bold;
            cursor: pointer;
        }
        .copy-btn:hover {
            background: #5548d6;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Gradient title
st.markdown("<div class='gradient-text'>COLDFLOW</div>", unsafe_allow_html=True)

st.title("📧 Professional Email Generator")

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
Subject: Application for {role}

Dear {receiver},

I am writing to apply for the {role} position, as I believe my qualifications and experience align perfectly with your requirements.

With expertise in {skills}, I bring a proven track record of success and the ability to contribute effectively to your team.  

Some of my relevant work includes:
{portfolio}

{extra_notes}

Looking forward to your response.

Best regards,  
{name}
    """

    st.markdown("### ✉️ Generated Email:")
    st.text_area("Generated Email", email_content, height=250)

    # ✅ Replaced "Download Email" with Copy to Clipboard
    st.markdown(
        f"""
        <button class="copy-btn" onclick="navigator.clipboard.writeText(`{email_content}`)">
            📋 Copy to Clipboard
        </button>
        """,
        unsafe_allow_html=True
    )



