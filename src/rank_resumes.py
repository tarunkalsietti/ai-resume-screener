# rank_resumes.py

import os
import pandas as pd
from .extract_text import extract_text_from_pdf
from .utils import load_skills
from .extract_and_compare_skills import extract_skills
from .embed_similarity_score import compute_similarity


def summarize_match(matched, missing):
    """
    Generate a human-readable summary based on skill match.
    """
    if not matched:
        return " No relevant skills found."
    if len(missing) <= 2:
        return " Strong match – almost all skills present."
    elif len(missing) <= 5:
        return " Moderate match – some skills missing."
    else:
        return " Weak match – many important skills missing."


def main():
    print("\n Ranking Resumes Based on JD Matching...\n")

    # === Load known skills and JD text ===
    skill_set = load_skills("data/skills_list.txt")
    jd_text = extract_text_from_pdf("data/sample_jd.pdf")
    jd_skills = extract_skills(jd_text, skill_set)

    report_rows = []

    # === Loop through all resumes ===
    resumes_dir = "data/resumes"
    for filename in os.listdir(resumes_dir):
        if filename.endswith(".pdf"):
            resume_path = os.path.join(resumes_dir, filename)
            resume_text = extract_text_from_pdf(resume_path)
            resume_skills = extract_skills(resume_text, skill_set)

            # === Skill match ===
            matched_skills = resume_skills.intersection(jd_skills)
            missing_skills = jd_skills.difference(resume_skills)

            skill_match_percent = round(len(matched_skills) / len(jd_skills) * 100, 2) if jd_skills else 0
            semantic_similarity = compute_similarity(resume_text, jd_text)
            summary = summarize_match(matched_skills, missing_skills)

            report_rows.append({
                "Resume Name": filename,
                "Skill Match (%)": skill_match_percent,
                "Semantic Match (%)": semantic_similarity,
                "Matched Skills": ", ".join(sorted(matched_skills)),
                "Missing Skills": ", ".join(sorted(missing_skills)),
                "Summary": summary
            })

    # === Create DataFrame and Sort ===
    df = pd.DataFrame(report_rows)
    df.sort_values(by=["Semantic Match (%)", "Skill Match (%)"], ascending=False, inplace=True)

    # === Save to CSV ===
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "report.csv")
    df.to_csv(output_file, index=False,float_format="%.2f")

    print(" Resume Ranking Complete!")
    print(f" Report saved to: {output_file}\n")
    print(df[["Resume Name", "Skill Match (%)", "Semantic Match (%)", "Summary"]])


if __name__ == "__main__":
    main()
