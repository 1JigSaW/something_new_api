from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import configure_logging, get_logger
from app.core.sentry import init_sentry
from app.core.settings import get_settings
from app.db.session import build_engine_and_sessionmaker
from app.api.router import api_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns
    -------
    FastAPI
        Configured FastAPI application instance.
    """
    settings = get_settings()
    configure_logging(level="INFO" if not settings.debug else "DEBUG")
    init_sentry(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
    )

    application = FastAPI(
        title="Something New API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    application.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(
        router=api_router,
        prefix="/api",
    )

    application.include_router(
        router=api_router,
        prefix="/api/v1",
    )

    db_engine, db_sessionmaker = build_engine_and_sessionmaker(
        database_url=(
            settings.database_url
            or "postgresql+asyncpg://postgres:postgres@localhost:5433/something_new"
        ),
    )
    application.state.db_engine = db_engine
    application.state.db_sessionmaker = db_sessionmaker

    @application.get("/health", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        logger = get_logger("health")
        logger.info("healthcheck")
        return {"status": "ok"}

    return application


app = create_app()
