# utils.py

import os

def load_text(path):
    """
    Loads text content from a file.
    WHY: Used to load resume and JD text extracted earlier.
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def load_skills(path):
    """
    Loads list of skills from a file (one skill per line).
    Returns: set of skills
    """
    with open(path, 'r', encoding='utf-8') as f:
        return set(line.strip().lower() for line in f if line.strip())


def explain_match(jd_skills, resume_skills):
    """
    Returns matched and missing skills comparing resume to JD.
    Compares JD and resume skills and explains the match:
    - What matched
    - What was missing (from JD perspective)

    Returns: matched, missing
    """
    matched = jd_skills.intersection(resume_skills)
    missing = jd_skills - resume_skills
    return matched, missing
