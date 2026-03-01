from pydantic_ai import Tool
from ddgs import DDGS

def duckduckgo_search_tool_func(query: str, max_results: int = 5) -> list[dict]:
    """Search the web for a query using DuckDuckGo."""
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        return [{"title": r["title"], "body": r["body"], "href": r["href"]} for r in results]

duckduckgo_search_tool = Tool(duckduckgo_search_tool_func)

