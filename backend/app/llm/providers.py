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
        self._fast_groq = None
        self._reasoning_groq = None
        self._gemini = None
        self.model_name = settings.default_fast_model

    def _get_fast_groq(self):
        if self._fast_groq is None:
            from langchain_groq import ChatGroq

            self._fast_groq = ChatGroq(
                api_key=settings.groq_api_key,
                model=settings.default_fast_model,
                temperature=0.2,
            )
        return self._fast_groq

    def _get_reasoning_groq(self):
        if self._reasoning_groq is None:
            from langchain_groq import ChatGroq

            self._reasoning_groq = ChatGroq(
                api_key=settings.groq_reasoning_api_key or settings.groq_api_key,
                model=settings.default_reasoning_model,
                temperature=0.2,
            )
        return self._reasoning_groq

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
        use_fast_groq = purpose in {"structure", "route"}
        if use_fast_groq and settings.groq_api_key:
            model = self._get_fast_groq()
            self.model_name = settings.default_fast_model
        elif settings.groq_reasoning_api_key or settings.groq_api_key:
            model = self._get_reasoning_groq()
            self.model_name = settings.default_reasoning_model
        elif settings.google_api_key:
            model = self._get_gemini()
            self.model_name = settings.default_reasoning_model
        else:
            return await DeterministicProvider().complete(prompt, purpose=purpose)

        response = await model.ainvoke(prompt)
        return str(response.content)


def get_model_provider() -> ModelProvider:
    if settings.groq_api_key or settings.groq_reasoning_api_key or settings.google_api_key:
        return LangChainProvider()
    return DeterministicProvider()
