# Documentation Index

Welcome to the ChatGPT MCP News Widget documentation!

## Quick Start

🚀 **New to the project?** Start here:
1. [Setup Guide](SETUP_GUIDE.md) - Complete installation and configuration
2. [Quick Start](#quick-start-guide) - Get running in 5 minutes

## Documentation

### Core Guides

- **[Setup Guide](SETUP_GUIDE.md)** - Complete setup instructions
  - Prerequisites
  - Local development setup
  - MongoDB configuration
  - OpenAI app setup
  - ChatGPT integration

- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment
  - Railway deployment (recommended)
  - Render, Fly.io, AWS EC2
  - Docker deployment
  - Security best practices

- **[Extending Guide](EXTENDING.md)** - Add new features
  - Creating custom tools
  - Widget customization
  - Tool examples
  - Best practices

### Quick Start Guide

```bash
# 1. Clone and setup
git clone https://github.com/vikkysarswat/chatgpt-mcp-news-widget.git
cd chatgpt-mcp-news-widget
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI

# 3. Seed database
python scripts/seed_mongodb.py

# 4. Test connection
python scripts/test_mcp_connection.py

# 5. Run server
python src/mcp_server.py
```

## Architecture

```
┌─────────────┐
│   ChatGPT    │
│ (User Chat) │
└─────┬──────┘
     │
     │ MCP Protocol
     │
┌────┴─────────────┐
│  MCP Server        │
│  (Python)          │
│  - fetch_news      │
│  - search_news     │
│  - [more tools]    │
└────┬─────────────┘
     │
     │ MongoDB Driver
     │
┌────┴─────────────┐
│  MongoDB Atlas     │
│  (Cloud Database)  │
│  - News Articles   │
└─────────────────┘
```

## Project Structure

```
chatgpt-mcp-news-widget/
├── src/                    # Source code
│   ├── mcp_server.py       # Main MCP server
│   ├── mongodb_client.py   # MongoDB operations
│   ├── config/             # Configuration
│   │   └── settings.py
│   └── tools/              # MCP tools
│       └── fetch_news.py
├── tests/                  # Unit tests
├── scripts/                # Utility scripts
│   ├── seed_mongodb.py
│   └── test_mcp_connection.py
├── openai_app/            # OpenAI app config
│   ├── app_manifest.json
│   └── widget_config.json
├── docs/                   # Documentation
│   ├── SETUP_GUIDE.md
│   ├── DEPLOYMENT.md
│   └── EXTENDING.md
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
└── README.md               # Project overview
```

## Key Features

### 📰 News Fetching
- Fetch latest news from MongoDB
- Filter by category, tags, date range
- Full-text search
- Customizable sorting

### 🎨 Rich Widgets
- Display news as interactive cards
- Grid and list layouts
- Images, metadata, and links
- Responsive design

### 🔧 Extensible
- Easy to add new tools
- Modular architecture
- Comprehensive documentation
- Test suite included

## API Reference

### fetch_news Tool

**Parameters:**
- `limit` (int, optional): Max articles (1-50, default: 10)
- `category` (string, optional): Filter by category
- `tags` (array, optional): Filter by tags
- `search_query` (string, optional): Search in title/content
- `hours_ago` (int, optional): Articles from last N hours
- `sort_by` (string, optional): Sort field (default: published_at)
- `sort_order` (string, optional): Sort order (asc/desc)

**Example:**
```json
{
  "limit": 5,
  "category": "technology",
  "hours_ago": 24
}
```

**Response:**
Formatted text with embedded JSON widget data.

## MongoDB Schema

### Articles Collection

```javascript
{
  _id: ObjectId,
  title: String,          // Required
  description: String,
  content: String,
  author: String,
  source: String,         // Required
  url: String,            // Required
  image_url: String,
  published_at: ISODate,  // Required
  category: String,       // Required
  tags: [String]
}
```

### Recommended Indexes

```javascript
// Performance optimization
db.articles.createIndex({ "published_at": -1 })
db.articles.createIndex({ "category": 1 })
db.articles.createIndex({ "tags": 1 })
db.articles.createIndex({ "title": "text", "content": "text" })
```

## Common Tasks

### Add Sample Data
```bash
python scripts/seed_mongodb.py
```

### Test Connection
```bash
python scripts/test_mcp_connection.py
```

### Run Tests
```bash
pytest tests/
```

### Deploy to Railway
```bash
# See DEPLOYMENT.md for complete guide
1. Connect GitHub repo to Railway
2. Set environment variables
3. Deploy automatically
```

### Add New Tool
See [EXTENDING.md](EXTENDING.md) for step-by-step guide.

## Troubleshooting

### Common Issues

**MongoDB Connection Failed**
- Verify URI in `.env`
- Check IP whitelist in Atlas
- Test with: `mongosh "YOUR_URI"`

**Server Won't Start**
- Check Python version (3.10+)
- Verify all dependencies installed
- Check logs for specific errors

**ChatGPT Can't Connect**
- Ensure server is running
- Verify URL in app manifest
- Check ngrok (for local dev)

**No News Displayed**
- Run seed script
- Verify collection has data
- Check MongoDB connection

For more troubleshooting, see [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting).

## Resources

### Official Documentation
- [OpenAI Platform](https://platform.openai.com/docs)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MongoDB Docs](https://docs.mongodb.com/)
- [Motor (Async MongoDB)](https://motor.readthedocs.io/)

### Related Projects
- [OpenAI Apps Examples](https://github.com/openai/openai-apps-examples)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

### Community
- [GitHub Issues](https://github.com/vikkysarswat/chatgpt-mcp-news-widget/issues)
- [GitHub Discussions](https://github.com/vikkysarswat/chatgpt-mcp-news-widget/discussions)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Support

Need help? 
- 🐛 [Report a Bug](https://github.com/vikkysarswat/chatgpt-mcp-news-widget/issues/new?labels=bug)
- 💡 [Request a Feature](https://github.com/vikkysarswat/chatgpt-mcp-news-widget/issues/new?labels=enhancement)
- 💬 [Ask a Question](https://github.com/vikkysarswat/chatgpt-mcp-news-widget/discussions)

---

**Happy coding!** 🚀

Made with ❤️ by [Nilesh Vikky](https://github.com/vikkysarswat)