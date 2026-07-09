import os
from openai import OpenAI
from dotenv import load_dotenv
from backend.utills.logger_utill import logger

load_dotenv()


class LLMParams:
    API_KEY: str = os.getenv("OPENAI_API_KEY")
    MODEL: str = "openai/gpt-4o-mini"  # openrouter model format
    MAX_TOKENS: int = 3000
    TEMPERATURE: float = 0.7
    BASE_URL: str = "https://openrouter.ai/api/v1"  # openrouter endpoint

class LLMAgent:
    def __init__(
        self,
        temperature: float = LLMParams.TEMPERATURE,
        max_tokens: int = LLMParams.MAX_TOKENS
    ) -> None:
        self.client = None
        self.model = LLMParams.MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens

    def set_client(self):
        try:
            self.client = OpenAI(
                api_key=LLMParams.API_KEY,
                base_url=LLMParams.BASE_URL  # ← add this
            )
            logger.info(f"{self.model} client initialized")
        except Exception as e:
            logger.debug(f"Set client functionality failed: {e}")

    def generate(self, prompt: str) -> str:
        """Generates content from OpenAI model for the given prompt."""
        try:
            if not self.client:
                self.set_client()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.debug(f"Generate functionality failed: {e}")