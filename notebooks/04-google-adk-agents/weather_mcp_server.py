#!/usr/bin/env python3
"""
Weather MCP Server for ADK Integration Demo

A sample MCP server providing weather-related tools that can be used
by Google ADK agents through MCPToolset integration.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample weather data (in production, this would come from a real weather API)
WEATHER_DATA = {
    "new york": {
        "current": {
            "temperature": 72,
            "humidity": 65,
            "conditions": "Partly cloudy",
            "wind_speed": 8,
            "wind_direction": "NW"
        },
        "forecast": [
            {"day": "Today", "high": 75, "low": 62, "conditions": "Partly cloudy"},
            {"day": "Tomorrow", "high": 78, "low": 65, "conditions": "Sunny"},
            {"day": "Day 3", "high": 73, "low": 60, "conditions": "Light rain"},
            {"day": "Day 4", "high": 70, "low": 58, "conditions": "Cloudy"},
            {"day": "Day 5", "high": 74, "low": 61, "conditions": "Sunny"}
        ]
    },
    "san francisco": {
        "current": {
            "temperature": 64,
            "humidity": 82,
            "conditions": "Foggy",
            "wind_speed": 12,
            "wind_direction": "W"
        },
        "forecast": [
            {"day": "Today", "high": 67, "low": 55, "conditions": "Foggy"},
            {"day": "Tomorrow", "high": 69, "low": 57, "conditions": "Partly cloudy"},
            {"day": "Day 3", "high": 71, "low": 59, "conditions": "Sunny"},
            {"day": "Day 4", "high": 68, "low": 56, "conditions": "Cloudy"},
            {"day": "Day 5", "high": 65, "low": 54, "conditions": "Foggy"}
        ]
    },
    "london": {
        "current": {
            "temperature": 59,
            "humidity": 78,
            "conditions": "Light rain",
            "wind_speed": 15,
            "wind_direction": "SW"
        },
        "forecast": [
            {"day": "Today", "high": 61, "low": 48, "conditions": "Light rain"},
            {"day": "Tomorrow", "high": 63, "low": 50, "conditions": "Cloudy"},
            {"day": "Day 3", "high": 66, "low": 52, "conditions": "Partly cloudy"},
            {"day": "Day 4", "high": 58, "low": 46, "conditions": "Heavy rain"},
            {"day": "Day 5", "high": 60, "low": 49, "conditions": "Cloudy"}
        ]
    }
}

# Initialize the MCP server
app = Server("weather-mcp-server")

@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available weather tools."""
    return [
        types.Tool(
            name="get_weather",
            description="Get current weather conditions for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or location"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["fahrenheit", "celsius"],
                        "description": "Temperature units",
                        "default": "fahrenheit"
                    }
                },
                "required": ["location"]
            }
        ),
        types.Tool(
            name="get_forecast",
            description="Get weather forecast for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or location"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to forecast (1-5)",
                        "minimum": 1,
                        "maximum": 5,
                        "default": 3
                    },
                    "units": {
                        "type": "string",
                        "enum": ["fahrenheit", "celsius"],
                        "description": "Temperature units",
                        "default": "fahrenheit"
                    }
                },
                "required": ["location"]
            }
        ),
        types.Tool(
            name="get_weather_alerts",
            description="Get weather alerts and warnings for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or location"
                    }
                },
                "required": ["location"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls."""
    logger.info(f"Weather tool called: {name} with arguments: {arguments}")
    
    location = arguments.get("location", "").lower()
    units = arguments.get("units", "fahrenheit")
    
    def convert_temperature(temp_f: float, target_units: str) -> float:
        """Convert temperature between Fahrenheit and Celsius."""
        if target_units == "celsius":
            return round((temp_f - 32) * 5/9, 1)
        return temp_f
    
    def format_temperature(temp: float, units: str) -> str:
        """Format temperature with units."""
        unit_symbol = "°F" if units == "fahrenheit" else "°C"
        return f"{temp}{unit_symbol}"
    
    if name == "get_weather":
        # Find weather data for location
        weather_info = None
        for city, data in WEATHER_DATA.items():
            if city in location or location in city:
                weather_info = data
                break
        
        if not weather_info:
            return [types.TextContent(
                type="text",
                text=f"❌ Weather data not available for '{arguments.get('location')}'. Available locations: {', '.join(WEATHER_DATA.keys())}"
            )]
        
        current = weather_info["current"]
        temp = convert_temperature(current["temperature"], units)
        
        result = {
            "location": arguments.get("location"),
            "current_conditions": {
                "temperature": format_temperature(temp, units),
                "humidity": f"{current['humidity']}%",
                "conditions": current["conditions"],
                "wind": f"{current['wind_speed']} mph {current['wind_direction']}"
            },
            "timestamp": datetime.now().isoformat(),
            "source": "Weather MCP Server"
        }
        
        formatted_response = f"""🌤️ **Current Weather for {arguments.get('location').title()}**

**Temperature:** {format_temperature(temp, units)}
**Conditions:** {current['conditions']}
**Humidity:** {current['humidity']}%
**Wind:** {current['wind_speed']} mph {current['wind_direction']}

*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"""
        
        return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get_forecast":
        days = min(arguments.get("days", 3), 5)
        
        # Find weather data for location
        weather_info = None
        for city, data in WEATHER_DATA.items():
            if city in location or location in city:
                weather_info = data
                break
        
        if not weather_info:
            return [types.TextContent(
                type="text",
                text=f"❌ Forecast data not available for '{arguments.get('location')}'. Available locations: {', '.join(WEATHER_DATA.keys())}"
            )]
        
        forecast = weather_info["forecast"][:days]
        
        formatted_response = f"📅 **{days}-Day Weather Forecast for {arguments.get('location').title()}**\n\n"
        
        for day_forecast in forecast:
            high_temp = convert_temperature(day_forecast["high"], units)
            low_temp = convert_temperature(day_forecast["low"], units)
            
            formatted_response += f"**{day_forecast['day']}:** {format_temperature(high_temp, units)} / {format_temperature(low_temp, units)} - {day_forecast['conditions']}\n"
        
        formatted_response += f"\n*Forecast generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        
        return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get_weather_alerts":
        # Simulate weather alerts (in production, this would come from weather services)
        alerts = []
        
        # Add some sample alerts based on location
        if "new york" in location:
            alerts.append({
                "type": "Advisory",
                "title": "Heat Advisory",
                "description": "Temperatures may reach 85°F today. Stay hydrated.",
                "severity": "Minor",
                "expires": (datetime.now() + timedelta(hours=8)).isoformat()
            })
        elif "london" in location:
            alerts.append({
                "type": "Warning",
                "title": "Heavy Rain Warning",
                "description": "Heavy rainfall expected. Potential for flooding in low-lying areas.",
                "severity": "Moderate",
                "expires": (datetime.now() + timedelta(hours=12)).isoformat()
            })
        
        if alerts:
            formatted_response = f"⚠️ **Weather Alerts for {arguments.get('location').title()}**\n\n"
            for alert in alerts:
                formatted_response += f"**{alert['type']}:** {alert['title']}\n"
                formatted_response += f"**Severity:** {alert['severity']}\n"
                formatted_response += f"**Description:** {alert['description']}\n"
                formatted_response += f"**Expires:** {alert['expires']}\n\n"
        else:
            formatted_response = f"✅ **No Weather Alerts for {arguments.get('location').title()}**\n\nNo current weather warnings or advisories."
        
        return [types.TextContent(type="text", text=formatted_response)]
    
    else:
        raise ValueError(f"Unknown weather tool: {name}")

async def main():
    """Run the weather MCP server."""
    logger.info("Starting Weather MCP Server for ADK integration...")
    logger.info("Available tools: get_weather, get_forecast, get_weather_alerts")
    logger.info("Available locations: " + ", ".join(WEATHER_DATA.keys()))
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
