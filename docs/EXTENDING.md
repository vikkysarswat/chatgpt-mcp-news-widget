# Extending the News MCP Server

This guide shows you how to add new tools to your MCP server beyond the basic `fetch_news` tool.

## Table of Contents

1. [Understanding MCP Tools](#understanding-mcp-tools)
2. [Creating a New Tool](#creating-a-new-tool)
3. [Tool Examples](#tool-examples)
4. [Widget Customization](#widget-customization)
5. [Best Practices](#best-practices)

## Understanding MCP Tools

MCP (Model Context Protocol) tools are functions that ChatGPT can call to perform specific tasks. Each tool:

- Has a unique name
- Defines input parameters (schema)
- Returns structured output
- Can be displayed as widgets in ChatGPT

## Creating a New Tool

### Step 1: Create Tool File

Create a new file in `src/tools/`, for example `src/tools/search_news.py`:

```python
"""Search news tool implementation."""

import logging
from typing import Any, Dict, List

from mcp.types import TextContent
from mongodb_client import MongoDBClient

logger = logging.getLogger(__name__)


class SearchNewsTool:
    """Tool for searching news articles."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize the search news tool.
        
        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client

    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute the search news tool.
        
        Args:
            arguments: Tool arguments
            
        Returns:
            List of content items
        """
        try:
            query = arguments.get("query", "")
            limit = arguments.get("limit", 10)
            
            # Perform search
            articles = await self.mongodb_client.fetch_news(
                search_query=query,
                limit=limit
            )
            
            # Format results
            if not articles:
                return [
                    TextContent(
                        type="text",
                        text=f"No articles found for '{query}'."
                    )
                ]
            
            # Create output
            output = f"Found {len(articles)} articles for '{query}':\n\n"
            for i, article in enumerate(articles, 1):
                output += f"{i}. {article['title']}\n"
                output += f"   {article['description'][:100]}...\n\n"
            
            return [
                TextContent(
                    type="text",
                    text=output
                )
            ]
            
        except Exception as e:
            logger.error(f"Error searching news: {e}", exc_info=True)
            return [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
```

### Step 2: Register Tool in MCP Server

Update `src/mcp_server.py`:

```python
from tools.fetch_news import FetchNewsTool
from tools.search_news import SearchNewsTool  # Add import

class MCPNewsServer:
    def __init__(self, settings: Settings):
        # ... existing code ...
        self.search_news_tool = SearchNewsTool(self.mongodb_client)  # Add
        
    def _register_handlers(self):
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                # ... existing fetch_news tool ...
                Tool(
                    name="search_news",
                    description="Search news articles by keywords",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Max results",
                                "default": 10
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]):
            if name == "fetch_news":
                return await self.fetch_news_tool.execute(arguments)
            elif name == "search_news":  # Add handler
                return await self.search_news_tool.execute(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
```

### Step 3: Update OpenAI App Manifest

Update `openai_app/app_manifest.json`:

```json
{
  "capabilities": {
    "tools": [
      {
        "name": "fetch_news",
        "description": "Fetch news articles from database"
      },
      {
        "name": "search_news",
        "description": "Search news by keywords"
      }
    ]
  }
}
```

### Step 4: Test Your Tool

Create a test file `tests/test_search_tool.py`:

```python
import pytest
from src.tools.search_news import SearchNewsTool

@pytest.mark.asyncio
async def test_search_news(mock_mongodb_client):
    tool = SearchNewsTool(mock_mongodb_client)
    result = await tool.execute({"query": "AI"})
    assert len(result) > 0
```

## Tool Examples

### Example 1: Get News Categories

```python
# src/tools/get_categories.py
class GetCategoriesTool:
    """Get available news categories."""
    
    def __init__(self, mongodb_client: MongoDBClient):
        self.mongodb_client = mongodb_client
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        categories = await self.mongodb_client.get_categories()
        
        output = "Available categories:\n\n"
        for cat in categories:
            count = await self.mongodb_client.count_articles(
                {"category": cat}
            )
            output += f"- {cat} ({count} articles)\n"
        
        return [TextContent(type="text", text=output)]
```

### Example 2: Get Trending News

```python
# src/tools/trending_news.py
from datetime import datetime, timedelta

class TrendingNewsTool:
    """Get trending news based on recency and category."""
    
    def __init__(self, mongodb_client: MongoDBClient):
        self.mongodb_client = mongodb_client
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        hours = arguments.get("hours", 24)
        limit = arguments.get("limit", 10)
        
        articles = await self.mongodb_client.fetch_news(
            hours_ago=hours,
            limit=limit,
            sort_by="published_at",
            sort_order="desc"
        )
        
        # Format as trending widget
        output = f"🔥 Trending in the last {hours} hours:\n\n"
        for i, article in enumerate(articles, 1):
            output += f"{i}. {article['title']}\n"
            output += f"   📰 {article['source']} | 🏷️ {article['category']}\n\n"
        
        return [TextContent(type="text", text=output)]
```

### Example 3: Save Article (User Favorites)

```python
# src/tools/save_article.py
class SaveArticleTool:
    """Save article to user's favorites."""
    
    def __init__(self, mongodb_client: MongoDBClient):
        self.mongodb_client = mongodb_client
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        article_id = arguments.get("article_id")
        user_id = arguments.get("user_id")  # From OAuth
        
        # Add to favorites collection
        favorites_collection = self.mongodb_client.database["favorites"]
        await favorites_collection.insert_one({
            "user_id": user_id,
            "article_id": article_id,
            "saved_at": datetime.utcnow()
        })
        
        return [
            TextContent(
                type="text",
                text="✓ Article saved to your favorites!"
            )
        ]
```

### Example 4: News Summary

```python
# src/tools/summarize_news.py
class SummarizeNewsTool:
    """Summarize multiple news articles."""
    
    def __init__(self, mongodb_client: MongoDBClient):
        self.mongodb_client = mongodb_client
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        category = arguments.get("category")
        hours = arguments.get("hours", 24)
        
        articles = await self.mongodb_client.fetch_news(
            category=category,
            hours_ago=hours,
            limit=20
        )
        
        # Create summary
        output = f"News Summary - {category} (last {hours}h):\n\n"
        output += f"Total articles: {len(articles)}\n\n"
        
        # Group by source
        sources = {}
        for article in articles:
            source = article['source']
            sources[source] = sources.get(source, 0) + 1
        
        output += "Top sources:\n"
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]:
            output += f"- {source}: {count} articles\n"
        
        return [TextContent(type="text", text=output)]
```

## Widget Customization

### Creating Custom Widgets

Add to `openai_app/widget_config.json`:

```json
{
  "type": "trending_widget",
  "name": "Trending News Widget",
  "schema": {
    "type": "object",
    "properties": {
      "articles": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "title": {"type": "string"},
            "trending_score": {"type": "number"},
            "emoji": {"type": "string"}
          }
        }
      }
    }
  },
  "template": {
    "layout": "list",
    "style": {
      "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      "color": "white",
      "padding": "20px",
      "borderRadius": "12px"
    },
    "elements": [
      {
        "type": "header",
        "content": "🔥 Trending Now",
        "style": {
          "fontSize": "24px",
          "fontWeight": "bold",
          "marginBottom": "16px"
        }
      },
      {
        "type": "list",
        "items": "{{articles}}",
        "itemTemplate": {
          "elements": [
            {
              "type": "text",
              "content": "{{emoji}} {{title}}",
              "style": {
                "fontSize": "16px",
                "marginBottom": "8px"
              }
            }
          ]
        }
      }
    ]
  }
}
```

## Best Practices

### 1. Error Handling

Always handle errors gracefully:

```python
try:
    result = await self.mongodb_client.fetch_news(...)
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    return [
        TextContent(
            type="text",
            text="Sorry, an error occurred. Please try again."
        )
    ]
```

### 2. Input Validation

```python
def validate_arguments(self, arguments: Dict[str, Any]):
    """Validate tool arguments."""
    limit = arguments.get("limit", 10)
    if limit < 1 or limit > 50:
        raise ValueError("Limit must be between 1 and 50")
    return limit
```

### 3. Logging

```python
logger.info(f"Executing tool with args: {arguments}")
logger.debug(f"Fetched {len(articles)} articles")
logger.warning(f"No results for query: {query}")
```

### 4. Performance

```python
# Use indexes
await collection.create_index([("field", 1)])

# Limit fields returned
result = await collection.find({}, {"_id": 1, "title": 1}).limit(10)

# Use pagination
skip = (page - 1) * page_size
results = await collection.find().skip(skip).limit(page_size)
```

### 5. Testing

Write tests for each tool:

```python
@pytest.mark.asyncio
async def test_tool_success(mock_client):
    tool = YourTool(mock_client)
    result = await tool.execute({"arg": "value"})
    assert len(result) > 0

@pytest.mark.asyncio
async def test_tool_error_handling(mock_client):
    mock_client.fetch_news.side_effect = Exception("Test error")
    tool = YourTool(mock_client)
    result = await tool.execute({})
    assert "error" in result[0].text.lower()
```

## Tool Ideas

Here are more tool ideas you can implement:

1. **Get News by Source** - Filter by specific news sources
2. **Get Author Profile** - Show articles by a specific author
3. **Compare Articles** - Compare coverage of the same story from different sources
4. **News Timeline** - Show chronological timeline of a story
5. **Related Articles** - Find articles related to a given article
6. **Export News** - Export articles as PDF or email
7. **News Alerts** - Set up notifications for specific topics
8. **Sentiment Analysis** - Analyze sentiment of news articles
9. **Translation** - Translate articles to different languages
10. **Bookmark Management** - Manage saved articles

## Next Steps

1. Pick a tool from the examples or ideas
2. Implement the tool following the guide
3. Add tests
4. Update documentation
5. Deploy and test in ChatGPT

Happy coding! 🚀