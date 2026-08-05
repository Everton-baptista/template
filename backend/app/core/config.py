import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Agno Multi-Agent System"
    ENV: str = "development"
    DEBUG: bool = True
    
    # LLM Provider Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    
    # Default Provider Settings
    DEFAULT_MODEL_PROVIDER: str = "openai"
    DEFAULT_MODEL_ID: str = "gpt-4o-mini"
    
    # Search Tools Keys
    EXA_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None
    
    # Database Settings
    DATABASE_URL: str = "postgresql://agno:agno_secret@localhost:5432/agno_db"
    VECTOR_DB_URL: str = "postgresql://agno:agno_secret@localhost:5432/agno_db"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8501", "*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
