import json
from groq import Groq
from app.config import settings
from app.utils.exceptions import SkillExtractionError
from app.services.skill_normalizer import normalize_skill

if settings.GROQ_API_KEY:
    groq_client = Groq(api_key=settings.GROQ_API_KEY)

# Extracts and normalizes technical skills from resume or JD text
def extract_skills_with_llm(text: str, context_type: str) -> list[str]:
    if not groq_client:
        raise SkillExtractionError("Internal configuration error")
    
    prompt = f"""Extract technical skills, tools, and technologies from the {context_type} below.

        Rules:
        - Only hard technical skills (e.g. Python, AWS, Docker, SQL)
        - Ignore soft skills, personal info, and generic phrases
        - Return JSON with a single key "skills" containing an array of strings

        {context_type}:
        {text[:4000]}"""

    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=settings.GROQ_LLM_MODEL,
            response_format={"type": "json_object"},
            temperature=0.0,
            max_tokens=1024,
        )
        skills = json.loads(response.choices[0].message.content).get("skills", [])
    except Exception as e:
        raise SkillExtractionError("Failed to extract skills from the document.")

    normalized = { normalize_skill(str(s)) for s in skills if isinstance(s, str)}

    return [
        s for s in normalized
        if s and len(s.split()) < 4
    ]