import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

class JobScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def is_valid_url(self, url):
        """Check if the URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def extract_job_details(self, url):
        """Extract job details from the given URL"""
        if not self.is_valid_url(url):
            return None, "Invalid URL provided"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            return None, f"Failed to access URL: {str(e)}"
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Try to extract job title
        job_title = self._extract_job_title(soup)
        
        # Try to extract experience requirements
        experience = self._extract_experience(soup)
        
        # Try to extract technical skills
        technical_skills = self._extract_skills(soup, technical=True)
        
        # Try to extract non-technical skills
        non_technical_skills = self._extract_skills(soup, technical=False)
        
        # Try to extract company name
        company_name = self._extract_company_name(soup, url)
        
        job_details = {
            "job_title": job_title,
            "experience": experience,
            "technical_skills": technical_skills,
            "non_technical_skills": non_technical_skills,
            "company_name": company_name,
            "job_url": url
        }
        
        return job_details, None
    
    def _extract_job_title(self, soup):
        """Extract job title from the page"""
        # Common selectors for job titles
        selectors = [
            'h1.job-title', 
            'h1[class*="title"]', 
            'h1[class*="header"]',
            '.job-details h1',
            '#job-title',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text and len(text) < 100:  # Reasonable length for a job title
                    return text
        
        # Fallback: look for h1 tags that might contain job title
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            text = h1.get_text(strip=True)
            if text and len(text) < 100:
                return text
        
        return "Not specified"
    
    def _extract_experience(self, soup):
        """Extract experience requirements from the page"""
        # Look for experience-related text
        text = soup.get_text().lower()
        experience_patterns = [
            r'(\d+[\+\-\s]*\d*)\s*(years?|yrs?)',
            r'experience.*(\d+[\+\-\s]*\d*)',
            r'(\d+[\+\-\s]*\d*).*experience'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Return the first match
                if isinstance(matches[0], tuple):
                    return matches[0][0] + " years"
                else:
                    return matches[0] + " years"
        
        return "Not specified"
    
    def _extract_skills(self, soup, technical=True):
        """Extract skills from the page"""
        text = soup.get_text().lower()
        
        # Technical skills keywords
        technical_keywords = [
            'python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 
            'angular', 'vue', 'node', 'express', 'django', 'flask', 'php', 
            'ruby', 'rails', 'c#', 'c++', 'swift', 'kotlin', 'typescript',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 
            'git', 'ci/cd', 'devops', 'machine learning', 'ai', 'data science',
            'tableau', 'power bi', 'tensorflow', 'pytorch', 'nosql', 'mongodb',
            'postgresql', 'mysql', 'linux', 'unix'
        ]
        
        # Non-technical skills keywords
        non_technical_keywords = [
            'communication', 'teamwork', 'leadership', 'problem solving',
            'critical thinking', 'adaptability', 'time management', 'creativity',
            'collaboration', 'negotiation', 'presentation', 'public speaking',
            'project management', 'agile', 'scrum', 'analytical', 'strategic thinking',
            'customer service', 'interpersonal', 'mentoring', 'training'
        ]
        
        keywords = technical_keywords if technical else non_technical_keywords
        found_skills = []
        
        for skill in keywords:
            if skill in text:
                found_skills.append(skill)
        
        return found_skills if found_skills else ["Not specified"]
    
    def _extract_company_name(self, soup, url):
        """Extract company name from the page or URL"""
        # Try to get from common selectors
        selectors = [
            '.company-name', 
            '[class*="company"]', 
            '[class*="organization"]',
            '.employer', 
            '.hiring-company'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text:
                    return text
        
        # Try to get from meta tags
        meta_selectors = [
            'meta[property="og:site_name"]',
            'meta[name="twitter:site"]'
        ]
        
        for selector in meta_selectors:
            element = soup.select_one(selector)
            if element and element.get('content'):
                return element.get('content')
        
        # Fallback: extract from URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        if '.' in domain:
            domain = domain.split('.')[0]
        
        return domain.capitalize() if domain else "The company"
