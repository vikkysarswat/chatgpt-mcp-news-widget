# ChatGPT MCP News Widget

An OpenAI app that uses Model Context Protocol (MCP) to fetch news from MongoDB and display it in ChatGPT through interactive widgets.

## Features

- 🔌 MCP server implementation in Python
- 📰 Fetch news from MongoDB collection
- 🎨 Display news in ChatGPT with rich widgets (similar to pizza example)
- 🔧 Extensible architecture for adding more tools

## Prerequisites

- Python 3.10+
- MongoDB Atlas account or local MongoDB instance
- OpenAI Platform account
- ChatGPT Plus subscription (for app connector)

## Project Structure

```
.
├── src/
│   ├── mcp_server.py          # Main MCP server implementation
│   ├── mongodb_client.py      # MongoDB connection and queries
│   └── tools/
│       └── fetch_news.py      # News fetching tool
├── openai_app/
│   ├── app_manifest.json      # OpenAI app manifest
│   └── actions.json           # Action definitions for widgets
├── config/
│   └── config.yaml            # Configuration file
├── tests/
│   └── test_news_tool.py      # Unit tests
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/vikkysarswat/chatgpt-mcp-news-widget.git
cd chatgpt-mcp-news-widget
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your MongoDB connection string:

```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=news_db
MONGODB_COLLECTION=articles
MCP_SERVER_PORT=3000
```

### 4. Set up MongoDB

Create a MongoDB collection with news articles. Example document structure:

```json
{
  "_id": "...",
  "title": "Breaking News Title",
  "description": "News article description",
  "content": "Full article content",
  "author": "John Doe",
  "source": "News Source",
  "url": "https://example.com/article",
  "image_url": "https://example.com/image.jpg",
  "published_at": "2025-10-15T10:00:00Z",
  "category": "technology",
  "tags": ["ai", "tech", "innovation"]
}
```

### 5. Run the MCP server

```bash
python src/mcp_server.py
```

### 6. Configure OpenAI App

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to "Apps" section
3. Create a new app
4. Upload the `openai_app/app_manifest.json`
5. Configure the MCP server endpoint
6. Add the app to ChatGPT

## Usage

Once configured, you can use the following commands in ChatGPT:

- "Fetch the latest news"
- "Show me technology news"
- "Get news from the last 24 hours"
- "Find news about AI"

The news will be displayed as interactive widgets with:
- Title and description
- Author and source
- Publication date
- Image thumbnail
- Link to full article

## MongoDB Schema

Recommended indexes for better performance:

```javascript
db.articles.createIndex({ "published_at": -1 })
db.articles.createIndex({ "category": 1 })
db.articles.createIndex({ "tags": 1 })
db.articles.createIndex({ "title": "text", "content": "text" })
```

## Adding More Tools

To add new tools:

1. Create a new file in `src/tools/`
2. Implement the tool following the MCP protocol
3. Register it in `src/mcp_server.py`
4. Update `openai_app/actions.json` with the new action definition

## Testing

```bash
python -m pytest tests/
```

## References

- [OpenAI Platform Documentation](https://platform.openai.com/docs)
- [Model Context Protocol (MCP) Spec](https://spec.modelcontextprotocol.io/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [OpenAI Apps Examples](https://github.com/openai/openai-apps-examples)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.