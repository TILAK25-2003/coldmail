from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

def extract_job_details(url):
    """Extract job details from a URL"""
    # Load the webpage content
    loader = WebBaseLoader(url)
    page_data = loader.load().pop().page_content
    
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
        The scraped text is from a job posting page.
        Your job is to extract the job details and return them in JSON format containing the following keys: 
        - role: the job title
        - experience: required experience level
        - skills: list of required skills and technologies
        - description: job description summary
        
        Only return the valid JSON.
        *** VALID JSON (NO PREAMBLE).
        """
    )
    
    # Create chain
    chain_extract = prompt_extract | llm
    response = chain_extract.invoke({'page_data': page_data})
    
    # Parse JSON response
    json_parser = JsonOutputParser()
    try:
        job_data = json_parser.parse(response.content)
        return job_data
    except:
        # Fallback: try to extract JSON from response
        content = response.content
        if '```json' in content:
            json_str = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            json_str = content.split('```')[1].split('```')[0].strip()
        else:
            json_str = content.strip()
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If all else fails, return a basic structure
            return {
                "role": "Extracted Role",
                "experience": "Experience not extracted",
                "skills": ["Skills not extracted"],
                "description": "Description not extracted"
            }