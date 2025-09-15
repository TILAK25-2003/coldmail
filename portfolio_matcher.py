import chromadb
import pandas as pd
import uuid
import os

# Initialize ChromaDB
def initialize_vectorstore():
    """Initialize or load the vector store"""
    client = chromadb.PersistentClient(path="vectorstore")
    collection = client.get_or_create_collection(name="portfolio")
    return collection

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

def setup_portfolio_collection():
    """Set up the portfolio collection in ChromaDB"""
    collection = initialize_vectorstore()
    df = load_portfolio_data()
    
    # Only add documents if collection is empty
    if collection.count() == 0:
        docs = df["Techstack"].astype(str).tolist()
        metadatas = [{"links": str(link)} for link in df["Links"].tolist()]
        ids = [str(uuid.uuid4()) for _ in range(len(docs))]
        
        collection.add(
            documents=docs,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(docs)} portfolio items to vector store")
    
    return collection

def find_relevant_projects(job_skills, user_skills, n_results=3):
    """Find relevant projects based on skills"""
    collection = setup_portfolio_collection()
    
    # Combine job skills and user skills for better matching
    query_skills = list(set(job_skills + user_skills))
    
    # Create a query from skills
    query_text = " ".join(query_skills) if isinstance(query_skills, list) else str(query_skills)
    
    # Query the collection
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Format results
    relevant_projects = []
    for i, doc in enumerate(results['documents'][0]):
        relevant_projects.append({
            "document": doc,
            "metadata": results['metadatas'][0][i]
        })
    
    return relevant_projects
