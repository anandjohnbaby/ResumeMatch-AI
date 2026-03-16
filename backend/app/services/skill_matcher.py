from app.models.schemas import AnalyzeResponse
from app.services.skill_extractor import extract_skills_with_llm
from app.services.skill_normalizer import normalize_skill

def match_skills(resume_text: str, jd_text: str, job_title: str) -> AnalyzeResponse:
    jd_skills = extract_skills_with_llm(jd_text, "Job Description")
    resume_skills = extract_skills_with_llm(resume_text, "Resume")

    if not jd_skills:
        return AnalyzeResponse(
            job_title=job_title,
            score=0.0,
            matched_skills=[],
            missing_skills=[],
            resume_skill_count=len(resume_skills),
            jd_skill_count=0,
        )

    matched = jd_skills.intersection(resume_skills)
    missing = jd_skills.difference(resume_skills)
    score = round((len(matched) / len(jd_skills)) * 100, 2)

    return AnalyzeResponse(
        job_title=job_title,
        score=score,
        matched_skills=sorted(matched),
        missing_skills=sorted(missing),
        resume_skill_count=len(resume_skills),
        jd_skill_count=len(jd_skills),
    )