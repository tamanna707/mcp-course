# Demo 2: Creating Our First MCP Server (Claude Desktop Integration)

## Overview

This demo shows how to create an MCP server that integrates directly with Claude Desktop, demonstrating the practical workflow that users experience when using MCP in real applications.

## What You'll Learn

- How to create an MCP server optimized for Claude Desktop
- How to configure Claude Desktop to use your MCP server
- Best practices for MCP server development
- Testing and debugging MCP servers

## Demo Components

1. `weather_server.py` - A weather information MCP server
2. `file_manager_server.py` - A file management MCP server  
3. `claude_desktop_config.json` - Configuration for Claude Desktop
4. `test_with_inspector.py` - Testing script using MCP Inspector
5. `requirements.txt` - Dependencies

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Claude Desktop

1. Open Claude Desktop settings
2. Navigate to the MCP servers configuration
3. Add the configuration from `claude_desktop_config.json`
4. Restart Claude Desktop

### 3. Run the Server
```bash
python weather_server.py
```

### 4. Test with Claude Desktop

Open Claude Desktop and try these prompts:
- "What's the weather like in New York?"
- "Can you check the weather forecast for London?"
- "List the files in the current directory"

## Key Features Demonstrated

- **Tool Implementation**: Weather data retrieval and file operations
- **Error Handling**: Graceful handling of API failures
- **Input Validation**: Proper parameter validation
- **Claude Desktop Integration**: Seamless user experience

## References

- [Claude Desktop MCP Guide](https://claude.ai/docs/mcp)
- [MCP Server Development Guide](https://modelcontextprotocol.io/docs/concepts/servers)
- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk)
