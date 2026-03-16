from pydantic import BaseModel, Field
class AnalyzeResponse(BaseModel):
    job_title: str
    score: float = Field(..., description="Match percentage 0–100")
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skill_count: int
    jd_skill_count: int