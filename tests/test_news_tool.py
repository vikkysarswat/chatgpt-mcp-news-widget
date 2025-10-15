"""Tests for the fetch news tool."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from src.tools.fetch_news import FetchNewsTool
from src.mongodb_client import MongoDBClient


@pytest.fixture
def mock_mongodb_client():
    """Create a mock MongoDB client."""
    client = MagicMock(spec=MongoDBClient)
    client.fetch_news = AsyncMock()
    return client


@pytest.fixture
def fetch_news_tool(mock_mongodb_client):
    """Create a FetchNewsTool instance with mock client."""
    return FetchNewsTool(mock_mongodb_client)


@pytest.fixture
def sample_articles():
    """Sample news articles for testing."""
    return [
        {
            "_id": "article1",
            "title": "AI Breakthrough in 2025",
            "description": "New AI model surpasses human performance",
            "content": "Full content here...",
            "author": "John Doe",
            "source": "Tech News",
            "url": "https://example.com/article1",
            "image_url": "https://example.com/image1.jpg",
            "published_at": "2025-10-15T10:00:00",
            "category": "technology",
            "tags": ["ai", "machine-learning"]
        },
        {
            "_id": "article2",
            "title": "Climate Change Update",
            "description": "Latest climate report released",
            "content": "Climate scientists announce...",
            "author": "Jane Smith",
            "source": "Science Daily",
            "url": "https://example.com/article2",
            "image_url": "https://example.com/image2.jpg",
            "published_at": "2025-10-14T15:30:00",
            "category": "science",
            "tags": ["climate", "environment"]
        }
    ]


@pytest.mark.asyncio
async def test_execute_default_parameters(fetch_news_tool, mock_mongodb_client, sample_articles):
    """Test execute with default parameters."""
    mock_mongodb_client.fetch_news.return_value = sample_articles
    
    result = await fetch_news_tool.execute({})
    
    assert len(result) == 1
    assert result[0].type == "text"
    assert "AI Breakthrough" in result[0].text
    assert "Climate Change" in result[0].text
    
    mock_mongodb_client.fetch_news.assert_called_once_with(
        limit=10,
        category=None,
        tags=None,
        search_query=None,
        hours_ago=None,
        sort_by="published_at",
        sort_order="desc"
    )


@pytest.mark.asyncio
async def test_execute_with_filters(fetch_news_tool, mock_mongodb_client, sample_articles):
    """Test execute with filter parameters."""
    mock_mongodb_client.fetch_news.return_value = [sample_articles[0]]
    
    arguments = {
        "limit": 5,
        "category": "technology",
        "tags": ["ai"],
        "hours_ago": 24
    }
    
    result = await fetch_news_tool.execute(arguments)
    
    assert len(result) == 1
    assert "AI Breakthrough" in result[0].text
    
    mock_mongodb_client.fetch_news.assert_called_once_with(
        limit=5,
        category="technology",
        tags=["ai"],
        search_query=None,
        hours_ago=24,
        sort_by="published_at",
        sort_order="desc"
    )


@pytest.mark.asyncio
async def test_execute_no_results(fetch_news_tool, mock_mongodb_client):
    """Test execute when no articles are found."""
    mock_mongodb_client.fetch_news.return_value = []
    
    result = await fetch_news_tool.execute({})
    
    assert len(result) == 1
    assert "No news articles found" in result[0].text


@pytest.mark.asyncio
async def test_execute_error_handling(fetch_news_tool, mock_mongodb_client):
    """Test execute handles errors gracefully."""
    mock_mongodb_client.fetch_news.side_effect = Exception("Database connection failed")
    
    result = await fetch_news_tool.execute({})
    
    assert len(result) == 1
    assert "Error fetching news" in result[0].text
    assert "Database connection failed" in result[0].text


def test_format_articles_for_widget(fetch_news_tool, sample_articles):
    """Test article formatting for widget display."""
    result = fetch_news_tool._format_articles_for_widget(sample_articles)
    
    assert len(result) == 1
    text = result[0].text
    
    # Check human-readable format
    assert "Found 2 news article(s)" in text
    assert "AI Breakthrough" in text
    assert "Climate Change" in text
    
    # Check JSON widget data is included
    assert "```json" in text
    assert '"type": "news_feed"' in text
    assert '"count": 2' in text


def test_create_readable_output(fetch_news_tool, sample_articles):
    """Test creation of human-readable output."""
    output = fetch_news_tool._create_readable_output(sample_articles)
    
    assert "Found 2 news article(s)" in output
    assert "**1. AI Breakthrough in 2025**" in output
    assert "**2. Climate Change Update**" in output
    assert "📰 Source: Tech News" in output
    assert "📰 Source: Science Daily" in output
    assert "✍️  Author: John Doe" in output
    assert "🏷️  Category: technology" in output
    assert "🔖 Tags: ai, machine-learning" in output