#!/usr/bin/env python3
"""
Simple OpenAI Agents SDK + MCP Integration Demo
Shows the minimal setup to use MCP servers with OpenAI agents
"""

import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, MCPServerStdio

# Load environment variables
load_dotenv()

async def simple_mcp_demo():
    """
    Demonstrates the simplest way to integrate MCP with OpenAI Agents SDK
    """
    print("🚀 Simple OpenAI Agents + MCP Demo")
    print("-" * 50)
    
    # Create OpenAI client
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Step 1: Create an MCP server connection
    # Using the simple MCP server from the ADK example
    mcp_server = MCPServerStdio(
        params={
            "command": "python",
            "args": [os.path.join("..", "04-google-adk-agents", "simple_mcp_server.py")]
        }
    )
    
    # Step 2: Create an agent with MCP servers
    agent = Agent(
        name="SimpleAssistant",
        instructions="""You are a helpful assistant with access to MCP tools.
        
You can:
- Get the current time in different formats
- Perform mathematical calculations
- Get weather information

Always use your tools when appropriate to help the user.""",
        mcp_servers=[mcp_server],
        model="gpt-4o"
    )
    
    # Step 3: Run the agent
    test_queries = [
        "What time is it right now?",
        "Calculate 15% tip on a $85.50 restaurant bill",
        "What's the weather like in San Francisco?"
    ]
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        
        # Run the agent
        response = await agent.run(client=client, query=query)
        
        # Extract and print the response
        if response.messages:
            print(f"🤖 Agent: {response.messages[-1].text}")

async def multiple_mcp_servers_demo():
    """
    Shows how to use multiple MCP servers with a single agent
    """
    print("\n🔧 Multiple MCP Servers Demo")
    print("-" * 50)
    
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create multiple MCP server connections
    mcp_servers = [
        # Filesystem server (official MCP server)
        MCPServerStdio(
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
            }
        ),
        # Our custom demo server
        MCPServerStdio(
            params={
                "command": "python",
                "args": [os.path.join("..", "04-google-adk-agents", "simple_mcp_server.py")]
            }
        )
    ]
    
    # Create agent with multiple MCP servers
    agent = Agent(
        name="MultiToolAssistant",
        instructions="""You are a helpful assistant with access to multiple MCP servers.
        
You can:
- Access and manipulate files in the /tmp directory
- Get current time in different formats
- Perform calculations
- Get weather information

Always explain what tools you're using and why.""",
        mcp_servers=mcp_servers,
        model="gpt-4o"
    )
    
    # Complex query requiring multiple tools
    complex_query = """
    Please do the following:
    1. Get the current time
    2. Create a file called 'demo_report.txt' in /tmp with today's date
    3. Calculate how many seconds are in 24 hours
    """
    
    print(f"👤 User: {complex_query}")
    
    response = await agent.run(client=client, query=complex_query)
    
    if response.messages:
        print(f"🤖 Agent: {response.messages[-1].text}")

async def specialized_agents_demo():
    """
    Demonstrates creating specialized agents with specific MCP tools
    """
    print("\n🎯 Specialized Agents Demo")
    print("-" * 50)
    
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Calculator specialist agent
    calc_agent = Agent(
        name="CalculatorSpecialist",
        instructions="""You are a mathematical specialist focused on calculations.
        
Always:
- Show your work step by step
- Explain the mathematical concepts
- Provide accurate results
- Use the calculator tool for all calculations""",
        mcp_servers=[
            MCPServerStdio(
                params={
                    "command": "python",
                    "args": [os.path.join("..", "04-google-adk-agents", "simple_mcp_server.py")]
                }
            )
        ],
        model="gpt-4o"
    )
    
    # File management specialist
    file_agent = Agent(
        name="FileSpecialist",
        instructions="""You are a file management specialist.
        
You can:
- List directory contents
- Read and write files
- Organize file structures
- Search through files

Be careful with file operations and always confirm actions.""",
        mcp_servers=[
            MCPServerStdio(
                params={
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
                }
            )
        ],
        model="gpt-4o"
    )
    
    # Test each specialist
    print("📊 Testing Calculator Specialist:")
    calc_query = "Calculate compound interest on $1000 at 5% annual rate for 10 years"
    response = await calc_agent.run(client=client, query=calc_query)
    if response.messages:
        print(f"Result: {response.messages[-1].text}")
    
    print("\n📁 Testing File Specialist:")
    file_query = "List all files in /tmp and tell me what's there"
    response = await file_agent.run(client=client, query=file_query)
    if response.messages:
        print(f"Result: {response.messages[-1].text}")

async def main():
    """Run all demos"""
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY environment variable")
        print("export OPENAI_API_KEY='your-api-key'")
        return
    
    try:
        # Run demos
        await simple_mcp_demo()
        await multiple_mcp_servers_demo()
        await specialized_agents_demo()
        
        print("\n✅ All demos completed successfully!")
        print("\nKey Takeaways:")
        print("- OpenAI Agents SDK has native MCP support")
        print("- Multiple MCP servers can be used by a single agent")
        print("- Tools are automatically discovered from MCP servers")
        print("- Specialized agents can use specific MCP tools")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the MCP servers are accessible")

if __name__ == "__main__":
    asyncio.run(main())