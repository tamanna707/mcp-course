#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "mcp[cli]==1.9.3",
#     "fastapi",
#     "uvicorn"
# ]
# ///

"""
Basic MCP Server Demo using FastMCP

This demo shows the fundamental concepts of MCP by creating a simple server
with a tool, resource, and prompt.

Based on MCP Python SDK documentation:
https://github.com/modelcontextprotocol/python-sdk
"""

from mcp.server.fastmcp import FastMCP
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
import json
from datetime import datetime

# Create an MCP server instance
mcp = FastMCP("basic-demo")

@mcp.tool()
def get_current_time() -> str:
    """
    Get the current time in ISO format.
    
    This is an example of an MCP Tool - a function that can be called by the LLM
    to perform actions or retrieve information.
    """
    return datetime.now().isoformat()

@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b

@mcp.resource("demo://greeting/{name}")
def get_greeting(name: str) -> str:
    """
    Get a personalized greeting.
    
    This is an example of an MCP Resource - read-only data that can be
    accessed by the LLM for context.
    
    Args:
        name: The name to include in the greeting
        
    Returns:
        A personalized greeting message
    """
    return f"Hello, {name}! Welcome to the MCP demo."

@mcp.prompt()
def introduction_prompt() -> str:
    """
    A sample prompt for introducing MCP concepts.
    
    This is an example of an MCP Prompt - a template that structures
    interactions and guides workflows.
    """
    return """You are an MCP demonstration assistant. Your role is to help users understand:

1. **Tools**: Functions you can call to perform actions (like getting the current time)
2. **Resources**: Read-only data you can access for context (like greetings)
3. **Prompts**: Templates that structure our interactions (like this one)

Available tools:
- get_current_time(): Returns the current timestamp
- add_numbers(a, b): Adds two numbers together

Available resources:
- demo://greeting/{name}: Gets a personalized greeting for any name

Please demonstrate these capabilities when asked!"""

@mcp.prompt()
def task_planning_prompt() -> str:
    """
    A prompt template for task planning and execution.
    """
    return """You are a task planning assistant. Break down complex requests into:

1. **Information Gathering**: What data do you need?
2. **Tool Selection**: Which tools can help accomplish the task?
3. **Execution Steps**: What's the logical sequence of actions?
4. **Verification**: How will you confirm success?

Use the available MCP tools and resources to accomplish user goals systematically."""

# Create Starlette application for HTTP transport
app = Starlette(
    debug=True,
    routes=[
        Mount("/", app=mcp.sse_app()),
    ],
)

if __name__ == "__main__":
    print("🚀 Starting Basic MCP Server Demo")
    print("📡 Server running on: http://localhost:8000")
    print("🔧 MCP endpoint: http://localhost:8000/sse")
    print("\n💡 This server demonstrates:")
    print("   - Tools: get_current_time, add_numbers")
    print("   - Resources: demo://greeting/{name}")
    print("   - Prompts: introduction_prompt, task_planning_prompt")
    print("\n🧪 Test with MCP Inspector:")
    print("   npx @modelcontextprotocol/inspector")
    print("   Then connect to: http://localhost:8000/sse")
    
    uvicorn.run(app, host="localhost", port=8000)
