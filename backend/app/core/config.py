from functools import cached_property
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: Literal["dev", "production"] = "dev"
    allow_dev_auth: bool = True
    backend_cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    groq_api_key: str = ""
    groq_reasoning_api_key: str = ""
    google_api_key: str = ""
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 10080
    admin_emails: str = ""
    search_provider: Literal["mock", "duckduckgo"] = "mock"
    default_fast_model: str = "llama-3.1-8b-instant"
    default_reasoning_model: str = "llama-3.3-70b-versatile"

    @cached_property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]

    @cached_property
    def admin_email_set(self) -> set[str]:
        return {
            email.strip().lower()
            for email in self.admin_emails.split(",")
            if email.strip()
        }

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def has_supabase_storage(self) -> bool:
        key = self.supabase_service_role_key.strip()
        return bool(self.supabase_url.strip() and key and "." in key)

    def missing_production_settings(self) -> list[str]:
        if not self.is_production:
            return []

        required_values = {
            "JWT_SECRET": self.jwt_secret,
            "SUPABASE_URL": self.supabase_url,
            "SUPABASE_SERVICE_ROLE_KEY": self.supabase_service_role_key,
        }
        return [
            name
            for name, value in required_values.items()
            if (
                not value.strip()
                or (name == "JWT_SECRET" and value == "change-me-in-production")
                or (name == "SUPABASE_SERVICE_ROLE_KEY" and "." not in value)
            )
        ]

    def assert_runtime_ready(self) -> None:
        missing = self.missing_production_settings()
        if missing:
            joined = ", ".join(missing)
            raise RuntimeError(f"Missing production settings: {joined}")


settings = Settings()




