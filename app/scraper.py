# scraper.py
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class SimpleScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _extract_company_from_url(self, url):
        """Extract company name from URL"""
        try:
            domain = urlparse(url).netloc
            company_name = domain.split('.')[-2]  # Get second-level domain
            return company_name.title()
        except:
            return "The Company"
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces
        text = re.sub(r'\n+', ' ', text)   # Replace newlines
        return text.strip()
    
    def _extract_role(self, soup, url):
        """Extract job role from page content"""
        # Common selectors for job titles
        role_selectors = [
            'h1[class*="job"][class*="title"]',
            'h1[class*="position"][class*="title"]',
            '.job-title',
            '.position-title',
            '[data-cy="job-title"]',
            'h1',
            'title'
        ]
        
        for selector in role_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = self._clean_text(element.get_text())
                if text and len(text) > 5 and len(text) < 100:
                    if any(word in text.lower() for word in ['job', 'career', 'position', 'role']):
                        continue  # Skip if it contains meta words
                    return text
        
        # Fallback: try to extract from URL or page title
        title = soup.find('title')
        if title:
            title_text = self._clean_text(title.get_text())
            # Remove common suffixes
            for suffix in [' - Careers', ' - Jobs', ' | Careers', ' | Jobs']:
                if suffix in title_text:
                    return title_text.split(suffix)[0]
            return title_text
        
        return "Professional Role"
    
    def _extract_experience(self, soup):
        """Extract experience requirements"""
        experience_patterns = [
            r'experience.*?(\d+[\+\-]?\d*.*?years?)',
            r'(\d+[\+\-]?\d*.*?years?.*?experience)',
            r'minimum.*?(\d+).*?years',
            r'(\d+\+?)\s*years',
            r'experience.*?(\d+\+?)',
        ]
        
        text = soup.get_text().lower()
        
        for pattern in experience_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                exp_text = self._clean_text(match.group(1))
                if exp_text and len(exp_text) < 50:
                    return exp_text.title()
        
        return "Experience varies"
    
    def _extract_skills(self, soup):
        """Extract required skills"""
        skill_keywords = [
            'python', 'javascript', 'java', 'react', 'node', 'sql', 'cloud', 'aws', 'azure',
            'docker', 'kubernetes', 'machine learning', 'ai', 'data analysis', 'communication',
            'leadership', 'management', 'excel', 'word', 'powerpoint', 'project management',
            'agile', 'scrum', 'marketing', 'sales', 'customer service', 'technical', 'design',
            'development', 'programming', 'coding', 'analytics', 'finance', 'accounting',
            'hr', 'human resources', 'recruitment', 'training', 'education', 'healthcare',
            'engineering', 'manufacturing', 'logistics', 'supply chain', 'retail', 'ecommerce'
        ]
        
        text = soup.get_text().lower()
        found_skills = []
        
        # Look for skills sections
        skill_section_selectors = [
            '.skills', '.requirements', '.qualifications', '.responsibilities',
            '[class*="skill"]', '[class*="requirement"]', '[class*="qualification"]'
        ]
        
        skill_text = ""
        for selector in skill_section_selectors:
            elements = soup.select(selector)
            for element in elements:
                skill_text += " " + element.get_text().lower()
        
        if not skill_text:
            skill_text = text
        
        # Extract skills
        for skill in skill_keywords:
            if skill in skill_text and skill not in found_skills:
                found_skills.append(skill)
        
        return ', '.join(found_skills[:8]) if found_skills else "Various relevant skills"
    
    def _extract_description(self, soup):
        """Extract job description"""
        description_selectors = [
            '.job-description',
            '.position-description',
            '.description',
            '[class*="description"]',
            '.role-details',
            '.job-details',
            'section',
            'div[class*="content"]'
        ]
        
        description_text = ""
        for selector in description_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = self._clean_text(element.get_text())
                if len(text) > 100 and len(text) < 2000:
                    description_text = text
                    break
        
        if not description_text:
            # Fallback: get meaningful text from the page
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = self._clean_text(p.get_text())
                if len(text) > 50 and len(text) < 500:
                    description_text = text
                    break
        
        if not description_text:
            description_text = "This position requires a qualified professional with relevant experience and skills."
        
        return description_text
    
    def scrape_job_info(self, url):
        """Main method to scrape job information from URL"""
        try:
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                return {
                    'error': 'Invalid URL format. Please include http:// or https://'
                }
            
            # Fetch the webpage
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            # Extract information
            company = self._extract_company_from_url(url)
            role = self._extract_role(soup, url)
            experience = self._extract_experience(soup)
            skills = self._extract_skills(soup)
            description = self._extract_description(soup)
            
            return {
                'role': role,
                'experience': experience,
                'skills': skills,
                'description': description,
                'company': company,
                'source': 'website',
                'url': url
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'error': f'Failed to access the website: {str(e)}',
                'role': 'Professional Role',
                'experience': 'Experience varies',
                'skills': 'Relevant skills',
                'description': 'Could not extract job details from the URL.',
                'company': self._extract_company_from_url(url),
                'source': 'error_fallback'
            }
        except Exception as e:
            return {
                'error': f'An error occurred: {str(e)}',
                'role': 'Professional Role',
                'experience': 'Experience varies',
                'skills': 'Relevant skills',
                'description': 'Error extracting job information.',
                'company': self._extract_company_from_url(url),
                'source': 'error_fallback'
            }
