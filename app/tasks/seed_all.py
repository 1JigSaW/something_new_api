import asyncio

from app.tasks.seed_meta import seed as seed_meta
from app.tasks.seed_challenges import seed as seed_challenges
from app.core.settings import get_settings
from app.db.session import build_engine_and_sessionmaker
from sqlalchemy.dialects.postgresql import insert
from app.models.user import User
from app.models.replacement import Replacement
from app.models.challenge_completion import ChallengeCompletion


async def seed() -> None:
    # Ensure DB is reachable
    settings = get_settings()
    _, session_maker = build_engine_and_sessionmaker(
        database_url=(
            settings.database_url
            or "postgresql+asyncpg://postgres:postgres@localhost:5433/something_new"
        ),
    )

    # Meta + challenges
    await seed_meta()
    await seed_challenges()

    # Users + sample data
    async with session_maker() as session:
        # Upsert demo users
        demo_users = [
            {"email": "demo1@example.com"},
            {"email": "demo2@example.com"},
        ]
        await session.execute(
            insert(User)
            .values(demo_users)
            .on_conflict_do_nothing(index_elements=["email"])
        )
        await session.commit()

        # Fetch users ids
        users = (await session.execute(User.__table__.select())).all()
        if users:
            user_id = users[0][0]
            # One replacement and one completion for visibility
            await session.execute(
                insert(Replacement)
                .values(
                    {
                        "user_id": user_id,
                        "from_item": "coffee",
                        "to_item": "water",
                    }
                )
                .on_conflict_do_nothing(index_elements=["id"])
            )
            await session.execute(
                insert(ChallengeCompletion)
                .values(
                    {
                        "user_id": user_id,
                        "challenge_id": 1,
                    }
                )
                .on_conflict_do_nothing(index_elements=["id"])
            )
            await session.commit()


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()


