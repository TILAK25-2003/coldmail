import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def extract_job_details(url):
    """
    Extract job details from a given URL using direct web scraping
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Try to extract job title from URL or page title
        title = extract_job_title(soup, url)
        
        return {
            'title': title,
            'description': text,
            'url': url,
            'source': urlparse(url).netloc
        }
        
    except Exception as e:
        raise Exception(f"Failed to extract job details: {str(e)}")

def extract_job_title(soup, url):
    """
    Extract job title from various possible locations
    """
    # Try from title tag
    title_tag = soup.find('title')
    if title_tag:
        title_text = title_tag.get_text().strip()
        # Common job title patterns
        patterns = [
            r'hiring:\s*(.+)',
            r'careers:\s*(.+)',
            r'job:\s*(.+)',
            r'position:\s*(.+)',
            r'-.+?-\s*(.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    
    # Try from h1 tags
    h1_tags = soup.find_all('h1')
    for h1 in h1_tags:
        h1_text = h1.get_text().strip()
        if len(h1_text) < 100 and any(keyword in h1_text.lower() for keyword in ['engineer', 'developer', 'manager', 'analyst', 'designer']):
            return h1_text
    
    # Fallback to URL parsing
    path = urlparse(url).path
    if '/' in path:
        last_part = path.split('/')[-1]
        if last_part and len(last_part) > 3:
            return last_part.replace('-', ' ').title()
    
    return "Unknown Position"
