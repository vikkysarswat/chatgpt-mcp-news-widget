# Contributing to ChatGPT MCP News Widget

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/vikkysarswat/chatgpt-mcp-news-widget/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing issues and discussions first
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style (PEP 8 for Python)
   - Add tests for new features
   - Update documentation

4. **Test your changes**
   ```bash
   pytest tests/
   python scripts/test_mcp_connection.py
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of your changes"
   ```
   
   Commit message format:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Test:` for test additions/modifications

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Include screenshots for UI changes

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/chatgpt-mcp-news-widget.git
   cd chatgpt-mcp-news-widget
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up pre-commit hooks (optional):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Example

```python
def fetch_news(
    limit: int = 10,
    category: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Fetch news articles from database.
    
    Args:
        limit: Maximum number of articles to fetch
        category: Optional category filter
        
    Returns:
        List of news articles
        
    Raises:
        ValueError: If limit is invalid
    """
    pass
```

## Testing

- Write tests for all new features
- Ensure existing tests pass
- Aim for good code coverage

```python
import pytest

@pytest.mark.asyncio
async def test_fetch_news():
    # Test implementation
    pass
```

## Documentation

- Update README.md if needed
- Add/update docstrings
- Update relevant docs in `docs/` folder
- Include code examples

## Project Structure

```
src/
  ├── mcp_server.py       # Main server
  ├── mongodb_client.py   # Database client
  ├── config/             # Configuration
  └── tools/              # MCP tools
      ├── fetch_news.py
      └── [new_tool].py   # Add new tools here

tests/                  # Test files
  ├── test_*.py
  └── conftest.py

scripts/                # Utility scripts
  ├── seed_mongodb.py
  └── test_mcp_connection.py

docs/                   # Documentation
openai_app/            # OpenAI app config
```

## Adding New Tools

See [EXTENDING.md](docs/EXTENDING.md) for detailed guide on adding new MCP tools.

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion
- Reach out to maintainers

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project

## License

By contributing, you agree that your contributions will be licensed under the MIT License.