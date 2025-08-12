# # app.py
# # python -m streamlit run app\app.py
# # app.py
# # wen u import files from other folder put that ofldername.file name 
# # and when  u import from same folder just use .file name(dont forgot the .)
# # if u dont create folder just do import file_name
# import streamlit as st
# st.set_page_config(page_title="Resume Matcher AI", layout="centered")
# # Add root to sys.path to allow imports from src/


import streamlit as st
st.set_page_config(page_title="Resume Matcher AI", layout="centered")
import sys
import os
from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import load_skills, explain_match, load_text
from src.extract_text import extract_text_from_pdf
from src.extract_and_compare_skills import extract_skills, load_skill_list
from src.embed_similarity_score import compute_similarity, split_jd_sections
from src.llm import generate_suggestions_and_resources  # ✅ new import

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

OUTPUT_DIR = Path("output")
SKILL_LIST_PATH = Path("data/skills_list.txt")
OUTPUT_DIR.mkdir(exist_ok=True)

st.title("📄 AI Resume Matcher")

st.markdown("""
Upload your **Resume PDF** and **Job Description PDF**, and let AI score how well your resume matches the JD.
""")

tab1, tab2 = st.tabs(["📄 Match Single Resume", "📊 Rank Multiple Resumes"])

with tab1:
    jd_pdf = st.file_uploader("📌 Upload Job Description (PDF)", type=["pdf"], key="jd")
    resume_pdf = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"], key="resume")

    if jd_pdf and resume_pdf:
        jd_path = OUTPUT_DIR / "jd_text.txt"
        resume_path = OUTPUT_DIR / "resume_text.txt"

        with open("temp_jd.pdf", "wb") as f:
            f.write(jd_pdf.read())
        with open("temp_resume.pdf", "wb") as f:
            f.write(resume_pdf.read())

        jd_text = extract_text_from_pdf("temp_jd.pdf")
        resume_text = extract_text_from_pdf("temp_resume.pdf")

        jd_path.write_text(jd_text, encoding="utf-8")
        resume_path.write_text(resume_text, encoding="utf-8")

        skill_set = load_skill_list(SKILL_LIST_PATH)
        resume_skills = extract_skills(resume_text, skill_set)
        must_text, optional_text = split_jd_sections(jd_text)
        must_skills = extract_skills(must_text, skill_set)
        optional_skills = extract_skills(optional_text, skill_set)

        matched_must, missing_must = explain_match(must_skills, resume_skills)
        matched_opt, missing_opt = explain_match(optional_skills, resume_skills)

        resume_text_combined = " ".join(resume_skills)
        must_text_combined = " ".join(must_skills)
        optional_text_combined = " ".join(optional_skills)

        must_score = compute_similarity(resume_text_combined, must_text_combined)
        optional_score = compute_similarity(resume_text_combined, optional_text_combined) if optional_text_combined else 0
        final_score = round(0.7 * must_score + 0.3 * optional_score, 2)

        st.subheader("🔍 Extracted Skills")
        st.markdown(f"**Resume Skills:** {', '.join(sorted(resume_skills)) or 'None'}")
        st.markdown(f"**Must-Have JD Skills:** {', '.join(sorted(must_skills)) or 'None'}")
        st.markdown(f"**Optional JD Skills:** {', '.join(sorted(optional_skills)) or 'None'}")

        st.subheader("📊 Skill Matching")
        st.markdown(f"✅ Matched Must-Have: {', '.join(sorted(matched_must)) or 'None'}")
        st.markdown(f"❌ Missing Must-Have: {', '.join(sorted(missing_must)) or 'None'}")
        st.markdown(f"✅ Matched Optional: {', '.join(sorted(matched_opt)) or 'None'}")
        st.markdown(f"❌ Missing Optional: {', '.join(sorted(missing_opt)) or 'None'}")

        st.subheader("📈 Scores")
        st.metric("Must-Have Match", f"{must_score:.2f}%")
        st.metric("Optional Match", f"{optional_score:.2f}%")
        st.metric("Final Weighted Score", f"{final_score:.2f}%")

        # ✅ New AI Suggestions
        missing_all = set(missing_must) | set(missing_opt)
        st.subheader("💡 AI-Powered Learning Suggestions")
        suggestions_text = generate_suggestions_and_resources(list(missing_all))
        st.markdown(suggestions_text)

        os.remove("temp_jd.pdf")
        os.remove("temp_resume.pdf")
    else:
        st.info("👆 Upload both Resume and JD PDFs to begin analysis.")

with tab2:
    st.markdown("Upload a JD and multiple resumes to rank them based on skill and semantic match.")
    jd_file = st.file_uploader("📌 Upload JD (PDF)", type="pdf", key="multi_jd")
    resume_files = st.file_uploader("📄 Upload Resumes (Multiple PDFs)", type="pdf", accept_multiple_files=True)

    if jd_file and resume_files:
        with open("temp_multi_jd.pdf", "wb") as f:
            f.write(jd_file.read())
        jd_text = extract_text_from_pdf("temp_multi_jd.pdf")
        skill_set = load_skill_list(SKILL_LIST_PATH)
        jd_skills = extract_skills(jd_text, skill_set)

        rows = []
        for file in resume_files:
            file_path = f"temp_{file.name}"
            with open(file_path, "wb") as f:
                f.write(file.read())
            resume_text = extract_text_from_pdf(file_path)
            resume_skills = extract_skills(resume_text, skill_set)

            matched = resume_skills.intersection(jd_skills)
            missing = jd_skills.difference(resume_skills)
            skill_match = round(len(matched) / len(jd_skills) * 100, 2) if jd_skills else 0
            semantic = compute_similarity(resume_text, jd_text)

            if not matched:
                summary = "❌ No relevant skills found."
            elif len(missing) <= 2:
                summary = "✅ Strong match – almost all skills present."
            elif len(missing) <= 5:
                summary = "⚠️ Moderate match – some skills missing."
            else:
                summary = "🔴 Weak match – many important skills missing."

            rows.append({
                "Resume": file.name,
                "Skill Match (%)": skill_match,
                "Semantic Match (%)": semantic,
                "Matched Skills": ", ".join(sorted(matched)),
                "Missing Skills": ", ".join(sorted(missing)),
                "Summary": summary
            })

            os.remove(file_path)

        df = pd.DataFrame(rows)
        df.sort_values(by=["Semantic Match (%)", "Skill Match (%)"], ascending=False, inplace=True)
        st.dataframe(df)
        os.remove("temp_multi_jd.pdf")
