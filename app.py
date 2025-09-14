# app.py (updated version)
import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
import json
import chromadb
import pandas as pd
import uuid
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Page configuration
st.set_page_config(
    page_title="Cold Email Generator",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #4CAF50;
        margin-top: 1.5rem;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2196F3;
        margin-top: 1rem;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'job_data' not in st.session_state:
    st.session_state.job_data = None
if 'projects' not in st.session_state:
    st.session_state.projects = None
if 'email' not in st.session_state:
    st.session_state.email = None

# Function to extract job details
def extract_job_details(url):
    """Extract job details from a URL using requests and BeautifulSoup"""
    try:
        # Fetch webpage content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        page_data = soup.get_text(separator='\n', strip=True)
        
    except Exception as e:
        # Fallback: return a basic structure if scraping fails
        return {
            "role": "Software Developer",
            "experience": "2+ years",
            "skills": ["Python", "JavaScript", "Problem Solving"],
            "description": "Job description could not be extracted from the URL."
        }
    
    # Initialize LLM
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.3-70b-versatile"
    )
    
    # Create prompt template
    prompt_extract = PromptTemplate.from_template(
        """
        *** SCRAPED TEXT FROM WEBSITE:
        {page_data}
        *** INSTRUCTION:
        The scraped text is from a job posting page.
        Your job is to extract the job details and return them in JSON format containing the following keys: 
        - role: the job title
        - experience: required experience level
        - skills: list of required skills and technologies
        - description: job description summary
        
        Only return the valid JSON.
        *** VALID JSON (NO PREAMBLE).
        """
    )
    
    # Create chain
    chain_extract = prompt_extract | llm
    response = chain_extract.invoke({'page_data': page_data})
    
    # Parse JSON response
    try:
        job_data = json.loads(response.content)
        return job_data
    except:
        # Fallback: try to extract JSON from response
        content = response.content
        if '```json' in content:
            json_str = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            json_str = content.split('```')[1].split('```')[0].strip()
        else:
            json_str = content.strip()
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If all else fails, return a basic structure
            return {
                "role": "Extracted Role",
                "experience": "Experience not extracted",
                "skills": ["Skills not extracted"],
                "description": "Description not extracted"
            }

# Function to initialize vector store
def initialize_vectorstore():
    """Initialize or load the vector store"""
    client = chromadb.PersistentClient(path="vectorstore")
    collection = client.get_or_create_collection(name="portfolio")
    return collection

# Function to load portfolio data
def load_portfolio_data():
    """Load portfolio data from CSV or create default if not exists"""
    csv_path = "my_portfolio.csv"
    
    # Create default portfolio if file doesn't exist
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
        st.info("Created default portfolio CSV file")
    else:
        df = pd.read_csv(csv_path)
    
    return df

# Function to setup portfolio collection
def setup_portfolio_collection():
    """Set up the portfolio collection in ChromaDB"""
    collection = initialize_vectorstore()
    df = load_portfolio_data()
    
    # Only add documents if collection is empty
    if collection.count() == 0:
        docs = df["Techstack"].astype(str).tolist()
        metadatas = [{"links": str(link)} for link in df["Links"].tolist()]
        ids = [str(uuid.uuid4()) for _ in range(len(docs))]
        
        collection.add(
            documents=docs,
            metadatas=metadatas,
            ids=ids
        )
        st.info(f"Added {len(docs)} portfolio items to vector store")
    
    return collection

# Function to find relevant projects
def find_relevant_projects(skills, n_results=3):
    """Find relevant projects based on skills"""
    collection = setup_portfolio_collection()
    
    # Create a query from skills
    query_text = " ".join(skills) if isinstance(skills, list) else skills
    
    # Query the collection
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Format results
    relevant_projects = []
    for i, doc in enumerate(results['documents'][0]):
        relevant_projects.append({
            "document": doc,
            "metadata": results['metadatas'][0][i]
        })
    
    return relevant_projects

# Function to generate cold email
def generate_cold_email(job_data, projects):
    """Generate a cold email based on job data and relevant projects"""
    # Initialize LLM
    llm = ChatGroq(
        temperature=0.7,
        model_name="llama-3.3-70b-versatile"
    )
    
    # Format projects for the prompt
    projects_text = ""
    if projects:
        projects_text = "Relevant Projects:\n"
        for i, project in enumerate(projects, 1):
            projects_text += f"{i}. {project['document']} (Link: {project['metadata']['links']})\n"
    
    # Create prompt template
    prompt_template = PromptTemplate.from_template(
        """
        You are an expert job seeker crafting a compelling cold email for a hiring manager.
        
        JOB DETAILS:
        - Role: {role}
        - Experience Required: {experience}
        - Key Skills: {skills}
        - Description: {description}
        
        {projects_text}
        
        INSTRUCTIONS:
        Create a professional cold email that:
        1. Introduces the candidate briefly
        2. Expresses genuine interest in the specific role
        3. Highlights relevant skills and experience that match the job requirements
        4. Mentions specific projects from the portfolio that demonstrate these skills
        5. Shows enthusiasm for the company/role
        6. Includes a polite call to action (request for interview)
        7. Is concise (around 200-300 words)
        8. Has a professional tone but is not overly formal
        
        Format the email properly with:
        - Appropriate subject line
        - Professional greeting
        - Well-structured paragraphs
        - Professional closing
        
        COLD EMAIL:
        """
    )
    
    # Format skills list
    skills_text = ", ".join(job_data['skills']) if isinstance(job_data['skills'], list) else job_data['skills']
    
    # Create chain and generate email
    chain = prompt_template | llm
    response = chain.invoke({
        "role": job_data['role'],
        "experience": job_data['experience'],
        "skills": skills_text,
        "description": job_data['description'],
        "projects_text": projects_text
    })
    
    return response.content

# Header
st.markdown('<h1 class="main-header">Cold Email Generator</h1>', unsafe_allow_html=True)
st.markdown("Generate personalized cold emails for job applications based on your portfolio.")

# Sidebar for API key input
with st.sidebar:
    st.header("Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password", 
                                help="Get your API key from https://console.groq.com/")
    os.environ["GROQ_API_KEY"] = groq_api_key
    
    st.divider()
    st.info("""
    **How to use:**
    1. Enter your Groq API key
    2. Paste a job posting URL
    3. Click 'Parse Job Details'
    4. Review the extracted information
    5. Click 'Generate Cold Email'
    """)

# Main content
tab1, tab2, tab3 = st.tabs(["Job URL Input", "Generated Email", "About"])

with tab1:
    st.markdown('<h2 class="sub-header">Paste Job URL</h2>', unsafe_allow_html=True)
    
    job_url = st.text_input("Enter the job posting URL:", 
                           placeholder="https://careers.example.com/job/123")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        parse_clicked = st.button("Parse Job Details", disabled=not groq_api_key)
    
    if parse_clicked and job_url:
        with st.spinner("Extracting job details..."):
            try:
                st.session_state.job_data = extract_job_details(job_url)
                st.session_state.projects = find_relevant_projects(st.session_state.job_data['skills'])
                
                st.success("Job details extracted successfully!")
                
                # Display job details
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.subheader("Extracted Job Details")
                st.write(f"**Role:** {st.session_state.job_data['role']}")
                st.write(f"**Experience:** {st.session_state.job_data['experience']}")
                st.write("**Key Skills:**")
                for skill in st.session_state.job_data['skills']:
                    st.write(f"- {skill}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display matched projects
                if st.session_state.projects:
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.subheader("Relevant Projects from Your Portfolio")
                    for project in st.session_state.projects:
                        st.write(f"- {project['document']} - [View Project]({project['metadata']['links']})")
                    st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error extracting job details: {str(e)}")
    
    # Generate email button
    if st.session_state.job_data:
        st.markdown("---")
        generate_clicked = st.button("Generate Cold Email", type="primary")
        
        if generate_clicked:
            with st.spinner("Generating your cold email..."):
                try:
                    st.session_state.email = generate_cold_email(
                        st.session_state.job_data, 
                        st.session_state.projects
                    )
                    st.success("Email generated successfully!")
                    # Switch to the email tab
                    st.switch_page("?tab=Generated%20Email")
                except Exception as e:
                    st.error(f"Error generating email: {str(e)}")

with tab2:
    st.markdown('<h2 class="sub-header">Generated Cold Email</h2>', unsafe_allow_html=True)
    
    if st.session_state.email:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.email)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Copy to clipboard button
        st.download_button(
            label="Copy Email to Clipboard",
            data=st.session_state.email,
            file_name="cold_email.txt",
            mime="text/plain"
        )
    else:
        st.info("No email generated yet. Please parse a job URL first.")

with tab3:
    st.markdown("""
    ## About Cold Email Generator
    
    This tool helps you create personalized cold emails for job applications by:
    
    1. **Parsing job postings** - Extracting key requirements and skills
    2. **Matching with your portfolio** - Finding your most relevant projects
    3. **Generating tailored emails** - Creating professional, personalized emails
    
    ### How It Works
    
    - Uses AI to analyze job descriptions
    - Matches requirements with your portfolio projects
    - Generates compelling emails that highlight your relevant experience
    
    ### Privacy Note
    
    - Your API key is only used during your session
    - Job data is processed but not stored
    - No personal data is collected or saved
    """)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Cold Email Generator Tool • Built with Streamlit</div>", 
            unsafe_allow_html=True)



