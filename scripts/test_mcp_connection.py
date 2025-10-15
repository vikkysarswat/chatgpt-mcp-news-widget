"""Script to test MCP server connection and fetch_news tool."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mongodb_client import MongoDBClient
from tools.fetch_news import FetchNewsTool
from config.settings import Settings


async def test_connection():
    """Test MongoDB connection and news fetching."""
    print("Testing MCP Server Components")
    print("=" * 50)
    
    # Load settings
    settings = Settings()
    print(f"\n1. Loading settings...")
    print(f"   Database: {settings.mongodb_database}")
    print(f"   Collection: {settings.mongodb_collection}")
    
    # Connect to MongoDB
    print(f"\n2. Connecting to MongoDB...")
    mongodb_client = MongoDBClient(
        uri=settings.mongodb_uri,
        database=settings.mongodb_database,
        collection=settings.mongodb_collection
    )
    
    try:
        await mongodb_client.connect()
        print("   ✓ Connected successfully!")
        
        # Test article count
        print(f"\n3. Checking article count...")
        count = await mongodb_client.count_articles()
        print(f"   Found {count} articles in collection")
        
        if count == 0:
            print("   ⚠ Warning: No articles found. Run 'python scripts/seed_mongodb.py' first.")
            return
        
        # Test fetch_news tool
        print(f"\n4. Testing fetch_news tool...")
        fetch_news_tool = FetchNewsTool(mongodb_client)
        
        # Test 1: Fetch latest 5 articles
        print("\n   Test 1: Fetch latest 5 articles")
        result = await fetch_news_tool.execute({"limit": 5})
        print(f"   ✓ Returned {len(result)} content items")
        if result:
            # Parse and display summary
            text = result[0].text
            if "Found" in text:
                first_line = text.split('\n')[0]
                print(f"   {first_line}")
        
        # Test 2: Fetch by category
        print("\n   Test 2: Fetch technology articles")
        result = await fetch_news_tool.execute({
            "category": "technology",
            "limit": 3
        })
        if result:
            text = result[0].text
            if "Found" in text:
                first_line = text.split('\n')[0]
                print(f"   {first_line}")
        
        # Test 3: Fetch with tags
        print("\n   Test 3: Fetch articles tagged with 'ai'")
        result = await fetch_news_tool.execute({
            "tags": ["ai"],
            "limit": 2
        })
        if result:
            text = result[0].text
            if "Found" in text:
                first_line = text.split('\n')[0]
                print(f"   {first_line}")
        
        # Test 4: Recent articles
        print("\n   Test 4: Fetch articles from last 24 hours")
        result = await fetch_news_tool.execute({
            "hours_ago": 24,
            "limit": 5
        })
        if result:
            text = result[0].text
            if "Found" in text:
                first_line = text.split('\n')[0]
                print(f"   {first_line}")
        
        # Display available categories and tags
        print(f"\n5. Available data...")
        categories = await mongodb_client.get_categories()
        print(f"   Categories: {', '.join(categories)}")
        
        tags = await mongodb_client.get_tags()
        print(f"   Tags: {', '.join(tags[:10])}{'...' if len(tags) > 10 else ''}")
        
        print("\n" + "=" * 50)
        print("✓ All tests passed successfully!")
        print("\nMCP server is ready to connect to ChatGPT.")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await mongodb_client.close()
        print("\nConnection closed.")


if __name__ == "__main__":
    asyncio.run(test_connection())