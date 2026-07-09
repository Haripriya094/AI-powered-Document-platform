from fastapi import APIRouter, UploadFile, File, Form
from backend.core.handlers.project_handler import InterviewManagement
from backend.constants.app_constants import APIS
from backend.utills.logger_utill import logger

interview_router = APIRouter()
handler = InterviewManagement()

@interview_router.post(APIS.interview_analyze, tags=["interview"])
async def analyze_interview(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),
    user_id: str = Form(...)        # ← add user_id
):
    final_json = {"status": "failed", "message": "analysis failed"}
    try:
        resume_bytes = await resume.read()
        jd_bytes = await job_description.read()
        result = handler.generate_interview_content(resume_bytes, jd_bytes, user_id)
        if result:
            return {"status": "success", "message": "analysis complete", "data": result}
        return final_json
    except Exception as e:
        logger.debug(f"Interview analyze API failed: {e}")
        return final_json