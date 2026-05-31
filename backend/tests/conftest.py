import pytest

from app.core.config import settings


@pytest.fixture(autouse=True)
def force_test_runtime(monkeypatch):
    monkeypatch.setattr(settings, "search_provider", "mock")
    monkeypatch.setattr(settings, "groq_api_key", "")
    monkeypatch.setattr(settings, "groq_reasoning_api_key", "")
    monkeypatch.setattr(settings, "google_api_key", "")
