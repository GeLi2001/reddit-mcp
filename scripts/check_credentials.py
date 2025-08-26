#!/usr/bin/env python3
"""
Debug Reddit API credentials.
"""

import os

import praw
from dotenv import load_dotenv


def main():
    """Check Reddit credentials step by step."""
    load_dotenv()
    
    print("🔧 Reddit API Credential Checker")
    print("=" * 40)
    
    # Check environment variables
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET") 
    user_agent = os.getenv("REDDIT_USER_AGENT")
    
    print(f"✅ Client ID: {client_id[:8] if client_id else 'MISSING'}...")
    print(f"✅ Client Secret: {'SET' if client_secret else 'MISSING'}")
    print(f"✅ User Agent: {user_agent if user_agent else 'MISSING'}")
    
    if not all([client_id, client_secret, user_agent]):
        print("❌ Missing credentials!")
        return
    
    print(f"\n🔍 Client ID length: {len(client_id)} chars")
    print(f"🔍 Client Secret length: {len(client_secret)} chars")
    
    # Expected lengths
    if len(client_id) < 10 or len(client_id) > 25:
        print("⚠️  Client ID seems wrong length (should be ~14-20 chars)")
    
    if len(client_secret) < 20 or len(client_secret) > 35:
        print("⚠️  Client Secret seems wrong length (should be ~27-30 chars)")
    
    # Test basic Reddit connection
    print(f"\n🔗 Testing Reddit API connection...")
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        
        # Test with a simple read-only call
        print("🔍 Testing read-only access...")
        
        # Get Reddit's own account info (public)
        me = reddit.user.me()
        if me is None:
            print("✅ Read-only access working! (No user authentication)")
            
            # Test subreddit access
            print("🔍 Testing subreddit access...")
            subreddit = reddit.subreddit("announcements")
            print(f"✅ Subreddit access: {subreddit.display_name}")
            print(f"   Subscribers: {subreddit.subscribers:,}")
            
        else:
            print(f"✅ Authenticated as: {me.name}")
            
    except Exception as e:
        print(f"❌ Reddit API Error: {str(e)}")
        print("\n🔧 Possible issues:")
        print("1. Wrong Client ID (should be under your app name)")
        print("2. Wrong Client Secret (longer string)")
        print("3. Reddit app not set to 'script' type")
        print("4. User agent not unique enough")

if __name__ == "__main__":
    main()
