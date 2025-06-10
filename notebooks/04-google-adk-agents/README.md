# Google ADK with MCP Integration Demo

This demo showcases how to build agents using Google's Agent Development Kit (ADK) that can connect to MCP servers to access external tools and data.

## What You'll Learn

- How to integrate MCP servers with Google ADK agents
- Using MCPToolset to expose MCP tools to ADK agents
- Building multi-agent systems with MCP capabilities
- Deploying ADK agents that leverage external MCP services

## Prerequisites

- Python 3.10+
- Google Cloud account (for Vertex AI access)
- ADK installed
- Basic understanding of MCP concepts

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google Cloud credentials:
```bash
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

3. Install ADK:
```bash
pip install google-adk
```

## Demo Files

- `adk_mcp_agent.py` - Main ADK agent with MCP integration
- `weather_mcp_server.py` - Sample weather MCP server
- `database_mcp_server.py` - Sample database MCP server  
- `requirements.txt` - Python dependencies
- `config.yaml` - ADK configuration

## Running the Demo

1. Start the MCP servers:
```bash
# Terminal 1 - Weather server
python weather_mcp_server.py

# Terminal 2 - Database server  
python database_mcp_server.py
```

2. Run the ADK agent:
```bash
python adk_mcp_agent.py
```

3. Test the integration through the ADK web interface or programmatically.

## Key Concepts

### MCPToolset Integration
ADK's `MCPToolset` class automatically discovers and adapts MCP tools for use within ADK agents:

```python
from adk.tools import MCPToolset

# Connect to MCP server
mcp_toolset = MCPToolset(
    server_config={
        "command": "python",
        "args": ["weather_mcp_server.py"],
        "transport": "stdio"
    }
)

# Use in agent
agent = LlmAgent(
    name="WeatherAgent",
    tools=[mcp_toolset]
)
```

### Agent Orchestration
ADK supports hierarchical agent structures where specialized agents handle specific tasks using MCP tools.

## References

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK MCP Integration Guide](https://google.github.io/adk-docs/tools/mcp-tools/)
- [Google ADK Examples](https://github.com/google/adk/tree/main/examples)
- [MCP Toolbox for Databases](https://cloud.google.com/blog/products/ai-machine-learning/mcp-toolbox-for-databases-now-supports-model-context-protocol)
