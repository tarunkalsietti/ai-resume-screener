import os
from pathlib import Path
from .utils import load_skills, explain_match, load_text


def load_score_file(path):
    """
    Loads scores from weighted_score.txt and returns them as floats.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    must = float(lines[0].split(":")[1].replace("%", "").strip())
    optional = float(lines[1].split(":")[1].replace("%", "").strip())
    final = float(lines[2].split(":")[1].replace("%", "").strip())
    return must, optional, final


def final_verdict(score):
    """
    Returns a verdict based on final score.
    """
    if score >= 85:
        return " Excellent Match"
    elif score >= 70:
        return " Good Match"
    elif score >= 50:
        return " Moderate Match"
    else:
        return " Poor Match"


def main():
    print("\n📄 Generating Final Resume Screening Report...\n")

    # === Paths ===
    output_dir = Path("output")
    resume_pdf_name = "resume1.pdf"
    jd_pdf_name = "sample_jd.pdf"

    resume_skills_path = output_dir / "resume_skills.txt"
    must_have_path = output_dir / "jd_must_have_skills.txt"
    optional_path = output_dir / "jd_optional_skills.txt"
    score_path = output_dir / "weighted_score.txt"
    report_path = output_dir / "final_report.txt"

    # === Load skills ===
    resume_skills = load_skills(resume_skills_path)
    must_skills = load_skills(must_have_path) if must_have_path.exists() else set()
    optional_skills = load_skills(optional_path) if optional_path.exists() else set()

    # === Match skills ===
    matched_must, missing_must = explain_match(must_skills, resume_skills)
    matched_optional, missing_optional = explain_match(optional_skills, resume_skills)

    # === Load scores ===
    must_score, optional_score, final_score = load_score_file(score_path)
    verdict = final_verdict(final_score)

    # === Format Report ===
    report = f"""
📄 Resume Screening Final Report
===============================

🧾 Resume: {resume_pdf_name}
 Job Description: {jd_pdf_name}

------------------------------------------------------------
 Extracted Skills
------------------------------------------------------------
• Resume Skills       : {", ".join(sorted(resume_skills)) or "None"}
• Must-Have Skills    : {", ".join(sorted(must_skills)) or "None"}
• Optional Skills     : {", ".join(sorted(optional_skills)) or "None"}

------------------------------------------------------------
 Skill Matching
------------------------------------------------------------
 Matched Must-Have Skills   : {", ".join(sorted(matched_must)) or "None"}
 Missing Must-Have Skills   : {", ".join(sorted(missing_must)) or "None"}

 Matched Optional Skills    : {", ".join(sorted(matched_optional)) or "None"}
 Missing Optional Skills    : {", ".join(sorted(missing_optional)) or "None"}

------------------------------------------------------------
📊 Scores
------------------------------------------------------------
 Must-Have Match Score   : {must_score}%
 Optional Match Score    : {optional_score}%
 Final Weighted Score    : {final_score}%

 Verdict: {verdict}

 Report saved to: {report_path}
"""

    print(report)

    # === Save report ===
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print("\n Final report generated successfully!")


if __name__ == "__main__":
    main()
