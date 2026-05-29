import json
import os
import httpx
from pydantic import BaseModel, ConfigDict, Field

from server import mcp

SEARXNG_URL = os.getenv("SEARXNG_URL", "http://127.0.0.1:1818/search")


class WebSearchInput(BaseModel):
    '''Input model for web search operations.'''
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    q: str = Field(..., description="The search query to look up on the web", min_length=1, max_length=500)
    lang: str = Field(default="en", description="Two-letter language code (ISO 639-1)", pattern=r'^[a-z]{2}$')
    region: str | None = Field(default="", description="Two-letter region code (ISO 3166-1), e.g. 'US'", pattern=r'^[A-Za-z]{2}$')
    safe: bool = Field(default=False, description="Enable SearXNG safesearch (filter explicit results)")
    max_results: int = Field(default=5, description="Maximum number of search results to return", ge=1, le=20)


@mcp.tool(
    name="websearch",
    annotations={
        "title": "Web Search",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def greenfish_websearch(params: WebSearchInput) -> str:
    '''Performs a web search and returns the results.
    This tool allows searching the live web for current information without requiring API keys.
    It is ideal for retrieving news, documentation, or general facts.
    Example:
        Use this tool when you need to find information about recent events or technical documentation.
    '''
    locale = f"{params.lang}-{params.region.upper()}" if params.region else params.lang
    query_params = {
        "q": params.q,
        "format": "json",
        "safesearch": 2 if params.safe else 0,
        "locale": locale,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(SEARXNG_URL, params=query_params, headers=headers)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        return f"Error: SearXNG instance returned status code {e.response.status_code}"
    except Exception as e:
        return f"Error performing web search: {str(e)}"

    results = []
    seen = set()
    for item in data.get("results", []):
        url = item.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        results.append({
            'title': item.get('title'),
            'url': url,
            'description': item.get('content'),
            'rank': len(results) + 1,
        })
        if len(results) >= params.max_results:
            break

    if not results:
        return f"No results found for '{params.q}'."
    return json.dumps(results, ensure_ascii=False)