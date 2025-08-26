"""Reddit MCP Server implementation using FastMCP."""

import logging
from typing import  Optional

from fastmcp import FastMCP

from .config import RedditConfig
from .reddit_client import RedditClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("reddit-mcp-tool")

# Global client instance
reddit_client: Optional[RedditClient] = None


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


@mcp.tool()
async def search_reddit_posts(
    subreddit: str,
    query: str, 
    limit: int = 10,
    sort: str = "relevance",
    time_filter: str = "all"
) -> str:
    """
    Search for posts in a specific subreddit

    Args:
        subreddit: The name of the subreddit to search in (without r/)
        query: The search query
        limit: Number of posts to return (default: 10, max: 100)
        sort: Sort method - "relevance", "hot", "top", "new", "comments" (default: "relevance")
        time_filter: Time filter - "all", "day", "week", "month", "year" (default: "all")

    Returns:
        Human readable string containing search results
    """
    if reddit_client is None:
        return "Error: Reddit client not initialized. Please check your configuration and ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT are set."
    
    try:
        posts = await reddit_client.search_posts(
            subreddit_name=subreddit,
            query=query,
            limit=min(limit, 100),
            sort=sort,
            time_filter=time_filter
        )
        
        if not posts:
            return f"No posts found in r/{subreddit} for query: '{query}'"
        
        result = f"Found {len(posts)} posts in r/{subreddit} for query: '{query}'\n\n"
        
        for i, post in enumerate(posts, 1):
            result += (
                f"{i}. **{post['title']}**\n"
                f"   Author: {post['author']}\n"
                f"   Score: {post['score']} (upvote ratio: {post['upvote_ratio']:.0%})\n"
                f"   Comments: {post['num_comments']}\n"
                f"   Link: {post['permalink']}\n"
                f"   Subreddit: r/{post['subreddit']}\n"
            )
            
            if post['selftext'] and len(post['selftext']) > 0:
                preview = post['selftext'][:200] + "..." if len(post['selftext']) > 200 else post['selftext']
                result += f"   Content: {preview}\n"
            
            result += "\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error searching posts in r/{subreddit}: {str(e)}")
        return f"Error searching posts in r/{subreddit}: {str(e)}"


@mcp.tool()
async def search_reddit_all(
    query: str,
    limit: int = 10,
    sort: str = "relevance", 
    time_filter: str = "all"
) -> str:
    """
    Search for posts across all of Reddit (site-wide search)

    Args:
        query: The search query to search across all Reddit
        limit: Number of posts to return (default: 10, max: 100)
        sort: Sort method - "relevance", "hot", "top", "new", "comments" (default: "relevance")
        time_filter: Time filter - "all", "day", "week", "month", "year" (default: "all")

    Returns:
        Human readable string containing search results from across Reddit
    """
    if reddit_client is None:
        return "Error: Reddit client not initialized. Please check your configuration and ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT are set."
    
    try:
        posts = await reddit_client.search_all_reddit(
            query=query,
            limit=min(limit, 100),
            sort=sort,
            time_filter=time_filter
        )
        
        if not posts:
            return f"No posts found across Reddit for query: '{query}'"
        
        result = f"Found {len(posts)} posts across all Reddit for query: '{query}'\n\n"
        
        for i, post in enumerate(posts, 1):
            result += (
                f"{i}. **{post['title']}**\n"
                f"   Author: {post['author']}\n"
                f"   Score: {post['score']} (upvote ratio: {post['upvote_ratio']:.0%})\n"
                f"   Comments: {post['num_comments']}\n"
                f"   Link: {post['permalink']}\n"
                f"   Subreddit: r/{post['subreddit']}\n"
            )
            
            if post['selftext'] and len(post['selftext']) > 0:
                preview = post['selftext'][:200] + "..." if len(post['selftext']) > 200 else post['selftext']
                result += f"   Content: {preview}\n"
            
            result += "\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error searching all Reddit for query '{query}': {str(e)}")
        return f"Error searching all Reddit for query '{query}': {str(e)}"


@mcp.tool()
async def get_reddit_post_details(post_id: str) -> str:
    """
    Get detailed information about a specific Reddit post

    Args:
        post_id: The Reddit post ID

    Returns:
        Human readable string containing detailed post information
    """
    if reddit_client is None:
        return "Error: Reddit client not initialized. Please check your configuration and ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT are set."
    
    try:
        post_details = await reddit_client.get_post_details(post_id)
        
        result = (
            f"**{post_details['title']}**\n\n"
            f"Author: {post_details['author']}\n"
            f"Score: {post_details['score']} (upvote ratio: {post_details['upvote_ratio']:.0%})\n"
            f"Comments: {post_details['num_comments']}\n"
            f"Link: {post_details['permalink']}\n"
            f"Subreddit: r/{post_details['subreddit']}\n"
            f"Domain: {post_details['domain']}\n"
            f"Locked: {post_details['locked']}\n"
            f"Stickied: {post_details['stickied']}\n"
        )
        
        if post_details.get('flair_text'):
            result += f"Flair: {post_details['flair_text']}\n"
        
        if post_details['selftext']:
            result += f"\nContent:\n{post_details['selftext']}\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting post details for {post_id}: {str(e)}")
        return f"Error getting post details for {post_id}: {str(e)}"


@mcp.tool()
async def get_subreddit_info(subreddit: str) -> str:
    """
    Get information about a subreddit

    Args:
        subreddit: The name of the subreddit (without r/)

    Returns:
        Human readable string containing subreddit information
    """
    if reddit_client is None:
        return "Error: Reddit client not initialized. Please check your configuration and ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT are set."
    
    try:
        subreddit_info = await reddit_client.get_subreddit_info(subreddit)
        
        result = (
            f"**r/{subreddit_info['name']}**\n\n"
            f"Title: {subreddit_info['title']}\n"
            f"Subscribers: {subreddit_info['subscribers']:,}\n"
            f"Active Users: {subreddit_info['active_user_count'] or 'N/A'}\n"
            f"NSFW: {subreddit_info['over18']}\n"
            f"URL: {subreddit_info['url']}\n\n"
            f"Description:\n{subreddit_info['public_description']}\n"
        )
        
        if subreddit_info['description'] and subreddit_info['description'] != subreddit_info['public_description']:
            result += f"\nFull Description:\n{subreddit_info['description']}\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting subreddit info for r/{subreddit}: {str(e)}")
        return f"Error getting subreddit info for r/{subreddit}: {str(e)}"


@mcp.tool()
async def get_hot_reddit_posts(subreddit: str, limit: int = 10) -> str:
    """
    Get hot posts from a subreddit

    Args:
        subreddit: The name of the subreddit (without r/)
        limit: Number of posts to return (default: 10, max: 100)

    Returns:
        Human readable string containing hot posts
    """
    if reddit_client is None:
        return "Error: Reddit client not initialized. Please check your configuration and ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT are set."
    
    try:
        posts = await reddit_client.get_hot_posts(subreddit, min(limit, 100))
        
        if not posts:
            return f"No hot posts found in r/{subreddit}"
        
        result = f"Hot posts from r/{subreddit}:\n\n"
        
        for i, post in enumerate(posts, 1):
            result += (
                f"{i}. **{post['title']}**\n"
                f"   Author: {post['author']}\n"
                f"   Score: {post['score']} (upvote ratio: {post['upvote_ratio']:.0%})\n"
                f"   Comments: {post['num_comments']}\n"
                f"   Link: {post['permalink']}\n"
            )
            
            if post['selftext'] and len(post['selftext']) > 0:
                preview = post['selftext'][:150] + "..." if len(post['selftext']) > 150 else post['selftext']
                result += f"   Content: {preview}\n"
            
            result += "\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting hot posts from r/{subreddit}: {str(e)}")
        return f"Error getting hot posts from r/{subreddit}: {str(e)}"


def run_server():
    """Entry point for the CLI command."""
    # Initialize Reddit client
    initialize_reddit_client()
    
    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    run_server()