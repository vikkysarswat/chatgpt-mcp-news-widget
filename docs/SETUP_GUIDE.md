# Complete Setup Guide

This guide will walk you through setting up the News MCP Server and connecting it to ChatGPT.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [MongoDB Configuration](#mongodb-configuration)
4. [Running the MCP Server](#running-the-mcp-server)
5. [OpenAI App Configuration](#openai-app-configuration)
6. [ChatGPT Integration](#chatgpt-integration)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required

- Python 3.10 or higher
- MongoDB Atlas account (free tier works) or local MongoDB
- Git
- OpenAI Platform account
- ChatGPT Plus subscription (for using custom apps)

### Recommended

- Virtual environment tool (venv, conda, or poetry)
- Code editor (VS Code, PyCharm, etc.)
- Postman or curl for API testing

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vikkysarswat/chatgpt-mcp-news-widget.git
cd chatgpt-mcp-news-widget
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## MongoDB Configuration

### Option 1: MongoDB Atlas (Cloud - Recommended)

1. **Create Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Sign up for a free account

2. **Create Cluster**
   - Click "Build a Database"
   - Choose "Free" tier (M0)
   - Select your preferred region
   - Name your cluster

3. **Configure Network Access**
   - Go to "Network Access"
   - Click "Add IP Address"
   - Choose "Allow Access from Anywhere" (0.0.0.0/0) for development
   - For production, specify your server IP

4. **Create Database User**
   - Go to "Database Access"
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Set username and password
   - Grant "Read and write to any database" privileges

5. **Get Connection String**
   - Go to "Databases"
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your actual password

### Option 2: Local MongoDB

1. **Install MongoDB**
   ```bash
   # Mac
   brew install mongodb-community

   # Ubuntu
   sudo apt-get install mongodb

   # Windows: Download from mongodb.com
   ```

2. **Start MongoDB**
   ```bash
   # Mac/Linux
   mongod --dbpath /path/to/data

   # Windows
   "C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath="C:\data\db"
   ```

3. **Connection String**
   ```
   mongodb://localhost:27017/
   ```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
# For MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority

# For Local MongoDB
# MONGODB_URI=mongodb://localhost:27017/

MONGODB_DATABASE=news_db
MONGODB_COLLECTION=articles
MCP_SERVER_PORT=3000
LOG_LEVEL=INFO
```

### 5. Seed Database with Sample Data

```bash
python scripts/seed_mongodb.py
```

This will create 10 sample news articles across various categories.

## Running the MCP Server

### 1. Test Connection First

```bash
python scripts/test_mcp_connection.py
```

You should see:
```
✓ All tests passed successfully!
MCP server is ready to connect to ChatGPT.
```

### 2. Start the Server

```bash
python src/mcp_server.py
```

The server will start and display:
```
INFO - Starting News MCP Server...
INFO - Connected to MongoDB: news_db
```

### 3. Keep Server Running

Leave this terminal window open. The MCP server needs to be running for ChatGPT to connect to it.

## OpenAI App Configuration

### 1. Access OpenAI Platform

- Go to [OpenAI Platform](https://platform.openai.com/)
- Sign in with your OpenAI account

### 2. Create New App

1. Navigate to **Apps** section (may be under "Beta" or "Tools")
2. Click **"Create App"** or **"New App"**
3. Fill in details:
   - **Name**: News Widget
   - **Description**: Fetch and display news with interactive widgets

### 3. Configure App Manifest

1. In the app configuration, find **"Manifest"** or **"Configuration"** section
2. Upload or paste the content from `openai_app/app_manifest.json`
3. Update the `url` field:
   ```json
   {
     "api": {
       "type": "mcp",
       "url": "http://YOUR_SERVER_URL:3000"
     }
   }
   ```

### 4. For Local Development

Since ChatGPT can't reach `localhost`, you need to expose your server:

#### Option A: ngrok (Recommended for testing)

```bash
# Install ngrok from ngrok.com
ngrok http 3000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`) and use it in your manifest.

#### Option B: Deploy to Cloud (For production)

See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions.

### 5. Save and Publish

1. Save the app configuration
2. Click **"Publish"** or **"Make Available"**
3. The app should now appear in your available apps list

## ChatGPT Integration

### 1. Access ChatGPT

- Go to [ChatGPT](https://chat.openai.com/)
- Ensure you're logged in with ChatGPT Plus

### 2. Enable the App

1. Click on your profile (bottom left)
2. Go to **Settings** → **Apps** or **Beta Features**
3. Find **"News Widget"** in the list
4. Toggle it **ON** or click **"Connect"**
5. Authorize the app if prompted

### 3. Test the Integration

Start a new chat and try these commands:

```
Fetch the latest news
```

```
Show me technology news from the last 24 hours
```

```
Get news about AI and machine learning
```

```
Find business news
```

You should see news articles displayed as interactive widgets with:
- Article images
- Titles and descriptions
- Author and source information
- Publication dates
- Category tags
- Links to full articles

## Testing

### Unit Tests

```bash
pytest tests/
```

### Manual Testing

1. **Test MongoDB Connection**
   ```bash
   python scripts/test_mcp_connection.py
   ```

2. **Test Specific Filters**
   ```python
   # Create a test file: test_manual.py
   import asyncio
   from src.mongodb_client import MongoDBClient
   from src.config.settings import Settings

   async def test():
       settings = Settings()
       client = MongoDBClient(
           uri=settings.mongodb_uri,
           database=settings.mongodb_database,
           collection=settings.mongodb_collection
       )
       await client.connect()
       
       # Test category filter
       articles = await client.fetch_news(category="technology", limit=3)
       print(f"Found {len(articles)} tech articles")
       
       await client.close()

   asyncio.run(test())
   ```

## Troubleshooting

### MCP Server Won't Start

**Problem**: Server fails to connect to MongoDB

**Solution**:
1. Verify MongoDB URI in `.env`
2. Check MongoDB is running (if local)
3. Verify network access in MongoDB Atlas
4. Test connection: `mongosh "YOUR_CONNECTION_STRING"`

### ChatGPT Can't Connect to Server

**Problem**: "Unable to reach server" error

**Solution**:
1. Ensure MCP server is running
2. Check firewall settings
3. Verify ngrok is running (for local dev)
4. Confirm URL in app manifest is correct
5. Try restarting the MCP server

### No News Displayed

**Problem**: "No news articles found"

**Solution**:
1. Run seed script: `python scripts/seed_mongodb.py`
2. Verify data exists: `python scripts/test_mcp_connection.py`
3. Check MongoDB collection has documents

### Widget Not Rendering

**Problem**: Plain text instead of widgets

**Solution**:
1. Verify `supports_widgets: true` in manifest
2. Check widget_config.json is properly formatted
3. Ensure data structure matches widget schema
4. Try different widget types

### Import Errors

**Problem**: ModuleNotFoundError

**Solution**:
1. Activate virtual environment
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Verify Python version: `python --version` (should be 3.10+)

### MongoDB Connection Timeout

**Problem**: Timeout connecting to Atlas

**Solution**:
1. Check internet connection
2. Verify IP whitelist in Atlas Network Access
3. Try connecting from different network
4. Check MongoDB Atlas status page

## Next Steps

1. **Add More Data**: Customize `scripts/seed_mongodb.py` with your own news sources
2. **Create More Tools**: See [EXTENDING.md](EXTENDING.md) for adding new MCP tools
3. **Deploy to Production**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment
4. **Customize Widgets**: Modify `openai_app/widget_config.json` for different layouts

## Getting Help

- **Issues**: Open an issue on [GitHub](https://github.com/vikkysarswat/chatgpt-mcp-news-widget/issues)
- **Discussions**: Join discussions for questions and ideas
- **Documentation**: Check the `docs/` folder for more guides

## Success Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] MongoDB configured (Atlas or local)
- [ ] `.env` file configured with connection string
- [ ] Database seeded with sample data
- [ ] MCP server starts without errors
- [ ] Test connection script passes
- [ ] OpenAI app created and configured
- [ ] Server exposed via ngrok (for local dev)
- [ ] App connected in ChatGPT
- [ ] News widgets display correctly in ChatGPT

Congratulations! Your News MCP Widget is now fully operational! 🎉