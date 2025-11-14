# universal_ai/config/settings.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    embed_provider: str = os.getenv("EMBED_PROVIDER", "openai")

    # Common configuration
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


settings= Settings()