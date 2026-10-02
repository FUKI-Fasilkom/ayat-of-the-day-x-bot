from pydantic import BaseModel, Field


class CreateTweetRequest(BaseModel):
    tweet_text: str = Field(min_length=1, max_length=280)


class CreateTweetResponse(BaseModel):
    tweet_id: str
    tweet_text: str | None = None


class ErrorResponse(BaseModel):
    detail: str

