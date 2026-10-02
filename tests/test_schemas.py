import pytest
from pydantic import ValidationError

from app.schemas import CreateTweetRequest


def test_accepts_a_non_empty_post_within_the_limit() -> None:
    request = CreateTweetRequest(tweet_text="Ayat of The Day")
    assert request.tweet_text == "Ayat of The Day"


@pytest.mark.parametrize("value", ["", "x" * 281])
def test_rejects_empty_or_oversized_posts(value: str) -> None:
    with pytest.raises(ValidationError):
        CreateTweetRequest(tweet_text=value)

