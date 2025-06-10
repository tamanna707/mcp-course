#!/usr/bin/env python3
"""
Example: ADK Agent connecting to an HTTP/SSE MCP Server
This shows how to connect to MCP servers running over HTTP with Server-Sent Events
"""

import asyncio
from typing import Any, Optional

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams

load_dotenv()

def create_agent_with_http_mcp(mcp_url: str = "http://localhost:8001/sse") -> LlmAgent:
    """
    Creates an ADK Agent that connects to an MCP server over HTTP/SSE.
    
    Args:
        mcp_url: The URL of the MCP server's SSE endpoint
    
    Returns:
        An LlmAgent configured with MCP tools
    """
    
    agent = LlmAgent(
        model="gemini-2.0-flash",
        name="http_mcp_assistant",
        instruction="""You are a helpful assistant that can access external tools via MCP.
        
        Use the available tools to help users with their requests.
        Always provide clear and concise responses.""",
        tools=[
            MCPToolset(
                connection_params=SseServerParams(url=mcp_url)
            )
        ],
    )
    
    return agent

async def demo_http_mcp_agent():
    """Demonstrate using an ADK agent with HTTP/SSE MCP server"""
    
    print("🌐 ADK Agent with HTTP/SSE MCP Server Demo")
    print("=" * 50)
    print("Note: This requires an MCP server running at http://localhost:8001/sse")
    print("=" * 50)
    
    try:
        # Create the agent
        agent = create_agent_with_http_mcp()
        
        # Create a runner
        runner = Runner(
            agent=agent,
            session_service=InMemorySessionService()
        )
        
        # Example interaction
        query = "What tools do you have available?"
        print(f"\n👤 User: {query}")
        
        response = await runner.run(
            prompt=query,
            session_id="demo_session"
        )
        
        print(f"🤖 Assistant: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure you have an MCP server running at http://localhost:8001/sse")

if __name__ == "__main__":
    asyncio.run(demo_http_mcp_agent())