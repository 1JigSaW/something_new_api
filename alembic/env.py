from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.settings import get_settings
from app.db.base import Base


config = context.config


target_metadata = Base.metadata


def get_url() -> str:
    settings = get_settings()
    return settings.database_url or "postgresql+asyncpg://postgres:postgres@localhost:5433/something_new"


def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_sync_migrations(
    connection,
) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(
        url=get_url(),
        pool_pre_ping=True,
    )
    async with engine.begin() as connection:
        await connection.run_sync(
            fn=run_sync_migrations,
        )
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(
        main=run_migrations_online(),
    )


