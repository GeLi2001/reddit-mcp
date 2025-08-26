#!/usr/bin/env python3
"""
Simple sync test of Reddit credentials.
"""

from reddit_mcp.config import RedditConfig
from reddit_mcp.reddit_client import RedditClient


def main():
    """Test Reddit client synchronously."""
    try:
        print("🔧 Testing Reddit API credentials...")
        
        # Initialize configuration
        config = RedditConfig.from_env()
        print(f"✅ Configuration loaded")
        print(f"   Client ID: {config.client_id[:8]}...")
        print(f"   User Agent: {config.user_agent}")
        
        # Initialize client
        client = RedditClient(config)
        print("✅ Reddit client initialized")
        
        # Test a simple API call
        print("\n🔍 Testing API call: Getting r/test subreddit info...")
        subreddit_info = client.get_subreddit_info("test")
        print(f"✅ Success! Subreddit: {subreddit_info['name']}")
        print(f"   Subscribers: {subreddit_info['subscribers']:,}")
        print(f"   Description: {subreddit_info['description'][:100]}...")
        
        print("\n🔍 Testing search: Searching for 'hello' in r/test...")
        posts = client.search_posts("test", "hello", limit=3)
        print(f"✅ Success! Found {len(posts)} posts")
        for i, post in enumerate(posts, 1):
            print(f"   {i}. {post['title'][:50]}... (Score: {post['score']})")
        
        print("\n🎉 All tests passed! Your Reddit MCP Tool is working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your .env file has correct Reddit API credentials")
        print("2. Verify your Reddit app is type 'script'")
        print("3. Make sure your app credentials are copied correctly")

if __name__ == "__main__":
    main()
