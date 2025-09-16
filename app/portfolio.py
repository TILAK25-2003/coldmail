import pandas as pd
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Portfolio:
    def __init__(self, file_path=None):
        # Use a relative path if no file path is provided
        if file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "resource", "my_portfolio.csv")
        
        self.file_path = file_path
        
        # Check if file exists
        if not os.path.exists(file_path):
            # Create a sample portfolio if file doesn't exist
            self._create_sample_portfolio(file_path)
        
        self.data = pd.read_csv(file_path)
        self.vectorizer = TfidfVectorizer()
        self._build_similarity_index()
    
    def _create_sample_portfolio(self, file_path):
        """Create a sample portfolio file if it doesn't exist"""
        sample_data = {
            "Techstack": [
                "React, Node.js, MongoDB",
                "Angular, .NET, SQL Server",
                "Vue.js, Ruby on Rails, PostgreSQL",
                "Python, Django, MySQL",
                "Java, Spring Boot, Oracle",
                "JavaScript, HTML, CSS",
                "React Native, Firebase",
                "Flutter, Dart",
                "Machine Learning, Python, TensorFlow",
                "Data Analysis, SQL, Python"
            ],
            "Links": [
                "https://example.com/react-portfolio",
                "https://example.com/angular-portfolio",
                "https://example.com/vue-portfolio",
                "https://example.com/python-portfolio",
                "https://example.com/java-portfolio",
                "https://example.com/javascript-portfolio",
                "https://example.com/reactnative-portfolio",
                "https://example.com/flutter-portfolio",
                "https://example.com/ml-portfolio",
                "https://example.com/data-portfolio"
            ]
        }
        sample_df = pd.DataFrame(sample_data)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        sample_df.to_csv(file_path, index=False)
    
    def _build_similarity_index(self):
        """Build TF-IDF vectors for portfolio items"""
        self.portfolio_texts = self.data["Techstack"].tolist()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.portfolio_texts)
    
    def query_links(self, skills):
        """Find most relevant portfolio items based on skills using TF-IDF cosine similarity"""
        if not skills or not skills.strip():
            # Return random items if no skills provided
            return self.data.sample(n=min(2, len(self.data))).to_dict('records')
        
        # Vectorize the query skills
        query_vec = self.vectorizer.transform([skills])
        
        # Calculate cosine similarities
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Get top 2 most similar items
        top_indices = similarities.argsort()[-2:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Only include if similarity is above threshold
                results.append({
                    "links": self.data.iloc[idx]["Links"],
                    "techstack": self.data.iloc[idx]["Techstack"],
                    "similarity": float(similarities[idx])
                })
        
        # Fallback to random items if no good matches found
        if not results:
            random_items = self.data.sample(n=min(2, len(self.data)))
            for _, row in random_items.iterrows():
                results.append({
                    "links": row["Links"],
                    "techstack": row["Techstack"],
                    "similarity": 0.0
                })
        
        return results
