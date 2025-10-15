"""MongoDB client for news article operations."""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure

logger = logging.getLogger(__name__)


class MongoDBClient:
    """MongoDB client for news operations."""

    def __init__(self, uri: str, database: str, collection: str):
        """Initialize MongoDB client.
        
        Args:
            uri: MongoDB connection URI
            database: Database name
            collection: Collection name
        """
        self.uri = uri
        self.database_name = database
        self.collection_name = collection
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self.collection: Optional[AsyncIOMotorCollection] = None

    async def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(self.uri)
            # Verify connection
            await self.client.admin.command('ping')
            
            self.database = self.client[self.database_name]
            self.collection = self.database[self.collection_name]
            
            logger.info(f"Connected to MongoDB: {self.database_name}.{self.collection_name}")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    async def fetch_news(
        self,
        limit: int = 10,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        search_query: Optional[str] = None,
        hours_ago: Optional[int] = None,
        sort_by: str = "published_at",
        sort_order: str = "desc"
    ) -> List[Dict[str, Any]]:
        """Fetch news articles from MongoDB.
        
        Args:
            limit: Maximum number of articles to fetch
            category: Filter by category
            tags: Filter by tags (articles must have at least one of these tags)
            search_query: Search in title and content
            hours_ago: Fetch articles from the last N hours
            sort_by: Field to sort by
            sort_order: Sort order ('asc' or 'desc')
            
        Returns:
            List of news articles
        """
        if not self.collection:
            raise RuntimeError("MongoDB client not connected")

        # Build query filter
        query_filter: Dict[str, Any] = {}

        if category:
            query_filter["category"] = category

        if tags:
            query_filter["tags"] = {"$in": tags}

        if hours_ago:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours_ago)
            query_filter["published_at"] = {"$gte": cutoff_time}

        if search_query:
            # Text search (requires text index on title and content fields)
            query_filter["$text"] = {"$search": search_query}

        # Determine sort direction
        sort_direction = DESCENDING if sort_order == "desc" else ASCENDING

        try:
            # Execute query
            cursor = self.collection.find(query_filter).sort(
                sort_by, sort_direction
            ).limit(limit)

            # Convert cursor to list
            articles = await cursor.to_list(length=limit)

            # Convert ObjectId to string for JSON serialization
            for article in articles:
                if "_id" in article:
                    article["_id"] = str(article["_id"])
                # Convert datetime to ISO format string
                if "published_at" in article and isinstance(article["published_at"], datetime):
                    article["published_at"] = article["published_at"].isoformat()

            logger.info(f"Fetched {len(articles)} articles")
            return articles

        except OperationFailure as e:
            logger.error(f"MongoDB operation failed: {e}")
            raise

    async def get_categories(self) -> List[str]:
        """Get all distinct categories.
        
        Returns:
            List of category names
        """
        if not self.collection:
            raise RuntimeError("MongoDB client not connected")

        categories = await self.collection.distinct("category")
        return categories

    async def get_tags(self) -> List[str]:
        """Get all distinct tags.
        
        Returns:
            List of tag names
        """
        if not self.collection:
            raise RuntimeError("MongoDB client not connected")

        tags = await self.collection.distinct("tags")
        return tags

    async def count_articles(self, query_filter: Optional[Dict[str, Any]] = None) -> int:
        """Count articles matching the filter.
        
        Args:
            query_filter: MongoDB query filter
            
        Returns:
            Number of matching articles
        """
        if not self.collection:
            raise RuntimeError("MongoDB client not connected")

        count = await self.collection.count_documents(query_filter or {})
        return count