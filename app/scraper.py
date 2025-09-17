# scraper.py
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

class AdvancedScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Common job platforms patterns
        self.job_platforms = {
            'linkedin': r'linkedin\.com/jobs',
            'indeed': r'indeed\.com',
            'naukri': r'naukri\.com',
            'monster': r'monster\.com',
            'glassdoor': r'glassdoor\.com',
            'simplyhired': r'simplyhired\.com',
            'careerbuilder': r'careerbuilder\.com'
        }
    
    def _extract_company_from_url(self, url):
        """Extract company name from URL with better accuracy"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # Remove www and common subdomains
            domain = re.sub(r'^www\.|^careers\.|^jobs\.|^recruitment\.', '', domain)
            
            # Extract company name from domain
            company_name = domain.split('.')[0]
            
            # Clean and format company name
            company_name = re.sub(r'[^a-zA-Z0-9]', ' ', company_name)
            company_name = company_name.title()
            company_name = re.sub(r'\s+', ' ', company_name).strip()
            
            return company_name if company_name else "The Company"
        except:
            return "The Company"
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        # Remove extra whitespace, newlines, and special characters
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:()\-&+/]', '', text)
        return text.strip()
    
    def _extract_from_common_selectors(self, soup, selectors):
        """Extract text using multiple CSS selectors"""
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = self._clean_text(element.get_text())
                if text and len(text) > 3:
                    return text
        return None
    
    def _extract_role(self, soup, url):
        """Enhanced job role extraction"""
        # Priority selectors for job titles
        role_selectors = [
            'h1[class*="title"][class*="job"]',
            'h1[class*="title"][class*="position"]',
            '[data-cy="job-title"]',
            '.job-title',
            '.position-title',
            '.jobTitle',
            '.job_header',
            '.topcard__title',
            '.jobsearch-JobInfoHeader-title',
            'h1.job-title',
            'title'
        ]
        
        role = self._extract_from_common_selectors(soup, role_selectors)
        
        if role:
            # Clean role title
            role = re.sub(r'(-|–|—|at|@|\\|/).*$', '', role, flags=re.IGNORECASE)
            role = self._clean_text(role)
            return role if role else "Professional Role"
        
        # Fallback to page title analysis
        title_tag = soup.find('title')
        if title_tag:
            title_text = self._clean_text(title_tag.get_text())
            # Remove platform names and company names
            for platform in ['LinkedIn', 'Indeed', 'Naukri', 'Monster', 'Glassdoor', ' - Jobs', ' | Careers']:
                title_text = title_text.replace(platform, '')
            return title_text if title_text else "Professional Role"
        
        return "Professional Role"
    
    def _extract_experience(self, soup):
        """Enhanced experience requirement extraction"""
        experience_patterns = [
            r'experience.*?(\d+[\+\-]?\d*\s*[-–]?\s*\d*\s*(?:years?|yrs?|y))',
            r'(\d+[\+\-]?\d*\s*[-–]?\s*\d*\s*(?:years?|yrs?|y)\s*experience)',
            r'minimum.*?(\d+[\+\-]?\d*\s*(?:years?|yrs?|y))',
            r'(\d+\+?\s*(?:years?|yrs?|y))',
            r'experience.*?(\d+\+?)',
            r'(\d+\s*[-–]\s*\d+\s*years?)'
        ]
        
        text = soup.get_text().lower()
        
        for pattern in experience_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                exp_text = self._clean_text(match.group(1))
                if exp_text and len(exp_text) < 30:
                    return exp_text.title()
        
        # Check common experience phrases
        experience_phrases = [
            'fresher', 'entry level', 'mid level', 'senior level',
            'experienced professional', 'leadership experience'
        ]
        
        for phrase in experience_phrases:
            if phrase in text:
                return phrase.title()
        
        return "Experience varies"
    
    def _extract_skills(self, soup):
        """Enhanced skills extraction for all job types"""
        # Comprehensive skill categories
        skill_categories = {
            'technical': [
                'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'html', 'css',
                'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring', 'sql', 'nosql',
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'devops',
                'machine learning', 'ai', 'data science', 'big data', 'tableau', 'power bi'
            ],
            'non_technical': [
                'communication', 'leadership', 'management', 'teamwork', 'problem solving',
                'critical thinking', 'time management', 'organization', 'adaptability',
                'creativity', 'negotiation', 'presentation', 'public speaking', 'writing',
                'research', 'analysis', 'strategic planning', 'project management'
            ],
            'business': [
                'sales', 'marketing', 'digital marketing', 'seo', 'sem', 'social media',
                'business development', 'account management', 'customer service',
                'finance', 'accounting', 'budgeting', 'forecasting', 'risk management',
                'hr', 'recruitment', 'training', 'talent acquisition'
            ],
            'creative': [
                'design', 'photoshop', 'illustrator', 'figma', 'sketch', 'ux', 'ui',
                'video editing', 'premiere pro', 'final cut', 'after effects',
                'content creation', 'copywriting', 'branding', 'graphic design'
            ]
        }
        
        text = soup.get_text().lower()
        found_skills = []
        
        # Look for skills sections first
        skill_section_selectors = [
            '.skills', '.requirements', '.qualifications', '.responsibilities',
            '[class*="skill"]', '[class*="requirement"]', '[class*="qualification"]',
            '.job-requirements', '.essential-skills', '.desired-skills'
        ]
        
        skill_text = ""
        for selector in skill_section_selectors:
            elements = soup.select(selector)
            for element in elements:
                skill_text += " " + element.get_text().lower()
        
        if not skill_text:
            skill_text = text
        
        # Extract skills from all categories
        for category, skills in skill_categories.items():
            for skill in skills:
                if skill in skill_text and skill not in found_skills:
                    found_skills.append(skill)
        
        return ', '.join(found_skills[:10]) if found_skills else "Relevant skills and experience"
    
    def _extract_description(self, soup):
        """Enhanced job description extraction"""
        description_selectors = [
            '.job-description',
            '.job-description-content',
            '.description',
            '.job-details',
            '.job-requirements',
            '.role-responsibilities',
            '[class*="description"]',
            '[class*="detail"]',
            '.jobsum
