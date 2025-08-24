import asyncio

from sqlalchemy.dialects.postgresql import insert

from app.core.settings import get_settings
from app.db.session import build_engine_and_sessionmaker
from app.models.meta import Category, Size, Tag


async def seed() -> None:
    settings = get_settings()
    _, session_maker = build_engine_and_sessionmaker(
        database_url=(
            settings.database_url
            or "postgresql+asyncpg://postgres:postgres@localhost:5433/something_new"
        ),
    )
    async with session_maker() as session:
        cats = ["movement", "breath", "mindset", "nutrition"]
        sizes = ["small", "medium", "large"]
        tags = ["walk", "mindful", "relax", "hydrate"]

        await session.execute(insert(Category).values([{"name": n} for n in cats]).on_conflict_do_nothing(index_elements=["name"]))
        await session.execute(insert(Size).values([{"name": n} for n in sizes]).on_conflict_do_nothing(index_elements=["name"]))
        await session.execute(insert(Tag).values([{"name": n} for n in tags]).on_conflict_do_nothing(index_elements=["name"]))
        await session.commit()


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()


