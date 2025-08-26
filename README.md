# Reddit MCP Tool

A Model Context Protocol (MCP) server that provides read-only tools for browsing and searching Reddit content through Reddit's official API. This server allows you to search for posts, read post details, and get subreddit information through MCP-compatible clients.

## Features

- 🔍 **Search Posts**: Search for posts in specific subreddits with various sorting and filtering options
- 📊 **Get Subreddit Info**: Retrieve detailed information about subreddits
- 🔥 **Get Hot Posts**: Fetch hot posts from subreddits
- 📋 **Get Post Details**: Get comprehensive details about specific posts

## Prerequisites

1. **Python 3.10+** installed on your system
2. **uv** package manager installed ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
3. **Reddit API credentials** (see setup section below)

## Reddit API Setup

1. **Create a Reddit App**:

   - Go to [Reddit App Preferences](https://old.reddit.com/prefs/apps/)
   - Click "Create App" or "Create Another App"
   - Choose "script" for the app type
   - Fill in the required fields:
     - Name: Your app name (e.g., "Reddit MCP Tool")
     - Description: Brief description
     - About URL: Can be blank
     - Redirect URI: http://localhost:8080 (required but not used)

2. **Get Your Credentials**:
   - **Client ID**: Found under your app name (short string)
   - **Client Secret**: Found in the app details (longer string)

## Installation

1. **Clone or download this repository**:

   ```bash
   git clone <repository-url>
   cd reddit-mcp-tool
   ```

2. **Install dependencies using uv**:

   ```bash
   uv sync
   ```

3. **Set up environment variables**:

   ```bash
   cp env.example .env
   ```

   Edit the `.env` file with your Reddit API credentials:

   ```env
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_client_secret_here
   REDDIT_USER_AGENT=reddit-mcp-tool:v0.1.0 (by /u/yourusername)
   ```

   **Note**: This server operates in read-only mode and only requires the client ID, secret, and user agent for basic API access.

## Usage

### Running the MCP Server

```bash
uv run reddit-mcp-tool
```

Or directly with Python:

```bash
uv run python -m reddit_mcp.server
```

### Available Tools

#### 1. Search Reddit Posts

Search for posts in a specific subreddit:

```json
{
  "name": "search_reddit_posts",
  "arguments": {
    "subreddit": "python",
    "query": "machine learning",
    "limit": 10,
    "sort": "relevance",
    "time_filter": "week"
  }
}
```

#### 2. Get Post Details

Get detailed information about a specific post:

```json
{
  "name": "get_reddit_post_details",
  "arguments": {
    "post_id": "abc123"
  }
}
```

#### 3. Get Subreddit Information

Get information about a subreddit:

```json
{
  "name": "get_subreddit_info",
  "arguments": {
    "subreddit": "python"
  }
}
```

#### 4. Get Hot Posts

Get hot posts from a subreddit:

```json
{
  "name": "get_hot_reddit_posts",
  "arguments": {
    "subreddit": "programming",
    "limit": 15
  }
}
```

## Configuration

### Environment Variables

| Variable               | Required | Description                        |
| ---------------------- | -------- | ---------------------------------- |
| `REDDIT_CLIENT_ID`     | Yes      | Your Reddit app's client ID        |
| `REDDIT_CLIENT_SECRET` | Yes      | Your Reddit app's client secret    |
| `REDDIT_USER_AGENT`    | Yes      | User agent string for API requests |

## Integration with MCP Clients

This server implements the Model Context Protocol and can be used with any MCP-compatible client. Configure your MCP client to connect to this server using stdio transport.

Example MCP client configuration:

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uv",
      "args": ["run", "reddit-mcp-tool"],
      "cwd": "/path/to/reddit-mcp-tool"
    }
  }
}
```

## Error Handling

The server includes comprehensive error handling for common scenarios:

- Invalid subreddit names
- Post not found
- Authentication failures
- Rate limiting
- Network errors

All errors are returned as descriptive text content through the MCP protocol.

## Rate Limiting

Reddit's API has rate limits. The server respects these limits, but you may encounter rate limiting errors if you make too many requests in a short period. The default rate limit for authenticated users is typically 60 requests per minute.

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black .
uv run ruff check .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Disclaimer

This tool is for educational and development purposes. Please ensure you comply with Reddit's API Terms of Service and community guidelines when using this tool. This is a read-only tool that respects Reddit's API limits and does not provide any posting or commenting capabilities.

## Notes

- This project was renamed to `reddit-mcp-tool` to avoid conflicts with the existing `reddit-mcp` package on PyPI
- Only read-only operations are supported (search, read posts, get subreddit info)
- No user authentication is required - only app credentials for basic API access
- Built with the reliable PRAW (Python Reddit API Wrapper) library
- Includes proper rate limiting and error handling
