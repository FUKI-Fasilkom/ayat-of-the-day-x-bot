import bs4
import requests
from x_client_transaction import ClientTransaction
from x_client_transaction.utils import generate_headers, get_ondemand_file_url, handle_x_migration

from app.exceptions import BotConfigurationError

X_HOME_URL = "https://x.com"


def build_client_transaction(cookies: dict[str, str]) -> ClientTransaction:
    session = requests.Session()
    session.headers = generate_headers()  # type: ignore[assignment]
    session.cookies.update(cookies)

    handle_x_migration(session=session)
    home_response = session.get(X_HOME_URL, timeout=(5, 30))
    home_response.raise_for_status()
    home_page = bs4.BeautifulSoup(home_response.content, "html.parser")

    try:
        ondemand_file_url = get_ondemand_file_url(response=home_page)
    except AttributeError as exc:
        raise BotConfigurationError(
            "Could not construct an X transaction ID. The session cookies may be expired or invalid."
        ) from exc

    ondemand_response = session.get(ondemand_file_url, timeout=(5, 30))  # type: ignore[arg-type]
    ondemand_response.raise_for_status()
    return ClientTransaction(
        home_page_response=home_page,
        ondemand_file_response=bs4.BeautifulSoup(ondemand_response.content, "html.parser"),
    )

