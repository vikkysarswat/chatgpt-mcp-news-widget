"""MCP Server for News Fetching from MongoDB.

This server implements the Model Context Protocol to provide news fetching
capabilities to OpenAI apps like ChatGPT.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from pydantic import BaseModel, Field

from mongodb_client import MongoDBClient
from tools.fetch_news import FetchNewsTool
from config.settings import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPNewsServer:
    """MCP Server for news fetching operations."""

    def __init__(self, settings: Settings):
        """Initialize the MCP server.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.server = Server("news-mcp-server")
        self.mongodb_client = MongoDBClient(
            uri=settings.mongodb_uri,
            database=settings.mongodb_database,
            collection=settings.mongodb_collection
        )
        self.fetch_news_tool = FetchNewsTool(self.mongodb_client)
        
        # Register handlers
        self._register_handlers()
        
    def _register_handlers(self):
        """Register MCP protocol handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="fetch_news",
                    description="Fetch news articles from MongoDB. You can filter by category, tags, date range, and search keywords.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of articles to fetch (default: 10, max: 50)",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 50
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter by news category (e.g., 'technology', 'business', 'sports')"
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Filter by tags (e.g., ['ai', 'machine-learning'])"
                            },
                            "search_query": {
                                "type": "string",
                                "description": "Search in title and content"
                            },
                            "hours_ago": {
                                "type": "integer",
                                "description": "Fetch articles from the last N hours",
                                "minimum": 1
                            },
                            "sort_by": {
                                "type": "string",
                                "enum": ["published_at", "title"],
                                "description": "Sort articles by field (default: published_at)",
                                "default": "published_at"
                            },
                            "sort_order": {
                                "type": "string",
                                "enum": ["asc", "desc"],
                                "description": "Sort order (default: desc)",
                                "default": "desc"
                            }
                        },
                        "required": []
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool execution.
            
            Args:
                name: Tool name
                arguments: Tool arguments
                
            Returns:
                List of content items
            """
            if name == "fetch_news":
                return await self.fetch_news_tool.execute(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting News MCP Server...")
        
        # Connect to MongoDB
        await self.mongodb_client.connect()
        logger.info(f"Connected to MongoDB: {self.settings.mongodb_database}")
        
        try:
            # Run the server with stdio transport
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        finally:
            # Clean up
            await self.mongodb_client.close()
            logger.info("Server stopped")


async def main():
    """Main entry point."""
    # Load settings
    settings = Settings()
    
    # Create and run server
    server = MCPNewsServer(settings)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())