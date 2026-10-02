from threading import Lock
from typing import Any

from app.config import Settings
from app.exceptions import BotConfigurationError


class TwitterClientProvider:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client: Any | None = None
        self._lock = Lock()

    def get_client(self) -> Any:
        if self._client is None:
            with self._lock:
                if self._client is None:
                    self._client = self._build_client()
        return self._client

    def _build_client(self) -> Any:
        from twitter_openapi_python import TwitterOpenapiPython
        from twitter_openapi_python import client as twitter_openapi_client

        from app.openapi_patches import relax_null_lists
        from app.transaction_id import build_client_transaction

        cookies = self._load_cookies()
        relax_null_lists()

        client = TwitterOpenapiPython()
        platform_header = f'"{self.settings.twitter_platform_header}"'
        client.additional_api_headers = {"sec-ch-ua-platform": platform_header}
        client.additional_browser_headers = {"sec-ch-ua-platform": platform_header}
        twitter_openapi_client.get_tid = lambda: build_client_transaction(cookies)
        return client.get_client_from_cookies(cookies=cookies)

    def _load_cookies(self) -> dict[str, str]:
        if not self.settings.twitter_auth_token or not self.settings.twitter_ct0:
            raise BotConfigurationError(
                "TWITTER_AUTH_TOKEN and TWITTER_CT0 must be configured for posting."
            )
        return {
            "auth_token": self.settings.twitter_auth_token,
            "ct0": self.settings.twitter_ct0,
        }

