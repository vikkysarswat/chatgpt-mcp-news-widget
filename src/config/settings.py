"""Application settings using Pydantic."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # MongoDB settings
    mongodb_uri: str
    mongodb_database: str = "news_db"
    mongodb_collection: str = "articles"
    
    # MCP Server settings
    mcp_server_port: int = 3000
    mcp_server_host: str = "0.0.0.0"
    
    # OpenAI settings (optional)
    openai_api_key: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    
    # Environment
    environment: str = "development"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )