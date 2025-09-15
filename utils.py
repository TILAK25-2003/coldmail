import re

def validate_url(url):
    """Validate URL format"""
    url_pattern = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'(([A-Z0-9-]+\.)+[A-Z]{2,63})'  # domain
        r'(:[0-9]{1,5})?'  # optional port
        r'(/.*)?$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))

def extract_domain(url):
    """Extract domain from URL"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return parsed.netloc or parsed.path

def format_skills_list(skills):
    """Format skills list for display"""
    if isinstance(skills, list):
        return [skill.strip() for skill in skills if skill.strip()]
    elif isinstance(skills, str):
        return [skill.strip() for skill in skills.split(",") if skill.strip()]
    return []
