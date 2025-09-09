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
            # Small challenges (5-30 min)
            {
                "title": "10-minute mindful walk",
                "short_description": "Go for a short walk and notice 5 things you've never seen before",
                "category": "movement",
                "tags": "walk,mindful,explore",
                "size": "small",
                "estimated_duration_min": 10,
                "is_premium_only": False,
            },
            {
                "title": "5-minute box breathing",
                "short_description": "Practice box breathing: 4 counts in, 4 hold, 4 out, 4 hold",
                "category": "breath",
                "tags": "breath,relax,focus",
                "size": "small",
                "estimated_duration_min": 5,
                "is_premium_only": False,
            },
            {
                "title": "15-minute journaling",
                "short_description": "Write about one thing you're grateful for today",
                "category": "mindset",
                "tags": "create,reflect,gratitude",
                "size": "small",
                "estimated_duration_min": 15,
                "is_premium_only": False,
            },
            {
                "title": "20-minute healthy snack prep",
                "short_description": "Prepare a healthy snack with ingredients you've never tried",
                "category": "nutrition",
                "tags": "create,explore,health",
                "size": "small",
                "estimated_duration_min": 20,
                "is_premium_only": False,
            },
            {
                "title": "25-minute doodle session",
                "short_description": "Draw whatever comes to mind for 25 minutes",
                "category": "creativity",
                "tags": "create,relax,express",
                "size": "small",
                "estimated_duration_min": 25,
                "is_premium_only": False,
            },
            
            # Medium challenges (30-90 min)
            {
                "title": "45-minute language lesson",
                "short_description": "Learn 10 new words in a language you're interested in",
                "category": "learning",
                "tags": "learn,expand,mind",
                "size": "medium",
                "estimated_duration_min": 45,
                "is_premium_only": False,
            },
            {
                "title": "60-minute social connection",
                "short_description": "Call someone you haven't spoken to in a while",
                "category": "social",
                "tags": "connect,reach,care",
                "size": "medium",
                "estimated_duration_min": 60,
                "is_premium_only": False,
            },
            {
                "title": "75-minute productivity boost",
                "short_description": "Organize your workspace and plan tomorrow's priorities",
                "category": "productivity",
                "tags": "focus,organize,plan",
                "size": "medium",
                "estimated_duration_min": 75,
                "is_premium_only": False,
            },
            {
                "title": "90-minute wellness routine",
                "short_description": "Create a personalized morning or evening wellness routine",
                "category": "wellness",
                "tags": "energy,health,balance",
                "size": "medium",
                "is_premium_only": False,
            },
            
            # Large challenges (2+ hours) - Premium only
            {
                "title": "3-hour creative project",
                "short_description": "Start and complete a creative project from scratch",
                "category": "creativity",
                "tags": "create,project,accomplish",
                "size": "large",
                "estimated_duration_min": 180,
                "is_premium_only": True,
            },
            {
                "title": "4-hour learning marathon",
                "short_description": "Deep dive into a topic you've always wanted to learn",
                "category": "learning",
                "tags": "learn,deep,expand",
                "size": "large",
                "estimated_duration_min": 240,
                "is_premium_only": True,
            },
            {
                "title": "5-hour adventure planning",
                "short_description": "Plan a weekend adventure or trip to a new place",
                "category": "adventure",
                "tags": "explore,plan,adventure",
                "size": "large",
                "estimated_duration_min": 300,
                "is_premium_only": True,
            },
        ]
        # Insert challenges one by one to handle nullable fields properly
        for challenge_data in values:
            stmt = insert(Challenge).values(challenge_data)
            await session.execute(stmt)
        await session.commit()


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()


