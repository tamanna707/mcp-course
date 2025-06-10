#!/usr/bin/env python3
"""
Sample MCP Servers for OpenAI Agents SDK Demo

This module provides sample MCP servers that can be used with OpenAI Agents SDK
to demonstrate MCP integration capabilities.
"""

import asyncio
import argparse
import json
import logging
import math
import random
from datetime import datetime
from typing import Any, Dict, List
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_weather_server():
    """Create a weather MCP server."""
    app = Server("weather-server")
    
    # Sample weather data
    WEATHER_DATA = {
        "new york": {"temp": 72, "condition": "Partly cloudy", "humidity": 65},
        "san francisco": {"temp": 64, "condition": "Foggy", "humidity": 82},
        "london": {"temp": 59, "condition": "Light rain", "humidity": 78},
        "tokyo": {"temp": 68, "condition": "Sunny", "humidity": 55},
        "sydney": {"temp": 75, "condition": "Clear", "humidity": 60}
    }
    
    @app.list_tools()
    async def list_tools() -> List[types.Tool]:
        return [
            types.Tool(
                name="get_weather",
                description="Get current weather for a location",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"}
                    },
                    "required": ["location"]
                }
            )
        ]
    
    @app.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
        if name == "get_weather":
            location = arguments.get("location", "").lower()
            
            for city, data in WEATHER_DATA.items():
                if city in location or location in city:
                    result = f"🌤️ Weather in {location.title()}:\n"
                    result += f"Temperature: {data['temp']}°F\n"
                    result += f"Condition: {data['condition']}\n"
                    result += f"Humidity: {data['humidity']}%"
                    return [types.TextContent(type="text", text=result)]
            
            return [types.TextContent(
                type="text", 
                text=f"Weather data not available for {location}"
            )]
        
        raise ValueError(f"Unknown tool: {name}")
    
    return app

def create_calculator_server():
    """Create a calculator MCP server."""
    app = Server("calculator-server")
    
    @app.list_tools()
    async def list_tools() -> List[types.Tool]:
        return [
            types.Tool(
                name="calculate",
                description="Perform mathematical calculations",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string", 
                            "description": "Mathematical expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            ),
            types.Tool(
                name="circle_area",
                description="Calculate the area of a circle",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "radius": {
                            "type": "number",
                            "description": "Radius of the circle"
                        }
                    },
                    "required": ["radius"]
                }
            ),
            types.Tool(
                name="compound_interest",
                description="Calculate compound interest",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "principal": {"type": "number", "description": "Initial amount"},
                        "rate": {"type": "number", "description": "Annual interest rate (as decimal)"},
                        "time": {"type": "number", "description": "Time in years"},
                        "compounds": {"type": "number", "description": "Compounds per year", "default": 1}
                    },
                    "required": ["principal", "rate", "time"]
                }
            )
        ]
    
    @app.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
        if name == "calculate":
            expression = arguments.get("expression", "")
            try:
                # Simple expression evaluation (be careful in production!)
                result = eval(expression)
                return [types.TextContent(
                    type="text",
                    text=f"🧮 Calculation: {expression} = {result}"
                )]
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error evaluating expression: {str(e)}"
                )]
        
        elif name == "circle_area":
            radius = arguments.get("radius", 0)
            area = math.pi * radius * radius
            return [types.TextContent(
                type="text",
                text=f"🔵 Circle with radius {radius}: Area = {area:.2f} square units"
            )]
        
        elif name == "compound_interest":
            principal = arguments.get("principal", 0)
            rate = arguments.get("rate", 0)
            time = arguments.get("time", 0)
            compounds = arguments.get("compounds", 1)
            
            amount = principal * (1 + rate/compounds) ** (compounds * time)
            interest = amount - principal
            
            result = f"💰 Compound Interest Calculation:\n"
            result += f"Principal: ${principal:,.2f}\n"
            result += f"Rate: {rate*100:.2f}% annually\n"
            result += f"Time: {time} years\n"
            result += f"Compounds: {compounds} times per year\n"
            result += f"Final Amount: ${amount:,.2f}\n"
            result += f"Interest Earned: ${interest:,.2f}"
            
            return [types.TextContent(type="text", text=result)]
        
        raise ValueError(f"Unknown tool: {name}")
    
    return app

def create_data_server():
    """Create a data analysis MCP server."""
    app = Server("data-server")
    
    @app.list_tools()
    async def list_tools() -> List[types.Tool]:
        return [
            types.Tool(
                name="generate_sample_data",
                description="Generate sample data for analysis",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "size": {"type": "integer", "description": "Number of data points", "default": 10},
                        "data_type": {
                            "type": "string",
                            "enum": ["sales", "temperatures", "scores"],
                            "description": "Type of data to generate"
                        }
                    },
                    "required": ["data_type"]
                }
            ),
            types.Tool(
                name="analyze_numbers",
                description="Analyze a list of numbers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "List of numbers to analyze"
                        }
                    },
                    "required": ["numbers"]
                }
            )
        ]
    
    @app.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
        if name == "generate_sample_data":
            size = arguments.get("size", 10)
            data_type = arguments.get("data_type", "sales")
            
            if data_type == "sales":
                data = [random.randint(1000, 10000) for _ in range(size)]
                unit = "dollars"
            elif data_type == "temperatures":
                data = [round(random.uniform(60, 90), 1) for _ in range(size)]
                unit = "°F"
            elif data_type == "scores":
                data = [random.randint(60, 100) for _ in range(size)]
                unit = "points"
            
            result = f"📊 Generated {size} {data_type} data points:\n"
            result += f"{data}\n"
            result += f"Unit: {unit}"
            
            return [types.TextContent(type="text", text=result)]
        
        elif name == "analyze_numbers":
            numbers = arguments.get("numbers", [])
            
            if not numbers:
                return [types.TextContent(
                    type="text",
                    text="❌ No numbers provided for analysis"
                )]
            
            mean = sum(numbers) / len(numbers)
            sorted_nums = sorted(numbers)
            median = sorted_nums[len(sorted_nums)//2]
            minimum = min(numbers)
            maximum = max(numbers)
            
            result = f"📈 Statistical Analysis:\n"
            result += f"Count: {len(numbers)}\n"
            result += f"Mean: {mean:.2f}\n"
            result += f"Median: {median}\n"
            result += f"Min: {minimum}\n"
            result += f"Max: {maximum}\n"
            result += f"Range: {maximum - minimum}"
            
            return [types.TextContent(type="text", text=result)]
        
        raise ValueError(f"Unknown tool: {name}")
    
    return app

async def run_server(server_type: str):
    """Run the specified MCP server."""
    if server_type == "weather":
        app = create_weather_server()
        logger.info("Starting Weather MCP Server...")
    elif server_type == "calculator":
        app = create_calculator_server()
        logger.info("Starting Calculator MCP Server...")
    elif server_type == "data":
        app = create_data_server()
        logger.info("Starting Data Analysis MCP Server...")
    else:
        raise ValueError(f"Unknown server type: {server_type}")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

def main():
    """Main function to run MCP servers."""
    parser = argparse.ArgumentParser(description="Run sample MCP servers for OpenAI Agents SDK demo")
    parser.add_argument(
        "--mode",
        choices=["weather", "calculator", "data"],
        required=True,
        help="Type of MCP server to run"
    )
    
    args = parser.parse_args()
    
    asyncio.run(run_server(args.mode))

if __name__ == "__main__":
    main()
