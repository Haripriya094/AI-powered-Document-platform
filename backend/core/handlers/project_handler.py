import fitz
import json
import re
from datetime import datetime
from backend.utills.llm_utill import LLMAgent
from backend.core.schemas.prompts import prompts
from backend.core.db.mongo.AST_collection import ASTCollection
from backend.utills.logger_utill import logger


class InterviewManagement:
    def __init__(self):
        self.agent = LLMAgent()
        self.ats_collection = ASTCollection()

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            return "\n".join(page.get_text() for page in doc)
        except Exception as e:
            logger.debug(f"PDF extraction failed: {e}")
            return ""

    def parse_response(self, raw: str) -> dict:
        try:
            cleaned = re.sub(r"```json|```", "", raw.strip()).strip()
            cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
            return json.loads(cleaned)
        except Exception as e:
            logger.debug(f"Response parsing failed: {e}")
            return {}

    def save_to_mongo(self, user_id: str, resume_text: str, jd_text: str, result: dict):
        try:
            record = {
                "user_id": user_id,
                "resume_text": resume_text,
                "jd_text": jd_text,
                "ats_score": result.get("ats_score"),
                "ats_feedback": result.get("ats_feedback"),
                "result": result,
                "analyzed_at": datetime.now().isoformat()
            }
            self.ats_collection.insert_one(record)
            logger.info(f"ATS result saved for user: {user_id}")
        except Exception as e:
            logger.debug(f"Failed to save ATS result: {e}")

    def generate_interview_content(self, pdf_bytes: bytes, jd_bytes: bytes, user_id: str) -> dict:
        try:
            resume_text = self.extract_text_from_pdf(pdf_bytes)
            jd_text = self.extract_text_from_pdf(jd_bytes)
            if not resume_text or not jd_text:
                logger.debug("Empty text extracted from one or both PDFs")
                return {}
            prompt = prompts.interview_prompt(resume_text, jd_text)
            raw = self.agent.generate(prompt)
            result = self.parse_response(raw)
            if result:
                self.save_to_mongo(user_id, resume_text, jd_text, result)
            return result
        except Exception as e:
            logger.debug(f"Generate interview content failed: {e}")
            return {}