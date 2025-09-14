# setup.py
import subprocess
import sys

def install_dependencies():
    """Install required packages"""
    requirements = [
        "streamlit>=1.28.0",
        "langchain_groq>=0.1.0",
        "langchain>=0.1.0",
        "chromadb>=0.4.15",
        "pandas>=2.0.0",
        "python-dotenv>=1.0.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.28.0"
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")

if __name__ == "__main__":
    install_dependencies()