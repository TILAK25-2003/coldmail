# chains.py
import json
import random
import os

class EmailGenerator:
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        # Try to load from file first
        try:
            templates_path = os.path.join(os.path.dirname(__file__), "..", "templates", "email_templates.json")
            with open(templates_path, 'r') as f:
                return json.load(f)
        except:
            # Fallback to default templates
            return {
                "greetings": [
                    "Dear Hiring Team,",
                    "Hello,",
                    "Greetings,",
                    "Dear Recruiter,"
                ],
                "introductions": [
                    "I am writing to express my interest in the {role} position I found on your website.",
                    "I was excited to see the opening for a {role} at your company.",
                    "I am reaching out regarding the {role} opportunity at your organization."
                ],
                "company_praise": [
                    "I've been following your company's work and am impressed by your innovative approach.",
                    "Your company's reputation in the industry is highly regarded.",
                    "I admire your company's commitment to excellence and innovation."
                ],
                "value_propositions": [
                    "With my experience in {skills}, I believe I can contribute significantly to your team.",
                    "My background in {skills} aligns perfectly with the requirements for this role.",
                    "I possess the {skills} expertise that would allow me to hit the ground running in this position."
                ],
                "portfolio_mentions": [
                    "You can see examples of my work in these relevant projects: {links}",
                    "I've worked on similar projects such as: {links}",
                    "My portfolio includes relevant work like: {links}"
                ],
                "call_to_actions": [
                    "I would welcome the opportunity to discuss how my skills can benefit your team.",
                    "I am available for an interview at your earliest convenience.",
                    "I look forward to the possibility of discussing this opportunity further."
                ],
                "closings": [
                    "Sincerely,",
                    "Best regards,",
                    "Thank you for your consideration,"
                ]
            }
    
    def generate_email(self, job_data, portfolio_links):
        # Extract job information
        role = job_data.get('role', 'the position')
        skills = job_data.get('skills', '')
        description = job_data.get('description', '')
        
        # Format portfolio links
        links_text = ""
        if portfolio_links:
            links_list = [link['links'] for link in portfolio_links]
            links_text = ", ".join(links_list)
        
        # Select random template parts
        greeting = random.choice(self.templates["greetings"])
        introduction = random.choice(self.templates["introductions"]).format(role=role)
        praise = random.choice(self.templates["company_praise"])
        value_prop = random.choice(self.templates["value_propositions"]).format(skills=skills)
        portfolio_mention = random.choice(self.templates["portfolio_mentions"]).format(links=links_text)
        call_to_action = random.choice(self.templates["call_to_actions"])
        closing = random.choice(self.templates["closings"])
        
        # Construct email
        email_lines = [
            greeting,
            "",
            introduction,
            praise,
            "",
            value_prop,
            "",
            portfolio_mention,
            "",
            "Here's how my experience aligns with your requirements:",
            description[:500] + "..." if len(description) > 500 else description,
            "",
            call_to_action,
            "",
            closing,
            "Mohan",
            "Business Development Executive",
            "AtliQ",
            "Email: mohan@atliq.com",
            "Phone: +91-9876543210"
        ]
        
        return "\n".join(email_lines)