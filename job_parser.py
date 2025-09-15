# job_parser.py
import requests
from bs4 import BeautifulSoup
import json
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def fetch_page_text(url, timeout=12):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36"
    }
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    # remove scripts/styles
    for s in soup(["script", "style", "noscript", "iframe"]):
        s.decompose()
    return soup.get_text(separator="\n", strip=True)

def extract_job_details(url):
    # fetch page text; raise exceptions up to caller for UI popup
    page_text = fetch_page_text(url)

    # build LLM
    groq_key = os.environ.get("GROQ_API_KEY")
    if not groq_key:
        raise RuntimeError("GROQ_API_KEY not found in environment. Set it in Streamlit sidebar.")
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.0)

    prompt_template = PromptTemplate.from_template("""
    You are an assistant that extracts structured fields from job postings.
    Input: raw scraped job posting text delimited by triple quotes.
    Output: JSON only (no explanation). Schema:
    {
      "role": "<job title>",
      "experience": "<experience required>",
      "skills": ["skill1", "skill2", ...],
      "description": "<short 2-3 sentence summary>",
      "relevant_projects_hint": ["project-type-1", "project-type-2"]
    }
    Scraped text:
    \"\"\"{page_text}\"\"\"
    """)
    chain = prompt_template | llm
    resp = chain.invoke({"page_text": page_text})

    # parse JSON robustly
    parser = JsonOutputParser()
    try:
        parsed = parser.parse(resp.content)
    except Exception:
        # fallback: try to load JSON via heuristics
        text = resp.content
        # pick first {...} block
        start = text.find("{")
        end = text.rfind("}")
        try:
            parsed = json.loads(text[start:end+1])
        except Exception:
            # graceful fallback
            parsed = {
                "role": "Unknown",
                "experience": "Not specified",
                "skills": [],
                "description": "Could not extract a summary.",
                "relevant_projects_hint": []
            }

    # normalize keys
    parsed.setdefault("skills", [])
    parsed.setdefault("description", "")
    parsed.setdefault("role", parsed.get("role", "Unknown"))
    parsed.setdefault("experience", parsed.get("experience", "Not specified"))
    return parsed
