# email_generator.py
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

def generate_cold_email(job_data, profile_skills, projects):
    """
    job_data: dict from extract_job_details
    profile_skills: list of user's extracted skills
    projects: list of projects (title, description, link) that matched
    Returns string email text.
    """
    groq_key = os.environ.get("GROQ_API_KEY")
    if not groq_key:
        raise RuntimeError("GROQ_API_KEY missing")

    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)

    projects_section = ""
    if projects:
        for i, p in enumerate(projects, 1):
            projects_section += f"{i}. {p.get('title')} — {p.get('link', '')}\n   {p.get('description','')}\n"

    prompt = PromptTemplate.from_template("""
    You are an expert career advisor writing a cold email for a candidate applying to a specific job.
    Use the following data and create:
    - a subject line
    - a short polite greeting
    - 3 short paragraphs: intro + relevant skills+projects + call-to-action
    - a professional sign-off
    Keep it ~180-260 words, confident but not pushy.

    JOB:
    Role: {role}
    Experience: {experience}
    Key skills: {skills}
    Description summary: {description}

    CANDIDATE (extracted):
    Skills: {profile_skills}
    Matched projects:
    {projects_section}

    Produce the email (subject + body). Do NOT include anything else.
    """)
    chain = prompt | llm
    resp = chain.invoke({
        "role": job_data.get("role",""),
        "experience": job_data.get("experience",""),
        "skills": ", ".join(job_data.get("skills", [])),
        "description": job_data.get("description",""),
        "profile_skills": ", ".join(profile_skills),
        "projects_section": projects_section
    })
    # resp.content contains the text result
    return resp.content
