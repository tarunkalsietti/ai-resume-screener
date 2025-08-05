💼 AI Resume Screener
[![View App](https://img.shields.io/badge/Live%20App-Streamlit-success?style=for-the-badge&logo=streamlit)](https://ai-resume-screener-tarunkalisetti.streamlit.app/)
👤 Author: Tarun Kalisetti
📫 LinkedIn • GitHub

An AI-powered application that screens resumes against job descriptions using Natural Language Processing and semantic similarity.

Built using Python, spaCy, Sentence-BERT, and Streamlit.

⚙️ Features
 Extracts text from Resume and Job Description PDFs
 Skill extraction using spaCy and a custom skill list
 Separates must-have and optional skills from the JD
 Calculates semantic similarity using Sentence-BERT
 Computes weighted match scores
 Provides verdicts (Excellent, Good, Moderate, Poor)
 Supports batch ranking of multiple resumes
 Clean, interactive Streamlit UI

🛠️ Tech Stack
🐍 Python

🌐 Streamlit

🧬 spaCy

🧠 Sentence-Transformers (SBERT)

📈 scikit-learn

📊 pandas

📄 PyMuPDF

📂 Folder Structure

ai-resume-screener/
├── app/              # Streamlit app entry point
├── data/             # skills_list.txt + sample PDFs
├── output/           # Output files (results, reports)
├── src/              # Core Python logic scripts
├── requirements.txt  # Python dependencies
├── .gitignore
└── README.md


🧪 How to Run Locally

# 1. Clone the repository
git clone https://github.com/tarunkalsietti/ai-resume-screener.git
cd ai-resume-screener

# 2. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 3. Run the Streamlit app
streamlit run app/app.py


🌐 Live Demo👉  (https://ai-resume-screener-tarunkalisetti.streamlit.app/)
 

📢 About the Project
This app is designed to bridge the gap between job descriptions and resumes. It helps job seekers understand how well their resume matches a JD, and aids recruiters in screening candidates more efficiently.
