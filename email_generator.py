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
            projects_text += f"• {proj['name']}: {proj['description']}\n"
    else:
        projects_text = "My experience includes working on various projects that have honed my skills in these areas."
    
    email = f"""Subject: Application for {job_role} Position at {company_name}

Dear {hiring_manager},

I am writing to express my enthusiastic interest in the {job_role} position at {company_name}. After reviewing your job description, I am confident that my skills and experience align perfectly with your requirements.

Your posting emphasizes the need for expertise in {', '.join(tech_skills[:3]) if tech_skills else 'key technical areas'} as well as strong {', '.join(soft_skills[:2]) if soft_skills else 'professional'} skills. 

{projects_text}

Some key strengths I would bring to {company_name} include:

• Technical Proficiency: {', '.join(tech_skills[:5]) if tech_skills else 'Relevant technical expertise'}
• Professional Skills: {', '.join(soft_skills[:3]) if soft_skills else 'Strong professional capabilities'}
• Proven track record of delivering results in similar roles

I am particularly impressed by {company_name}'s work in the industry and would be thrilled to contribute to your team's success.

I would welcome the opportunity to discuss how my skills and experience can benefit {company_name}. Thank you for considering my application.

Best regards,
{your_name}
Email: {your_email}
Phone: {your_phone}
LinkedIn: linkedin.com/in/{your_name.replace(' ', '').lower()}

P.S. I have attached my resume for your review and would be happy to provide references upon request.
"""

    return email
