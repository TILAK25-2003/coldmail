# job_parser.py (no API key required)
import requests
from bs4 import BeautifulSoup
import re

def extract_job_details(url):
    """Extract job details from a URL without using LLM"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        # Get clean text
        text = soup.get_text(separator='\n', strip=True)
        
        # Extract job title (common patterns)
        title = "Software Developer"
        title_patterns = [
            r'job title[:\s-]*([^\n]+)',
            r'position[:\s-]*([^\n]+)',
            r'role[:\s-]*([^\n]+)',
            r'<h1[^>]*>(.*?)</h1>',
            r'<title>(.*?)</title>'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                break
        
        # Extract skills (common tech keywords)
        common_skills = [
            'python', 'javascript', 'java', 'react', 'node', 'angular', 'vue',
            'html', 'css', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
            'aws', 'azure', 'docker', 'kubernetes', 'linux', 'git', 'rest',
            'api', 'machine learning', 'ai', 'tensorflow', 'pytorch'
        ]
        
        found_skills = []
        for skill in common_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                found_skills.append(skill.title())
        
        # If no skills found, use defaults
        if not found_skills:
            found_skills = ["Python", "JavaScript", "Problem Solving"]
        
        # Extract experience level
        experience = "2+ years"
        exp_patterns = [
            r'experience[:\s-]*([^\n]+)',
            r'years.*experience[:\s-]*([^\n]+)',
            r'(\d+[\+\-]*\s*years?)'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                experience = match.group(1).strip()
                break
        
        # Create description snippet
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        description = ". ".join(sentences[:2]) + "." if sentences else "Job description not available."
        
        if len(description) > 200:
            description = description[:197] + "..."
        
        return {
            "role": title,
            "experience": experience,
            "skills": found_skills[:8],  # Limit to top 8 skills
            "description": description
        }
        
    except Exception as e:
        print(f"Error extracting job details: {e}")
        # Return default data
        return {
            "role": "Software Developer",
            "experience": "2+ years",
            "skills": ["Python", "JavaScript", "Problem Solving"],
            "description": f"Position at {url}. Please refer to the original posting for complete details."
        }
