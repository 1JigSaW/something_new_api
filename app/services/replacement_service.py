from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.replacement_repo import ReplacementRepository
from app.repositories.user_repo import UserRepository


FREE_DAILY_REPLACEMENTS = 1


class ReplacementService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.repo = ReplacementRepository(session=session)
        self.user_repo = UserRepository(session=session)

    async def create_with_limit(
        self,
        user_id: int,
        from_item: str,
        to_item: str,
        today: date,
    ):
        count_today = await self.repo.count_for_day(user_id=user_id, d=today)
        if count_today >= FREE_DAILY_REPLACEMENTS:
            raise ValueError("daily_limit_exceeded")
        obj = await self.repo.create(user_id=user_id, from_item=from_item, to_item=to_item)
        await self.session.commit()
        return obj


