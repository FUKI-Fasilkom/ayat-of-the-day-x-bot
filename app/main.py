import logging

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.auth import require_service_token
from app.config import get_settings
from app.dependencies import get_tweet_service
from app.exceptions import BotConfigurationError, XPostError
from app.schemas import CreateTweetRequest, CreateTweetResponse, ErrorResponse
from app.tweet_service import TweetService

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="Dedicated X posting service for Ayat of The Day.",
    )

    @application.exception_handler(BotConfigurationError)
    async def configuration_error(
        _request: Request,
        exception: BotConfigurationError,
    ) -> JSONResponse:
        logger.error("Twitter bot configuration error: %s", exception)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(detail=str(exception)).model_dump(),
        )

    @application.exception_handler(XPostError)
    async def posting_error(_request: Request, exception: XPostError) -> JSONResponse:
        logger.warning("X posting failed: %s", exception)
        return JSONResponse(
            status_code=502,
            content=ErrorResponse(detail=str(exception)).model_dump(),
        )

    @application.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "twitter-bot-aod"}

    @application.post(
        "/api/v1/tweets",
        response_model=CreateTweetResponse,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(require_service_token)],
    )
    def create_tweet(
        payload: CreateTweetRequest,
        service: TweetService = Depends(get_tweet_service),
    ) -> CreateTweetResponse:
        return service.create_tweet(payload)

    return application


app = create_app()

