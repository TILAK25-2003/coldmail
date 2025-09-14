# app.py (final with Groq API support)
import streamlit as st
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import re
from groq import Groq

# ----- Portfolio Matcher Functions -----
def load_portfolio_data():
    """Load portfolio data from CSV or create default if not exists"""
    csv_path = "my_portfolio.csv"
    
    if not os.path.exists(csv_path):
        default_data = {
            "Techstack": [
                "React, Node.js, MongoDB",
                "Python, Django, PostgreSQL",
                "Java, Spring Boot, MySQL",
                "JavaScript, React, Node.js",
                "Python, Machine Learning, TensorFlow",
                "AWS, Docker, Kubernetes",
                "React Native, Firebase, JavaScript",
                "Vue.js, Express, MongoDB"
            ],
            "Links": [
                "https://example.com/react-project",
                "https://example.com/python-project",
                "https://example.com/java-project",
                "https://example.com/js-project",
                "https://example.com/ml-project",
                "https://example.com/devops-project",
                "https://example.com/mobile-project",
                "https://example.com/vue-project"
            ]
        }
        df = pd.DataFrame(default_data)
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path)
    
    return df

def find_relevant_projects(skills, n_results=3):
    """Find relevant projects based on skills using simple text matching"""
    try:
        df = load_portfolio_data()
        
        if isinstance(skills, str):
            skills = [skill.strip() for skill in skills.split(',')]
        
        scored_projects = []
        for _, row in df.iterrows():
            score = 0
            techstack = str(row['Techstack']).lower()
            
            for skill in skills:
                skill_lower = str(skill).lower().strip()
                if skill_lower in techstack:
                    score += 3
                elif any(skill_lower in word for word in techstack.split()):
                    score += 1
            
            scored_projects.append({
                'score': score,
                'document': row['Techstack'],
                'metadata': {'links': row['Links']}
            })
        
        scored_projects.sort(key=lambda x: x['score'], reverse=True)
        top_projects = scored_projects[:n_results]
        
        return [{"document": p['document'], "metadata": p['metadata']} for p in top_projects]
        
    except Exception:
        return [
            {"document": "Python, Django, PostgreSQL", "metadata": {"links": "https://example.com/python-project"}},
            {"document": "React, Node.js, MongoDB", "metadata": {"links": "https://example.com/react-project"}}
        ]

# ----- Job Parser Functions -----
def extract_job_details(url):
    """Extract job details from a URL without using LLM"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        text = soup.get_text(separator='\n', strip=True)
        
        title = "Software Developer"
        title_patterns = [
            r'job title[:\s-]*([^\n]+)',
            r'position[:\s-]*([^\n]+)',
            r'role[:\s-]*([^\n]+)'
        ]
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                break
        
        common_skills = [
            'python', 'javascript', 'java', 'react', 'node', 'angular', 'vue',
            'html', 'css', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
            'aws', 'azure', 'docker', 'kubernetes', 'linux', 'git', 'rest',
            'api', 'machine learning', 'ai', 'tensorflow', 'pytorch'
        ]
        found_skills = [s.title() for s in common_skills if re.search(r'\b' + re.escape(s) + r'\b', text, re.IGNORECASE)]
        if not found_skills:
            found_skills = ["Python", "JavaScript", "Problem Solving"]
        
        experience = "2+ years"
        exp_patterns = [
            r'(\d+[\+\-]*\s*years?)',
            r'(\d+)\+?\s*yrs'
        ]
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                experience = match.group(1).strip()
                break
        
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        description = ". ".join(sentences[:2]) + "." if sentences else "Job description not available."
        if len(description) > 200:
            description = description[:197] + "..."
        
        return {
            "role": title,
            "experience": experience,
            "skills": found_skills[:8],
            "description": description
        }
        
    except Exception:
        return {
            "role": "Software Developer",
            "experience": "2+ years",
            "skills": ["Python", "JavaScript", "Problem Solving"],
            "description": f"Position at {url}. Please refer to the posting for details."
        }

# ----- Email Generators -----
def generate_cold_email(job_data, projects):
    """Template-based fallback email generator"""
    template = {
        "subject": "Application for {role} Position",
        "greeting": "Dear Hiring Manager,",
        "body": """
I am writing to express my interest in the {role} position at your company. 
With {experience} of experience in {skills}, I believe I possess the qualifications you're seeking.

My relevant experience includes:
{projects}

{description}

I am excited about the opportunity to contribute to your team and would welcome the chance to discuss how my skills can benefit your organization.
""",
        "closing": "Sincerely,\n[Your Name]\n[Your Phone Number]\n[Your Email]"
    }
    
    skills_text = ", ".join(job_data['skills']) if isinstance(job_data['skills'], list) else job_data['skills']
    projects_text = "\n".join([f"• {p['document']} - {p['metadata']['links']}" for p in projects]) if projects else "• Various projects demonstrating proficiency in the required skills"
    
    email = f"Subject: {template['subject'].format(role=job_data['role'])}\n\n"
    email += f"{template['greeting']}\n\n"
    email += template['body'].format(
        role=job_data['role'],
        experience=job_data['experience'],
        skills=skills_text,
        projects=projects_text,
        description=job_data['description']
    )
    email += f"\n\n{template['closing']}"
    return email

def generate_email_with_groq(job_data, projects, groq_key):
    """LLM-powered email using Groq API"""
    try:
        client = Groq(api_key=groq_key)

        prompt = f"""
        Write a professional cold email for a job application.

        Role: {job_data['role']}
        Experience: {job_data['experience']}
        Skills: {", ".join(job_data['skills'])}
        Job Description: {job_data['description']}

        Relevant Projects:
        {chr(10).join([f"- {p['document']} ({p['metadata']['links']})" for p in projects])}

        Include:
        - Subject line
        - Proper greeting
        - Body paragraph
        - Closing with placeholders for my name/contact
        """

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message["content"].strip()

    except Exception as e:
        st.error(f"Groq API error: {str(e)}")
        return None

# ----- Streamlit App -----
st.set_page_config(page_title="Cold Email Generator", page_icon="✉️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 3rem;color: #1E88E5;text-align: center;margin-bottom: 2rem;}
    .sub-header {font-size: 1.5rem;color: #0D47A1;margin-top: 1.5rem;margin-bottom: 1rem;}
    .success-box {background-color: #E8F5E9;padding: 1.5rem;border-radius: 0.5rem;
                  border-left: 5px solid #4CAF50;margin-top: 1.5rem;}
    .info-box {background-color: #E3F2FD;padding: 1rem;border-radius: 0.5rem;
               border-left: 5px solid #2196F3;margin-top: 1rem;}
    .stButton button {background-color: #1E88E5;color: white;font-weight: bold;width: 100%;}
</style>
""", unsafe_allow_html=True)

# Init session state
for key in ["job_data", "projects", "email", "groq_key"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Header
st.markdown('<h1 class="main-header">Cold Email Generator</h1>', unsafe_allow_html=True)
st.markdown("Generate personalized cold emails for job applications based on your portfolio.")

# Sidebar
with st.sidebar:
    st.header("Settings")
    groq_key = st.text_input("Groq API Key", type="password", placeholder="sk-...")
    st.session_state.groq_key = groq_key if groq_key else None
    use_groq = st.checkbox("Use Groq AI for Email", value=False)
    
    st.divider()
    st.info("""
    **Instructions:**
    1. Paste a job posting URL
    2. (Optional) Enter Groq API key & check box
    3. Parse job details & generate email
    """)

# Tabs
tab1, tab2, tab3 = st.tabs(["Job URL Input", "Generated Email", "About"])

with tab1:
    st.markdown('<h2 class="sub-header">Paste Job URL</h2>', unsafe_allow_html=True)
    job_url = st.text_input("Enter the job posting URL:", placeholder="https://careers.example.com/job/123")
    
    if st.button("Parse Job Details") and job_url:
        with st.spinner("Extracting job details..."):
            st.session_state.job_data = extract_job_details(job_url)
            st.session_state.projects = find_relevant_projects(st.session_state.job_data['skills'])
            st.success("Job details extracted successfully!")
            
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.subheader("Extracted Job Details")
            st.write(f"**Role:** {st.session_state.job_data['role']}")
            st.write(f"**Experience:** {st.session_state.job_data['experience']}")
            st.write("**Key Skills:**")
            for skill in st.session_state.job_data['skills']:
                st.write(f"- {skill}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.session_state.projects:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.subheader("Relevant Projects from Your Portfolio")
                for p in st.session_state.projects:
                    st.write(f"- {p['document']} - [View Project]({p['metadata']['links']})")
                st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.job_data:
        st.markdown("---")
        if st.button("Generate Cold Email", type="primary"):
            with st.spinner("Generating your cold email..."):
                if use_groq and st.session_state.groq_key:
                    email = generate_email_with_groq(st.session_state.job_data, st.session_state.projects, st.session_state.groq_key)
                else:
                    email = generate_cold_email(st.session_state.job_data, st.session_state.projects)
                
                if email:
                    st.session_state.email = email
                    st.success("Email generated successfully! Check the 'Generated Email' tab.")

with tab2:
    st.markdown('<h2 class="sub-header">Generated Cold Email</h2>', unsafe_allow_html=True)
    if st.session_state.email:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.text(st.session_state.email)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.download_button("Download Email as TXT", st.session_state.email, file_name="cold_email.txt", mime="text/plain")
    else:
        st.info("No email generated yet. Please parse a job URL first.")

with tab3:
    st.markdown("""
    ## About Cold Email Generator
    
    This tool helps you create personalized cold emails for job applications by:
    - Parsing job postings with regex
    - Matching with your portfolio projects
    - Generating tailored emails (with or without Groq AI)
    
    ### Modes
    - **Default Mode**: Uses template-based emails (no API key required)
    - **Groq Mode**: Uses LLM (requires API key)
    
    ### Privacy
    - All processing is local except optional Groq calls
    - No personal data is stored
    """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Cold Email Generator • Built with Streamlit</div>", unsafe_allow_html=True)




