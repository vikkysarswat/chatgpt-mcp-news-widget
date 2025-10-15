"""Fetch news tool implementation."""

import json
import logging
from typing import Any, Dict, List

from mcp.types import TextContent, ImageContent, EmbeddedResource

from mongodb_client import MongoDBClient

logger = logging.getLogger(__name__)


class FetchNewsTool:
    """Tool for fetching news articles from MongoDB."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize the fetch news tool.
        
        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client

    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent | ImageContent | EmbeddedResource]:
        """Execute the fetch news tool.
        
        Args:
            arguments: Tool arguments containing filters and options
            
        Returns:
            List of content items formatted for ChatGPT widget display
        """
        try:
            # Extract arguments with defaults
            limit = arguments.get("limit", 10)
            category = arguments.get("category")
            tags = arguments.get("tags")
            search_query = arguments.get("search_query")
            hours_ago = arguments.get("hours_ago")
            sort_by = arguments.get("sort_by", "published_at")
            sort_order = arguments.get("sort_order", "desc")

            logger.info(f"Fetching news with arguments: {arguments}")

            # Fetch articles from MongoDB
            articles = await self.mongodb_client.fetch_news(
                limit=limit,
                category=category,
                tags=tags,
                search_query=search_query,
                hours_ago=hours_ago,
                sort_by=sort_by,
                sort_order=sort_order
            )

            if not articles:
                return [
                    TextContent(
                        type="text",
                        text="No news articles found matching your criteria."
                    )
                ]

            # Format articles for widget display
            return self._format_articles_for_widget(articles)

        except Exception as e:
            logger.error(f"Error fetching news: {e}", exc_info=True)
            return [
                TextContent(
                    type="text",
                    text=f"Error fetching news: {str(e)}"
                )
            ]

    def _format_articles_for_widget(self, articles: List[Dict[str, Any]]) -> List[TextContent]:
        """Format articles for ChatGPT widget display.
        
        This formats the articles in a structured way that ChatGPT can render
        as interactive widgets, similar to the pizza example.
        
        Args:
            articles: List of news articles from MongoDB
            
        Returns:
            List of TextContent with structured widget data
        """
        # Create a structured response that ChatGPT can render as widgets
        widget_data = {
            "type": "news_feed",
            "count": len(articles),
            "articles": []
        }

        for article in articles:
            widget_article = {
                "id": article.get("_id"),
                "title": article.get("title", "Untitled"),
                "description": article.get("description", ""),
                "content": article.get("content", "")[:500] + "..." if article.get("content") else "",
                "author": article.get("author", "Unknown"),
                "source": article.get("source", "Unknown Source"),
                "url": article.get("url", ""),
                "image_url": article.get("image_url", ""),
                "published_at": article.get("published_at", ""),
                "category": article.get("category", "general"),
                "tags": article.get("tags", [])
            }
            widget_data["articles"].append(widget_article)

        # Return formatted content
        # The text includes both human-readable format and JSON for widget rendering
        text_content = self._create_readable_output(articles)
        json_content = json.dumps(widget_data, indent=2)

        return [
            TextContent(
                type="text",
                text=f"{text_content}\n\n<!-- Widget Data -->\n```json\n{json_content}\n```"
            )
        ]

    def _create_readable_output(self, articles: List[Dict[str, Any]]) -> str:
        """Create human-readable text output.
        
        Args:
            articles: List of news articles
            
        Returns:
            Formatted text output
        """
        output = f"Found {len(articles)} news article(s):\n\n"

        for i, article in enumerate(articles, 1):
            output += f"**{i}. {article.get('title', 'Untitled')}**\n"
            output += f"   📰 Source: {article.get('source', 'Unknown')}\n"
            
            if article.get('author'):
                output += f"   ✍️  Author: {article.get('author')}\n"
            
            if article.get('published_at'):
                output += f"   📅 Published: {article.get('published_at')}\n"
            
            if article.get('category'):
                output += f"   🏷️  Category: {article.get('category')}\n"
            
            if article.get('tags'):
                tags = ", ".join(article.get('tags', [])[:5])
                output += f"   🔖 Tags: {tags}\n"
            
            if article.get('description'):
                desc = article.get('description', '')[:200]
                output += f"   📝 {desc}...\n"
            
            if article.get('url'):
                output += f"   🔗 [Read more]({article.get('url')})\n"
            
            output += "\n"

        return output