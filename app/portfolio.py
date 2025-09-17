# portfolio.py
import pandas as pd
from difflib import SequenceMatcher
from typing import List, Dict, Any

class Portfolio:
    """
    Simple portfolio manager that loads a DataFrame (or fallback sample)
    and returns relevant portfolio links based on skill-string similarity.
    """

    def __init__(self, file_path: str = None):
        """
        If file_path is given, it should be a CSV with columns:
        'Techstack' and 'Links' (optionally 'Title' and 'Description').
        Otherwise a small built-in sample dataset is used.
        """
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
            except Exception:
                self.data = self._sample_data()
        else:
            self.data = self._sample_data()
        # Ensure expected columns exist
        if "Techstack" not in self.data.columns or "Links" not in self.data.columns:
            self.data = self._sample_data()

    def _sample_data(self) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "Title": "Personal Portfolio - Python & Web",
                "Techstack": "Python, FastAPI, Flask, JavaScript, React, SQL, Docker",
                "Description": "Fullstack apps, REST APIs and microservices.",
                "Links": "https://example.com/portfolio-python"
            },
            {
                "Title": "Data Analysis Projects",
                "Techstack": "Python, Pandas, NumPy, Scikit-learn, Tableau",
                "Description": "Data cleaning, EDA and ML models.",
                "Links": "https://example.com/portfolio-data"
            },
            {
                "Title": "Business Development Case Studies",
                "Techstack": "Sales, Negotiation, CRM, Outreach, Lead Gen",
                "Description": "Generated qualified leads and closed deals.",
                "Links": "https://example.com/portfolio-bizdev"
            },
            {
                "Title": "UI/UX & Design",
                "Techstack": "Figma, Prototyping, User Research, Design Systems",
                "Description": "Design deliverables and case studies.",
                "Links": "https://example.com/portfolio-design"
            }
        ])

    @staticmethod
    def _similar(a: str, b: str) -> float:
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def query_links(self, skills: str, top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Given a comma/space separated skills string, return a list of
        relevant portfolio items with a similarity score in [0,1].
        """
        if not skills:
            return []

        # Normalize input into a single string
        skill_text = skills if isinstance(skills, str) else " ".join(skills)

        results = []
        for _, row in self.data.iterrows():
            techstack = str(row.get("Techstack", ""))
            # compute best similarity across the two strings
            sim = self._similar(skill_text, techstack)
            results.append({
                "title": row.get("Title", techstack),
                "links": row.get("Links", ""),
                "techstack": techstack,
                "description": row.get("Description", ""),
                "similarity": sim
            })

        results = sorted(results, key=lambda x: x["similarity"], reverse=True)
        return results[:top_n]
