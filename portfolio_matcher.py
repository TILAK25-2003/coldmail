def find_relevant_projects(job_text, portfolio_projects):
    """Find relevant portfolio projects based on job description"""
    if not job_text or not portfolio_projects:
        return []
    
    job_lower = job_text.lower()
    relevant_projects = []
    
    for project in portfolio_projects:
        # Check if any project skills are in job description
        for skill in project.get('skills', []):
            if skill.lower() in job_lower:
                relevant_projects.append(project)
                break
    
    return relevant_projects

# Sample portfolio
SAMPLE_PORTFOLIO = [
    {
        'name': 'Web Application',
        'description': 'Built a responsive web app with React',
        'skills': ['React', 'JavaScript', 'CSS', 'HTML'],
        'url': 'https://github.com/example/webapp'
    },
    {
        'name': 'Data Project',
        'description': 'Python data analysis project',
        'skills': ['Python', 'Pandas', 'Data Analysis'],
        'url': 'https://github.com/example/data-project'
    }
]
