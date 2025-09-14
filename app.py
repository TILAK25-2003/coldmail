import streamlit as st
from job_parser import extract_job_details
from portfolio_matcher import find_relevant_projects, SAMPLE_PORTFOLIO

# Define your actual portfolio projects - REPLACE WITH YOUR REAL PROJECTS
MY_PORTFOLIO = [
    {
        'name': 'E-commerce Website',
        'description': 'Full-stack e-commerce platform with React and Node.js handling user authentication, payment processing, and inventory management',
        'skills': ['React', 'Node.js', 'MongoDB', 'JavaScript', 'Express', 'REST API'],
        'url': 'https://github.com/yourusername/ecommerce'
    },
    {
        'name': 'Data Analysis Dashboard',
        'description': 'Interactive data visualization dashboard using Python, Pandas and Plotly for real-time analytics',
        'skills': ['Python', 'Pandas', 'Plotly', 'Data Analysis', 'Data Visualization', 'SQL'],
        'url': 'https://github.com/yourusername/data-dashboard'
    },
    {
        'name': 'Machine Learning Classifier',
        'description': 'Machine learning model for image classification using TensorFlow and Keras with 95% accuracy',
        'skills': ['Python', 'TensorFlow', 'Keras', 'Machine Learning', 'Deep Learning', 'NumPy'],
        'url': 'https://github.com/yourusername/ml-classifier'
    },
    {
        'name': 'Task Management App',
        'description': 'Mobile task management application built with React Native featuring offline capabilities and push notifications',
        'skills': ['React Native', 'JavaScript', 'Redux', 'Firebase', 'Mobile Development'],
        'url': 'https://github.com/yourusername/task-app'
    }
]

def main():
    st.set_page_config(page_title="ColdMail - Job Application Assistant", page_icon="💼")
    
    st.title("💼 ColdMail - Job Application Assistant")
    st.write("Analyze job postings and find relevant portfolio projects for your applications.")
    
    # Option to use sample portfolio or custom one
    use_custom_portfolio = st.checkbox("Use my custom portfolio", value=True)
    portfolio_to_use = MY_PORTFOLIO if use_custom_portfolio else SAMPLE_PORTFOLIO
    
    job_url = st.text_input("Enter job posting URL:", placeholder="https://example.com/job-posting")
    
    if st.button("Analyze Job Posting") and job_url:
        with st.spinner("Analyzing job posting and finding relevant projects..."):
            try:
                # Extract job details
                job_details = extract_job_details(job_url)
                job_description = job_details.get('description', '')
                job_title = job_details.get('title', 'Unknown Position')
                
                st.subheader(f"Job Analysis: {job_title}")
                
                if job_description:
                    st.text_area("Extracted Job Description", job_description, height=200)
                    
                    # Find relevant projects
                    relevant_projects = find_relevant_projects(job_description, portfolio_to_use)
                    
                    st.subheader("🎯 Relevant Portfolio Projects")
                    
                    if relevant_projects:
                        for i, project in enumerate(relevant_projects, 1):
                            with st.expander(f"Project {i}: {project['name']}"):
                                st.write(f"**Description:** {project['description']}")
                                st.write(f"**Skills:** {', '.join(project['skills'])}")
                                if project.get('url'):
                                    st.write(f"**URL:** {project['url']}")
                    else:
                        st.warning("No relevant portfolio projects found for this job description.")
                        
                else:
                    st.error("Could not extract job description from the URL.")
                    
            except Exception as e:
                st.error(f"Error processing job posting: {str(e)}")
    
    # Add some instructions
    with st.expander("ℹ️ How to use this tool"):
        st.write("""
        1. Paste the URL of any job posting
        2. The tool will extract the job description
        3. It will analyze your portfolio projects and find the most relevant ones
        4. Use these relevant projects to tailor your cover letter and resume
        5. Replace the sample portfolio with your actual projects in app.py
        """)

if __name__ == "__main__":
    main()
