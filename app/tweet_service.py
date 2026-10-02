from app.exceptions import BotConfigurationError, XPostError
from app.schemas import CreateTweetRequest, CreateTweetResponse
from app.twitter_client import TwitterClientProvider


class TweetService:
    def __init__(self, client_provider: TwitterClientProvider) -> None:
        self.client_provider = client_provider

    def create_tweet(self, payload: CreateTweetRequest) -> CreateTweetResponse:
        try:
            response = self.client_provider.get_client().get_post_api().post_create_tweet(
                tweet_text=payload.tweet_text,
            )
        except (BotConfigurationError, XPostError):
            raise
        except Exception as exc:
            raise XPostError("X did not accept the post request.") from exc

        try:
            result = response.data.data.create_tweet
            tweet = result.tweet_results.result if result is not None else None
        except (AttributeError, TypeError) as exc:
            raise XPostError("X returned an unexpected create-post response.") from exc

        if tweet is None or not tweet.rest_id:
            raise XPostError("X did not return the created post ID.")

        tweet_text = tweet.legacy.full_text if tweet.legacy is not None else None
        return CreateTweetResponse(tweet_id=tweet.rest_id, tweet_text=tweet_text)

