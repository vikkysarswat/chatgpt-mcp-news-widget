# Utility Scripts

This directory contains utility scripts for managing the news MCP server.

## Available Scripts

### seed_mongodb.py

Seeds MongoDB with sample news articles for testing.

**Usage:**
```bash
python scripts/seed_mongodb.py
```

**What it does:**
- Creates 10 sample news articles across different categories
- Sets up MongoDB indexes for optimized queries
- Provides option to clear existing data before seeding

**Categories included:**
- Technology
- Science
- Health
- Business
- Sports
- Environment
- Energy

### test_mcp_connection.py

Tests the MCP server components and MongoDB connection.

**Usage:**
```bash
python scripts/test_mcp_connection.py
```

**Tests performed:**
1. MongoDB connection
2. Article count verification
3. Fetch latest articles
4. Filter by category
5. Filter by tags
6. Time-based filtering
7. List available categories and tags

## Setup Before Running Scripts

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your MongoDB connection string
```

3. Run seed script:
```bash
python scripts/seed_mongodb.py
```

4. Test connection:
```bash
python scripts/test_mcp_connection.py
```

## Adding More Sample Data

To add more sample articles, edit `seed_mongodb.py` and add entries to the `SAMPLE_NEWS` list:

```python
SAMPLE_NEWS.append({
    "title": "Your Article Title",
    "description": "Brief description",
    "content": "Full content...",
    "author": "Author Name",
    "source": "News Source",
    "url": "https://example.com/article",
    "image_url": "https://example.com/image.jpg",
    "published_at": datetime.utcnow(),
    "category": "category_name",
    "tags": ["tag1", "tag2"]
})
```

## Troubleshooting

### "No module named 'src'"

Make sure you're running the scripts from the project root directory:
```bash
cd /path/to/chatgpt-mcp-news-widget
python scripts/seed_mongodb.py
```

### "Failed to connect to MongoDB"

Check your `.env` file and verify:
- MongoDB URI is correct
- Database credentials are valid
- Network allows connection to MongoDB
- MongoDB server is running

### "No articles found"

Run the seed script first:
```bash
python scripts/seed_mongodb.py
```