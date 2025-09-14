def generate_cold_email(your_name, company_name, hiring_manager, job_role, 
                       technical_skills, soft_skills, relevant_projects, experience_required):
    """Generate a comprehensive cold email"""
    
    # Format skills
    tech_skills_str = ', '.join(technical_skills[:5]) if technical_skills else "relevant technologies"
    soft_skills_str = ', '.join(soft_skills[:3]) if soft_skills else "key soft skills"
    
    # Format projects
    if relevant_projects:
        projects_text = "\n".join([
            f"- {proj['name']}: {proj['description']}" 
            for proj in relevant_projects[:2]
        ])
    else:
        projects_text = "I have successfully delivered projects that demonstrate my capabilities in similar domains."
    
    email = f"""Subject: Application for {job_role} Position at {company_name}

Dear {hiring_manager},

I am writing to express my enthusiastic interest in the {job_role} position at {company_name}. With {experience_required if experience_required != 'Not specified' else 'extensive'} experience and a proven track record in similar roles, I am confident in my ability to contribute significantly to your team.

My technical expertise includes {tech_skills_str}, complemented by strong {soft_skills_str}. I have successfully delivered projects such as:
{projects_text}

What particularly excites me about the opportunity at {company_name} is [mention something specific about the company if known - their mission, recent achievements, or projects].

My experience aligns well with your requirements:
- Technical proficiency in {tech_skills_str}
- Strong {soft_skills_str} for effective collaboration
- Proven ability to deliver results in dynamic environments

I am impressed by {company_name}'s [mention something positive - innovation, culture, market position] and would be thrilled to contribute to your continued success.

I would welcome the opportunity to discuss how my skills and experience can benefit {company_name}. Thank you for considering my application.

Best regards,
{your_name}
{your_name.replace(' ', '').lower()}@email.com
+1 (555) 123-4567
LinkedIn: linkedin.com/in/{your_name.replace(' ', '').lower()}

P.S. I've been following {company_name}'s work in [industry/field] and am particularly impressed by [specific achievement or aspect]."""
    
    return email
