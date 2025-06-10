# OpenAI Agents SDK with MCP Integration Demo

This demo showcases how to build agents using OpenAI's Agents SDK that can connect to MCP servers to access external tools and data sources.

## What You'll Learn

- How to integrate MCP servers with OpenAI Agents SDK
- Using MCPServerStdio, MCPServerSse, and MCPServerStreamableHttp classes
- Building agents that leverage external MCP services
- Orchestrating multi-agent workflows with MCP capabilities

## Prerequisites

- Python 3.10+
- OpenAI API key
- Basic understanding of OpenAI Agents SDK and MCP concepts

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

3. Create a `.env` file:
```env
OPENAI_API_KEY=your-openai-api-key
```

## Demo Files

- `openai_mcp_agent.py` - Main OpenAI agent with MCP integration
- `multi_agent_coordinator.py` - Multi-agent system using MCP tools
- `mcp_server_examples.py` - Sample MCP servers for the demo
- `requirements.txt` - Python dependencies

## Running the Demo

1. Start any required MCP servers:
```bash
# If using local MCP servers
python mcp_server_examples.py
```

2. Run the OpenAI agents:
```bash
# Basic agent
python openai_mcp_agent.py

# Multi-agent coordinator
python multi_agent_coordinator.py
```

## Key Concepts

### MCP Server Integration
OpenAI Agents SDK supports three types of MCP servers:

```python
from openai_agents import Agent, MCPServerStdio, MCPServerSse, MCPServerStreamableHttp

# Stdio server (local)
stdio_server = MCPServerStdio(
    params={"command": "python", "args": ["server.py"]}
)

# SSE server (HTTP)
sse_server = MCPServerSse(
    url="http://localhost:8000/sse"
)

# Streamable HTTP server
http_server = MCPServerStreamableHttp(
    url="http://localhost:3000/mcp"
)

# Create agent with MCP servers
agent = Agent(
    name="Assistant",
    instructions="Use the tools to achieve the task",
    mcp_servers=[stdio_server, sse_server, http_server]
)
```

### Agent Orchestration
The SDK supports handoffs and guardrails for multi-agent coordination:

```python
# Agent with handoff capabilities
agent = Agent(
    name="MainAgent",
    instructions="Delegate tasks to specialized agents",
    handoff_targets=["SpecializedAgent"]
)
```

### Tool Discovery
MCP tools are automatically discovered and made available to agents:
- `list_tools()` is called on each agent run
- Tools are dynamically loaded from MCP servers
- LLM becomes aware of available capabilities

## References

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents MCP Integration](https://openai.github.io/openai-agents-python/mcp/)
- [MCP in OpenAI Products Announcement](https://venturebeat.com/ai/the-open-source-model-context-protocol-was-just-updated-heres-why-its-a-big-deal/)
- [OpenAI Agents SDK Examples](https://github.com/openai/openai-agents-python/tree/main/examples)
