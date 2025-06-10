#!/usr/bin/env python3
"""
Simple MCP Server for ADK Integration Demo
Provides basic tools for demonstrating MCP capabilities with Google ADK
"""

import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
import datetime
import json

# Create the MCP server instance
server = Server("simple-demo-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="get_current_time",
            description="Get the current time in various formats",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "Time format (e.g., 'iso', 'human', 'unix')",
                        "enum": ["iso", "human", "unix"],
                        "default": "human"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="calculate",
            description="Perform basic mathematical calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2')"
                    }
                },
                "required": ["expression"]
            }
        ),
        Tool(
            name="get_weather_info",
            description="Get simulated weather information for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name for weather information"
                    }
                },
                "required": ["location"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "get_current_time":
        format_type = arguments.get("format", "human")
        now = datetime.datetime.now()
        
        if format_type == "iso":
            result = now.isoformat()
        elif format_type == "unix":
            result = str(int(now.timestamp()))
        else:  # human
            result = now.strftime("%A, %B %d, %Y at %I:%M %p")
        
        return [TextContent(type="text", text=f"Current time: {result}")]
    
    elif name == "calculate":
        expression = arguments.get("expression", "")
        try:
            # Basic safe evaluation (limited to simple math operations)
            allowed_names = {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow
            }
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return [TextContent(type="text", text=f"Result: {result}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error calculating: {str(e)}")]
    
    elif name == "get_weather_info":
        location = arguments.get("location", "Unknown")
        # Simulated weather data
        weather_data = {
            "temperature": "72°F",
            "condition": "Partly cloudy",
            "humidity": "65%",
            "wind": "10 mph NW"
        }
        
        weather_json = json.dumps({
            "location": location,
            "weather": weather_data,
            "forecast": "Mild temperatures with occasional clouds"
        }, indent=2)
        
        return [TextContent(type="text", text=weather_json)]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())