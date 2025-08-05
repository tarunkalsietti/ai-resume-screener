*# AI Resume Screener*



*An AI-powered application that screens resumes against job descriptions using NLP and semantic similarity.*  

*Built using Python, spaCy, Sentence-BERT, and Streamlit.*



*---*



*##  Features*



*- Extracts text from JD and Resume PDFs*

*- Skill extraction using spaCy and predefined skill list*

*- Separates \*\*must-have\*\* and \*\*optional\*\* skills from JD*

*- Calculates semantic similarity using Sentence-BERT*

*- Computes weighted match scores*

*- Provides verdicts (Excellent, Good, Moderate, Poor)*

*- **B**atch ranking of multiple resumes*

*- Interactive Streamlit UI*



*---*



*## 🛠️ Tech Stack*



*- Python*

*- Streamlit*

*- spaCy*

*- Sentence-Transformers (SBERT)*

*- scikit-learn*

*- pandas*

*- PyMuPDF*



*---*



*## 📂 Folder Structure*

*AI Resume Screener/*

*├── app/ # Streamlit app.py*

*├── data/ # skills\_list.txt and sample PDFs*

*├── output/ # Generated output files*

*├── # All Python logic scripts*

*├── requirements.txt*

*├── .gitignore*

*└── README.md*









*---*



*## 🧪 How to Run Locally*



*1. Clone the repo:*

*```bash*

*git clone https://github.com/tarunkalsietti/ai-resume-screener.git*

*cd ai-resume-screener*







*2.Install dependencies:*



*pip install -r requirements.txt*

*python -m spacy download en\_core\_web\_sm*



*3.Run the app:*

*streamlit run app/app.py*







