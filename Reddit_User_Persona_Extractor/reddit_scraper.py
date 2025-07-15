import os
import praw
from urllib.parse import urlparse

def extract_username(profile_url):
    """Extract Reddit username from profile URL."""
    return urlparse(profile_url).path.strip("/").split("/")[-1]

def get_reddit_instance():
    """Returns authenticated Reddit instance using PRAW."""
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = "RedditPersonaScript/0.1 by u/realdex7er"

    if not client_id or not client_secret:
        raise EnvironmentError("Reddit API credentials not found. Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET.")

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

def scrape_user_data(username):
    """Fetches submissions and comments of a user."""
    reddit = get_reddit_instance()
    redditor = reddit.redditor(username)

    posts = []
    comments = []

    try:
        for post in redditor.submissions.new(limit=50):
            posts.append({
                "title": post.title,
                "body": post.selftext,
                "url": post.permalink
            })

        for comment in redditor.comments.new(limit=100):
            comments.append({
                "body": comment.body,
                "url": comment.permalink
            })

    except Exception:
        # Fail silently, avoid printing errors
        return [], []

    return posts, comments
