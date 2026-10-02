from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.dependencies import get_tweet_service
from app.main import create_app
from app.schemas import CreateTweetRequest, CreateTweetResponse


class FakeTweetService:
    def create_tweet(self, payload: CreateTweetRequest) -> CreateTweetResponse:
        return CreateTweetResponse(tweet_id="123456789", tweet_text=payload.tweet_text)


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("SERVICE_BEARER_TOKEN", "test-service-token")
    get_settings.cache_clear()
    application = create_app()
    application.dependency_overrides[get_tweet_service] = FakeTweetService
    with TestClient(application) as test_client:
        yield test_client
    get_settings.cache_clear()


def test_health_is_available_without_session_credentials(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "twitter-bot-aod"}


def test_create_post_requires_the_service_token(client: TestClient) -> None:
    response = client.post("/api/v1/tweets", json={"tweet_text": "Ayat of The Day"})
    assert response.status_code == 401


def test_create_post_returns_the_contract_expected_by_aod(client: TestClient) -> None:
    response = client.post(
        "/api/v1/tweets",
        headers={"Authorization": "Bearer test-service-token"},
        json={"tweet_text": "Ayat of The Day"},
    )
    assert response.status_code == 201
    assert response.json() == {"tweet_id": "123456789", "tweet_text": "Ayat of The Day"}
