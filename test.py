# test_app.py
import sys
import os

# Test the imports
try:
    from job_parser import extract_job_details
    print("✓ job_parser imported successfully")
    
    # Test the function
    test_url = "https://example.com/job"
    result = extract_job_details(test_url)
    print("✓ Job parser test passed:", result["role"])
    
except Exception as e:
    print("✗ job_parser failed:", e)

try:
    from portfolio_matcher import find_relevant_projects
    print("✓ portfolio_matcher imported successfully")
    
    # Test the function
    test_skills = ["Python", "JavaScript"]
    result = find_relevant_projects(test_skills)
    print("✓ Portfolio matcher test passed:", len(result), "projects found")
    
except Exception as e:
    print("✗ portfolio_matcher failed:", e)

try:
    from email_generator import generate_cold_email
    print("✓ email_generator imported successfully")
    
    # Test the function
    test_job_data = {
        "role": "Software Developer",
        "experience": "2+ years", 
        "skills": ["Python", "JavaScript"],
        "description": "Test job description"
    }
    test_projects = [{"document": "Test project", "metadata": {"links": "https://example.com"}}]
    result = generate_cold_email(test_job_data, test_projects)
    print("✓ Email generator test passed - email length:", len(result))
    
except Exception as e:
    print("✗ email_generator failed:", e)

print("\nAll tests completed!")