# Cold Email Generator

A Streamlit web application that generates personalized cold emails for job applications based on parsed job descriptions and your portfolio.

## Features

- Extract key information from job posting URLs
- Match job requirements with your portfolio projects
- Generate personalized cold emails using AI
- Clean, user-friendly interface

## Setup

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate






## How the Cold Email Generator Works (In Simple Steps)

### 🎯 **What It Does**
This tool helps you create personalized emails to send to companies when you're applying for jobs. Instead of sending the same generic email to everyone, it creates a custom email that matches exactly what the job is looking for.

---

### 🔄 **The Step-by-Step Process**

#### **Step 1: You Provide the Job Link**
- You copy the web address of a job you're interested in (like from LinkedIn, company career pages, etc.)
- You paste this web address into the tool

#### **Step 2: The Tool "Reads" the Job Description**
- The tool visits the job webpage and reads all the text
- It looks for important information like:
  - What job title they're hiring for
  - What skills they want
  - How much experience they require
  - What the job involves day-to-day

#### **Step 3: It Checks Your Portfolio**
- The tool looks at your previous work (your "portfolio")
- It tries to find projects you've done that match what the job requires
- For example, if the job needs "Python programming," it looks for your Python projects

#### **Step 4: It Writes Your Email**
- Using all this information, the tool writes a custom email for you
- It includes:
  - A polite introduction
  - Mention of the specific job you're applying for
  - Highlights of your relevant skills and projects
  - A professional closing with a request for an interview

#### **Step 5: You Get Your Ready-to-Use Email**
- The tool shows you the complete email
- You can copy it, make any small adjustments if needed, and send it directly to the employer

---

### 🧩 **The "Magic" Behind the Scenes**

Think of it like having three assistants working together:

1. **The Researcher** - Goes to the job website and gathers all the important details about what the company wants

2. **The Matchmaker** - Looks through your past work and finds the projects that best fit what the job requires

3. **The Writer** - Takes all this information and writes a professional, personalized email that shows why you're perfect for the job

---

### ⏱️ **Time Saved**
What might take you 30-60 minutes to do manually (reading the job description, reviewing your portfolio, crafting a custom email) now takes just a few minutes.

### 🎨 **Why It Works Better**
- **Personalized**: Every email is unique to the specific job
- **Relevant**: Highlights exactly what the employer is looking for
- **Professional**: Uses appropriate business language and formatting
- **Efficient**: Saves you time while producing high-quality emails

---

### 📋 **What You Need to Provide**
1. The web address of the job you want to apply for
2. Information about your skills and past projects (this can be added beforehand)
3. A Groq API key (this is like a password that lets the tool use the advanced writing AI)

That's it! The tool handles the rest, giving you a ready-to-send email that's tailored specifically to each job opportunity you're interested in.
