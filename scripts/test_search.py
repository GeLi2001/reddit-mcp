#!/usr/bin/env python3
"""
Quick search test for Reddit MCP Tool.
"""

from reddit_mcp.config import RedditConfig
from reddit_mcp.reddit_client import RedditClient


def main():
    """Test search functionality."""
    try:
        print("🔍 Testing Reddit Search...")
        
        config = RedditConfig.from_env()
        client = RedditClient(config)
        
        # Test search
        posts = client.search_posts("python", "machine learning", limit=3)
        
        print(f"✅ Search successful! Found {len(posts)} posts:")
        for i, post in enumerate(posts, 1):
            print(f"  {i}. {post['title'][:60]}...")
            print(f"     Score: {post['score']}, Comments: {post['num_comments']}")
        
        print("\n🎉 Your Reddit MCP Tool search is working!")
        
    except Exception as e:
        print(f"❌ Search failed: {e}")
        print("💡 Make sure your Reddit app is type 'script' and credentials are correct")

if __name__ == "__main__":
    main()
