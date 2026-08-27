import os

import uvicorn
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route
from contextlib import asynccontextmanager

from server import mcp
import endpoints


async def health(request):
    return PlainTextResponse("ok")

@asynccontextmanager
async def lifespan(app: Starlette):
    # This initializes the required task groups for the HTTP transport
    async with mcp.session_manager.run():
        yield

if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "1235"))

    mcp_app = mcp.streamable_http_app()

    app = Starlette(routes=[
        Route("/health", health, methods=["GET"]),
        Mount("/", app=mcp_app),
    ], lifespan=lifespan)

    app = CORSMiddleware(
        app,
        allow_origins=["*"],
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["*"],
        expose_headers=["Mcp-Session-Id"],
    )

    uvicorn.run(app, host=host, port=port)
