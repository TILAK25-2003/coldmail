# scraper.py
import requests
from bs4 import BeautifulSoup
import re

class SimpleScraper:
    """
    Conservative scraper: tries to fetch the URL, extracts title, meta description,
    and heuristically extracts role, experience, skills and company name.
    If fetching fails (no internet / blocked), returns a helpful fallback dict.
    """

    USER_AGENT = "Mozilla/5.0 (compatible; COLDFLOW-bot/1.0)"

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _extract_skills_from_text(self, text: str) -> str:
        # Simple heuristic: look for "skills", "requirements", "must have" sections
        # and return the first few comma-separated tokens found.
        text_lower = text.lower()
        patterns = [
            r"(skills[:\s]*)([^\n\r]{20,400})",
            r"(requirements[:\s]*)([^\n\r]{20,400})",
            r"(responsibilities[:\s]*)([^\n\r]{20,400})"
        ]
        for p in patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                fragment = m.group(2)
                # take up to first 200 chars and try to extract comma separated skills
                fragment = fragment[:300]
                # remove html-like leftovers
                fragment = re.sub(r'<[^>]+>', '', fragment)
                # try to pull tokens
                tokens = re.split(r'[,\n••\-\•]', fragment)
                tokens = [t.strip() for t in tokens if len(t.strip()) > 1]
                if tokens:
                    return ", ".join(tokens[:10])
        # fallback: try to find common language names
        languages = ["python", "javascript", "java", "c++", "c#", "sql", "react", "node", "aws", "docker"]
        found = [w for w in languages if w in text_lower]
        return ", ".join(found) if found else ""

    def scrape_job_info(self, url: str) -> dict:
        if not url:
            return {"error": "No URL provided."}
        headers = {"User-Agent": self.USER_AGENT}
        try:
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code != 200:
                return {"error": f"HTTP {resp.status_code} when requesting the URL."}
            html = resp.text
            soup = BeautifulSoup(html, "html.parser")

            # Title and meta description
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            meta_desc = ""
            md = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
            if md and md.get("content"):
                meta_desc = md.get("content").strip()

            # Join visible text for heuristics
            texts = soup.stripped_strings
            page_text = " ".join(list(texts))[:50000]  # limit length

            # heuristics
            role = title or re.search(r'([\w\s\-\|:]{3,80}?) at ', page_text) and (title) or ""
            # try to find company
            company = ""
            # look for "at <Company>" patterns
            m_co = re.search(r'at\s+([A-Z][A-Za-z0-9&\-\s]{2,50})', page_text)
            if m_co:
                company = m_co.group(1).strip()

            experience = ""
            m_exp = re.search(r'(\d+\+?\s*(?:years|yrs|year))', page_text, re.IGNORECASE)
            if m_exp:
                experience = m_exp.group(1)

            skills = self._extract_skills_from_text(page_text)
            description = meta_desc or page_text[:2000]

            # make fallback minimal if nothing found
            job_data = {
                "role": role or "Job Position",
                "experience": experience or "Not specified",
                "skills": skills or "Not specified",
                "description": self._clean_text(description),
                "company": company or ""
            }
            return job_data

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}. You may be offline or the site blocked requests."}
        except Exception as e:
            return {"error": f"Unexpected scraping error: {e}"}
