from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def build_engine_and_sessionmaker(
    database_url: str,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(
        url=database_url,
        pool_pre_ping=True,
    )
    session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    return engine, session_maker


async def get_db_session(
    request: Request,
) -> AsyncIterator[AsyncSession]:
    session_maker: async_sessionmaker[AsyncSession] = request.app.state.db_sessionmaker
    async with session_maker() as session:
        yield session


