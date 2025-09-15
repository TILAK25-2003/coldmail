import os
import re
import requests
import streamlit as st
from bs4 import BeautifulSoup
from groq import Groq
from urllib.parse import urlparse
import json

# Set page configuration
st.set_page_config(
    page_title="Cold Email Generator",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .generated-email {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        padding: 20px;
        margin-top: 20px;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
def initialize_groq_client():
    if 'GROQ_API_KEY' in st.secrets:
        api_key = st.secrets['GROQ_API_KEY']
    else:
        api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")
    
    if not api_key:
        st.sidebar.warning("Please enter your Groq API key to continue")
        st.stop()
    
    try:
        client = Groq(api_key=api_key)
        return client
    except Exception as e:
        st.sidebar.error(f"Error initializing Groq client: {str(e)}")
        st.stop()

# Validate URL format
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Extract text from URL
def extract_text_from_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:10000]  # Limit text to avoid token limits
    except Exception as e:
        st.error(f"Error extracting text from URL: {str(e)}")
        return None

# Extract job details using LLM
def extract_job_details(client, text):
    prompt = f"""
    Extract the following information from this job posting text. If information is not available, say "Not specified".
    
    Return the information in JSON format with these keys:
    - job_role
    - experience_required
    - technical_skills
    - non_technical_skills
    - portfolio_projects
    - company_name
    
    Job Posting Text:
    {text}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at extracting structured information from job postings. Always return valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",  # You can change this to other Groq models
            temperature=0.1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"}
        )
        
        response = chat_completion.choices[0].message.content
        return json.loads(response)
    except Exception as e:
        st.error(f"Error extracting job details: {str(e)}")
        return None

# Generate cold email using LLM
def generate_cold_email(client, job_details, user_inputs):
    prompt = f"""
    Generate a professional cold email for a job application based on the following job details and applicant information.
    
    Job Details:
    {json.dumps(job_details, indent=2)}
    
    Applicant Information:
    - Name: {user_inputs['name']}
    - Background: {user_inputs['background']}
    - Specific skills/expertise: {user_inputs['skills']}
    - Why interested in this role: {user_inputs['interest_reason']}
    
    Requirements:
    - The email should be professional but not overly formal
    - Highlight how the applicant's skills match the job requirements
    - Mention specific projects or experiences that relate to the job
    - Keep it concise (around 200-300 words)
    - Include a subject line
    - Format the email properly with greeting, body, and closing
    - Do not make up information that isn't provided
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert career coach who helps job applicants write compelling cold emails for job applications."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating cold email: {str(e)}")
        return None

# Main application
def main():
    st.markdown('<h1 class="main-header">✉️ Cold Email Generator</h1>', unsafe_allow_html=True)
    st.markdown("Generate personalized cold emails for job applications based on the job posting URL.")
    
    # Initialize Groq client
    client = initialize_groq_client()
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Job Details")
        job_url = st.text_input("Job Posting URL:", placeholder="https://example.com/job-posting")
        
        st.header("Your Information")
        name = st.text_input("Your Name:", placeholder="John Doe")
        background = st.text_area("Your Background:", placeholder="Brief description of your professional background...")
        skills = st.text_area("Your Key Skills:", placeholder="List your key skills relevant to this job...")
        interest_reason = st.text_area("Why are you interested in this role?", placeholder="Explain why you're interested in this specific role...")
        
        generate_btn = st.button("Generate Cold Email", type="primary", use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### How it works:")
        st.markdown("1. Enter the URL of the job posting")
        st.markdown("2. Provide your personal information")
        st.markdown("3. Click 'Generate Cold Email'")
        st.markdown("4. The AI will analyze the job and create a personalized email")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if job_url and not is_valid_url(job_url):
            st.markdown('<div class="error-box">Please enter a valid URL</div>', unsafe_allow_html=True)
    
    with col2:
        if generate_btn:
            if not job_url:
                st.markdown('<div class="error-box">Please enter a job posting URL</div>', unsafe_allow_html=True)
            elif not is_valid_url(job_url):
                st.markdown('<div class="error-box">Please enter a valid URL</div>', unsafe_allow_html=True)
            elif not all([name, background, skills, interest_reason]):
                st.markdown('<div class="error-box">Please fill in all your information</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Analyzing job posting..."):
                    # Extract text from URL
                    page_text = extract_text_from_url(job_url)
                    
                    if not page_text:
                        st.markdown('<div class="error-box">Could not extract text from the URL. Please check if the URL is correct and accessible.</div>', unsafe_allow_html=True)
                    else:
                        # Extract job details
                        job_details = extract_job_details(client, page_text)
                        
                        if job_details:
                            st.markdown('<div class="success-box">Successfully extracted job details!</div>', unsafe_allow_html=True)
                            
                            with st.expander("View Extracted Job Details"):
                                st.json(job_details)
                            
                            # Prepare user inputs
                            user_inputs = {
                                'name': name,
                                'background': background,
                                'skills': skills,
                                'interest_reason': interest_reason
                            }
                            
                            # Generate cold email
                            with st.spinner("Generating cold email..."):
                                cold_email = generate_cold_email(client, job_details, user_inputs)
                                
                                if cold_email:
                                    st.markdown("### Generated Cold Email")
                                    st.markdown('<div class="generated-email">', unsafe_allow_html=True)
                                    st.markdown(cold_email)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # Add download button
                                    st.download_button(
                                        label="Download Email",
                                        data=cold_email,
                                        file_name="cold_email.txt",
                                        mime="text/plain"
                                    )
                                else:
                                    st.markdown('<div class="error-box">Failed to generate cold email. Please try again.</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-box">Failed to extract job details. The URL might not contain a valid job posting or the format is not supported.</div>', unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
