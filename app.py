# app.py
import os
import streamlit as st
from urllib.parse import urlparse

from job_parser import extract_job_details
from portfolio_parser import extract_profile_skills_and_projects
from email_generator import generate_cold_email
from difflib import SequenceMatcher

st.set_page_config(page_title="Cold Email Generator", layout="wide", page_icon="✉️")

# --- Sidebar: Groq API Key ---
st.sidebar.header("Configuration")
groq_key = st.sidebar.text_input("Groq API Key", type="password",
                                 help="Get an API key from https://console.groq.com/ and paste it here.")
if groq_key:
    os.environ["GROQ_API_KEY"] = groq_key

st.sidebar.markdown("---")
st.sidebar.info("""How it works:
1. Paste a job posting URL (technical or non-technical).
2. Paste your LinkedIn and GitHub public profile URLs.
3. Parse job and profiles, review autofilled skills/projects.
4. Generate a tailored cold email.
""")

# --- Main UI ---
st.title("Cold Email Generator")
st.markdown("Generate a personalized cold email for a job posting by matching the job requirements with your LinkedIn & GitHub profile.")

job_url = st.text_input("Job posting URL", placeholder="https://company.com/jobs/software-engineer-123")
linked_in = st.text_input("LinkedIn profile URL (public)", placeholder="https://www.linkedin.com/in/yourname")
github = st.text_input("GitHub profile URL (public)", placeholder="https://github.com/yourname")

col1, col2 = st.columns([1, 1])
with col1:
    parse_btn = st.button("Parse Job & Profiles", disabled=not groq_key)
with col2:
    generate_btn = st.button("Generate Cold Email", disabled=not groq_key)

# session storage
if "job" not in st.session_state:
    st.session_state.job = None
if "profile" not in st.session_state:
    st.session_state.profile = {"skills": [], "projects": []}
if "matched_projects" not in st.session_state:
    st.session_state.matched_projects = []
if "email" not in st.session_state:
    st.session_state.email = None

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and parsed.netloc != ""
    except:
        return False

# Parse button action
if parse_btn:
    # basic URL validation and pop-up for wrong URL
    if not (job_url and is_valid_url(job_url)):
        with st.modal("Invalid job URL"):
            st.error("The job URL you entered looks invalid. Please paste a full URL (starting with https://).")
    else:
        with st.spinner("Extracting job posting..."):
            try:
                job = extract_job_details(job_url)
                st.session_state.job = job
                st.success("Job parsed successfully.")
            except Exception as e:
                st.error(f"Failed to parse job: {e}")
                st.session_state.job = None

    # parse profiles if provided
    if linked_in and is_valid_url(linked_in):
        with st.spinner("Extracting LinkedIn profile..."):
            try:
                li_data = extract_profile_skills_and_projects(linked_in, source="linkedin")
                # merge skills and projects
                st.session_state.profile["skills"] = list(set(st.session_state.profile["skills"] + li_data.get("skills", [])))
                st.session_state.profile["projects"].extend(li_data.get("projects", []))
                st.success("LinkedIn profile parsed.")
            except Exception as e:
                st.warning(f"Could not parse LinkedIn: {e}")
    if github and is_valid_url(github):
        with st.spinner("Extracting GitHub profile..."):
            try:
                gh_data = extract_profile_skills_and_projects(github, source="github")
                st.session_state.profile["skills"] = list(set(st.session_state.profile["skills"] + gh_data.get("skills", [])))
                st.session_state.profile["projects"].extend(gh_data.get("projects", []))
                st.success("GitHub profile parsed.")
            except Exception as e:
                st.warning(f"Could not parse GitHub: {e}")

    # After parsing, attempt to auto-match skills -> show preview
    if st.session_state.job:
        job_skills = [s.lower() for s in st.session_state.job.get("skills", [])]
        matched = []
        for skill in st.session_state.profile["skills"]:
            # fuzzy match simple check
            for js in job_skills:
                ratio = SequenceMatcher(None, skill.lower(), js).ratio()
                if skill.lower() == js or ratio > 0.75 or js in skill.lower() or skill.lower() in js:
                    matched.append(skill)
        st.session_state.matched_projects = []
        # match projects that include matched skills in description
        for p in st.session_state.profile["projects"]:
            ptext = (p.get("title","") + " " + p.get("description","")).lower()
            for m in matched:
                if m.lower() in ptext:
                    st.session_state.matched_projects.append(p)
                    break

# Show parsed info on UI
st.markdown("### Parsed Job Details")
if st.session_state.job:
    st.write("**Role:**", st.session_state.job.get("role"))
    st.write("**Experience:**", st.session_state.job.get("experience"))
    st.write("**Key skills:**", ", ".join(st.session_state.job.get("skills", [])))
    st.write("**Description (summary):**", st.session_state.job.get("description"))
else:
    st.info("No job parsed yet. Click **Parse Job & Profiles** after entering valid URLs and your Groq API key.")

st.markdown("---")
st.markdown("### Extracted Profile Skills & Projects")
st.write("**Auto-extracted skills:**", ", ".join(st.session_state.profile.get("skills", [])) or "None")
if st.session_state.profile.get("projects"):
    for p in st.session_state.profile["projects"]:
        st.write(f"- {p.get('title')} — {p.get('link','')}")
else:
    st.info("No projects parsed yet.")

st.markdown("---")
st.markdown("### Matched projects (based on job skills)")
if st.session_state.matched_projects:
    for p in st.session_state.matched_projects:
        st.write(f"- {p.get('title')} — {p.get('link','')}")
else:
    st.info("No matching projects found yet. Make sure your profiles or projects mention the required skills.")

# Generate email action
if generate_btn:
    if not st.session_state.job:
        st.error("Please parse a valid job posting first.")
    else:
        with st.spinner("Generating cold email..."):
            try:
                email = generate_cold_email(
                    job_data=st.session_state.job,
                    profile_skills=st.session_state.profile["skills"],
                    projects=st.session_state.matched_projects
                )
                st.session_state.email = email
                st.success("Email generated.")
            except Exception as e:
                st.error(f"Email generation failed: {e}")

st.markdown("---")
st.markdown("### Generated Cold Email")
if st.session_state.email:
    st.code(st.session_state.email)
    st.download_button("Download email (.txt)", st.session_state.email, file_name="cold_email.txt")
else:
    st.info("No email yet. Generate one after parsing.")
