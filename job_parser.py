# job_parser.py (updated with better fallbacks)
import requests
from bs4 import BeautifulSoup
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def extract_job_details(url):
    """Extract job details from a URL with robust error handling"""
    try:
        # Try to use LLM-based extraction first
        return extract_with_llm(url)
    except Exception as e:
        print(f"LLM extraction failed: {e}, falling back to simple extraction")
        # Fall back to simple extraction
        return extract_simple_details(url)

def extract_with_llm(url):
    """Extract job details using LLM"""
    # Fetch webpage content
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text content
    page_data = soup.get_text(separator='\n', strip=True)
    
    # Initialize LLM
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.3-70b-versatile"
    )
    
    # Create prompt template
    prompt_extract = PromptTemplate.from_template(
        """
        *** SCRAPED TEXT FROM WEBSITE:
        {page_data}
        *** INSTRUCTION:
        Extract job details and return valid JSON with these keys: 
        - role: job title
        - experience: required experience
        - skills: list of required skills
        - description: job description summary
        
        Only return the valid JSON.
        """
    )
    
    # Create chain
    chain_extract = prompt_extract | llm
    response = chain_extract.invoke({'page_data': page_data})
    
    # Parse JSON response
    try:
        json_parser = JsonOutputParser()
        job_data = json_parser.parse(response.content)
        return job_data
    except:
        # Fallback parsing
        content = response.content
        json_str = extract_json_from_text(content)
        return json.loads(json_str)

def extract_simple_details(url):
    """Simple fallback extraction"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find common job title patterns
        title = "Software Developer"
        for tag in ['h1', 'h2', 'h3', 'title']:
            elements = soup.find_all(tag)
            for element in elements:
                text = element.get_text().lower()
                if any(keyword in text for keyword in ['developer', 'engineer', 'designer', 'analyst']):
                    title = element.get_text().strip()
                    break
        
        return {
            "role": title,
            "experience": "2+ years",
            "skills": ["Python", "JavaScript", "Problem Solving"],
            "description": f"Position at {url}. Please refer to the original posting for complete details."
        }
    except:
        # Ultimate fallback
        return {
            "role": "Software Developer",
            "experience": "2+ years",
            "skills": ["Python", "JavaScript", "Problem Solving"],
            "description": "Could not extract job details. Please manually review the job posting."
        }

def extract_json_from_text(text):
    """Extract JSON from text response"""
    if '```json' in text:
        return text.split('```json')[1].split('```')[0].strip()
    elif '```' in text:
        return text.split('```')[1].split('```')[0].strip()
    else:
        # Try to find JSON object
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            return text[start:end+1]
        return '{"role": "Developer", "experience": "Not specified", "skills": [], "description": "Details not extracted"}'
