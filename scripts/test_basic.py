#!/usr/bin/env python3
"""
Most basic Reddit API test possible.
"""

import os

import praw
from dotenv import load_dotenv


def main():
    load_dotenv()
    
    print("🔧 Ultra Basic Reddit Test")
    print("=" * 30)
    
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )
        
        print("✅ Reddit instance created")
        print(f"📊 Read-only: {reddit.read_only}")
        
        # Test 1: Just get a subreddit object (no API call yet)
        print("\n🔍 Test 1: Creating subreddit object...")
        sub = reddit.subreddit("python")
        print(f"✅ Subreddit object created: {sub}")
        
        # Test 2: Access the name (minimal API call)
        print("\n🔍 Test 2: Getting subreddit name...")
        try:
            name = sub.display_name
            print(f"✅ Name: {name}")
        except Exception as e:
            print(f"❌ Name failed: {e}")
            return
        
        # Test 3: Try to get one post (most basic content access)
        print("\n🔍 Test 3: Getting one hot post...")
        try:
            posts = list(sub.hot(limit=1))
            if posts:
                post = posts[0]
                print(f"✅ Got post: {post.title[:50]}...")
                print(f"   Score: {post.score}")
                print(f"   Author: {post.author}")
                print("🎉 SUCCESS! Your Reddit MCP Tool should work!")
            else:
                print("⚠️  No posts found")
        except Exception as e:
            print(f"❌ Posts failed: {e}")
            print("\n🚨 This is the exact same error your MCP tool will have")
            
        # Test 4: Check Reddit API limits/status
        print(f"\n📈 Reddit API Status:")
        print(f"   Read-only mode: {reddit.read_only}")
        # print(f"   Auth: {reddit._core._authorized}")  # This property doesn't exist in PRAW 7.x
        
    except Exception as e:
        print(f"❌ Critical error: {e}")

if __name__ == "__main__":
    main()
