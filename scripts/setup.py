#!/usr/bin/env python3
"""
Setup script for Reddit MCP Tool.
Helps users configure their environment and test their Reddit API credentials.
"""

import os
import shutil
import sys
from pathlib import Path

def main():
    print("🚀 Reddit MCP Tool Setup")
    print("=" * 40)
    
    # Check if .env exists
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📋 Creating .env file from env.example...")
            shutil.copy(env_example, env_file)
            print("✅ .env file created!")
        else:
            print("❌ env.example file not found!")
            return 1
    else:
        print("✅ .env file already exists")
    
    print("\n📝 Next steps:")
    print("1. Edit the .env file with your Reddit API credentials")
    print("2. Get credentials from: https://old.reddit.com/prefs/apps/")
    print("3. Create a 'script' type app")
    print("4. Fill in these values in .env:")
    print("   - REDDIT_CLIENT_ID (14 character string)")
    print("   - REDDIT_CLIENT_SECRET (27 character string)")
    print("   - REDDIT_USER_AGENT (descriptive string)")
    
    print("\n🧪 Test your setup:")
    print("   uv run python scripts/test_basic.py")
    
    print("\n🏃 Run the MCP server:")
    print("   uv run reddit-mcp-tool")
    
    print("\n📖 For Claude Desktop, add this to your config:")
    print('''
{
  "mcpServers": {
    "reddit-mcp-tool": {
      "command": "uv",
      "args": ["run", "reddit-mcp-tool"],
      "cwd": "/path/to/reddit-mcp",
      "env": {
        "REDDIT_CLIENT_ID": "your_client_id_here",
        "REDDIT_CLIENT_SECRET": "your_client_secret_here",
        "REDDIT_USER_AGENT": "reddit-mcp-tool:v0.2.0 (by /u/yourusername)"
      }
    }
  }
}
    ''')
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
