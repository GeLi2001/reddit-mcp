"""Reddit API client wrapper."""

from typing import Any, Dict, List

import asyncpraw

from .config import RedditConfig


class RedditClient:
    """Reddit API client for MCP server."""
    
    def __init__(self, config: RedditConfig):
        """Initialize Reddit client with read-only configuration."""
        self.config = config
        self._reddit = None
    
    @property
    def reddit(self):
        """Lazy initialize AsyncPRAW Reddit instance."""
        if self._reddit is None:
            self._reddit = asyncpraw.Reddit(
                client_id=self.config.client_id,
                client_secret=self.config.client_secret,
                user_agent=self.config.user_agent,
            )
        return self._reddit
    
    async def search_posts(
        self, 
        subreddit_name: str, 
        query: str, 
        limit: int = 10,
        sort: str = "relevance",
        time_filter: str = "all"
    ) -> List[Dict[str, Any]]:
        """Search for posts in a subreddit."""
        try:
            subreddit = await self.reddit.subreddit(subreddit_name)
            
            # Search posts
            posts = []
            search_results = subreddit.search(
                query, 
                limit=limit, 
                sort=sort, 
                time_filter=time_filter
            )
            
            async for submission in search_results:
                post_data = {
                    "id": submission.id,
                    "title": submission.title,
                    "author": str(submission.author) if submission.author else "[deleted]",
                    "score": submission.score,
                    "upvote_ratio": submission.upvote_ratio,
                    "url": submission.url,
                    "permalink": f"https://reddit.com{submission.permalink}",
                    "created_utc": submission.created_utc,
                    "num_comments": submission.num_comments,
                    "selftext": submission.selftext[:500] + "..." if len(submission.selftext) > 500 else submission.selftext,
                    "is_self": submission.is_self,
                    "domain": submission.domain,
                    "subreddit": str(submission.subreddit),
                }
                posts.append(post_data)
            
            return posts
            
        except Exception as e:
            raise Exception(f"Error searching posts in r/{subreddit_name}: {str(e)}")
    
    async def get_post_details(self, post_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific post."""
        try:
            submission = await self.reddit.submission(id=post_id)
            
            return {
                "id": submission.id,
                "title": submission.title,
                "author": str(submission.author) if submission.author else "[deleted]",
                "score": submission.score,
                "upvote_ratio": submission.upvote_ratio,
                "url": submission.url,
                "permalink": f"https://reddit.com{submission.permalink}",
                "created_utc": submission.created_utc,
                "num_comments": submission.num_comments,
                "selftext": submission.selftext,
                "is_self": submission.is_self,
                "domain": submission.domain,
                "subreddit": str(submission.subreddit),
                "flair_text": submission.link_flair_text,
                "locked": submission.locked,
                "stickied": submission.stickied,
            }
            
        except Exception as e:
            raise Exception(f"Error getting post details for {post_id}: {str(e)}")
    

    

    
    async def get_subreddit_info(self, subreddit_name: str) -> Dict[str, Any]:
        """Get information about a subreddit."""
        try:
            subreddit = await self.reddit.subreddit(subreddit_name)
            
            return {
                "name": subreddit.display_name,
                "title": subreddit.title,
                "description": subreddit.description[:500] + "..." if len(subreddit.description) > 500 else subreddit.description,
                "subscribers": subreddit.subscribers,
                "active_user_count": subreddit.active_user_count,
                "created_utc": subreddit.created_utc,
                "over18": subreddit.over18,
                "public_description": subreddit.public_description,
                "url": f"https://reddit.com/r/{subreddit.display_name}",
            }
            
        except Exception as e:
            raise Exception(f"Error getting subreddit info for r/{subreddit_name}: {str(e)}")
    
    async def get_hot_posts(self, subreddit_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get hot posts from a subreddit."""
        try:
            subreddit = await self.reddit.subreddit(subreddit_name)
            
            posts = []
            async for submission in subreddit.hot(limit=limit):
                post_data = {
                    "id": submission.id,
                    "title": submission.title,
                    "author": str(submission.author) if submission.author else "[deleted]",
                    "score": submission.score,
                    "upvote_ratio": submission.upvote_ratio,
                    "url": submission.url,
                    "permalink": f"https://reddit.com{submission.permalink}",
                    "created_utc": submission.created_utc,
                    "num_comments": submission.num_comments,
                    "selftext": submission.selftext[:200] + "..." if len(submission.selftext) > 200 else submission.selftext,
                    "is_self": submission.is_self,
                    "domain": submission.domain,
                    "subreddit": str(submission.subreddit),
                }
                posts.append(post_data)
            
            return posts
            
        except Exception as e:
            raise Exception(f"Error getting hot posts from r/{subreddit_name}: {str(e)}")
    
    async def search_all_reddit(
        self, 
        query: str, 
        limit: int = 10,
        sort: str = "relevance",
        time_filter: str = "all"
    ) -> List[Dict[str, Any]]:
        """Search for posts across all of Reddit (site-wide search)."""
        try:
            # Search all of reddit using the 'all' subreddit
            all_subreddit = await self.reddit.subreddit("all")
            
            posts = []
            search_results = all_subreddit.search(
                query, 
                limit=limit, 
                sort=sort, 
                time_filter=time_filter
            )
            
            async for submission in search_results:
                post_data = {
                    "id": submission.id,
                    "title": submission.title,
                    "author": str(submission.author) if submission.author else "[deleted]",
                    "score": submission.score,
                    "upvote_ratio": submission.upvote_ratio,
                    "url": submission.url,
                    "permalink": f"https://reddit.com{submission.permalink}",
                    "created_utc": submission.created_utc,
                    "num_comments": submission.num_comments,
                    "selftext": submission.selftext[:500] + "..." if len(submission.selftext) > 500 else submission.selftext,
                    "is_self": submission.is_self,
                    "domain": submission.domain,
                    "subreddit": str(submission.subreddit),
                }
                posts.append(post_data)
            
            return posts
            
        except Exception as e:
            raise Exception(f"Error searching all Reddit for query '{query}': {str(e)}")