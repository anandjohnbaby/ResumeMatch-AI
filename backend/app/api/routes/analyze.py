from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models.schemas import AnalyzeResponse
from app.services.pdf_extractor import extract_text_from_pdf
from app.services.skill_matcher import match_skills
from app.utils.exceptions import PDFExtractionError, SkillExtractionError

router = APIRouter(prefix="/api", tags=["Resume Analysis"])

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_title: str = Form(...), 
    jd: str = Form(...)
):
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_bytes = await resume.read()

    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except PDFExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        result = match_skills(resume_text, jd, job_title)
    except SkillExtractionError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return result