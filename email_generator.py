# email_generator.py
import json
import random
import os
from datetime import datetime

class EmailGenerator:
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        # Comprehensive professional templates for various industries
        return {
            "technical": {
                "greetings": [
                    "Dear Hiring Manager,",
                    "Dear Hiring Team,",
                    "Dear Recruitment Committee,",
                    "Dear Sir/Madam,",
                ],
                "introductions": [
                    "I am writing to express my sincere interest in the {role} position at {company}, which I discovered through your careers portal.",
                    "With great enthusiasm, I submit my application for the {role} position at {company} that was advertised on your website.",
                    "I am writing to apply for the {role} position at {company}, as I believe my qualifications and experience align perfectly with your requirements.",
                ],
                "value_propositions": [
                    "With over {experience} of specialized experience in {skills}, I am confident in my ability to deliver exceptional results and contribute significantly to your team's success.",
                    "My extensive background in {skills} has equipped me with the technical expertise and problem-solving capabilities necessary to excel in this challenging role.",
                    "I bring a proven track record of success in {skills}, with demonstrated achievements that I believe would translate well to the objectives of this position.",
                ],
                "achievement_statements": [
                    "Throughout my career, I have successfully implemented solutions that resulted in measurable improvements in efficiency and productivity.",
                    "I have consistently demonstrated the ability to manage complex projects from conception to completion, delivering on time and within budget.",
                    "My technical expertise has enabled me to solve challenging problems and drive innovation in previous roles.",
                ]
            },
            "non_technical": {
                "greetings": [
                    "Dear Hiring Manager,",
                    "Dear Selection Committee,",
                    "Dear Sir/Madam,",
                    "To Whom It May Concern,",
                ],
                "introductions": [
                    "I am writing to express my keen interest in the {role} position at {company}, which I believe aligns perfectly with my professional background and career aspirations.",
                    "I am excited to submit my application for the {role} position at {company}, as advertised on your official website.",
                    "With great interest, I am applying for the {role} position at {company}, confident that my skills and experience make me an ideal candidate for this role.",
                ],
                "value_propositions": [
                    "With {experience} of professional experience in {skills}, I possess the comprehensive skill set and strategic mindset required to excel in this position.",
                    "My background in {skills} has provided me with the expertise to drive operational excellence and deliver sustainable results in dynamic business environments.",
                    "I offer a unique combination of {skills} that enables me to approach challenges with innovative solutions and deliver measurable business outcomes.",
                ],
                "achievement_statements": [
                    "I have consistently exceeded performance targets and delivered exceptional results in fast-paced professional environments.",
                    "My strategic approach to problem-solving has enabled me to identify opportunities for improvement and implement effective solutions.",
                    "I have successfully built and maintained strong professional relationships with stakeholders at all organizational levels.",
                ]
            },
            "executive": {
                "greetings": [
                    "Dear Hiring Committee,",
                    "Dear Selection Board,",
                    "Dear Sir/Madam,",
                ],
                "introductions": [
                    "I am writing to express my sincere interest in the {role} position at {company}, as I believe my executive experience and leadership capabilities align perfectly with your organization's strategic direction.",
                    "With considerable interest, I submit my application for the {role} position at {company}, confident that my extensive experience in leadership roles positions me as a strong candidate.",
                    "I am writing to apply for the {role} position at {company}, bringing a wealth of executive experience and a proven track record of driving organizational success.",
                ],
                "value_propositions": [
                    "With over {experience} of executive leadership experience in {skills}, I have demonstrated the ability to develop and execute strategies that drive growth and operational excellence.",
                    "My comprehensive expertise in {skills} has enabled me to lead organizations through transformative periods, delivering sustainable results and enhancing stakeholder value.",
                    "I bring a distinguished record of leadership in {skills}, with particular strength in developing high-performing teams and implementing innovative business solutions.",
                ],
                "achievement_statements": [
                    "I have successfully led organizational transformations that resulted in significant improvements in operational efficiency and market positioning.",
                    "My strategic vision has consistently delivered exceptional financial results and enhanced competitive advantage in challenging market conditions.",
                    "I have built and mentored high-performing executive teams that have consistently exceeded business objectives and driven sustainable growth.",
                ]
            },
            "shared": {
                "company_praise": [
                    "I have long admired {company}'s reputation for excellence and commitment to innovation in the {industry} sector.",
                    "Your organization's dedication to {value} aligns closely with my professional values and career aspirations.",
                    "I have been impressed by {company}'s consistent market leadership and commitment to quality, which makes this opportunity particularly appealing.",
                    "{company}'s innovative approach to {industry} and strong corporate values resonate deeply with my professional philosophy.",
                ],
                "portfolio_mentions": [
                    "I invite you to review my portfolio of relevant work, which demonstrates my capabilities in this area: {links}",
                    "Examples of my previous accomplishments and projects can be found in my portfolio: {links}",
                    "My track record of success is evidenced in the following portfolio pieces: {links}",
                ],
                "call_to_actions": [
                    "I would welcome the opportunity to discuss how my experience and qualifications can contribute to {company}'s continued success.",
                    "I am available for an interview at your earliest convenience to further explore how I might add value to your organization.",
                    "I look forward to the possibility of discussing this opportunity further and am available for a meeting at your convenience.",
                ],
                "closings": [
                    "Sincerely,",
                    "Respectfully yours,",
                    "With best regards,",
                ]
            }
        }
    
    def _detect_role_level(self, role, experience):
        """Determine the seniority level based on role title and experience"""
        role_lower = (role or '').lower()
        experience_years = self._parse_experience(experience)
        
        # Executive level detection
        executive_keywords = [
            'director', 'vp', 'vice president', 'c-level', 'chief', 'executive',
            'head of', 'senior vice president', 'managing director'
        ]
        
        for keyword in executive_keywords:
            if keyword in role_lower:
                return "executive"
        
        # Determine level based on experience
        if experience_years >= 8:
            return "executive"
        elif experience_years >= 3:
            return "technical" if any(tech_word in role_lower for tech_word in ['developer', 'engineer', 'technical']) else "non_technical"
        else:
            return "non_technical"
    
    def _parse_experience(self, experience_text):
        """Parse experience text to extract years"""
        if not experience_text:
            return 3  # Default assumption
        
        # Extract numbers from experience text
        import re
        numbers = re.findall(r'\d+', experience_text)
        if numbers:
            return int(numbers[0])
        return 3  # Default if no numbers found
    
    def _is_technical_role(self, role, skills):
        """Determine if a role is technical based on keywords"""
        technical_keywords = [
            'developer', 'engineer', 'programmer', 'technical', 'technology',
            'software', 'data', 'system', 'network', 'IT', 'devops', 'cyber',
            'security', 'analyst', 'architect', 'scientist', 'database', 'cloud',
            'backend', 'frontend', 'fullstack', 'code', 'programming', 'technical'
        ]
        
        role_lower = (role or '').lower()
        skills_lower = (skills or '').lower()
        
        # Check if role or skills contain technical keywords
        for keyword in technical_keywords:
            if keyword in role_lower or keyword in skills_lower:
                return True
        return False
    
    def _get_industry_from_company(self, company):
        """Simple industry detection based on company name keywords"""
        if not company:
            return "industry"
        
        company_lower = company.lower()
        
        if any(word in company_lower for word in ['tech', 'software', 'computer', 'data', 'cloud']):
            return "technology"
        elif any(word in company_lower for word in ['finance', 'bank', 'investment', 'capital']):
            return "financial services"
        elif any(word in company_lower for word in ['health', 'medical', 'pharma', 'care']):
            return "healthcare"
        elif any(word in company_lower for word in ['retail', 'shop', 'store', 'commerce']):
            return "retail"
        elif any(word in company_lower for word in ['consulting', 'advisor', 'services']):
            return "professional services"
        else:
            return "industry"
    
    def generate_email(self, job_data, portfolio_links, user_info):
        # Extract job information
        role = job_data.get('role', 'the position')
        company = job_data.get('company', 'your organization') or 'your organization'
        experience_req = job_data.get('experience', '')
        skills = job_data.get('skills', 'relevant skills')
        description = job_data.get('description', '')
        
        # Determine role type and level
        is_technical = self._is_technical_role(role, skills)
        role_level = self._detect_role_level(role, experience_req)
        
        # Use appropriate template set
        if role_level == "executive":
            template_set = self.templates["executive"]
        else:
            template_set = self.templates["technical"] if is_technical else self.templates["non_technical"]
        
        # Get industry for company praise
        industry = self._get_industry_from_company(company)
        
        # Format portfolio links
        links_text = ""
        if portfolio_links:
            links_list = [link['links'] for link in portfolio_links]
            links_text = ", ".join(links_list)
        
        # Select appropriate template parts
        greeting = random.choice(template_set["greetings"])
        introduction = random.choice(template_set["introductions"]).format(role=role, company=company)
        praise = random.choice(self.templates["shared"]["company_praise"]).format(
            company=company, 
            industry=industry,
            value="innovation"
        )
        value_prop = random.choice(template_set["value_propositions"]).format(
            skills=skills, 
            experience=experience_req or "several years"
        )
        achievement = random.choice(template_set["achievement_statements"])
        portfolio_mention = random.choice(self.templates["shared"]["portfolio_mentions"]).format(links=links_text) if links_text else ""
        call_to_action = random.choice(self.templates["shared"]["call_to_actions"]).format(company=company)
        closing = random.choice(self.templates["shared"]["closings"])
        
        # Construct professional email with proper formatting
        email_lines = [
            f"Subject: Application for {role} Position",
            "",
            greeting,
            "",
            introduction,
            "",
            praise,
            "",
            value_prop,
            "",
            achievement,
            ""
        ]
        
        # Add portfolio mention if available
        if portfolio_mention:
            email_lines.extend([portfolio_mention, ""])
        
        # Add description excerpt if available and relevant
        if description and len(description) > 20:
            email_lines.extend([
                "I was particularly impressed by the following aspects of the position:",
                f"\"{description[:200]}{'...' if len(description) > 200 else ''}\"",
                ""
            ])
        
        email_lines.extend([
            call_to_action,
            "",
            closing,
            "",
            user_info['name'],
            user_info['role'],
            user_info['company'],
            f"Email: {user_info['email']}",
            f"Phone: {user_info['phone']}"
        ])
        
        # Add LinkedIn if provided
        if user_info.get('linkedin'):
            email_lines.append(f"LinkedIn: {user_info['linkedin']}")
        
        # Add date if available
        email_lines.append(f"Date: {datetime.now().strftime('%B %d, %Y')}")
        
        return "\n".join(email_lines)