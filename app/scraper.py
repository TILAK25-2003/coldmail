# scraper.py
import re
try:
    from langchain_community.document_loaders import WebBaseLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

class SimpleScraper:
    def __init__(self):
        self.company_mapping = {
            'spencer': 'Spencer Technologies',
            'google': 'Google',
            'microsoft': 'Microsoft',
            'amazon': 'Amazon',
            'apple': 'Apple',
            'ibm': 'IBM',
            'facebook': 'Meta',
            'netflix': 'Netflix',
            'twitter': 'X Corp',
            'linkedin': 'LinkedIn',
            'salesforce': 'Salesforce',
            'oracle': 'Oracle',
            'adobe': 'Adobe',
            'intel': 'Intel',
            'nvidia': 'NVIDIA'
        }
    
    def _extract_company_from_url(self, url):
        """Extract company name from URL"""
        domain = re.findall(r'https?://(?:www\.)?([^/]+)', url)
        if domain:
            domain_name = domain[0].split('.')[0]
            return self.company_mapping.get(domain_name.lower(), domain_name.title() + " Inc.")
        return "Respected Organization"
    
    def scrape_job_info(self, url):
        # Extract company name from URL
        company = self._extract_company_from_url(url)
        
        # Try to use LangChain for actual scraping if available
        if LANGCHAIN_AVAILABLE:
            try:
                loader = WebBaseLoader(url)
                data = loader.load()
                if data and len(data) > 0:
                    content = data[0].page_content[:1000]  # Get first 1000 characters
                    return self._analyze_content(content, company, url)
            except Exception as e:
                print(f"LangChain scraping failed: {e}")
                # Fall back to mock data
        
        # Fallback: Return mock data based on URL content
        return self._get_mock_data_based_on_url(url, company)
    
    def _analyze_content(self, content, company, url):
        """Analyze scraped content to extract job information"""
        content_lower = content.lower()
        
        # Simple pattern matching from actual content
        role = self._extract_role(content_lower)
        skills = self._extract_skills(content_lower)
        
        return {
            'role': role,
            'experience': self._extract_experience(content_lower),
            'skills': skills,
            'description': content[:500] + '...' if len(content) > 500 else content,
            'company': company,
            'source': 'actual_website'
        }
    
    def _extract_role(self, content):
        """Extract job role from content"""
        role_patterns = [
            r'position[:\s]*([^\n]+)',
            r'role[:\s]*([^\n]+)',
            r'job title[:\s]*([^\n]+)',
            r'hiring[:\s]*([^\n]+)',
            r'we are looking for a[n]? ([^\n.,!?]+)',
        ]
        
        for pattern in role_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Professional Role"
    
    def _extract_experience(self, content):
        """Extract experience requirement from content"""
        exp_patterns = [
            r'experience[:\s]*([^\n]+)',
            r'years.*experience[:\s]*([^\n]+)',
            r'(\d+)\+? years',
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "2+ years"
    
    def _extract_skills(self, content):
        """Extract skills from content"""
        skill_keywords = [
            'python', 'javascript', 'java', 'react', 'node', 'sql', 'cloud',
            'aws', 'azure', 'docker', 'kubernetes', 'machine learning', 'ai',
            'data analysis', 'communication', 'leadership', 'management'
        ]
        
        found_skills = []
        for skill in skill_keywords:
            if skill in content:
                found_skills.append(skill)
        
        return ', '.join(found_skills[:5]) if found_skills else "Relevant skills"
    
    def _get_mock_data_based_on_url(self, url, company):
        """Fallback to mock data based on URL patterns"""
        url_lower = url.lower()
        
        # Technical roles
        if any(keyword in url_lower for keyword in ['software', 'developer', 'engineer', 'programmer']):
            return {
                'role': 'Senior Software Engineer',
                'experience': '5+ years',
                'skills': 'Python, JavaScript, React, Node.js, Cloud Architecture',
                'description': 'Design and implement scalable software solutions while collaborating with cross-functional teams to deliver high-quality products.',
                'company': company,
                'source': 'mock_data'
            }
        elif any(keyword in url_lower for keyword in ['data', 'analyst', 'scientist']):
            return {
                'role': 'Data Scientist',
                'experience': '3+ years',
                'skills': 'Python, SQL, Machine Learning, Data Visualization, Statistical Analysis',
                'description': 'Develop predictive models and analyze complex datasets to drive business insights and support data-driven decision making.',
                'company': company,
                'source': 'mock_data'
            }
        # Non-technical roles
        elif any(keyword in url_lower for keyword in ['sales', 'account', 'business development']):
            return {
                'role': 'Senior Account Executive',
                'experience': '4+ years',
                'skills': 'Enterprise Sales, Relationship Management, Negotiation, CRM',
                'description': 'Drive revenue growth through strategic account management and develop long-term relationships with key enterprise clients.',
                'company': company,
                'source': 'mock_data'
            }
        else:
            # Generic professional role
            return {
                'role': 'Professional Specialist',
                'experience': '3+ years',
                'skills': 'Strategic Planning, Problem Solving, Communication, Leadership',
                'description': 'This position requires a professional with demonstrated expertise in delivering results in a dynamic business environment.',
                'company': company,
                'source': 'mock_data'
            }
