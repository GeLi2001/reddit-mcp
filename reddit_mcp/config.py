"""Configuration management for Reddit MCP."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class RedditConfig:
    """Reddit API configuration for read-only access."""
    
    client_id: str
    client_secret: str
    user_agent: str
    
    @classmethod
    def from_env(cls) -> "RedditConfig":
        """Load configuration from environment variables."""
        load_dotenv()
        
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT")
        
        if not client_id or not client_secret or not user_agent:
            raise ValueError(
                "Missing required Reddit API configuration. "
                "Please set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT"
            )
        
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
