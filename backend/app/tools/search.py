from urllib.parse import quote_plus

import httpx
from pydantic import BaseModel

from app.core.config import settings


class SearchResult(BaseModel):
    title: str
    url: str
    summary: str


class ControlledSearchTool:
    """MVP-safe search abstraction with a production-ready provider boundary."""

    async def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        safe_limit = max(1, min(limit, 5))
        if settings.search_provider == "duckduckgo":
            results = await self._duckduckgo_search(query, safe_limit)
            if results:
                return results
        return self._mock_search(query, safe_limit)

    def _mock_search(self, query: str, limit: int) -> list[SearchResult]:
        return [
            SearchResult(
                title=f"Controlled research result {index + 1}",
                url="https://example.com",
                summary=f"Controlled search result for '{query}'",
            )
            for index in range(limit)
        ]

    async def _duckduckgo_search(self, query: str, limit: int) -> list[SearchResult]:
        url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(url)
            response.raise_for_status()
            payload = response.json()

        results: list[SearchResult] = []
        for topic in payload.get("RelatedTopics", []):
            candidates = topic.get("Topics", [topic])
            for candidate in candidates:
                title = candidate.get("Text")
                result_url = candidate.get("FirstURL")
                if title and result_url:
                    results.append(
                        SearchResult(
                            title=title[:120],
                            url=result_url,
                            summary=title,
                        )
                    )
                if len(results) >= limit:
                    return results
        return results
