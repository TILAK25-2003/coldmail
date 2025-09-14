def generate_cold_email(your_name, company_name, hiring_manager, job_role, job_skills, relevant_projects, job_description, your_email, your_phone):
    """Generate a comprehensive cold email"""
    
    # Skills categorization
    tech_skills = [skill for skill in job_skills if skill in [
        'Python', 'JavaScript', 'Java', 'React', 'Node.js', 'SQL', 'HTML', 'CSS',
        'AWS', 'Docker', 'Kubernetes', 'Machine Learning', 'Data Analysis'
    ]]
    
    soft_skills = [skill for skill in job_skills if skill in [
        'Communication', 'Leadership', 'Teamwork', 'Problem Solving', 'Project Management'
    ]]
    
    # Projects section
    projects_text = ""
    if relevant_projects:
        projects_text = "I have successfully delivered projects that demonstrate these skills:\n"
        for proj in relevant_projects[:2]:
            projects_text += f"• {proj['name']}: {proj['
