from functools import lru_cache

from app.config import get_settings
from app.tweet_service import TweetService
from app.twitter_client import TwitterClientProvider


@lru_cache
def get_twitter_client_provider() -> TwitterClientProvider:
    return TwitterClientProvider(get_settings())


def get_tweet_service() -> TweetService:
    return TweetService(get_twitter_client_provider())

