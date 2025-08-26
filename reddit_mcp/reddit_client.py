"""Reddit API client wrapper."""

from typing import Any, Dict, List

import praw

from .config import RedditConfig


class RedditClient:
    """Reddit API client for MCP server."""
    
    def __init__(self, config: RedditConfig):
        """Initialize Reddit client with read-only configuration."""
        self.config = config
        
        # Initialize PRAW Reddit instance for read-only access
        self.reddit = praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent,
        )
    
    def search_posts(
        self, 
        subreddit_name: str, 
        query: str, 
        limit: int = 10,
        sort: str = "relevance",
        time_filter: str = "all"
    ) -> List[Dict[str, Any]]:
        """Search for posts in a subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Search posts
            posts = []
            search_results = subreddit.search(
                query, 
                limit=limit, 
                sort=sort, 
                time_filter=time_filter
            )
            
            for submission in search_results:
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
    
    def get_post_details(self, post_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific post."""
        try:
            submission = self.reddit.submission(id=post_id)
            
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
    

    

    
    def get_subreddit_info(self, subreddit_name: str) -> Dict[str, Any]:
        """Get information about a subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
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
    
    def get_hot_posts(self, subreddit_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get hot posts from a subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            posts = []
            for submission in subreddit.hot(limit=limit):
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
    
    def search_all_reddit(
        self, 
        query: str, 
        limit: int = 10,
        sort: str = "relevance",
        time_filter: str = "all"
    ) -> List[Dict[str, Any]]:
        """Search for posts across all of Reddit (site-wide search)."""
        try:
            # Search all of reddit using the 'all' subreddit
            all_subreddit = self.reddit.subreddit("all")
            
            posts = []
            search_results = all_subreddit.search(
                query, 
                limit=limit, 
                sort=sort, 
                time_filter=time_filter
            )
            
            for submission in search_results:
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