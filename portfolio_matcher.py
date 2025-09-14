def find_relevant_projects(job_text, portfolio_projects):
    """Find relevant portfolio projects based on job description"""
    if not job_text or not portfolio_projects:
        return []
    
    job_lower = job_text.lower()
    relevant_projects = []
    
    for project in portfolio_projects:
        relevance_score = 0
        
        # Check project skills
        for skill in project.get('skills', []):
            if skill.lower() in job_lower:
                relevance_score += 2
        
        # Check project description
        project_desc = project.get('description', '').lower()
        if any(word in job_lower for word in project_desc.split()[:10]):  # First 10 words
            relevance_score += 1
        
        # Check project name
        project_name = project.get('name', '').lower()
        if any(word in job_lower for word in project_name.split()):
            relevance_score += 1
        
        if relevance_score > 0:
            project_with_score = project.copy()
            project_with_score['relevance_score'] = relevance_score
            relevant_projects.append(project_with_score)
    
    # Sort by relevance score
    relevant_projects.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    return relevant_projects[:3]  # Return top 3 most relevant

# Sample portfolio
SAMPLE_PORTFOLIO = [
    {
        'name': 'Web Application',
        'description': 'Built a responsive web app with React and Node.js',
        'skills': ['React', 'Node.js', 'JavaScript', 'CSS', 'HTML'],
        'url': 'https://github.com/example/webapp'
    },
    {
        'name': 'Data Analysis Project',
        'description': 'Python data analysis and visualization project',
        'skills': ['Python', 'Pandas', 'Matplotlib', 'Data Analysis', 'SQL'],
        'url': 'https://github.com/example/data-project'
    }
]
