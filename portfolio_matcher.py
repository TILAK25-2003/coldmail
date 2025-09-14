# portfolio_matcher.py
import pandas as pd
import os

def load_portfolio_data():
    """Load portfolio data from CSV or create default if not exists"""
    csv_path = "my_portfolio.csv"
    
    # Create default portfolio if file doesn't exist
    if not os.path.exists(csv_path):
        default_data = {
            "Techstack": [
                "React, Node.js, MongoDB",
                "Python, Django, PostgreSQL",
                "Java, Spring Boot, MySQL",
                "JavaScript, React, Node.js",
                "Python, Machine Learning, TensorFlow",
                "AWS, Docker, Kubernetes",
                "React Native, Firebase, JavaScript",
                "Vue.js, Express, MongoDB"
            ],
            "Links": [
                "https://example.com/react-project",
                "https://example.com/python-project",
                "https://example.com/java-project",
                "https://example.com/js-project",
                "https://example.com/ml-project",
                "https://example.com/devops-project",
                "https://example.com/mobile-project",
                "https://example.com/vue-project"
            ]
        }
        df = pd.DataFrame(default_data)
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path)
    
    return df

def find_relevant_projects(skills, n_results=3):
    """Find relevant projects based on skills using simple text matching"""
    try:
        df = load_portfolio_data()
        
        # Convert skills to a list if it's a string
        if isinstance(skills, str):
            skills = [skill.strip() for skill in skills.split(',')]
        
        # Score each project based on skill matches
        scored_projects = []
        for index, row in df.iterrows():
            score = 0
            techstack = str(row['Techstack']).lower()
            
            for skill in skills:
                skill_lower = str(skill).lower().strip()
                if skill_lower in techstack:
                    score += 3
                elif any(skill_lower in word for word in techstack.split()):
                    score += 1
            
            scored_projects.append({
                'score': score,
                'document': row['Techstack'],
                'metadata': {'links': row['Links']}
            })
        
        # Sort by score and return top n results
        scored_projects.sort(key=lambda x: x['score'], reverse=True)
        top_projects = scored_projects[:n_results]
        
        # Format results
        relevant_projects = []
        for project in top_projects:
            relevant_projects.append({
                "document": project['document'],
                "metadata": project['metadata']
            })
        
        return relevant_projects
        
    except Exception as e:
        # Fallback: return default projects
        return [
            {"document": "Python, Django, PostgreSQL", "metadata": {"links": "https://example.com/python-project"}},
            {"document": "React, Node.js, MongoDB", "metadata": {"links": "https://example.com/react-project"}}
        ]

