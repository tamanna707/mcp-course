#!/usr/bin/env python3
"""
LangGraph Agent with MCP Integration Demo

This example shows how to create a LangGraph agent that can use tools from MCP servers,
demonstrating the integration between LangGraph and the Model Context Protocol.

Based on:
- LangGraph MCP Documentation: https://langchain-ai.github.io/langgraph/agents/mcp/
- LangChain MCP Adapters: https://changelog.langchain.com/announcements/mcp-adapters-for-langchain-and-langgraph
"""

import asyncio
import logging
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# LangGraph and LangChain imports
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph

# MCP integration
from langchain_mcp_adapters.client import MultiServerMCPClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class LangGraphMCPAgent:
    """
    A LangGraph agent that integrates with multiple MCP servers to provide
    enhanced capabilities through external tools and data sources.
    """
    
    def __init__(self, model_provider: str = "openai"):
        self.model_provider = model_provider
        self.agent = None
        self.mcp_client = None
        
    def _get_model(self):
        """Get the appropriate LLM model."""
        if self.model_provider == "openai":
            return ChatOpenAI(
                model="gpt-4o",
                temperature=0.1,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif self.model_provider == "anthropic":
            return ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                temperature=0.1,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")
    
    async def setup_agent(self):
        """Set up the LangGraph agent with MCP integration."""
        logger.info("Setting up LangGraph agent with MCP integration...")
        
        # Configure MCP servers
        mcp_server_configs = {
            "web_search": {
                "command": "python",
                "args": ["mcp_servers/web_search_server.py"],
                "transport": "stdio"
            },
            "file_system": {
                # Using the official MCP filesystem server
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
                "transport": "stdio"
            },
            "calculator": {
                "command": "python", 
                "args": ["mcp_servers/calculator_server.py"],
                "transport": "stdio"
            }
        }
        
        # Create MCP client
        self.mcp_client = MultiServerMCPClient(mcp_server_configs)
        
        # Get tools from MCP servers
        tools = await self.mcp_client.get_tools()
        logger.info(f"Loaded {len(tools)} tools from MCP servers")
        
        # Create LangGraph ReAct agent
        model = self._get_model()
        self.agent = create_react_agent(
            model=model,
            tools=tools,
            state_modifier="""You are a helpful AI assistant with access to various tools through MCP servers.
            
You can:
- Search the web for current information
- Perform mathematical calculations
- Access and manipulate files
- Analyze data and provide insights

When using tools:
- Always explain what you're doing
- Use multiple tools if needed to provide comprehensive answers
- Verify information when possible
- Format responses clearly and helpfully

Be thorough but concise in your responses."""
        )
        
        logger.info("LangGraph agent with MCP integration set up successfully!")
    
    async def run_conversation(self, user_input: str, session_id: str = "default") -> str:
        """Run a conversation with the agent."""
        if not self.agent:
            await self.setup_agent()
        
        try:
            # Create message with user input
            messages = [HumanMessage(content=user_input)]
            
            # Run the agent
            result = await self.agent.ainvoke(
                {"messages": messages},
                {"configurable": {"session_id": session_id}}
            )
            
            # Extract the final response
            if result and "messages" in result:
                last_message = result["messages"][-1]
                return last_message.content
            else:
                return "I apologize, but I couldn't generate a response."
                
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            return f"I encountered an error: {str(e)}"
    
    async def cleanup(self):
        """Clean up resources."""
        if self.mcp_client:
            await self.mcp_client.close()

class ResearchAssistant(LangGraphMCPAgent):
    """
    Specialized research assistant that uses MCP tools for comprehensive research tasks.
    """
    
    async def setup_agent(self):
        """Set up research-specific MCP configuration."""
        logger.info("Setting up Research Assistant with specialized MCP tools...")
        
        # Research-focused MCP server configuration
        mcp_server_configs = {
            "web_search": {
                "command": "python",
                "args": ["mcp_servers/web_search_server.py"],
                "transport": "stdio"
            },
            "arxiv": {
                "command": "python",
                "args": ["mcp_servers/arxiv_server.py"],
                "transport": "stdio"
            },
            "data_analysis": {
                "command": "python",
                "args": ["mcp_servers/data_analysis_server.py"],
                "transport": "stdio"
            }
        }
        
        self.mcp_client = MultiServerMCPClient(mcp_server_configs)
        tools = await self.mcp_client.get_tools()
        
        model = self._get_model()
        self.agent = create_react_agent(
            model=model,
            tools=tools,
            state_modifier="""You are a research assistant specialized in gathering, analyzing, and synthesizing information.

Your research process should be:
1. **Information Gathering**: Use web search and academic sources (arXiv) to collect relevant information
2. **Data Analysis**: Process and analyze any quantitative data found
3. **Synthesis**: Combine information from multiple sources to provide comprehensive insights
4. **Verification**: Cross-reference information when possible

Research Guidelines:
- Always cite your sources
- Look for recent and authoritative information
- Consider multiple perspectives on complex topics
- Provide balanced analysis with supporting evidence
- Highlight any limitations or uncertainties in the data

Format your research reports with:
- Executive Summary
- Key Findings
- Detailed Analysis
- Sources and References
- Recommendations (if applicable)"""
        )
        
        logger.info("Research Assistant set up successfully!")
    
    async def conduct_research(self, topic: str, depth: str = "moderate") -> str:
        """Conduct comprehensive research on a topic."""
        research_prompt = f"""
Please conduct {depth} research on the following topic: {topic}

Research requirements:
- Use web search to find current information and trends
- Look for academic papers on arXiv if relevant
- Analyze any data or statistics found
- Provide a comprehensive report with citations

Please follow your research process systematically.
"""
        
        return await self.run_conversation(research_prompt)

async def demo_basic_agent():
    """Demonstrate basic LangGraph + MCP integration."""
    print("\n🤖 LangGraph + MCP Basic Agent Demo")
    print("=" * 50)
    
    agent = LangGraphMCPAgent(model_provider="openai")
    
    try:
        # Test queries that utilize different MCP tools
        test_queries = [
            "What's the current weather in San Francisco and what's 15% of 850?",
            "Search for recent news about artificial intelligence and save a summary to a file",
            "Calculate the area of a circle with radius 7.5 and explain the formula"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n👤 Query {i}: {query}")
            response = await agent.run_conversation(query)
            print(f"🤖 Response: {response}")
            
    finally:
        await agent.cleanup()

async def demo_research_assistant():
    """Demonstrate the specialized research assistant."""
    print("\n🔬 LangGraph + MCP Research Assistant Demo")
    print("=" * 50)
    
    assistant = ResearchAssistant(model_provider="openai")
    
    try:
        research_topics = [
            "Recent developments in quantum computing",
            "Impact of large language models on software development"
        ]
        
        for topic in research_topics:
            print(f"\n📚 Research Topic: {topic}")
            response = await assistant.conduct_research(topic, depth="moderate")
            print(f"📋 Research Report:\n{response}")
            
    finally:
        await assistant.cleanup()

async def demo_multi_step_workflow():
    """Demonstrate a complex multi-step workflow using MCP tools."""
    print("\n🔄 LangGraph + MCP Multi-Step Workflow Demo")
    print("=" * 50)
    
    agent = LangGraphMCPAgent(model_provider="openai")
    
    try:
        workflow_prompt = """
I need you to help me with a complex task that involves multiple steps:

1. Search for the latest information about "Python 3.13 new features"
2. Calculate how many days it's been since Python 3.13 was released (approximate if needed)
3. Create a summary file with the key features and save it as "python3.13_summary.txt"
4. Perform any additional analysis you think would be helpful

Please work through this systematically, using the appropriate tools for each step.
"""
        
        print(f"👤 Complex Workflow Request:")
        print(workflow_prompt)
        
        response = await agent.run_conversation(workflow_prompt)
        print(f"\n🤖 Workflow Result:\n{response}")
        
    finally:
        await agent.cleanup()

async def demo_mcp_tool_discovery():
    """Demonstrate MCP tool discovery and capabilities."""
    print("\n🔍 MCP Tool Discovery Demo")
    print("=" * 50)
    
    # Show how to inspect available MCP tools
    mcp_server_configs = {
        "web_search": {
            "command": "python",
            "args": ["mcp_servers/web_search_server.py"],
            "transport": "stdio"
        },
        "calculator": {
            "command": "python",
            "args": ["mcp_servers/calculator_server.py"],
            "transport": "stdio"
        }
    }
    
    async with MultiServerMCPClient(mcp_server_configs) as mcp_client:
        tools = await mcp_client.get_tools()
        
        print(f"📋 Discovered {len(tools)} MCP tools:")
        for tool in tools:
            print(f"  • {tool.name}: {tool.description}")
            if hasattr(tool, 'args_schema') and tool.args_schema:
                print(f"    Schema: {tool.args_schema}")
        
        print("\n✅ Tool discovery complete!")

async def main():
    """Main demo function."""
    print("🚀 LangGraph + MCP Integration Demo")
    print("=" * 50)
    print("This demo shows how to build LangGraph agents that leverage MCP servers")
    print("for enhanced capabilities including web search, calculations, and file operations.")
    
    # Check prerequisites
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("\n❌ Missing API keys!")
        print("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable:")
        print("export OPENAI_API_KEY='your-openai-api-key'")
        return
    
    try:
        # Run demos
        await demo_mcp_tool_discovery()
        await demo_basic_agent()
        await demo_research_assistant()
        await demo_multi_step_workflow()
        
        print("\n✅ All LangGraph + MCP demos completed!")
        print("\nKey Takeaways:")
        print("- MultiServerMCPClient enables connecting to multiple MCP servers")
        print("- LangGraph's create_react_agent works seamlessly with MCP tools")
        print("- Specialized agents can use different MCP tool combinations")
        print("- Complex workflows can leverage multiple tools systematically")
        
    except ImportError as e:
        print(f"\n❌ Missing dependencies: {e}")
        print("Please install required packages:")
        print("pip install -r requirements.txt")
        
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        print("Make sure MCP servers are available and API keys are configured.")

if __name__ == "__main__":
    asyncio.run(main())
