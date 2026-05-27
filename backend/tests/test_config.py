import pytest

from app.core.config import Settings


def test_dev_mode_does_not_require_external_services() -> None:
    settings = Settings(app_env="dev", _env_file=None)

    assert settings.missing_production_settings() == []
    settings.assert_runtime_ready()


def test_production_mode_requires_external_services() -> None:
    settings = Settings(
        app_env="production",
        clerk_jwks_url="",
        supabase_url="",
        supabase_service_role_key="",
        _env_file=None,
    )

    assert settings.missing_production_settings() == [
        "CLERK_JWKS_URL",
        "SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE_KEY",
    ]
    with pytest.raises(RuntimeError):
        settings.assert_runtime_ready()


def test_production_mode_accepts_required_settings() -> None:
    settings = Settings(
        app_env="production",
        clerk_jwks_url="https://example.clerk.accounts.dev/.well-known/jwks.json",
        supabase_url="https://example.supabase.co",
        supabase_service_role_key="service-role-key",
        _env_file=None,
    )

    assert settings.missing_production_settings() == []
    settings.assert_runtime_ready()

