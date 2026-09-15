"""
Central configuration for the Listrix backend.

All secrets and environment-specific values are loaded from environment
variables (via a local .env file in development). Nothing sensitive is
hardcoded here, and OPENAI_API_KEY is never sent to the frontend.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from slowapi import Limiter
from slowapi.util import get_remote_address


class Settings(BaseSettings):
    # --- OpenAI ---
    OPENAI_API_KEY: str  # required, no default: fails loudly if missing
    OPENAI_MODEL: str = "gpt-4o-mini"

    # --- Database (MySQL) ---
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str = "listrix_db"

    # --- Admin access for knowledge-base management endpoints ---
    ADMIN_API_KEY: str  # required: protects POST/PUT/DELETE /knowledge

    # --- CORS: comma-separated list of allowed origins ---
    CORS_ORIGINS: str = "https://listoradigitalmedia.com"

    # --- Rate limiting ---
    CHAT_RATE_LIMIT: str = "20/minute"
    CONTACT_RATE_LIMIT: str = "10/minute"

    ENVIRONMENT: str = "production"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()

# Shared rate limiter instance, keyed by client IP. Imported by both
# main.py (to register the app-level handler) and individual routes
# (to decorate specific endpoints).
limiter = Limiter(key_func=get_remote_address)
