"""Pytest configuration and shared fixtures."""

import pytest
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def mock_settings():
    """Mock application settings."""
    from config.settings import Settings
    
    return Settings(
        mongodb_uri="mongodb://localhost:27017",
        mongodb_database="test_db",
        mongodb_collection="test_articles",
        mcp_server_port=3000,
        log_level="DEBUG",
        environment="testing"
    )