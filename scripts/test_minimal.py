#!/usr/bin/env python3
"""
Minimal Reddit API test.
"""

import os

import praw
from dotenv import load_dotenv


def main():
    load_dotenv()
    
    print("🔧 Minimal Reddit Test")
    
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )
    
    print("✅ Reddit instance created")
    
    # Try different subreddits
    test_subreddits = ["popular", "all", "AskReddit", "funny"]
    
    for sub_name in test_subreddits:
        try:
            print(f"\n🔍 Testing r/{sub_name}...")
            subreddit = reddit.subreddit(sub_name)
            
            # Just try to access the display name
            name = subreddit.display_name
            print(f"   ✅ Name: {name}")
            
            # Try to get subscriber count (this sometimes fails with 401)
            try:
                subs = subreddit.subscribers
                print(f"   ✅ Subscribers: {subs:,}")
            except Exception as e:
                print(f"   ⚠️  Subscribers failed: {e}")
            
            # Try to get a few hot posts
            try:
                hot_posts = list(subreddit.hot(limit=2))
                print(f"   ✅ Hot posts: {len(hot_posts)} found")
                for post in hot_posts:
                    print(f"      - {post.title[:40]}...")
                break  # If we get here, it's working!
                
            except Exception as e:
                print(f"   ⚠️  Hot posts failed: {e}")
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print(f"\n🎯 If any test succeeded above, your credentials are working!")

if __name__ == "__main__":
    main()
