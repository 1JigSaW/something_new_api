import asyncio

from sqlalchemy.dialects.postgresql import insert

from app.core.settings import get_settings
from app.db.session import build_engine_and_sessionmaker
from app.models.challenge import Challenge


async def seed() -> None:
    settings = get_settings()
    engine, session_maker = build_engine_and_sessionmaker(
        database_url=(
            settings.database_url
            or "postgresql+asyncpg://postgres:postgres@localhost:5433/something_new"
        ),
    )
    async with session_maker() as session:
        values = [
            {
                "title": "10-minute walk",
                "short_description": "Go for a short mindful walk",
                "category": "movement",
                "tags": "walk,mindful",
                "size": "small",
                "estimated_duration_min": 10,
                "is_premium_only": False,
            },
            {
                "title": "5-minute breathing",
                "short_description": "Box breathing for 5 minutes",
                "category": "breath",
                "tags": "breath,relax",
                "size": "small",
                "estimated_duration_min": 5,
                "is_premium_only": False,
            },
        ]
        stmt = insert(Challenge).values(values).on_conflict_do_nothing(index_elements=["id"])
        await session.execute(stmt)
        await session.commit()


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()


