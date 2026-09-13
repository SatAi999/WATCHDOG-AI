import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "WATCHDOG"
    APP_ENV: str = "development"
    EXECUTION_MODE: str = "LIVE"  # "LIVE" or "DEMO"
    
    DATABASE_URL: str = "sqlite:///./watchdog.db"
    
    # Anakin API Credentials
    ANAKIN_API_KEY: Optional[str] = os.getenv("ANAKIN_API_KEY", "")
    ANAKIN_BASE_URL: str = "https://api.anakin.ai/v1"
    ANAKIN_WEBHOOK_SECRET: Optional[str] = os.getenv("ANAKIN_WEBHOOK_SECRET", "watchdog_secret_key_123")
    
    # Groq & LLM Credentials
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY", "")
    LLM_API_KEY: Optional[str] = os.getenv("LLM_API_KEY", os.getenv("GROQ_API_KEY", ""))
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    
    # Optional Fallbacks
    JINA_API_KEY: Optional[str] = os.getenv("JINA_API_KEY", "")
    FIRECRAWL_API_KEY: Optional[str] = os.getenv("FIRECRAWL_API_KEY", "")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
