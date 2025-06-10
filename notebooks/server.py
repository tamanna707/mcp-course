#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "beautifulsoup4==4.12.3",
#     "google-adk==0.3.0",
#     "requests==2.32.3",
#     "html2text",
#     "mcp[cli]==1.9.3",
#     "uvicorn",
#     "starlette"
# ]
# ///
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from html2text import html2text
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount
from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS

# Create an MCP server instance with an identifier ("wiki")
mcp = FastMCP("wiki")

@mcp.tool()
def extract_wikipedia_article(url: str) -> str:
    """
    Retrieves and processes a Wikipedia article from the given URL, extracting
    the main content and converting it to Markdown format.
    
    Usage:
        extract_wikipedia_article("https://en.wikipedia.org/wiki/Gemini_(chatbot)")
    """
    try:
        if not url.startswith("http"):
            raise ValueError("URL must begin with http or https protocol.")
        
        response = requests.get(url, timeout=8)
        if response.status_code != 200:
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Unable to access the article. Server returned status: {response.status_code}"
                )
            )
        
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", {"id": "mw-content-text"})
        
        if not content_div:
            raise McpError(
                ErrorData(
                    code=INVALID_PARAMS,
                    message="The main article content section was not found at the specified Wikipedia URL."
                )
            )
        
        markdown_text = html2text(str(content_div))
        return markdown_text
        
    except Exception as e:
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR, 
                message=f"An unexpected error occurred: {str(e)}"
            )
        ) from e

# Create Starlette application
app = Starlette(
    debug=True,
    routes=[
        Mount("/", app=mcp.sse_app()),
    ],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)