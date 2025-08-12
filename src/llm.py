import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # Loads .env file

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_suggestions_and_resources(missing_skills):
    """
    Given a list of missing skills, ask Groq LLM for:
    - How to improve in each skill
    - Recommended resources (links, free courses, etc.)
    """
    if not missing_skills:
        return "🎉 No missing skills! You're fully aligned with the job requirements."

    prompt = f"""
    You are an AI career coach. The user is missing these skills: {", ".join(missing_skills)}.
    For each skill:
    1. Rank its importance for a typical job that requires it (High / Medium / Low).
    2. Suggest whether it's Beginner, Intermediate, or Expert level for the job.
    3. Give a short, actionable improvement tip (1 sentence).
    4. Provide 3 high-quality learning resources (include clickable URLs).
    5. Suggest a 30-day plan to start learning.

    Format your response as markdown with clear headings for each skill.
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Or another Groq-supported model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()

