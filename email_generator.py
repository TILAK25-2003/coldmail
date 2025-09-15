from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

def generate_cold_email(job_data, projects, profile_data, tone="Professional", length="Medium", focus="Skills"):
    """Generate a cold email based on job data, projects, and profile data"""
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
    
    # Format profile data for the prompt
    profile_text = ""
    if profile_data and profile_data.get('skills'):
        profile_text = "Candidate Skills:\n- " + "\n- ".join(profile_data['skills']) + "\n\n"
    
    if profile_data and profile_data.get('profiles'):
        if 'linkedin' in profile_data['profiles']:
            linkedin_data = profile_data['profiles']['linkedin']
            profile_text += "LinkedIn Summary:\n"
            if linkedin_data.get('experience'):
                profile_text += f"Experience: {linkedin_data['experience']}\n"
            if linkedin_data.get('education'):
                profile_text += f"Education: {linkedin_data['education']}\n"
        
        if 'github' in profile_data['profiles']:
            github_data = profile_data['profiles']['github']
            profile_text += "GitHub Summary:\n"
            if github_data.get('activity'):
                profile_text += f"Activity: {github_data['activity']}\n"
    
    # Create prompt template with customization options
    prompt_template = PromptTemplate.from_template(
        """
        You are an expert job seeker crafting a compelling cold email for a hiring manager.
        
        JOB DETAILS:
        - Role: {role}
        - Experience Required: {experience}
        - Key Skills: {skills}
        - Description: {description}
        
        {profile_text}
        
        {projects_text}
        
        ADDITIONAL INSTRUCTIONS:
        - Tone: {tone}
        - Length: {length}
        - Primary Focus: {focus}
        
        Create a professional cold email that:
        1. Introduces the candidate briefly
        2. Expresses genuine interest in the specific role
        3. Highlights relevant skills and experience that match the job requirements
        4. Mentions specific projects from the portfolio that demonstrate these skills
        5. Shows enthusiasm for the company/role
        6. Includes a polite call to action (request for interview)
        7. Has a professional tone but is not overly formal
        
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
    
    # Determine length guidance
    length_guidance = ""
    if length == "Concise":
        length_guidance = "Keep the email brief (150-200 words)"
    elif length == "Medium":
        length_guidance = "Make the email detailed but not too long (200-250 words)"
    else:  # Detailed
        length_guidance = "Provide comprehensive details (250-300 words)"
    
    # Create chain and generate email
    chain = prompt_template | llm
    response = chain.invoke({
        "role": job_data['role'],
        "experience": job_data['experience'],
        "skills": skills_text,
        "description": job_data['description'],
        "profile_text": profile_text,
        "projects_text": projects_text,
        "tone": tone,
        "length": length_guidance,
        "focus": focus
    })
    
    return response.content
