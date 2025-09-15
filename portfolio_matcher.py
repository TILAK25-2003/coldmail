import pandas as pd
import os
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load a lightweight sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

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
        print("Created default portfolio CSV file")
    else:
        df = pd.read_csv(csv_path)
    
    return df

def find_relevant_projects(job_skills, user_skills, n_results=3):
    """Find relevant projects based on skills using semantic similarity"""
    df = load_portfolio_data()
    
    # Combine job skills and user skills for better matching
    query_skills = list(set(job_skills + user_skills))
    query_text = " ".join(query_skills) if isinstance(query_skills, list) else str(query_skills)
    
    # Encode the query
    query_embedding = model.encode(query_text, convert_to_tensor=True)
    
    # Encode all portfolio items
    portfolio_items = df["Techstack"].astype(str).tolist()
    portfolio_embeddings = model.encode(portfolio_items, convert_to_tensor=True)
    
    # Calculate similarity
    similarities = util.pytorch_cos_sim(query_embedding, portfolio_embeddings)[0]
    
    # Get top n results
    top_indices = np.argsort(similarities.cpu().numpy())[-n_results:][::-1]
    
    # Format results
    relevant_projects = []
    for idx in top_indices:
        relevant_projects.append({
            "document": portfolio_items[idx],
            "metadata": {"links": df.iloc[idx]["Links"]}
        })
    
    return relevant_projects
