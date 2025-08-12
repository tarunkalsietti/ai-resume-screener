# _skill_matcher.py

import os
# make sure u remove the . while importing files to run here even if u dont it will sill run in app.py but codes dont run here
from .utils import load_skills, explain_match



if __name__ == "__main__":
    #  Load extracted skills
    resume_skills = load_skills("output/resume_skills.txt")
    jd_skills = load_skills("output/jd_skills.txt")

    # Optional: Also load separated must-have and optional skills if saved
    must_have_path = "output/jd_must_have_skills.txt"
    optional_path = "output/jd_optional_skills.txt"

    must_have_skills = load_skills(must_have_path) if os.path.exists(must_have_path) else set()
    optional_skills = load_skills(optional_path) if os.path.exists(optional_path) else set()

    #  Compare: Resume vs JD (All)
    matched_all, missing_all = explain_match(jd_skills, resume_skills)

    #  Compare: Resume vs Must-Have
    matched_must, missing_must = explain_match(must_have_skills, resume_skills)

    #  Compare: Resume vs Optional
    matched_optional, missing_optional = explain_match(optional_skills, resume_skills)

    #  Print summary
    print("\n Matching Skills Report")
    print(" Matched All JD Skills:", matched_all)
    print(" Missing All JD Skills:", missing_all)
    print("\n Matched Must-Have Skills:", matched_must)
    print(" Missing Must-Have Skills:", missing_must)
    print("\n Matched Optional Skills:", matched_optional)
    print(" Missing Optional Skills:", missing_optional)

    #  Save to file
    with open("output/skill_match_summary.txt", "w", encoding="utf-8") as f:
        f.write(" Matched JD Skills:\n" + "\n".join(sorted(matched_all)) + "\n\n")
        f.write(" Missing JD Skills:\n" + "\n".join(sorted(missing_all)) + "\n\n")

        f.write(" Matched Must-Have Skills:\n" + "\n".join(sorted(matched_must)) + "\n\n")
        f.write(" Missing Must-Have Skills:\n" + "\n".join(sorted(missing_must)) + "\n\n")

        f.write(" Matched Optional Skills:\n" + "\n".join(sorted(matched_optional)) + "\n\n")
        f.write(" Missing Optional Skills:\n" + "\n".join(sorted(missing_optional)) + "\n")

    print("\n Saved skill match summary to output/skill_match_summary.txt")
