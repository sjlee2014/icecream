from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./data/chatbot.db"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # Chatbot Settings
    BUSINESS_NAME: str = "아이스크림몰"
    BUSINESS_HOURS: str = "평일 09:00-18:00"
    SUPPORT_EMAIL: str = "support@i-screammall.co.kr"
    SUPPORT_PHONE: str = "1588-0000"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
