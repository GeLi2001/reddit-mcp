"""Reddit MCP Server implementation with proper MCP SDK patterns."""

import json
import logging
from typing import Any, Dict, List, Optional, Sequence

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.types import CallToolResult, TextContent, Tool

from .config import RedditConfig
from .reddit_client import RedditClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("reddit-mcp-tool")

# Global client instance
reddit_client: Optional[RedditClient] = None


def get_available_tools() -> List[Tool]:
    """Get the list of available Reddit tools."""
    return [
        Tool(
            name="search_reddit_posts",
            description="Search for posts in a specific subreddit",
            inputSchema={
                "type": "object",
                "properties": {
                    "subreddit": {
                        "type": "string",
                        "description": "The name of the subreddit to search in (without r/)"
                    },
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to return (default: 10, max: 100)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "sort": {
                        "type": "string",
                        "description": "Sort method for search results",
                        "enum": ["relevance", "hot", "top", "new", "comments"],
                        "default": "relevance"
                    },
                    "time_filter": {
                        "type": "string",
                        "description": "Time filter for search results",
                        "enum": ["all", "day", "week", "month", "year"],
                        "default": "all"
                    }
                },
                "required": ["subreddit", "query"]
            }
        ),
        Tool(
            name="get_reddit_post_details",
            description="Get detailed information about a specific Reddit post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {
                        "type": "string",
                        "description": "The Reddit post ID"
                    }
                },
                "required": ["post_id"]
            }
        ),
        Tool(
            name="get_subreddit_info",
            description="Get information about a subreddit",
            inputSchema={
                "type": "object",
                "properties": {
                    "subreddit": {
                        "type": "string",
                        "description": "The name of the subreddit (without r/)"
                    }
                },
                "required": ["subreddit"]
            }
        ),
        Tool(
            name="get_hot_reddit_posts",
            description="Get hot posts from a subreddit",
            inputSchema={
                "type": "object",
                "properties": {
                    "subreddit": {
                        "type": "string",
                        "description": "The name of the subreddit (without r/)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to return (default: 10, max: 100)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["subreddit"]
            }
        ),
        Tool(
            name="search_reddit_all",
            description="Search for posts across all of Reddit (site-wide search)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to search across all Reddit"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to return (default: 10, max: 100)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "sort": {
                        "type": "string",
                        "description": "Sort method for search results",
                        "enum": ["relevance", "hot", "top", "new", "comments"],
                        "default": "relevance"
                    },
                    "time_filter": {
                        "type": "string",
                        "description": "Time filter for search results",
                        "enum": ["all", "day", "week", "month", "year"],
                        "default": "all"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Handle tools list request."""
    return get_available_tools()


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any] | None) -> CallToolResult:
    """Handle tool call requests."""
    global reddit_client
    
    # Safety guard
    arguments = arguments or {}
    
    if reddit_client is None:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="Error: Reddit client not initialized. Please check your configuration and ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT are set."
                )
            ]
        )
    
    try:
        if name == "search_reddit_posts":
            subreddit = arguments.get("subreddit")
            query = arguments.get("query")
            limit = arguments.get("limit", 10)
            sort = arguments.get("sort", "relevance")
            time_filter = arguments.get("time_filter", "all")
            
            posts = await reddit_client.search_posts(
                subreddit_name=subreddit,
                query=query,
                limit=limit,
                sort=sort,
                time_filter=time_filter
            )
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Found {len(posts)} posts in r/{subreddit} for query: '{query}'\n\n" +
                             json.dumps(posts, indent=2, default=str)
                    )
                ]
            )
        
        elif name == "get_reddit_post_details":
            post_id = arguments.get("post_id")
            post_details = await reddit_client.get_post_details(post_id)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Post details for {post_id}:\n\n" +
                             json.dumps(post_details, indent=2, default=str)
                    )
                ]
            )
        
        elif name == "get_subreddit_info":
            subreddit = arguments.get("subreddit")
            subreddit_info = await reddit_client.get_subreddit_info(subreddit)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Subreddit information for r/{subreddit}:\n\n" +
                             json.dumps(subreddit_info, indent=2, default=str)
                    )
                ]
            )
        
        elif name == "get_hot_reddit_posts":
            subreddit = arguments.get("subreddit")
            limit = arguments.get("limit", 10)
            
            posts = await reddit_client.get_hot_posts(subreddit, limit)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Hot posts from r/{subreddit}:\n\n" +
                             json.dumps(posts, indent=2, default=str)
                    )
                ]
            )
        
        elif name == "search_reddit_all":
            query = arguments.get("query")
            limit = arguments.get("limit", 10)
            sort = arguments.get("sort", "relevance")
            time_filter = arguments.get("time_filter", "all")
            
            posts = await reddit_client.search_all_reddit(
                query=query,
                limit=limit,
                sort=sort,
                time_filter=time_filter
            )
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Found {len(posts)} posts across all Reddit for query: '{query}'\n\n" +
                             json.dumps(posts, indent=2, default=str)
                    )
                ]
            )
        
        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )
                ]
            )
    
    except Exception as e:
        logger.error(f"Error calling tool {name}: {str(e)}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        )


def initialize_reddit_client():
    """Initialize the Reddit client with configuration."""
    global reddit_client
    try:
        config = RedditConfig.from_env()
        reddit_client = RedditClient(config)
        logger.info("Reddit client initialized successfully in read-only mode")
            
    except Exception as e:
        logger.error(f"Failed to initialize Reddit client: {str(e)}")
        reddit_client = None


async def main():
    """Main entry point for the Reddit MCP server."""
    import asyncio

    from mcp.server.stdio import stdio_server

    # Initialize Reddit client
    initialize_reddit_client()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="reddit-mcp-tool",
                server_version="0.1.9",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def run_server():
    """Entry point for the CLI command."""
    import asyncio
    asyncio.run(main())


if __name__ == "__main__":
    run_server()
