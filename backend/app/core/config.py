from functools import cached_property
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: Literal["dev", "production"] = "dev"
    allow_dev_auth: bool = True
    backend_cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    clerk_secret_key: str = ""
    clerk_jwks_url: str = ""
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    groq_api_key: str = ""
    groq_reasoning_api_key: str = ""
    google_api_key: str = ""
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

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    def missing_production_settings(self) -> list[str]:
        if not self.is_production:
            return []

        required_values = {
            "CLERK_JWKS_URL": self.clerk_jwks_url,
            "SUPABASE_URL": self.supabase_url,
            "SUPABASE_SERVICE_ROLE_KEY": self.supabase_service_role_key,
        }
        return [name for name, value in required_values.items() if not value.strip()]

    def assert_runtime_ready(self) -> None:
        missing = self.missing_production_settings()
        if missing:
            joined = ", ".join(missing)
            raise RuntimeError(f"Missing production settings: {joined}")


settings = Settings()
