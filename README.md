# 🚀 AI Job Application Agent

### Your Personal Career Copilot powered by Google Gemini

## 📖 Overview

The **AI Job Application Agent** is a sophisticated, modular command-line tool designed to automate and optimize the tedious process of job applications. 

Unlike simple script generators, this project uses an **Agentic Architecture**. It employs specialized AI agents (Ingestor, Analyzer, Strategist, Writer, Coach) that work together to analyze Job Descriptions (JDs), tailor resumes, draft personalized emails, and even prepare you for interviews.

Powered by **Google Gemini 2.5** (for reasoning) and **Google Embeddings** (for semantic matching), it ensures that every application is data-driven and highly personalized.

---

## ✨ Key Features

This tool offers a full suite of career automation features:

### 🔍 1. Intelligent JD Analyzer
*   Parses complex Job Descriptions to extract core skills, experience levels, and responsibilities.
*   Converts unstructured text into structured JSON data.

### ✂️ 2. Smart Resume Tailoring
*   Rewrites your "Professional Summary" to align with the specific job.
*   Optimizes bullet points with keywords found in the JD to pass ATS (Applicant Tracking Systems).

### 📊 3. Fitment Strategy Engine
*   **Vector Embeddings:** Uses mathematical vector comparison to calculate a "Match Score" (0-100%).
*   **Gap Analysis:** Identifies exactly which skills you are missing compared to the JD.

### ✍️ 4. Automated Content Generator
*   **Cover Letters:** Generates professional cover letters in seconds.
*   **Recruiter Emails:** Drafts cold outreach and follow-up emails ready to send.

### 🎤 5. Interview Coach Agent
*   Predicts **5 Technical Questions** based on the specific role.
*   Predicts **3 Behavioral Questions** based on your experience level.
*   Provides "Ideal Answer Strategies" for every question.

### 🖥️ 6. Full CLI Workflow
*   A beautiful command-line interface with progress bars and colored output.
*   One command (`process-all`) runs the entire workflow from start to finish.

---

## 🏗️ The "Agentic" Architecture

This project is built on a modular "Agent" system. Each module handles a specific domain of the job application process:

*   **Ingestion Agent:** Handles PDF/Text file reading and cleaning.
*   **Analyzer Agent:** The "Brain" that extracts meaning from raw text.
*   **Strategist Agent:** The "Mathematician" that computes similarity scores using Embeddings.
*   **Writer Agent:** The "Creative" that drafts emails and letters.
*   **Coach Agent:** The "Mentor" that prepares you for the interview.

---

## 🛠️ Tech Stack

*   **Language:** Python 3.10+
*   **LLM:** Google Gemini 2.5 Flash
*   **Embeddings:** Google Text Embedding 004
*   **CLI Interface:** Typer & Rich
*   **Data Handling:** PyPDF, JSON, YAML

---

## 🚀 Installation & Setup

Follow these steps to set up the agent on your local machine.

1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-job-agent.git
cd ai-job-agent

2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
# Windows
python -m venv venv
.\venv\Scripts\activate
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure API Keys
You need a Google Gemini API key (free tier available).
Create a file named .env in the root directory.
Add your key:
GOOGLE_API_KEY=your_actual_api_key_here

💻 Usage Guide
The tool is run via the command line. Ensure your input files (Resume PDF and Job Description Text) are inside the data/input/ folder.
🌟 The "One-Click" Workflow (Recommended)
Runs the full pipeline: Analysis -> Fitment -> Tailoring -> Writing -> Interview Prep.
python -m src.main process-all my_resume.pdf job_desc.txt

🔧 Individual Commands
Check Fitment Score:
python -m src.main check-fit my_resume.pdf job_desc.txt

Generate Cover Letter & Emails:
python -m src.main write-content my_resume.pdf job_desc.txt

Tailor Resume Content:
python -m src.main tailor-resume my_resume.pdf job_desc.txt

Prepare for Interview:
python -m src.main prepare-interview my_resume.pdf job_desc.txt


📂 Project Structure
ai-job-agent/
├── data/
│   ├── input/          # Place your Resume.pdf and JD.txt here
│   └── output/         # Generated results appear here
├── src/
│   ├── agents/         # The AI Workers (Ingestor, Writer, Coach, etc.)
│   ├── core/           # Configuration & LLM Connection
│   ├── templates/      # Prompts (YAML)
│   └── main.py         # CLI Entry Point
├── .env                # API Keys (Not shared)
├── requirements.txt    # Python Dependencies
└── README.md           # Documentation

Developed with ❤️ by [SHIVENDR]