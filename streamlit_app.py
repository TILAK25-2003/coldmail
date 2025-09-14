import streamlit as st

st.title("COLDMAIL")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
# deploy_setup.py
import os
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required = ['streamlit', 'langchain_groq', 'langchain-community', 'chromadb', 'pandas']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def create_requirements_file():
    """Create a requirements.txt file"""
    requirements = """
streamlit>=1.28.0
langchain_groq>=0.1.0
langchain-community>=0.0.20
chromadb>=0.4.15
pandas>=2.0.0
python-dotenv>=1.0.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("Created requirements.txt")

def setup_environment():
    """Set up the environment for deployment"""
    print("Setting up deployment environment...")
    
    # Check for missing dependencies
    missing = check_dependencies()
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print("Please install them with: pip install " + " ".join(missing))
        return False
    
    # Create requirements file
    create_requirements_file()
    
    # Create .streamlit directory and config
    streamlit_dir = Path('.streamlit')
    streamlit_dir.mkdir(exist_ok=True)
    
    config = """
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
serverAddress = "0.0.0.0"
"""
    
    with open(streamlit_dir / 'config.toml', 'w') as f:
        f.write(config)
    
    print("Created Streamlit configuration")
    return True

def run_locally():
    """Run the app locally"""
    print("Starting Streamlit server locally...")
    print("Your app will be available at: http://localhost:8501")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    print("Streamlit App Deployment Setup")
    print("=" * 40)
    
    if setup_environment():
        print("\nSetup completed successfully!")
        print("\nTo run locally, use: streamlit run app.py")
        
        # Ask if user wants to run locally
        response = input("\nDo you want to run the app locally now? (y/n): ")
        if response.lower() == 'y':
            run_locally()
    else:
        print("\nSetup failed. Please check the errors above.")
