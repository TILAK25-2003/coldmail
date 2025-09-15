# portfolio_parser.py
import requests
from bs4 import BeautifulSoup
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def _fetch_text_from_url(url, timeout=12):
    headers = {"User-Agent":"Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for s in soup(["script","style","noscript","iframe"]):
        s.decompose()
    return soup.get_text(separator="\n", strip=True)

def extract_profile_skills_and_projects(profile_url, source="linkedin"):
    """
    source: 'linkedin' or 'github'
    Returns { "skills": [...], "projects": [{title, description, link}] }
    """
    page_text = _fetch_text_from_url(profile_url)
    groq_key = os.environ.get("GROQ_API_KEY")
    if not groq_key:
        raise RuntimeError("GROQ_API_KEY missing")
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.0)

    prompt = PromptTemplate.from_template("""
    You will be given the visible text from a public {source} profile page.
    Extract:
    - skills: list of concise skills (both technical and non-technical)
    - projects: list of up to 8 projects with { "title": "...", "description": "...", "link": "..." }
    Output: JSON only, keys: skills, projects
    Page text:
    \"\"\"{page_text}\"\"\"
    """.format(source=source))

    chain = prompt | llm
    resp = chain.invoke({"page_text": page_text})

    parser = JsonOutputParser()
    try:
        parsed = parser.parse(resp.content)
    except Exception:
        # best-effort fallback
        import json
        text = resp.content
        start = text.find("{")
        end = text.rfind("}")
        try:
            parsed = json.loads(text[start:end+1])
        except:
            parsed = {"skills": [], "projects": []}

    parsed.setdefault("skills", [])
    parsed.setdefault("projects", [])
    # normalize project entries
    projects = []
    for p in parsed["projects"]:
        if isinstance(p, dict):
            projects.append({"title": p.get("title","Untitled"), "description": p.get("description",""), "link": p.get("link","")})
    parsed["projects"] = projects
    return parsed
