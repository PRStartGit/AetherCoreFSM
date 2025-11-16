from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Zynthio - Safety Management Platform"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Multi-tenant safety management platform"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    # For development: SQLite (default)
    # For production: PostgreSQL (set via environment variable)
    # Example: postgresql://user:password@localhost:5432/dbname
    DATABASE_URL: str = "sqlite:///./aethercore.db"

    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:4200",
        "http://localhost:8000",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:8000",
    ]

    # Email Configuration
    # SMTP Settings (Primary - Cost-effective)
    SMTP_HOST: Optional[str] = None  # e.g., smtp.gmail.com, smtp.office365.com
    SMTP_PORT: int = 587  # 587 for TLS, 465 for SSL
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False

    # Email Settings
    FROM_EMAIL: str = "noreply@zynthio.com"
    FROM_NAME: str = "Zynthio Site Monitoring"

    # SendGrid (Fallback option)
    SENDGRID_API_KEY: Optional[str] = None

    # Email Templates Directory
    EMAIL_TEMPLATES_DIR: str = "app/email_templates"

    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".pdf"}

    # Celery / Redis (for background tasks)
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100

    # Subscription
    DEFAULT_SUBSCRIPTION_PRICE_PER_SITE: float = 50.0  # Monthly price per site
    FREE_TRIAL_DAYS: int = 365  # First year free

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
