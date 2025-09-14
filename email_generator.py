from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

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
