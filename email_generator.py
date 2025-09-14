# email_generator.py (no API key required)
import random

def generate_cold_email(job_data, projects):
    """Generate a cold email using templates instead of AI"""
    
    # Email templates
    templates = [
        {
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
        },
        {
            "subject": "Interest in {role} Role",
            "greeting": "Hello,",
            "body": """
I was thrilled to see the opening for a {role} at your company. 
With my background in {skills} and {experience} of professional experience, I'm confident I can excel in this role.

Some of my relevant work includes:
{projects}

{description}

I would be delighted to discuss how my expertise aligns with your needs. Thank you for considering my application.
""",
            "closing": "Best regards,\n[Your Name]\n[Your Portfolio URL]\n[Your Email]"
        },
        {
            "subject": "{role} Application - [Your Name]",
            "greeting": "Dear Hiring Team,",
            "body": """
I am applying for the {role} position with enthusiasm. 
My {experience} working with {skills} has prepared me to make significant contributions to your organization.

Highlights of my relevant experience:
{projects}

{description}

I look forward to the possibility of discussing this opportunity further with you.
""",
            "closing": "Respectfully,\n[Your Name]\n[Your LinkedIn Profile]\n[Your Phone Number]"
        }
    ]
    
    # Select a random template
    template = random.choice(templates)
    
    # Format skills
    skills_text = ", ".join(job_data['skills']) if isinstance(job_data['skills'], list) else job_data['skills']
    
    # Format projects
    projects_text = ""
    if projects:
        projects_text = "\n".join([f"• {p['document']} - {p['metadata']['links']}" for p in projects])
    else:
        projects_text = "• Various projects demonstrating proficiency in the required skills"
    
    # Fill in the template
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
