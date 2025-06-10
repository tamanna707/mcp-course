#!/usr/bin/env python3
"""
OpenAI Agents SDK with MCP Integration Demo

This example shows how to create OpenAI agents that can use tools from MCP servers,
demonstrating the integration between OpenAI's Agents SDK and the Model Context Protocol.

Based on:
- OpenAI Agents SDK Documentation: https://openai.github.io/openai-agents-python/
- OpenAI MCP Integration: https://openai.github.io/openai-agents-python/mcp/
"""

import asyncio
import logging
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# OpenAI Agents SDK imports
from openai import OpenAI
from openai_agents import Agent, MCPServerStdio, MCPServerSse, MCPServerStreamableHttp
from openai_agents.handoffs import Handoff
from openai_agents.runtime import run_agent, run_agents_loop

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class OpenAIMCPAgent:
    """
    An OpenAI agent that integrates with MCP servers to provide enhanced capabilities
    through external tools and data sources.
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.agents = {}
        self.mcp_servers = {}
        
    def create_mcp_servers(self):
        """Create and configure MCP servers."""
        logger.info("Setting up MCP servers...")
        
        # Stdio MCP server (local)
        self.mcp_servers["filesystem"] = MCPServerStdio(
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
            }
        )
        
        # Custom MCP servers (if available)
        try:
            self.mcp_servers["weather"] = MCPServerStdio(
                params={
                    "command": "python",
                    "args": ["mcp_server_examples.py", "--mode", "weather"]
                }
            )
            
            self.mcp_servers["calculator"] = MCPServerStdio(
                params={
                    "command": "python", 
                    "args": ["mcp_server_examples.py", "--mode", "calculator"]
                }
            )
        except Exception as e:
            logger.warning(f"Custom MCP servers not available: {e}")
        
        # HTTP MCP server example (uncomment if you have a remote server)
        # self.mcp_servers["remote_api"] = MCPServerSse(
        #     url="http://localhost:8000/sse"
        # )
        
        logger.info(f"Configured {len(self.mcp_servers)} MCP servers")
    
    def create_main_agent(self):
        """Create the main agent with MCP integration."""
        logger.info("Creating main agent with MCP integration...")
        
        # Get all MCP servers for the main agent
        mcp_server_list = list(self.mcp_servers.values())
        
        self.agents["main"] = Agent(
            name="MainAssistant",
            instructions="""You are a helpful AI assistant with access to various tools through MCP servers.

You can:
- Access and manipulate files on the filesystem
- Get weather information for any location
- Perform mathematical calculations
- Connect to external APIs and services

When helping users:
1. Always explain what tools you're using and why
2. Use multiple tools if needed to provide comprehensive answers
3. Be transparent about your capabilities and limitations
4. Format responses clearly and helpfully

If a task requires specialized knowledge or capabilities that another agent might handle better, 
consider if you should delegate the task.""",
            mcp_servers=mcp_server_list,
            model="gpt-4o"
        )
        
        logger.info("Main agent created successfully!")
    
    def create_specialized_agents(self):
        """Create specialized agents for specific tasks."""
        logger.info("Creating specialized agents...")
        
        # Weather specialist agent
        weather_servers = [self.mcp_servers.get("weather")] if "weather" in self.mcp_servers else []
        if weather_servers and weather_servers[0]:
            self.agents["weather_specialist"] = Agent(
                name="WeatherSpecialist",
                instructions="""You are a weather specialist. You have access to weather tools and should:

1. Provide accurate, up-to-date weather information
2. Explain weather patterns and phenomena when relevant
3. Give practical advice based on weather conditions
4. Use appropriate weather terminology

Always cite your data sources and provide timestamps when available.""",
                mcp_servers=weather_servers,
                model="gpt-4o"
            )
        
        # File management specialist
        filesystem_servers = [self.mcp_servers.get("filesystem")] if "filesystem" in self.mcp_servers else []
        if filesystem_servers and filesystem_servers[0]:
            self.agents["file_specialist"] = Agent(
                name="FileSpecialist", 
                instructions="""You are a file management specialist. You can:

1. Read, write, and organize files
2. Search through file contents
3. Create and manage directory structures
4. Process and analyze text files

Security reminders:
- Only access files you're explicitly asked to work with
- Be careful with file operations that could be destructive
- Always confirm before making significant changes""",
                mcp_servers=filesystem_servers,
                model="gpt-4o"
            )
        
        # Calculator specialist
        calc_servers = [self.mcp_servers.get("calculator")] if "calculator" in self.mcp_servers else []
        if calc_servers and calc_servers[0]:
            self.agents["calc_specialist"] = Agent(
                name="CalculatorSpecialist",
                instructions="""You are a mathematical calculation specialist. You can:

1. Perform complex mathematical calculations
2. Solve equations and mathematical problems
3. Convert between different units and systems
4. Explain mathematical concepts and procedures

Always show your work and explain the steps in your calculations.""",
                mcp_servers=calc_servers,
                model="gpt-4o"
            )
        
        logger.info(f"Created {len(self.agents) - 1} specialized agents")
    
    def setup_handoffs(self):
        """Set up handoff capabilities between agents."""
        if "main" not in self.agents:
            return
            
        logger.info("Setting up agent handoffs...")
        
        handoff_targets = []
        
        # Add handoffs to available specialized agents
        for agent_name, agent in self.agents.items():
            if agent_name != "main":
                handoff_targets.append(agent_name)
        
        if handoff_targets:
            # Update main agent with handoff capabilities
            self.agents["main"].handoff_targets = handoff_targets
            logger.info(f"Main agent can now hand off to: {handoff_targets}")
    
    async def run_single_agent(self, query: str, agent_name: str = "main") -> str:
        """Run a single agent with the given query."""
        if agent_name not in self.agents:
            return f"Agent '{agent_name}' not found. Available agents: {list(self.agents.keys())}"
        
        try:
            logger.info(f"Running {agent_name} agent with query: {query[:50]}...")
            
            # Run the agent
            result = await run_agent(
                agent=self.agents[agent_name],
                query=query,
                client=self.client
            )
            
            return result.messages[-1].content if result.messages else "No response generated"
            
        except Exception as e:
            logger.error(f"Error running {agent_name} agent: {e}")
            return f"Error: {str(e)}"
    
    async def run_multi_agent_conversation(self, initial_query: str) -> List[str]:
        """Run a multi-agent conversation with handoffs."""
        try:
            logger.info(f"Starting multi-agent conversation: {initial_query[:50]}...")
            
            # Use the main agent as the entry point
            responses = []
            
            result = await run_agents_loop(
                agents=list(self.agents.values()),
                initial_query=initial_query,
                client=self.client,
                max_turns=10  # Prevent infinite loops
            )
            
            # Extract responses from the conversation
            for message in result.messages:
                responses.append(f"{message.sender}: {message.content}")
            
            return responses
            
        except Exception as e:
            logger.error(f"Error in multi-agent conversation: {e}")
            return [f"Error: {str(e)}"]

async def demo_basic_mcp_integration():
    """Demonstrate basic MCP integration with OpenAI agents."""
    print("\n🤖 OpenAI Agents + MCP Basic Integration Demo")
    print("=" * 60)
    
    agent_system = OpenAIMCPAgent()
    
    # Setup
    agent_system.create_mcp_servers()
    agent_system.create_main_agent()
    
    # Test queries
    test_queries = [
        "What files are in the /tmp directory?",
        "Create a file called 'test.txt' with the content 'Hello MCP!'",
        "Calculate the area of a circle with radius 5.5"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n👤 Query {i}: {query}")
        response = await agent_system.run_single_agent(query)
        print(f"🤖 Response: {response}")

async def demo_specialized_agents():
    """Demonstrate specialized agents using different MCP servers."""
    print("\n🎯 OpenAI Agents + MCP Specialized Agents Demo")
    print("=" * 60)
    
    agent_system = OpenAIMCPAgent()
    
    # Setup
    agent_system.create_mcp_servers()
    agent_system.create_main_agent()
    agent_system.create_specialized_agents()
    
    # Test each specialized agent
    test_scenarios = [
        ("file_specialist", "List all files in /tmp and create a summary file"),
        ("calc_specialist", "Calculate compound interest: $1000 at 5% for 10 years"),
        ("weather_specialist", "What's the weather like in New York today?")
    ]
    
    for agent_name, query in test_scenarios:
        if agent_name in agent_system.agents:
            print(f"\n🎯 {agent_name.title()}: {query}")
            response = await agent_system.run_single_agent(query, agent_name)
            print(f"🤖 Response: {response}")
        else:
            print(f"\n⚠️ {agent_name} not available (MCP server may not be running)")

async def demo_multi_agent_coordination():
    """Demonstrate multi-agent coordination with handoffs."""
    print("\n🤝 OpenAI Agents + MCP Multi-Agent Coordination Demo")
    print("=" * 60)
    
    agent_system = OpenAIMCPAgent()
    
    # Setup
    agent_system.create_mcp_servers()
    agent_system.create_main_agent()
    agent_system.create_specialized_agents()
    agent_system.setup_handoffs()
    
    # Complex query that might require multiple agents
    complex_query = """
    I need help with a project analysis:
    1. Create a file called 'project_analysis.txt'
    2. Calculate the ROI if we invest $50,000 and expect $75,000 return
    3. Add the ROI calculation to the file
    4. If possible, get weather information for our office location (San Francisco)
    
    Please coordinate between your specialized capabilities to complete this task.
    """
    
    print(f"👤 Complex Multi-Agent Query:")
    print(complex_query)
    
    # This would ideally use handoffs, but we'll simulate with the main agent
    response = await agent_system.run_single_agent(complex_query)
    print(f"\n🤖 Coordinated Response: {response}")

async def demo_mcp_server_types():
    """Demonstrate different MCP server transport types."""
    print("\n🔗 MCP Server Transport Types Demo")
    print("=" * 60)
    
    # Show different MCP server configurations
    print("1. 📡 Stdio MCP Server (Local Process):")
    stdio_config = {
        "type": "MCPServerStdio",
        "params": {
            "command": "python",
            "args": ["server.py"]
        },
        "description": "Runs as a local subprocess, communicates via stdin/stdout"
    }
    print(f"   Configuration: {stdio_config}")
    
    print("\n2. 🌐 SSE MCP Server (HTTP Server-Sent Events):")
    sse_config = {
        "type": "MCPServerSse", 
        "url": "http://localhost:8000/sse",
        "description": "Connects to remote HTTP server using Server-Sent Events"
    }
    print(f"   Configuration: {sse_config}")
    
    print("\n3. 🔄 Streamable HTTP MCP Server:")
    http_config = {
        "type": "MCPServerStreamableHttp",
        "url": "http://localhost:3000/mcp", 
        "description": "Uses Streamable HTTP transport for bidirectional communication"
    }
    print(f"   Configuration: {http_config}")
    
    print("\n📋 Transport Comparison:")
    print("   • Stdio: Best for local development, secure, fast")
    print("   • SSE: Good for remote servers, web-friendly")
    print("   • Streamable HTTP: Most flexible, supports advanced features")

async def demo_agent_capabilities():
    """Demonstrate OpenAI Agents SDK capabilities with MCP."""
    print("\n⚡ OpenAI Agents SDK + MCP Capabilities Demo")
    print("=" * 60)
    
    capabilities = {
        "Tool Integration": [
            "Automatic tool discovery from MCP servers",
            "Dynamic tool loading on agent execution",
            "Schema-based tool validation"
        ],
        "Agent Orchestration": [
            "Handoffs between specialized agents",
            "Guardrails for agent behavior",
            "Session management and state"
        ],
        "Observability": [
            "Built-in tracing and debugging",
            "Tool execution monitoring", 
            "Error handling and recovery"
        ],
        "MCP Integration": [
            "Multiple transport protocols",
            "Server lifecycle management",
            "Tool filtering and organization"
        ]
    }
    
    for category, features in capabilities.items():
        print(f"\n🔧 {category}:")
        for feature in features:
            print(f"   • {feature}")

async def main():
    """Main demo function."""
    print("🚀 OpenAI Agents SDK + MCP Integration Demo")
    print("=" * 60)
    print("This demo shows how to build agents using OpenAI's Agents SDK")
    print("that can leverage tools from MCP servers for enhanced capabilities.")
    
    # Check prerequisites
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Missing OPENAI_API_KEY environment variable")
        print("Please set it to your OpenAI API key:")
        print("export OPENAI_API_KEY='your-openai-api-key'")
        return
    
    try:
        # Run demos
        await demo_mcp_server_types()
        await demo_agent_capabilities()
        await demo_basic_mcp_integration()
        await demo_specialized_agents()
        await demo_multi_agent_coordination()
        
        print("\n✅ All OpenAI Agents + MCP demos completed!")
        print("\nKey Takeaways:")
        print("- OpenAI Agents SDK natively supports MCP integration")
        print("- Multiple MCP transport types available (stdio, SSE, HTTP)")
        print("- Agent handoffs enable sophisticated workflows")
        print("- Tools are automatically discovered and integrated")
        print("- Built-in observability and debugging capabilities")
        
    except ImportError as e:
        print(f"\n❌ Missing dependencies: {e}")
        print("Please install required packages:")
        print("pip install -r requirements.txt")
        
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        print("Make sure MCP servers are available and OpenAI API key is configured.")

if __name__ == "__main__":
    asyncio.run(main())
