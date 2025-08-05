# src/1_extract_text.py

import fitz  # PyMuPDF
import os
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """
     Extracts and returns full text from a PDF file using PyMuPDF.
    Returns- Extracted text content.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()


def save_text(text, path):

    # Saves given text content to a file.
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    # === Define paths ===
    resume_pdf = Path("data/resumes/resume1.pdf")
    jd_pdf = Path("data/sample_jd.pdf")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    resume_text_path = output_dir / "resume_text.txt"
    jd_text_path = output_dir / "jd_text.txt"

    # === Extract text from PDFs ===
    resume_text = extract_text_from_pdf(resume_pdf)
    jd_text = extract_text_from_pdf(jd_pdf)

    # === Save extracted text ===
    save_text(resume_text, resume_text_path)
    save_text(jd_text, jd_text_path)

    # === Show preview ===
    print("\n Resume Text Preview:")
    print(resume_text[:500])

    print("\n Job Description Text Preview:")
    print(jd_text[:500])

    print(f"\n Text files saved to '{resume_text_path}' and '{jd_text_path}'")


if __name__ == "__main__":
    main()
