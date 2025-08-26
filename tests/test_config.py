"""Tests for reddit_mcp.config module."""

import os
import pytest
from unittest.mock import patch
from reddit_mcp.config import RedditConfig


def test_config_from_env_success():
    """Test successful configuration loading from environment."""
    with patch.dict(os.environ, {
        'REDDIT_CLIENT_ID': 'test_client_id',
        'REDDIT_CLIENT_SECRET': 'test_client_secret',
        'REDDIT_USER_AGENT': 'test_user_agent',
    }):
        config = RedditConfig.from_env()
        assert config.client_id == 'test_client_id'
        assert config.client_secret == 'test_client_secret'
        assert config.user_agent == 'test_user_agent'


def test_config_from_env_missing_required():
    """Test configuration loading fails with missing required vars."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Missing required Reddit API configuration"):
            RedditConfig.from_env()


def test_config_from_env_partial_missing():
    """Test configuration loading fails with partially missing vars."""
    with patch.dict(os.environ, {
        'REDDIT_CLIENT_ID': 'test_client_id',
        # Missing SECRET and USER_AGENT
    }, clear=True):
        with pytest.raises(ValueError, match="Missing required Reddit API configuration"):
            RedditConfig.from_env()
