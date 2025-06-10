#!/usr/bin/env python3
"""
Google ADK Agent with MCP Integration Demo
Shows how to use MCP servers with Google's Agent Development Kit
"""

import asyncio
import os
from typing import Optional
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from dotenv import load_dotenv

load_dotenv()

def create_adk_agent_with_mcp() -> LlmAgent:
    """
    Create an ADK agent equipped with tools from the MCP server.
    This demonstrates the simplest way to integrate MCP with ADK.
    """
    
    # Get the path to our MCP server
    mcp_server_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "simple_mcp_server.py"
    )
    
    # Create the agent with MCPToolset
    agent = LlmAgent(
        model="gemini-2.0-flash",
        name="mcp_demo_assistant",
        instruction="""You are a helpful assistant with access to various tools through MCP.
        
        You can:
        - Get the current time in different formats
        - Perform mathematical calculations
        - Get weather information for any location
        
        Always use your tools when appropriate to help the user.""",
        tools=[
            MCPToolset(
                connection_params=StdioServerParameters(
                    command="python",
                    args=[mcp_server_path],
                ),
                # Optional: We could filter tools if needed
                # tool_filter=["get_current_time", "calculate"]
            )
        ],
    )
    
    return agent

async def run_demo():
    """Run a simple demonstration of the ADK agent with MCP tools"""
    
    print("🚀 Starting Google ADK + MCP Demo")
    print("-" * 50)
    
    # Create the agent
    agent = create_adk_agent_with_mcp()
    
    # Create a runner to execute the agent
    runner = Runner(
        agent=agent,
        session_service=InMemorySessionService()
    )
    
    # Example queries to demonstrate MCP tool usage
    demo_queries = [
        "What time is it right now?",
        "Calculate 15% tip on a $85.50 restaurant bill",
        "What's the weather like in San Francisco?"
    ]
    
    # Process each query
    for query in demo_queries:
        print(f"\n👤 User: {query}")
        
        # Create a new session for each query
        session_id = f"demo_session_{demo_queries.index(query)}"
        
        # Execute the query
        response = await runner.run(
            prompt=query,
            session_id=session_id
        )
        
        print(f"🤖 Assistant: {response.text}")
        print("-" * 50)

async def interactive_demo():
    """Run an interactive demo where users can chat with the agent"""
    
    print("🚀 Starting Interactive Google ADK + MCP Demo")
    print("Type 'exit' to quit")
    print("-" * 50)
    
    # Create the agent
    agent = create_adk_agent_with_mcp()
    
    # Create a runner
    runner = Runner(
        agent=agent,
        session_service=InMemorySessionService()
    )
    
    session_id = "interactive_session"
    
    while True:
        # Get user input
        user_input = input("\n👤 You: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye! 👋")
            break
        
        try:
            # Execute the query
            response = await runner.run(
                prompt=user_input,
                session_id=session_id
            )
            
            print(f"🤖 Assistant: {response.text}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_demo())
    else:
        asyncio.run(run_demo())

if __name__ == "__main__":
    main()