#!/usr/bin/env python3
"""
Example usage of the Reddit MCP Tool.

This script demonstrates how to use the Reddit client directly
for testing purposes. The actual MCP server runs via stdio transport.
"""

import asyncio
import json

from reddit_mcp.config import RedditConfig
from reddit_mcp.reddit_client import RedditClient


async def main():
    """Example usage of Reddit MCP components."""
    try:
        # Initialize configuration
        print("Initializing Reddit client...")
        config = RedditConfig.from_env()
        client = RedditClient(config)
        
        # Read-only mode
        print("ℹ️ Read-only mode - can search and read posts")
        
        # Example 1: Get subreddit information
        print("\n1. Getting subreddit information for r/python...")
        subreddit_info = client.get_subreddit_info("python")
        print(f"Subreddit: {subreddit_info['name']}")
        print(f"Subscribers: {subreddit_info['subscribers']:,}")
        print(f"Description: {subreddit_info['description'][:100]}...")
        
        # Example 2: Get hot posts
        print("\n2. Getting hot posts from r/python...")
        hot_posts = client.get_hot_posts("python", limit=5)
        for i, post in enumerate(hot_posts, 1):
            print(f"{i}. {post['title'][:60]}... (Score: {post['score']})")
        
        # Example 3: Search for posts
        print("\n3. Searching for 'machine learning' in r/python...")
        search_results = client.search_posts(
            subreddit_name="python",
            query="machine learning",
            limit=3,
            sort="relevance"
        )
        for i, post in enumerate(search_results, 1):
            print(f"{i}. {post['title'][:60]}... (Score: {post['score']})")
        
        # Example 4: Get detailed post information
        if search_results:
            post_id = search_results[0]['id']
            print(f"\n4. Getting detailed information for post {post_id}...")
            post_details = client.get_post_details(post_id)
            print(f"Title: {post_details['title']}")
            print(f"Author: {post_details['author']}")
            print(f"Comments: {post_details['num_comments']}")
            print(f"URL: {post_details['permalink']}")
        
        print("\n✅ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Created a .env file with your Reddit API credentials")
        print("2. Set up a Reddit app at https://old.reddit.com/prefs/apps/")
        print("3. Added the required environment variables")


if __name__ == "__main__":
    asyncio.run(main())
