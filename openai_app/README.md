# OpenAI App Configuration

This directory contains the configuration files for integrating the MCP news server with OpenAI's ChatGPT as an app connector.

## Files

### app_manifest.json

The main app manifest file that defines:
- App metadata (name, description, logo)
- API configuration (MCP endpoint)
- Capabilities (tools and rendering options)

### widget_config.json

Widget configuration that defines:
- Widget types (news_card, news_list, news_grid)
- Widget schemas and templates
- Styling and layout options

## Setup Instructions

### 1. Deploy Your MCP Server

First, ensure your MCP server is running and accessible. For local development:

```bash
# From the project root
python src/mcp_server.py
```

For production, deploy to a cloud service (e.g., Railway, Render, AWS).

### 2. Update the Manifest

Edit `app_manifest.json` and update:

```json
{
  "api": {
    "url": "https://your-server-url.com"  // Replace with your actual URL
  },
  "contact_email": "your-email@example.com"  // Your contact email
}
```

### 3. Create an OpenAI App

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to the **Apps** section
3. Click **Create App**
4. Fill in the app details:
   - **Name**: News Widget
   - **Description**: Fetch and display news with widgets
5. Upload or paste the `app_manifest.json` content
6. Save the app

### 4. Configure App in ChatGPT

1. Open ChatGPT (requires Plus subscription)
2. Go to Settings → Apps
3. Find your "News Widget" app
4. Click **Connect**
5. Authorize the app

### 5. Test the Integration

Try these prompts in ChatGPT:

- "Show me the latest news"
- "Fetch technology news from the last 24 hours"
- "Get news about AI and machine learning"
- "Show me business news"

## Widget Rendering

The news will be displayed as rich widgets with:

- **Title**: Bold, prominent headline
- **Image**: Article thumbnail (if available)
- **Description**: Brief summary
- **Metadata**: Author, source, publication date
- **Tags**: Category and topic tags
- **Action Button**: Link to read full article

## Customization

### Adding New Widget Types

1. Add a new widget definition in `widget_config.json`:

```json
{
  "type": "news_headline",
  "name": "News Headline",
  "schema": {
    // Define schema
  },
  "template": {
    // Define template
  }
}
```

2. Update the manifest to include the new widget type:

```json
{
  "capabilities": {
    "rendering": {
      "widget_types": ["news_card", "news_list", "news_grid", "news_headline"]
    }
  }
}
```

### Styling Widgets

Modify the `style` objects in `widget_config.json` to customize:
- Colors
- Fonts
- Spacing
- Borders
- Shadows

## Troubleshooting

### App Not Appearing in ChatGPT

- Verify you have ChatGPT Plus subscription
- Check that the app is published in OpenAI Platform
- Ensure the MCP server URL is accessible from OpenAI's servers

### Widgets Not Rendering

- Verify the widget data structure matches the schema
- Check browser console for errors
- Ensure `supports_widgets: true` in manifest

### MCP Server Connection Errors

- Verify the server is running
- Check firewall/security group settings
- Ensure the URL in manifest is correct
- Test the endpoint directly using curl or Postman

## Advanced Configuration

### Authentication

To add user authentication:

1. Update manifest:
```json
{
  "api": {
    "has_user_authentication": true,
    "auth": {
      "type": "oauth2",
      "authorization_url": "https://your-auth-server.com/oauth/authorize",
      "token_url": "https://your-auth-server.com/oauth/token"
    }
  }
}
```

2. Implement OAuth2 flow in your MCP server

### Rate Limiting

Add rate limiting configuration:

```json
{
  "api": {
    "rate_limit": {
      "requests_per_minute": 60,
      "requests_per_day": 1000
    }
  }
}
```

## Resources

- [OpenAI Apps Documentation](https://platform.openai.com/docs/apps)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Widget Examples](https://github.com/openai/openai-apps-examples)
