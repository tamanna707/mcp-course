#!/usr/bin/env python3
"""
Simple LangGraph + MCP Integration Demo
Shows the minimal setup to use MCP servers with LangGraph agents
"""

import asyncio
import os
from dotenv import load_dotenv

# Core imports
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load environment variables
load_dotenv()

async def simple_mcp_demo():
    """
    Demonstrates the simplest way to integrate MCP with LangGraph
    """
    print("🚀 Simple LangGraph + MCP Demo")
    print("-" * 50)
    
    # Step 1: Configure MCP servers
    # Using the simple MCP server from the ADK example
    mcp_configs = {
        "demo_tools": {
            "command": "python",
            "args": [os.path.join("..", "04-google-adk-agents", "simple_mcp_server.py")],
            "transport": "stdio"
        }
    }
    
    # Step 2: Create MCP client and get tools
    async with MultiServerMCPClient(mcp_configs) as mcp_client:
        tools = await mcp_client.get_tools()
        print(f"✅ Loaded {len(tools)} tools from MCP server")
        
        # Show available tools
        for tool in tools:
            print(f"  • {tool.name}: {tool.description}")
        
        # Step 3: Create LangGraph agent with MCP tools
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        agent = create_react_agent(
            llm,
            tools,
            state_modifier="You are a helpful assistant with access to MCP tools."
        )
        
        # Step 4: Use the agent
        test_queries = [
            "What time is it?",
            "Calculate 15% tip on $85.50",
            "What's the weather in San Francisco?"
        ]
        
        for query in test_queries:
            print(f"\n👤 User: {query}")
            
            result = await agent.ainvoke({
                "messages": [{"role": "user", "content": query}]
            })
            
            # Extract the response
            last_message = result["messages"][-1]
            print(f"🤖 Agent: {last_message.content}")

async def advanced_mcp_demo():
    """
    Shows more advanced MCP integration patterns
    """
    print("\n🔧 Advanced LangGraph + MCP Demo")
    print("-" * 50)
    
    # Multiple MCP servers configuration
    mcp_configs = {
        "filesystem": {
            # Official MCP filesystem server
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
            "transport": "stdio"
        },
        "demo_tools": {
            "command": "python",
            "args": [os.path.join("..", "04-google-adk-agents", "simple_mcp_server.py")],
            "transport": "stdio"
        }
    }
    
    async with MultiServerMCPClient(mcp_configs) as mcp_client:
        tools = await mcp_client.get_tools()
        print(f"✅ Loaded {len(tools)} tools from multiple MCP servers")
        
        # Create agent with custom system prompt
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        agent = create_react_agent(
            llm,
            tools,
            state_modifier="""You are a helpful assistant with access to multiple MCP servers.
            
You can:
- Access and manipulate files in the /tmp directory
- Get current time in different formats
- Perform calculations
- Get weather information

Always explain what tools you're using and why."""
        )
        
        # Complex multi-tool query
        complex_query = """
        Please do the following:
        1. Get the current time
        2. Create a file called 'demo_report.txt' in /tmp with today's date
        3. Calculate how many seconds are in 24 hours
        """
        
        print(f"\n👤 User: {complex_query}")
        
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": complex_query}]
        })
        
        print(f"🤖 Agent: {result['messages'][-1].content}")

async def streaming_demo():
    """
    Demonstrates streaming responses with MCP tools
    """
    print("\n🌊 Streaming LangGraph + MCP Demo")
    print("-" * 50)
    
    mcp_configs = {
        "demo_tools": {
            "command": "python",
            "args": [os.path.join("..", "04-google-adk-agents", "simple_mcp_server.py")],
            "transport": "stdio"
        }
    }
    
    async with MultiServerMCPClient(mcp_configs) as mcp_client:
        tools = await mcp_client.get_tools()
        
        llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)
        agent = create_react_agent(llm, tools)
        
        query = "Tell me the current time and then calculate 20% of 150"
        print(f"👤 User: {query}")
        print("🤖 Agent: ", end="", flush=True)
        
        # Stream the response
        async for chunk in agent.astream({
            "messages": [{"role": "user", "content": query}]
        }):
            if "messages" in chunk and chunk["messages"]:
                message = chunk["messages"][-1]
                if hasattr(message, "content") and message.content:
                    print(message.content, end="", flush=True)
        
        print()  # New line after streaming

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
        await advanced_mcp_demo()
        await streaming_demo()
        
        print("\n✅ All demos completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the MCP server is accessible")

if __name__ == "__main__":
    asyncio.run(main())