# Reddit MCP Tool - Troubleshooting Guide

This guide helps you resolve common issues when setting up and using the Reddit MCP Tool.

## Quick Setup

1. **Run the setup script:**
   ```bash
   uv run python scripts/setup.py
   ```

2. **Edit your .env file with real credentials:**
   ```bash
   # Edit .env with your favorite editor
   nano .env
   # or
   code .env
   ```

3. **Test your setup:**
   ```bash
   uv run python scripts/test_basic.py
   ```

## Common Issues

### 1. "Server transport closed unexpectedly"

**Symptoms:**
- MCP server starts but immediately disconnects
- Claude shows "Server disconnected" error
- Logs show transport closed messages

**Cause:** Missing or invalid Reddit API credentials

**Solution:**
1. Create `.env` file: `cp env.example .env`
2. Get Reddit API credentials from https://old.reddit.com/prefs/apps/
3. Fill in your `.env` file with real values
4. Restart the MCP server

### 2. "Reddit client not initialized"

**Symptoms:**
- Server starts but all tool calls return initialization errors
- Error mentions missing REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, or REDDIT_USER_AGENT

**Solution:**
Same as issue #1 - you need valid Reddit API credentials in your `.env` file.

### 3. "ModuleNotFoundError: No module named 'praw'"

**Symptoms:**
- Test scripts fail to run
- Import errors when running tests

**Solution:**
```bash
uv sync  # Install all dependencies including praw
```

### 4. Reddit API Authentication Errors

**Symptoms:**
- "401 Unauthorized" errors
- "Invalid client_id" or "Invalid client_secret"

**Solution:**
1. Double-check your Reddit app credentials
2. Ensure you created a "script" type app (not "web app")
3. Verify client_id and client_secret are copied correctly
4. Make sure your user_agent is descriptive and unique

### 5. Rate Limiting Issues

**Symptoms:**
- "429 Too Many Requests" errors
- Slow responses or timeouts

**Solution:**
- Reddit allows 60 requests per minute for authenticated users
- Wait a minute between heavy usage
- Consider reducing the `limit` parameter in your requests

## Getting Reddit API Credentials

1. **Go to Reddit App Preferences:**
   https://old.reddit.com/prefs/apps/

2. **Click "Create App" or "Create Another App"**

3. **Fill in the form:**
   - **Name:** reddit-mcp-tool (or any name you prefer)
   - **App type:** Select "script"
   - **Description:** Reddit MCP Tool for Claude Desktop
   - **About URL:** Leave blank or add your GitHub repo
   - **Redirect URI:** http://localhost:8080 (required but not used)

4. **Get your credentials:**
   - **Client ID:** The short string under your app name (14 characters)
   - **Client Secret:** The longer string in the app details (27 characters)

5. **Create a user agent:**
   - Format: `reddit-mcp-tool:v0.2.0 (by /u/yourusername)`
   - Replace `yourusername` with your Reddit username

## Testing Your Setup

### Basic Test
```bash
uv run python scripts/test_basic.py
```

### Test with MCP Server
```bash
# Start the server
uv run reddit-mcp-tool

# In another terminal, test with MCP client
# (This requires an MCP client like Claude Desktop)
```

### Manual API Test
```python
import os
from dotenv import load_dotenv
import praw

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

# Test basic access
print(f"Read-only: {reddit.read_only}")
subreddit = reddit.subreddit("python")
print(f"Subreddit: {subreddit.display_name}")

# Test getting a post
for post in subreddit.hot(limit=1):
    print(f"Post: {post.title}")
    break
```

## Claude Desktop Configuration

Add this to your Claude Desktop MCP configuration file:

### For Local Development:
```json
{
  "mcpServers": {
    "reddit-mcp-tool": {
      "command": "uv",
      "args": ["run", "reddit-mcp-tool"],
      "cwd": "/path/to/your/reddit-mcp-tool",
      "env": {
        "REDDIT_CLIENT_ID": "your_actual_client_id",
        "REDDIT_CLIENT_SECRET": "your_actual_client_secret",
        "REDDIT_USER_AGENT": "reddit-mcp-tool:v0.2.0 (by /u/yourusername)"
      }
    }
  }
}
```

### For Published Package:
```json
{
  "mcpServers": {
    "reddit-mcp-tool": {
      "command": "uvx",
      "args": ["reddit-mcp-tool@latest"],
      "env": {
        "REDDIT_CLIENT_ID": "your_actual_client_id",
        "REDDIT_CLIENT_SECRET": "your_actual_client_secret",
        "REDDIT_USER_AGENT": "reddit-mcp-tool:v0.2.0 (by /u/yourusername)"
      }
    }
  }
}
```

**Important:** Replace the placeholder values with your actual Reddit API credentials!

## Still Having Issues?

1. **Check the logs:** Look for error messages when starting the server
2. **Verify dependencies:** Run `uv sync` to ensure all packages are installed
3. **Test Reddit API directly:** Use the manual test script above
4. **Check Reddit API status:** Visit https://www.redditstatus.com/
5. **Review Reddit API docs:** https://www.reddit.com/dev/api/

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `REDDIT_CLIENT_ID` | Yes | Your Reddit app's client ID | `abc123def456ghi7` |
| `REDDIT_CLIENT_SECRET` | Yes | Your Reddit app's client secret | `xyz789uvw456rst123abc789def456` |
| `REDDIT_USER_AGENT` | Yes | Descriptive user agent string | `reddit-mcp-tool:v0.2.0 (by /u/myusername)` |

## Support

- **GitHub Issues:** Report bugs and feature requests
- **Reddit API Help:** /r/redditdev subreddit
- **MCP Documentation:** https://modelcontextprotocol.io/
