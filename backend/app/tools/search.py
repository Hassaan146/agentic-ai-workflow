import re
from html.parser import HTMLParser
from urllib.parse import parse_qs, quote_plus, unquote, urlparse

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
        if self._current_tag in {"p", "li", "article", "section"} and len(text.split()) >= 8:
            self.paragraphs.append(text)


class _DuckDuckGoHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._active_href = ""
        self._active_text: list[str] = []
        self.results: list[SearchResult] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() != "a":
            return
        attr_map = {name.lower(): value for name, value in attrs if name and value}
        href = attr_map.get("href", "")
        class_name = attr_map.get("class", "")
        if "result__a" in class_name or "result-link" in class_name:
            self._active_href = href
            self._active_text = []

    def handle_data(self, data: str) -> None:
        if self._active_href:
            text = _clean_text(data)
            if text:
                self._active_text.append(text)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or not self._active_href:
            return
        title = _clean_text(" ".join(self._active_text))
        url = _normalize_duckduckgo_url(self._active_href)
        if title and url and not any(item.url == url for item in self.results):
            self.results.append(
                SearchResult(
                    title=title[:140],
                    url=url,
                    summary=title,
                    source_context="DuckDuckGo HTML search result.",
                )
            )
        self._active_href = ""
        self._active_text = []


class ControlledSearchTool:
    """Controlled search and scrape abstraction for evidence-based answers."""

    async def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        safe_limit = max(1, min(limit, 5))
        if settings.search_provider == "duckduckgo":
            raw_results: list[SearchResult] = []
            for variant in _query_variants(query):
                raw_results.extend(await self._duckduckgo_search(variant, safe_limit))
                raw_results.extend(await self._duckduckgo_html_search(variant, safe_limit))
                raw_results = _dedupe_results(raw_results)
                if len(raw_results) >= safe_limit * 2:
                    break
            if raw_results:
                scraped = await self._scrape_results(raw_results[: safe_limit * 2])
                scraped.sort(key=lambda item: ("page scrape failed" in item.source_context.lower(), -len(item.facts)))
                return scraped[:safe_limit]
            return self._no_live_results(query, safe_limit)
        return self._mock_search(query, safe_limit)

    def _mock_search(self, query: str, limit: int) -> list[SearchResult]:
        return [
            SearchResult(
                title=f"Mock research result {index + 1}",
                url="https://example.com",
                summary=f"Mock search result for '{query}'",
                source_context="Mock local evidence used because SEARCH_PROVIDER is set to mock.",
                facts=[
                    f"The workflow searched for: {query}",
                    "Set SEARCH_PROVIDER=duckduckgo to fetch and scrape live public pages.",
                ],
            )
            for index in range(limit)
        ]

    def _no_live_results(self, query: str, limit: int) -> list[SearchResult]:
        return [
            SearchResult(
                title="No live search result returned",
                url="",
                summary=f"DuckDuckGo did not return a usable result for '{query}'.",
                source_context="DuckDuckGo live search returned no parseable URLs.",
                facts=["Try a broader query or check network access from the backend process."],
            )
            for _ in range(1)
        ][:limit]

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
                            source_context="DuckDuckGo instant-answer related topic result.",
                        )
                    )
                if len(results) >= limit:
                    return results
        return results

    async def _duckduckgo_html_search(self, query: str, limit: int) -> list[SearchResult]:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        headers = {"User-Agent": "Mozilla/5.0 AgenticAIWorkflow/0.1"}
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

        parser = _DuckDuckGoHTMLParser()
        parser.feed(response.text[:400_000])
        return parser.results[:limit]

    async def _scrape_results(self, results: list[SearchResult]) -> list[SearchResult]:
        enriched: list[SearchResult] = []
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            for result in results:
                if not result.url:
                    enriched.append(result)
                    continue
                try:
                    response = await client.get(result.url, headers={"User-Agent": "Mozilla/5.0 AgenticAIWorkflow/0.1"})
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
                                "facts": facts or [summary[:320]],
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


def _query_variants(query: str) -> list[str]:
    clean = re.sub(r"^find relevant information for:\s*", "", query, flags=re.IGNORECASE).strip()
    variants = [
        clean,
        f"{clean} history",
        f"{clean} current status",
        f"{clean} future sustainability",
    ]
    deduped: list[str] = []
    for variant in variants:
        if variant and variant.lower() not in {item.lower() for item in deduped}:
            deduped.append(variant)
    return deduped


def _dedupe_results(results: list[SearchResult]) -> list[SearchResult]:
    seen: set[str] = set()
    deduped: list[SearchResult] = []
    for result in results:
        if not result.url or result.url in seen:
            continue
        seen.add(result.url)
        deduped.append(result)
    return deduped


def _normalize_duckduckgo_url(href: str) -> str:
    if href.startswith("//"):
        href = "https:" + href
    parsed = urlparse(href)
    if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
        target = parse_qs(parsed.query).get("uddg", [""])[0]
        return unquote(target)
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return ""


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
