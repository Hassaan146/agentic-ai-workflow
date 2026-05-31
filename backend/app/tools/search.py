import re
from html.parser import HTMLParser
from urllib.parse import quote_plus

import httpx
from pydantic import BaseModel, Field

from app.core.config import settings


class SearchResult(BaseModel):
    title: str
    url: str
    summary: str
    source_context: str = ""
    facts: list[str] = Field(default_factory=list)


class _ReadableHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._current_tag = ""
        self.title = ""
        self.meta_description = ""
        self.paragraphs: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        self._current_tag = tag.lower()
        if self._current_tag == "meta":
            attr_map = {name.lower(): value for name, value in attrs if name and value}
            if attr_map.get("name", "").lower() == "description":
                self.meta_description = _clean_text(attr_map.get("content", ""))

    def handle_endtag(self, tag: str) -> None:
        if self._current_tag == tag.lower():
            self._current_tag = ""

    def handle_data(self, data: str) -> None:
        text = _clean_text(data)
        if not text:
            return
        if self._current_tag == "title" and not self.title:
            self.title = text
        if self._current_tag in {"p", "li"} and len(text.split()) >= 8:
            self.paragraphs.append(text)


class ControlledSearchTool:
    """Controlled search and scrape abstraction for evidence-based answers."""

    async def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        safe_limit = max(1, min(limit, 5))
        if settings.search_provider == "duckduckgo":
            results = await self._duckduckgo_search(query, safe_limit)
            if results:
                return await self._scrape_results(results)
        return self._mock_search(query, safe_limit)

    def _mock_search(self, query: str, limit: int) -> list[SearchResult]:
        return [
            SearchResult(
                title=f"Controlled research result {index + 1}",
                url="https://example.com",
                summary=f"Controlled search result for '{query}'",
                source_context="Mock local evidence used because SEARCH_PROVIDER is not set to duckduckgo.",
                facts=[
                    f"The workflow searched for: {query}",
                    "Set SEARCH_PROVIDER=duckduckgo to fetch and scrape live public pages.",
                ],
            )
            for index in range(limit)
        ]

    async def _duckduckgo_search(self, query: str, limit: int) -> list[SearchResult]:
        url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
        async with httpx.AsyncClient(timeout=8, follow_redirects=True) as client:
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
                            title=_clean_text(title)[:140],
                            url=result_url,
                            summary=_clean_text(title),
                            source_context="DuckDuckGo related topic result.",
                        )
                    )
                if len(results) >= limit:
                    return results
        return results

    async def _scrape_results(self, results: list[SearchResult]) -> list[SearchResult]:
        enriched: list[SearchResult] = []
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            for result in results:
                try:
                    response = await client.get(result.url, headers={"User-Agent": "AgenticAIWorkflowBot/0.1"})
                    response.raise_for_status()
                    parser = _ReadableHTMLParser()
                    parser.feed(response.text[:250_000])
                    facts = _pick_facts(parser.paragraphs)
                    title = parser.title or result.title
                    summary = parser.meta_description or result.summary
                    enriched.append(
                        result.model_copy(
                            update={
                                "title": title[:140],
                                "summary": summary[:500],
                                "source_context": f"Scraped page: {response.url}",
                                "facts": facts,
                            }
                        )
                    )
                except Exception as exc:
                    enriched.append(
                        result.model_copy(
                            update={
                                "source_context": f"Search result found, but page scrape failed: {exc}",
                                "facts": [result.summary],
                            }
                        )
                    )
        return enriched


def _pick_facts(paragraphs: list[str], limit: int = 4) -> list[str]:
    facts: list[str] = []
    for paragraph in paragraphs:
        if paragraph not in facts:
            facts.append(paragraph[:320])
        if len(facts) >= limit:
            break
    return facts


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
