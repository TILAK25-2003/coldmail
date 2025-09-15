import os
import groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailGenerator:
    def __init__(self):
        # Initialize Groq client with API key from environment variable
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def generate_email(self, job_details, user_context=None):
        """Generate a cold email based on job details"""
        if not user_context:
            user_context = {
                "name": "John Doe",
                "background": "experienced professional",
                "skills": "relevant skills"
            }
        
        # Prepare the prompt for the LLM
        prompt = self._create_prompt(job_details, user_context)
        
        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that generates professional cold emails for job applications. Create compelling, personalized emails that highlight the candidate's relevant skills and experiences."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-8b-instant",  # You can change this to other available models
                temperature=0.7,
                max_tokens=1000
            )
            
            return chat_completion.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Error generating email: {str(e)}"
    
    def _create_prompt(self, job_details, user_context):
        """Create a detailed prompt for the LLM"""
        prompt = f"""
        Create a professional cold email for a job application based on the following details:
        
        Job Title: {job_details.get('job_title', 'Not specified')}
        Company: {job_details.get('company_name', 'Not specified')}
        Experience Required: {job_details.get('experience', 'Not specified')}
        Technical Skills Required: {', '.join(job_details.get('technical_skills', []))}
        Non-Technical Skills Required: {', '.join(job_details.get('non_technical_skills', []))}
        Job URL: {job_details.get('job_url', 'Not provided')}
        
        Candidate Information:
        Name: {user_context.get('name', 'John Doe')}
        Background: {user_context.get('background', 'experienced professional')}
        Skills: {user_context.get('skills', 'relevant skills')}
        
        Please generate a personalized email that:
        1. Addresses the hiring manager appropriately
        2. Expresses genuine interest in the position and company
        3. Highlights how the candidate's skills and experience match the job requirements
        4. Is concise but compelling (around 200-300 words)
        5. Includes a professional closing with the candidate's name
        
        Make the email sound natural and engaging, not generic. Focus on the most relevant qualifications for this specific role.
        """
        
        return prompt
