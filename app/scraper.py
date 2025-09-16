# scraper.py
import re

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
        
        # Return mock data based on URL content
        url_lower = url.lower()
        
        # Technical roles
        if any(keyword in url_lower for keyword in ['software', 'developer', 'engineer', 'programmer']):
            return {
                'role': 'Senior Software Engineer',
                'experience': '5+ years',
                'skills': 'Python, JavaScript, React, Node.js, Cloud Architecture',
                'description': 'Design and implement scalable software solutions while collaborating with cross-functional teams to deliver high-quality products.',
                'company': company
            }
        elif any(keyword in url_lower for keyword in ['data', 'analyst', 'scientist']):
            return {
                'role': 'Data Scientist',
                'experience': '3+ years',
                'skills': 'Python, SQL, Machine Learning, Data Visualization, Statistical Analysis',
                'description': 'Develop predictive models and analyze complex datasets to drive business insights and support data-driven decision making.',
                'company': company
            }
        # Non-technical roles
        elif any(keyword in url_lower for keyword in ['sales', 'account', 'business development']):
            return {
                'role': 'Senior Account Executive',
                'experience': '4+ years',
                'skills': 'Enterprise Sales, Relationship Management, Negotiation, CRM',
                'description': 'Drive revenue growth through strategic account management and develop long-term relationships with key enterprise clients.',
                'company': company
            }
        elif any(keyword in url_lower for keyword in ['marketing', 'digital', 'social media']):
            return {
                'role': 'Marketing Manager',
                'experience': '5+ years',
                'skills': 'Digital Marketing, Brand Strategy, Campaign Management, Analytics',
                'description': 'Develop and execute comprehensive marketing strategies to enhance brand presence and drive customer engagement.',
                'company': company
            }
        elif any(keyword in url_lower for keyword in ['hr', 'human resources', 'recruitment']):
            return {
                'role': 'HR Business Partner',
                'experience': '4+ years',
                'skills': 'Talent Acquisition, Employee Relations, HR Strategy, Performance Management',
                'description': 'Partner with business leaders to develop and implement HR strategies that support organizational objectives.',
                'company': company
            }
        elif any(keyword in url_lower for keyword in ['finance', 'accounting', 'financial']):
            return {
                'role': 'Financial Analyst',
                'experience': '3+ years',
                'skills': 'Financial Modeling, Data Analysis, Excel, Reporting',
                'description': 'Conduct financial analysis and prepare reports to support strategic planning and business decision making.',
                'company': company
            }
        elif any(keyword in url_lower for keyword in ['manager', 'director', 'lead']):
            return {
                'role': 'Project Manager',
                'experience': '6+ years',
                'skills': 'Project Management, Agile Methodology, Team Leadership, Stakeholder Management',
                'description': 'Lead cross-functional teams to deliver complex projects on time and within budget while ensuring quality standards.',
                'company': company
            }
        else:
            # Generic professional role
            return {
                'role': 'Professional Specialist',
                'experience': '3+ years',
                'skills': 'Strategic Planning, Problem Solving, Communication, Leadership',
                'description': 'This position requires a professional with demonstrated expertise in delivering results in a dynamic business environment.',
                'company': company
            }
