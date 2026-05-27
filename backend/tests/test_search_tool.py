import pytest

from app.tools.search import ControlledSearchTool


@pytest.mark.asyncio
async def test_controlled_search_limits_results() -> None:
    tool = ControlledSearchTool()

    results = await tool.search("cars under $500", limit=20)

    assert len(results) == 5
    assert results[0].title
    assert results[0].url

