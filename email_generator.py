def generate_cold_email(your_name, company_name, hiring_manager, job_role, job_skills, relevant_projects, job_description):
    """Generate a cold email based on job details"""
    
    # Skills string
    skills_str = ', '.join(job_skills) if job_skills else "various technologies"
    
    # Projects string
    if relevant_projects:
        projects_text = "\n".join([
            f"- {proj['name']}: {proj['description']}" 
            for proj in relevant_projects[:2]  # Max 2 projects
        ])
    else:
        projects_text = "I have worked on several relevant projects that demonstrate my capabilities."
    
    email = f"""Subject: Application for {job_role} Position at {company_name}

Dear {hiring_manager},

I am writing to express my interest in the {job_role} position at {company_name}. I was excited to see your posting and believe my skills and experience align well with your requirements.

I have experience with {skills_str} and have successfully delivered projects such as:
{projects_text}

From your job description, I understand you're looking for someone with expertise in {skills_str}. My background includes:

- Developing solutions using {skills_str}
- Collaborating with cross-functional teams
- Delivering high-quality software on time

I am particularly impressed by {company_name}'s work and would be thrilled to contribute to your team.

I would welcome the opportunity to discuss how my skills can benefit {company_name}. Thank you for considering my application.

Best regards,
{your_name}
{your_name.replace(' ', '').lower()}@email.com
+1 (555) 123-4567
LinkedIn: linkedin.com/in/{your_name.replace(' ', '').lower()}
"""

    return email
