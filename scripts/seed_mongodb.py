"""Script to seed MongoDB with sample news articles."""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import Settings


# Sample news data
SAMPLE_NEWS = [
    {
        "title": "AI Reaches New Milestone in Natural Language Understanding",
        "description": "Researchers announce breakthrough in AI's ability to understand context and nuance in human language.",
        "content": "In a significant development for artificial intelligence, researchers have announced a breakthrough in natural language understanding. The new model demonstrates unprecedented ability to grasp context, detect nuance, and generate human-like responses across multiple languages.",
        "author": "Dr. Sarah Chen",
        "source": "AI Research Today",
        "url": "https://example.com/ai-milestone-2025",
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",
        "published_at": datetime.utcnow() - timedelta(hours=2),
        "category": "technology",
        "tags": ["ai", "machine-learning", "nlp", "research"]
    },
    {
        "title": "Global Climate Summit Announces Historic Agreement",
        "description": "World leaders commit to ambitious carbon reduction targets at landmark climate conference.",
        "content": "In a historic move, leaders from over 150 countries have signed a comprehensive agreement to reduce global carbon emissions by 50% by 2035. The summit, held in Geneva, marks a turning point in international climate cooperation.",
        "author": "Michael Rodriguez",
        "source": "Environmental News Network",
        "url": "https://example.com/climate-summit-2025",
        "image_url": "https://images.unsplash.com/photo-1569163139394-de4798aa62b5?w=800",
        "published_at": datetime.utcnow() - timedelta(hours=5),
        "category": "environment",
        "tags": ["climate", "environment", "politics", "sustainability"]
    },
    {
        "title": "Tech Giants Announce Collaboration on Quantum Computing",
        "description": "Major technology companies join forces to accelerate quantum computing development.",
        "content": "Leading technology companies have announced an unprecedented collaboration to advance quantum computing research. The partnership aims to make quantum computing more accessible and practical for real-world applications within the next five years.",
        "author": "Lisa Wang",
        "source": "Tech Innovation Weekly",
        "url": "https://example.com/quantum-collaboration",
        "image_url": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800",
        "published_at": datetime.utcnow() - timedelta(hours=8),
        "category": "technology",
        "tags": ["quantum-computing", "technology", "innovation", "collaboration"]
    },
    {
        "title": "New Study Reveals Benefits of Mediterranean Diet",
        "description": "Long-term research shows significant health improvements from Mediterranean-style eating.",
        "content": "A comprehensive 10-year study published in the Journal of Nutrition demonstrates that adherence to a Mediterranean diet leads to substantial improvements in cardiovascular health, longevity, and overall well-being.",
        "author": "Dr. Amanda Foster",
        "source": "Health & Wellness Journal",
        "url": "https://example.com/mediterranean-diet-study",
        "image_url": "https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=800",
        "published_at": datetime.utcnow() - timedelta(hours=12),
        "category": "health",
        "tags": ["health", "nutrition", "diet", "research"]
    },
    {
        "title": "SpaceX Successfully Launches Mars Mission",
        "description": "Latest spacecraft begins journey to the Red Planet with advanced scientific instruments.",
        "content": "SpaceX has successfully launched its most ambitious Mars mission to date. The spacecraft carries cutting-edge scientific instruments designed to search for signs of past microbial life and collect samples for eventual return to Earth.",
        "author": "James Mitchell",
        "source": "Space Exploration News",
        "url": "https://example.com/spacex-mars-mission",
        "image_url": "https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?w=800",
        "published_at": datetime.utcnow() - timedelta(hours=18),
        "category": "science",
        "tags": ["space", "mars", "spacex", "exploration"]
    },
    {
        "title": "Renewable Energy Surpasses Fossil Fuels in EU",
        "description": "Historic milestone as clean energy becomes dominant power source across Europe.",
        "content": "For the first time in history, renewable energy sources have generated more electricity than fossil fuels across the European Union. Solar and wind power led the transition, marking a significant step toward carbon neutrality.",
        "author": "Emma Larsson",
        "source": "Green Energy Today",
        "url": "https://example.com/eu-renewable-energy",
        "image_url": "https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=800",
        "published_at": datetime.utcnow() - timedelta(days=1),
        "category": "energy",
        "tags": ["renewable-energy", "solar", "wind", "sustainability", "europe"]
    },
    {
        "title": "Breakthrough in Cancer Treatment Shows Promise",
        "description": "New immunotherapy approach demonstrates remarkable success in clinical trials.",
        "content": "Medical researchers have announced promising results from clinical trials of a novel cancer immunotherapy. The treatment has shown an 80% success rate in certain types of cancer, offering new hope to patients worldwide.",
        "author": "Dr. Robert Kim",
        "source": "Medical Advances Journal",
        "url": "https://example.com/cancer-breakthrough",
        "image_url": "https://images.unsplash.com/photo-1579154204601-01588f351e67?w=800",
        "published_at": datetime.utcnow() - timedelta(days=1, hours=6),
        "category": "health",
        "tags": ["health", "cancer", "research", "medical", "breakthrough"]
    },
    {
        "title": "Stock Markets Reach All-Time High",
        "description": "Global markets surge as economic indicators show strong growth.",
        "content": "Major stock indices around the world have reached record highs, driven by positive economic data and strong corporate earnings. Analysts attribute the rally to improved consumer confidence and technological innovation.",
        "author": "David Thompson",
        "source": "Financial Times",
        "url": "https://example.com/markets-all-time-high",
        "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "published_at": datetime.utcnow() - timedelta(days=2),
        "category": "business",
        "tags": ["finance", "stocks", "economy", "markets"]
    },
    {
        "title": "Olympic Games 2028: New Sports Added to Lineup",
        "description": "IOC announces inclusion of esports and other modern competitions.",
        "content": "The International Olympic Committee has officially added several new sports to the 2028 Olympic Games, including esports, breaking (breakdancing), and skateboarding. The decision reflects the Olympics' effort to appeal to younger audiences.",
        "author": "Sophie Martin",
        "source": "Sports International",
        "url": "https://example.com/olympics-new-sports",
        "image_url": "https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=800",
        "published_at": datetime.utcnow() - timedelta(days=2, hours=12),
        "category": "sports",
        "tags": ["sports", "olympics", "esports", "competition"]
    },
    {
        "title": "Scientists Discover New Deep-Sea Species",
        "description": "Expedition uncovers fascinating new life forms in unexplored ocean depths.",
        "content": "A deep-sea exploration mission has discovered dozens of previously unknown species living at extreme depths. The findings highlight how much of Earth's oceans remain unexplored and the importance of marine conservation.",
        "author": "Dr. Maria Santos",
        "source": "Ocean Discovery Magazine",
        "url": "https://example.com/deep-sea-species",
        "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
        "published_at": datetime.utcnow() - timedelta(days=3),
        "category": "science",
        "tags": ["science", "ocean", "discovery", "marine-biology"]
    }
]


async def seed_database():
    """Seed MongoDB with sample news articles."""
    # Load settings
    settings = Settings()
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.mongodb_uri)
    database = client[settings.mongodb_database]
    collection = database[settings.mongodb_collection]
    
    try:
        # Check if collection already has data
        count = await collection.count_documents({})
        
        if count > 0:
            response = input(f"Collection already has {count} documents. Clear and reseed? (y/n): ")
            if response.lower() == 'y':
                await collection.delete_many({})
                print(f"Cleared {count} existing documents.")
            else:
                print("Seeding cancelled.")
                return
        
        # Insert sample data
        result = await collection.insert_many(SAMPLE_NEWS)
        print(f"Successfully inserted {len(result.inserted_ids)} news articles!")
        
        # Create indexes for better performance
        await collection.create_index([("published_at", -1)])
        await collection.create_index([("category", 1)])
        await collection.create_index([("tags", 1)])
        await collection.create_index([("title", "text"), ("content", "text")])
        print("Created indexes for optimized queries.")
        
        # Display sample
        print("\nSample articles:")
        async for article in collection.find().limit(3):
            print(f"  - {article['title']} ({article['category']})")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    print("MongoDB News Database Seeder")
    print("=" * 50)
    asyncio.run(seed_database())