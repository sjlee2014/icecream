from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/icecream_db"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # Scraper
    SCRAPER_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    SCRAPER_HEADLESS: bool = True
    SCRAPER_INTERVAL_HOURS: int = 6
    TARGET_URL: str = "https://i-screammall.co.kr/"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
