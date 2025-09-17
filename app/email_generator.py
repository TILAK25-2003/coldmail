# email_generator.py
from typing import List, Dict, Any
import textwrap

class EmailGenerator:
    """
    Generates polished cold emails tailored for:
      - technical audiences (engineers, data scientists)
      - non-technical audiences (sales, BD, HR)
      - professionals (senior roles, leadership)
    The main entrypoint is generate_email(job_data, portfolio_links, user_info).
    """

    def __init__(self):
        pass

    def _detect_audience(self, job_data: Dict[str, Any]) -> str:
        """
        Heuristic to choose audience: 'technical' or 'non-technical' or 'leadership'
        """
        skills = (job_data.get("skills") or "").lower()
        role = (job_data.get("role") or "").lower()
        # leadership keywords
        leadership_kw = ["manager", "lead", "head", "director", "vp", "vice", "principal", "sr "]
        if any(k in role for k in leadership_kw):
            return "leadership"
        technical_indicators = ["python", "java", "react", "node", "sql", "ml", "machine learning",
                                "docker", "aws", "kubernetes", "c++", "c#", "golang", "backend", "frontend"]
        if any(t in skills for t in technical_indicators) or any(t in role for t in technical_indicators):
            return "technical"
        # default
        return "non-technical"

    def _format_links_section(self, portfolio_links: List[Dict[str, Any]]) -> str:
        if not portfolio_links:
            return ""
        lines = ["Relevant work I can share:"]
        for p in portfolio_links:
            title = p.get("title") or p.get("techstack") or p.get("links")
            link = p.get("links", "")
            sim = p.get("similarity", 0)
            lines.append(f"- {title} — {link} (match: {sim:.2f})")
        return "\n".join(lines)

    def _subject_for(self, job_data: Dict[str, Any], user_info: Dict[str, Any]) -> str:
        role = job_data.get("role", "the role")
        company = job_data.get("company", "")
        if company:
            return f"Interest in {role} at {company} — {user_info.get('name')}"
        return f"Application: {role} — {user_info.get('name')}"

    def generate_email(self, job_data: Dict[str, Any], portfolio_links: List[Dict[str, Any]], user_info: Dict[str, Any],
                       audience: str = None, tone: str = "professional") -> str:
        """
        Main generator. audience can be 'technical', 'non-technical', 'leadership', or None (auto).
        tone can be 'professional' or 'friendly'.
        Returns full email text with Subject line included.
        """
        if audience is None:
            audience = self._detect_audience(job_data)

        role = job_data.get("role", "")
        company = job_data.get("company", "")
        experience = job_data.get("experience", "")
        skills = job_data.get("skills", "")
        description = job_data.get("description", "")

        name = user_info.get("name", "")
        user_role = user_info.get("role", "")
        user_company = user_info.get("company", "")
        email = user_info.get("email", "")
        phone = user_info.get("phone", "")
        linkedin = user_info.get("linkedin", "")

        subject = self._subject_for(job_data, user_info)

        # Openers — tailored by audience
        if audience == "technical":
            opener = (
                f"Hi Hiring Team,\n\n"
                f"I'm {name}, a {user_role} with {experience} experience working on {skills}."
            )
            body_bullets = [
                "Built backend services and APIs, improving request throughput and reliability.",
                "Delivered data-driven features using Python, SQL and ML pipelines (if applicable).",
            ]
        elif audience == "leadership":
            opener = (
                f"Hello {company or 'Hiring Team'},\n\n"
                f"My name is {name}, currently {user_role} at {user_company}. I have {experience} of experience "
                "leading cross-functional teams and delivering measurable outcomes."
            )
            body_bullets = [
                "Led product initiatives that improved customer retention and revenue.",
                "Built and mentored teams to ship on time and with quality.",
            ]
        else:  # non-technical
            opener = (
                f"Hi Hiring Team,\n\n"
                f"I'm {name}, a {user_role} with {experience} experience in areas related to {skills}."
            )
            body_bullets = [
                "Proven track record in stakeholder outreach, partnership development, and deal closure.",
                "Strong communication skills; able to translate product value to non-technical partners."
            ]

        # Tailor the value paragraph
        value_paragraph = ""
        if audience == "technical":
            value_paragraph = (
                "I noticed the role focuses on: " + (skills or "the listed skills") + ".\n"
                "I bring hands-on experience in these technologies and a pragmatic approach to shipping features. "
                "A couple of highlights:\n"
            )
        elif audience == "leadership":
            value_paragraph = (
                "I understand the role demands strategic leadership and delivery across teams. "
                "My focus is on outcome-driven execution and building high-performing teams. Highlights include:\n"
            )
        else:
            value_paragraph = (
                "From the description I see a need for strong relationship building and execution. "
                "I deliver measurable outcomes through focused outreach and partnership strategies. Highlights:\n"
            )

        # Add bullet points from body_bullets and job-specific info
        bullets_text = "\n".join([f"- {b}" for b in body_bullets])

        # Portfolio/links section
        links_section = self._format_links_section(portfolio_links)

        # Closing + CTA
        cta = (
            "If this sounds relevant, I'd love 15–20 minutes to discuss how I can contribute to your team. "
            "I'm flexible with timing — happy to work around your schedule."
        )

        signature_lines = [
            f"Best regards,",
            f"{name}",
            f"{user_role}" + (f" | {user_company}" if user_company else ""),
        ]
        if linkedin:
            signature_lines.append(f"LinkedIn: {linkedin}")
        if email:
            signature_lines.append(f"Email: {email}")
        if phone:
            signature_lines.append(f"Phone: {phone}")

        # Compose final email text
        email_parts = [
            f"Subject: {subject}",
            "",
            opener,
            "",
            value_paragraph,
            bullets_text,
            "",
        ]
        if description:
            email_parts.append("A brief snippet from the job description I noted:")
            email_parts.append(textwrap.fill(description[:600], width=88))
            email_parts.append("")
        if links_section:
            email_parts.append(links_section)
            email_parts.append("")
        email_parts.append(cta)
        email_parts.append("")
        email_parts.extend(signature_lines)

        final_email = "\n".join([p for p in email_parts if p is not None and p != ""])
        # tidy spacing
        final_email = reformat_whitespace(final_email)
        return final_email

def reformat_whitespace(text: str) -> str:
    # reduce repeated blank lines to max 1
    import re
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return text.strip()
