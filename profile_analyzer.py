import requests
from bs4 import BeautifulSoup
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def extract_skills_from_profiles(profile_urls):
    """
    Extract skills from LinkedIn and GitHub profiles
    
    Args:
        profile_urls: List of tuples (platform, url)
    
    Returns:
        Dictionary with extracted skills and profile information
    """
    all_skills = []
    profile_data = {
        'skills': [],
        'profiles': {}
    }
    
    # Initialize LLM
    llm = ChatGroq(
        temperature=0.1,
        model_name="llama-3.3-70b-versatile"
    )
    
    for platform, url in profile_urls:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            page_data = soup.get_text(separator='\n', strip=True)
            
            # Create prompt based on platform
            if platform == "linkedin":
                prompt_template = PromptTemplate.from_template(
                    """
                    Analyze this LinkedIn profile and extract:
                    1. Technical skills (programming languages, tools, technologies)
                    2. Soft skills (communication, leadership, etc.)
                    3. Experience summary
                    4. Education background
                    
                    Return the results as JSON with these keys:
                    - technical_skills: list of technical skills
                    - soft_skills: list of soft skills  
                    - experience: summary of experience
                    - education: summary of education
                    
                    PROFILE DATA:
                    {page_data}
                    
                    Return only valid JSON.
                    """
                )
            else:  # github
                prompt_template = PromptTemplate.from_template(
                    """
                    Analyze this GitHub profile and extract:
                    1. Programming languages used
                    2. Technologies and frameworks
                    3. Project domains (web development, data science, etc.)
                    4. Activity level and contributions
                    
                    Return the results as JSON with these keys:
                    - languages: list of programming languages
                    - technologies: list of technologies and frameworks
                    - domains: list of project domains
                    - activity: description of activity level
                    
                    PROFILE DATA:
                    {page_data}
                    
                    Return only valid JSON.
                    """
                )
            
            # Extract information using LLM
            chain = prompt_template | llm
            response = chain.invoke({'page_data': page_data[:8000]})  # Limit length
            
            # Parse JSON response
            json_parser = JsonOutputParser()
            try:
                profile_info = json_parser.parse(response.content)
                
                # Extract skills based on platform
                if platform == "linkedin":
                    skills = profile_info.get('technical_skills', []) + profile_info.get('soft_skills', [])
                else:  # github
                    skills = profile_info.get('languages', []) + profile_info.get('technologies', [])
                
                # Add to overall skills list
                all_skills.extend(skills)
                
                # Store profile data
                profile_data['profiles'][platform] = profile_info
                
            except Exception as e:
                print(f"Error parsing {platform} profile: {e}")
                continue
                
        except Exception as e:
            print(f"Error scraping {platform} profile: {e}")
            continue
    
    # Deduplicate skills
    profile_data['skills'] = list(set([skill.lower().strip() for skill in all_skills if skill.strip()]))
    
    return profile_data
