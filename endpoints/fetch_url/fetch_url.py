import asyncio
import json
import httpx
import trafilatura
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from server import mcp


class FetchUrlInput(BaseModel):
    '''Input model for fetching and extracting content from a URL.'''
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    url: HttpUrl = Field(..., description="The URL to fetch and extract readable content from")
    max_chars: int = Field(default=8000, description="Maximum number of characters of extracted text to return", ge=100, le=50000)


@mcp.tool(
    name="fetch_url",
    annotations={
        "title": "Fetch URL Content",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def greenfish_fetch_url(params: FetchUrlInput) -> str:
    '''Fetches a web page and returns its main readable content, stripped of navigation, ads and boilerplate.
    Use this to read the full text of a specific article or documentation page when you already have its URL.
    '''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = str(params.url)
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "html" not in content_type.lower():
                return f"Error: unsupported content type '{content_type}', expected HTML."
            html = response.text
    except httpx.HTTPStatusError as e:
        return f"Error: server returned status code {e.response.status_code}"
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

    extracted = await asyncio.to_thread(
        trafilatura.extract,
        html,
        output_format="json",
        with_metadata=True,
        include_comments=False,
        favor_precision=True,
    )
    if not extracted:
        return f"No readable content could be extracted from '{url}'."

    data = json.loads(extracted)
    text = data.get("text") or ""
    result = {
        "url": data.get("url") or url,
        "title": data.get("title"),
        "date": data.get("date"),
        "content": text[:params.max_chars],
        "truncated": len(text) > params.max_chars,
    }
    return json.dumps(result, ensure_ascii=False)