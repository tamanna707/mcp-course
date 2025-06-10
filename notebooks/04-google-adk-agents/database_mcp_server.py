#!/usr/bin/env python3
"""
Database MCP Server for ADK Integration Demo

A sample MCP server providing database query tools that can be used
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

# Sample database data
DATABASE = {
    "weather_history": [
        {"date": "2024-12-01", "location": "New York", "temperature": 68, "conditions": "Sunny"},
        {"date": "2024-12-02", "location": "New York", "temperature": 71, "conditions": "Partly cloudy"},
        {"date": "2024-12-03", "location": "New York", "temperature": 65, "conditions": "Cloudy"},
        {"date": "2024-12-01", "location": "San Francisco", "temperature": 62, "conditions": "Foggy"},
        {"date": "2024-12-02", "location": "San Francisco", "temperature": 64, "conditions": "Sunny"},
        {"date": "2024-12-03", "location": "San Francisco", "temperature": 66, "conditions": "Partly cloudy"},
        {"date": "2024-12-01", "location": "London", "temperature": 55, "conditions": "Rainy"},
        {"date": "2024-12-02", "location": "London", "temperature": 58, "conditions": "Cloudy"},
        {"date": "2024-12-03", "location": "London", "temperature": 60, "conditions": "Partly cloudy"},
    ],
    "locations": [
        {"name": "New York", "country": "USA", "timezone": "EST", "coordinates": {"lat": 40.7128, "lon": -74.0060}},
        {"name": "San Francisco", "country": "USA", "timezone": "PST", "coordinates": {"lat": 37.7749, "lon": -122.4194}},
        {"name": "London", "country": "UK", "timezone": "GMT", "coordinates": {"lat": 51.5074, "lon": -0.1278}},
        {"name": "Paris", "country": "France", "timezone": "CET", "coordinates": {"lat": 48.8566, "lon": 2.3522}},
        {"name": "Tokyo", "country": "Japan", "timezone": "JST", "coordinates": {"lat": 35.6762, "lon": 139.6503}},
    ],
    "events": [
        {"date": "2024-12-10", "location": "New York", "event": "Outdoor Concert", "weather_dependent": True},
        {"date": "2024-12-12", "location": "San Francisco", "event": "Tech Conference", "weather_dependent": False},
        {"date": "2024-12-15", "location": "London", "event": "Marathon", "weather_dependent": True},
        {"date": "2024-12-18", "location": "Paris", "event": "Fashion Show", "weather_dependent": False},
        {"date": "2024-12-20", "location": "Tokyo", "event": "Cherry Blossom Festival", "weather_dependent": True},
    ]
}

# Initialize the MCP server
app = Server("database-mcp-server")

@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available database tools."""
    return [
        types.Tool(
            name="query_weather_history",
            description="Query historical weather data from the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to query (optional)"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format (optional)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format (optional)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of records to return",
                        "default": 10
                    }
                }
            }
        ),
        types.Tool(
            name="get_location_info",
            description="Get detailed information about a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location name to look up"
                    }
                },
                "required": ["location"]
            }
        ),
        types.Tool(
            name="find_events",
            description="Find events in the database, optionally filtered by location or weather dependency",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to filter by (optional)"
                    },
                    "weather_dependent": {
                        "type": "boolean",
                        "description": "Filter by weather dependency (optional)"
                    },
                    "date_from": {
                        "type": "string",
                        "description": "Start date filter in YYYY-MM-DD format (optional)"
                    },
                    "date_to": {
                        "type": "string",
                        "description": "End date filter in YYYY-MM-DD format (optional)"
                    }
                }
            }
        ),
        types.Tool(
            name="calculate_weather_stats",
            description="Calculate weather statistics for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to calculate stats for"
                    },
                    "metric": {
                        "type": "string",
                        "enum": ["average_temperature", "temperature_range", "conditions_summary"],
                        "description": "Type of statistic to calculate",
                        "default": "average_temperature"
                    }
                },
                "required": ["location"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls."""
    logger.info(f"Database tool called: {name} with arguments: {arguments}")
    
    if name == "query_weather_history":
        location = arguments.get("location", "").lower()
        start_date = arguments.get("start_date")
        end_date = arguments.get("end_date")
        limit = arguments.get("limit", 10)
        
        # Filter weather history data
        filtered_data = DATABASE["weather_history"]
        
        if location:
            filtered_data = [record for record in filtered_data if location in record["location"].lower()]
        
        if start_date:
            filtered_data = [record for record in filtered_data if record["date"] >= start_date]
        
        if end_date:
            filtered_data = [record for record in filtered_data if record["date"] <= end_date]
        
        # Apply limit
        filtered_data = filtered_data[:limit]
        
        if not filtered_data:
            return [types.TextContent(
                type="text",
                text="❌ No weather history records found matching the criteria."
            )]
        
        formatted_response = f"📊 **Weather History Query Results**\n\n"
        formatted_response += f"**Records found:** {len(filtered_data)}\n\n"
        
        for record in filtered_data:
            formatted_response += f"**{record['date']}** - {record['location']}: {record['temperature']}°F, {record['conditions']}\n"
        
        # Add summary statistics
        if filtered_data:
            temps = [record["temperature"] for record in filtered_data]
            avg_temp = sum(temps) / len(temps)
            min_temp = min(temps)
            max_temp = max(temps)
            
            formatted_response += f"\n**Summary Statistics:**\n"
            formatted_response += f"- Average Temperature: {avg_temp:.1f}°F\n"
            formatted_response += f"- Temperature Range: {min_temp}°F - {max_temp}°F\n"
        
        return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get_location_info":
        location = arguments.get("location", "").lower()
        
        # Find location info
        location_info = None
        for loc in DATABASE["locations"]:
            if location in loc["name"].lower():
                location_info = loc
                break
        
        if not location_info:
            return [types.TextContent(
                type="text",
                text=f"❌ Location '{arguments.get('location')}' not found in database. Available locations: {', '.join([loc['name'] for loc in DATABASE['locations']])}"
            )]
        
        formatted_response = f"🌍 **Location Information: {location_info['name']}**\n\n"
        formatted_response += f"**Country:** {location_info['country']}\n"
        formatted_response += f"**Timezone:** {location_info['timezone']}\n"
        formatted_response += f"**Coordinates:** {location_info['coordinates']['lat']}°, {location_info['coordinates']['lon']}°\n"
        
        # Add related weather history count
        history_count = len([record for record in DATABASE["weather_history"] 
                           if location_info["name"].lower() in record["location"].lower()])
        formatted_response += f"**Historical Records:** {history_count} weather records available\n"
        
        # Add upcoming events
        upcoming_events = [event for event in DATABASE["events"] 
                          if location_info["name"].lower() in event["location"].lower()]
        if upcoming_events:
            formatted_response += f"**Upcoming Events:** {len(upcoming_events)} events scheduled\n"
        
        return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "find_events":
        location = arguments.get("location", "").lower()
        weather_dependent = arguments.get("weather_dependent")
        date_from = arguments.get("date_from")
        date_to = arguments.get("date_to")
        
        # Filter events
        filtered_events = DATABASE["events"]
        
        if location:
            filtered_events = [event for event in filtered_events if location in event["location"].lower()]
        
        if weather_dependent is not None:
            filtered_events = [event for event in filtered_events if event["weather_dependent"] == weather_dependent]
        
        if date_from:
            filtered_events = [event for event in filtered_events if event["date"] >= date_from]
        
        if date_to:
            filtered_events = [event for event in filtered_events if event["date"] <= date_to]
        
        if not filtered_events:
            return [types.TextContent(
                type="text",
                text="❌ No events found matching the criteria."
            )]
        
        formatted_response = f"📅 **Events Query Results**\n\n"
        formatted_response += f"**Events found:** {len(filtered_events)}\n\n"
        
        for event in filtered_events:
            weather_icon = "🌤️" if event["weather_dependent"] else "🏢"
            formatted_response += f"{weather_icon} **{event['date']}** - {event['location']}: {event['event']}\n"
            formatted_response += f"   Weather Dependent: {'Yes' if event['weather_dependent'] else 'No'}\n\n"
        
        return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "calculate_weather_stats":
        location = arguments.get("location", "").lower()
        metric = arguments.get("metric", "average_temperature")
        
        # Find weather data for location
        location_data = [record for record in DATABASE["weather_history"] 
                        if location in record["location"].lower()]
        
        if not location_data:
            return [types.TextContent(
                type="text",
                text=f"❌ No weather data found for '{arguments.get('location')}'"
            )]
        
        formatted_response = f"📈 **Weather Statistics for {arguments.get('location').title()}**\n\n"
        
        if metric == "average_temperature":
            temps = [record["temperature"] for record in location_data]
            avg_temp = sum(temps) / len(temps)
            formatted_response += f"**Average Temperature:** {avg_temp:.1f}°F\n"
            formatted_response += f"**Based on:** {len(location_data)} records\n"
            
        elif metric == "temperature_range":
            temps = [record["temperature"] for record in location_data]
            min_temp = min(temps)
            max_temp = max(temps)
            temp_range = max_temp - min_temp
            formatted_response += f"**Temperature Range:** {temp_range}°F\n"
            formatted_response += f"**Minimum:** {min_temp}°F\n"
            formatted_response += f"**Maximum:** {max_temp}°F\n"
            
        elif metric == "conditions_summary":
            conditions = [record["conditions"] for record in location_data]
            condition_counts = {}
            for condition in conditions:
                condition_counts[condition] = condition_counts.get(condition, 0) + 1
            
            formatted_response += f"**Weather Conditions Summary:**\n"
            for condition, count in sorted(condition_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(conditions)) * 100
                formatted_response += f"- {condition}: {count} days ({percentage:.1f}%)\n"
        
        formatted_response += f"\n*Analysis period: {len(location_data)} days*"
        
        return [types.TextContent(type="text", text=formatted_response)]
    
    else:
        raise ValueError(f"Unknown database tool: {name}")

async def main():
    """Run the database MCP server."""
    logger.info("Starting Database MCP Server for ADK integration...")
    logger.info("Available tools: query_weather_history, get_location_info, find_events, calculate_weather_stats")
    logger.info(f"Database contains {len(DATABASE['weather_history'])} weather records, {len(DATABASE['locations'])} locations, {len(DATABASE['events'])} events")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
