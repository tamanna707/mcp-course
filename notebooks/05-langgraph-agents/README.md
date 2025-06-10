# LangGraph with MCP Integration Demo

This demo showcases how to build agents using LangGraph that can connect to MCP servers to access external tools and data sources.

## What You'll Learn

- How to integrate MCP servers with LangGraph agents
- Using MultiServerMCPClient to connect to multiple MCP servers
- Building ReAct agents that leverage MCP tools
- Creating multi-agent workflows with MCP capabilities

## Prerequisites

- Python 3.10+
- OpenAI API key (or other LLM provider)
- Basic understanding of LangGraph and MCP concepts

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
ANTHROPIC_API_KEY=your-anthropic-api-key  # Optional
```

## Demo Files

- `langgraph_mcp_agent.py` - Main LangGraph agent with MCP integration
- `research_assistant.py` - Research assistant using multiple MCP servers
- `multi_agent_system.py` - Multi-agent coordination with MCP tools
- `mcp_servers/` - Sample MCP servers for the demo
- `requirements.txt` - Python dependencies

## Running the Demo

1. Start the MCP servers (if using local servers):
```bash
# Terminal 1 - Web search server
python mcp_servers/web_search_server.py

# Terminal 2 - File system server
python mcp_servers/file_system_server.py
```

2. Run the LangGraph agents:
```bash
# Simple agent
python langgraph_mcp_agent.py

# Research assistant
python research_assistant.py

# Multi-agent system
python multi_agent_system.py
```

## Key Concepts

### MultiServerMCPClient
LangGraph uses `langchain-mcp-adapters` to connect to multiple MCP servers:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

async with MultiServerMCPClient({
    "web_search": {
        "command": "python",
        "args": ["web_search_server.py"],
        "transport": "stdio"
    },
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"],
        "transport": "stdio"
    }
}) as mcp_client:
    tools = await mcp_client.get_tools()
    # Use tools with LangGraph agents
```

### ReAct Agent Pattern
LangGraph's `create_react_agent` works seamlessly with MCP tools:

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=ChatOpenAI(model="gpt-4"),
    tools=mcp_tools
)
```

### Multi-Agent Coordination
LangGraph enables complex workflows where different agents use different MCP servers for specialized tasks.

## References

- [LangGraph MCP Integration](https://langchain-ai.github.io/langgraph/agents/mcp/)
- [LangChain MCP Adapters](https://changelog.langchain.com/announcements/mcp-adapters-for-langchain-and-langgraph)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [MCP Tools Examples](https://github.com/esxr/langgraph-mcp)
