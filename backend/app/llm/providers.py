from app.core.config import settings


class ModelProvider:
    provider_name = "base"
    model_name = "unknown"

    async def complete(self, prompt: str, *, purpose: str = "general") -> str:
        raise NotImplementedError


class DeterministicProvider(ModelProvider):
    provider_name = "deterministic"
    model_name = "local-dev-fallback"

    async def complete(self, prompt: str, *, purpose: str = "general") -> str:
        return f"Deterministic {purpose} response based on: {prompt[:240]}"


class LangChainProvider(ModelProvider):
    provider_name = "langchain"

    def __init__(self) -> None:
        self._groq = None
        self._gemini = None
        self.model_name = settings.default_fast_model

    def _get_groq(self):
        if self._groq is None:
            from langchain_groq import ChatGroq

            self._groq = ChatGroq(
                api_key=settings.groq_api_key,
                model=settings.default_fast_model,
                temperature=0.2,
            )
        return self._groq

    def _get_gemini(self):
        if self._gemini is None:
            from langchain_google_genai import ChatGoogleGenerativeAI

            self._gemini = ChatGoogleGenerativeAI(
                google_api_key=settings.google_api_key,
                model=settings.default_reasoning_model,
                temperature=0.2,
            )
        return self._gemini

    async def complete(self, prompt: str, *, purpose: str = "general") -> str:
        use_groq = purpose in {"structure", "route"} or not settings.google_api_key
        model = self._get_groq() if use_groq else self._get_gemini()
        self.model_name = settings.default_fast_model if use_groq else settings.default_reasoning_model
        response = await model.ainvoke(prompt)
        return str(response.content)


def get_model_provider() -> ModelProvider:
    if settings.groq_api_key or settings.google_api_key:
        return LangChainProvider()
    return DeterministicProvider()
