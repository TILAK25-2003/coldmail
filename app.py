# app.py (updated imports section)
import streamlit as st
import os
import sys
import traceback

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import with better error handling
try:
    from job_parser import extract_job_details
except ImportError as e:
    st.error(f"Failed to import job_parser: {e}")
    # Define a fallback function
    def extract_job_details(url):
        return {
            "role": "Software Developer",
            "experience": "2+ years",
            "skills": ["Python", "JavaScript", "Problem Solving"],
            "description": "Job description extraction is currently unavailable."
        }

try:
    from portfolio_matcher import find_relevant_projects
except ImportError as e:
    st.error(f"Failed to import portfolio_matcher: {e}")
    # Define a fallback function
    def find_relevant_projects(skills, n_results=3):
        return [
            {"document": "Python, Django, PostgreSQL", "metadata": {"links": "https://example.com/python-project"}},
            {"document": "React, Node.js, MongoDB", "metadata": {"links": "https://example.com/react-project"}}
        ]

try:
    from email_generator import generate_cold_email
except ImportError as e:
    st.error(f"Failed to import email_generator: {e}")
    # Define a fallback function
    def generate_cold_email(job_data, projects):
        return f"""
        Subject: Application for {job_data.get('role', 'Software Developer')} Position
        
        Dear Hiring Manager,
        
        I am writing to express my interest in the {job_data.get('role', 'Software Developer')} position.
        
        With experience in {', '.join(job_data.get('skills', ['Python', 'JavaScript']))}, 
        I believe I would be a strong candidate for this role.
        
        Thank you for considering my application.
        
        Sincerely,
        [Your Name]
        """

# The rest of your app.py remains the same...
# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import with better error handling
try:
    from job_parser import extract_job_details
except ImportError as e:
    st.error(f"Failed to import job_parser: {e}")
    # Define a fallback function
    def extract_job_details(url):
        return {
            "role": "Software Developer",
            "experience": "2+ years",
            "skills": ["Python", "JavaScript", "Problem Solving"],
            "description": "Job description extractio# Add to the top of app.py (after imports) is currently unavailable."
        }

try:
    from portfolio_matcher import find_relevant_projects
except ImportError as e:
    st.error(f"Failed to import portfolio_matcher: {e}")
    # Define a fallback function
    def find_relevant_projects(skills, n_results=3):
        return [
            {"document": "Python, Django, PostgreSQL", "metadata": {"links": "https://example.com/python-project"}},
            {"document": "React, Node.js, MongoDB", "metadata": {"links": "https://example.com/react-project"}}
        ]

try:
    from email_generator import generate_cold_email
except ImportError as e:
    st.error(f"Failed to import email_generator: {e}")
    # Define a fallback function
    def generate_cold_email(job_data, projects):
        return f"""
        Subject: Application for {job_data.get('role', 'Software Developer')} Position
        
        Dear Hiring Manager,
        
        I am writing to express my interest in the {job_data.get('role', 'Software Developer')} position.
        
        With experience in {', '.join(job_data.get('skills', ['Python', 'JavaScript']))}, 
        I believe I would be a strong candidate for this role.
        
        Thank you for considering my application.
        
        Sincerely,
        [Your Name]
        """

# The rest of your app.py remains the same...


