import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "ResumeMatch AI"
    GROQ_API_KEY: str = ""
    GROQ_LLM_MODEL: str = "llama-3.3-70b-versatile"
    FRONTEND_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frontend")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()