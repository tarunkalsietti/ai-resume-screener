# src/3_embed_similarity_score.py

import os
from pathlib import Path
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from extract_and_compare_skills import extract_skills
from utils import load_skills, load_text

# Load model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

# its for to get must and optional skills using the key words 
def split_jd_sections(jd_text):
    jd_lower = jd_text.lower()
    must_keywords = ["must have", "required skills", "requirements", "qualifications"]
    optional_keywords = ["nice to have", "preferred", "optional", "bonus"]

    must_pos, optional_pos = -1, -1

# loop through mustkeywords u found 
#look at book for better understanding og whow it works each block
    for kw in must_keywords:
        if kw in jd_lower:
            must_pos = jd_lower.find(kw)
            break

    for kw in optional_keywords:
        if kw in jd_lower:
            optional_pos = jd_lower.find(kw)
            break

    must_text = jd_text[must_pos:optional_pos] if must_pos != -1 and optional_pos > must_pos else jd_text
    optional_text = jd_text[optional_pos:] if optional_pos != -1 else ""

    return must_text.strip(), optional_text.strip()


def compute_similarity(text1, text2):
    emb1 = model.encode([text1])[0]
    emb2 = model.encode([text2])[0]
    score = cosine_similarity([emb1], [emb2])[0][0]
    return round(score * 100, 2)

# to load our predefined skill 
def load_skill_list(path):
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip().lower() for line in f if line.strip())

# to save files
def save_skills(skills, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(skills)))


def main():
    # === Paths ===
    base_dir = Path("output")
    skill_list_path = Path("data/skills_list.txt")
    jd_path = base_dir / "jd_text.txt"
    resume_skills_path = base_dir / "resume_skills.txt"

    must_out_path = base_dir / "jd_must_have_skills.txt"
    optional_out_path = base_dir / "jd_optional_skills.txt"
    score_out_path = base_dir / "weighted_score.txt"

    # === Load data ===
    jd_text = load_text(jd_path)
    resume_skills = load_skills(resume_skills_path)
    skill_set = load_skill_list(skill_list_path)
    print("\n YOUR RESUME SKILLS: ",",".join(resume_skills))
    # === Split JD ===
    must_text, optional_text = split_jd_sections(jd_text)

    # === Extract skills ===
    must_skills = extract_skills(must_text, skill_set)
    optional_skills = extract_skills(optional_text, skill_set)

    print("\n Extracted Must-Have Skills:")
    print(", ".join(must_skills) if must_skills else "None found.")

    print("\n Extracted Optional Skills:")
    print(", ".join(optional_skills) if optional_skills else "None found.")

    # === Save skills ===
    save_skills(must_skills, must_out_path)
    save_skills(optional_skills, optional_out_path)

    print(f"\n Saved must-have skills to {must_out_path}")
    print(f" Saved optional skills to {optional_out_path}")

    # === Compute similarity ===
    resume_text = " ".join(resume_skills)
    must_text_for_sim = " ".join(must_skills)
    optional_text_for_sim = " ".join(optional_skills)

    must_score = compute_similarity(resume_text, must_text_for_sim)
    optional_score = compute_similarity(resume_text, optional_text_for_sim)
    final_score = round(0.7 * must_score + 0.3 * optional_score, 2)

    print(f"\n Must-Have Match Score: {must_score}%")
    print(f" Optional Match Score: {optional_score}%")
    print(f"\n Final Weighted Match Score: {final_score}%")

    # === Save score ===
    with open(score_out_path, "w", encoding="utf-8") as f:
        f.write(f"Must-Have Skills Score: {must_score}%\n")
        f.write(f"Optional Skills Score: {optional_score}%\n")
        f.write(f"Final Weighted Match Score: {final_score}%\n")

    print(f"\n Saved score to {score_out_path}")


if __name__ == "__main__":
    main()
