# src/2_extract_and_compare_skills.py

import spacy
import os
from pathlib import Path
# Made filenames and paths easier to manage using pathlib.
from .utils import load_text, explain_match   
# loading from utils 

# Load spaCy English NLP model
nlp = spacy.load("en_core_web_sm")


def extract_skills(text, skill_set):
    """
    Extracts skills from input text using spaCy's tokens and noun chunks.
    text = Input resume or JD text.
    skill_set (set): Set of known skills to match against.
     it Returns:  set: Extracted skills present in the given text.
    """
    doc = nlp(text)

    # Extract tokens (e.g., "Python", "Excel")
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]

    # Extract noun phrases (e.g., "data analysis")
    noun_chunks = [chunk.text.lower().strip() for chunk in doc.noun_chunks]

    all_phrases = set(tokens + noun_chunks)
    matched_skills = all_phrases.intersection(skill_set)

    return matched_skills



# to load skills from skillset that we predefined it will clear extra  white spaces and  load that skills
def load_skill_list(path):
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip().lower() for line in f if line.strip())

# to save our new files
def save_skills(skills, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(skills)))


def main():
    #  Paths 
    base_dir = Path("output")
    base_dir.mkdir(exist_ok=True)
    skill_list_path = Path("data/skills_list.txt")

    resume_text_path = base_dir / "resume_text.txt"
    jd_text_path = base_dir / "jd_text.txt"

    resume_skills_path = base_dir / "resume_skills.txt"
    jd_skills_path = base_dir / "jd_skills.txt"
    report_path = base_dir / "skill_match_explanation.txt"

    # === Load skills list and text content ===
    skill_set = load_skill_list(skill_list_path)
    resume_text = load_text(resume_text_path)
    jd_text = load_text(jd_text_path)

    # === Extract skills ===
    resume_skills = extract_skills(resume_text, skill_set)
    jd_skills = extract_skills(jd_text, skill_set)

    # === Save extracted skills ===
    save_skills(resume_skills, resume_skills_path)
    save_skills(jd_skills, jd_skills_path)

    print("\n Extracted Skills :")
    print("• Resume:", resume_skills)
    print("• JD:", jd_skills)

    # Match and explain 
    matched, missing = explain_match(jd_skills, resume_skills)

    #Save explanation report 
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(" Matched Skills :\n" + "\n".join(sorted(matched)) + "\n\n")
        f.write(" Missing JD Skills :\n" + "\n".join(sorted(missing)))

    print("\n Skill Match Report:")
    print("• Matched :", matched)
    print("• Missing :", missing)
    print(f"\n  Report saved to  : {report_path}")


if __name__ == "__main__":
    main()






    # OR can do like this saving if not path usage

    # # Save extracted skills and print them
    # os.makedirs("output", exist_ok=True)
    # with open("output/resume_skills.txt", "w", encoding="utf-8") as f:
    #     f.write("\n".join(resume_skills))
    # with open("output/jd_skills.txt", "w", encoding="utf-8") as f:
    #     f.write("\n".join(jd_skills))

    