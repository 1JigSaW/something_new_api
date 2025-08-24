from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.challenge_completion_repo import ChallengeCompletionRepository


FREE_DAILY_CHALLENGES = 1


class ChallengeCompletionService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.repo = ChallengeCompletionRepository(session=session)

    async def complete_with_limit(
        self,
        user_id: int,
        challenge_id: int,
        today: date,
    ):
        count_today = await self.repo.count_for_day(user_id=user_id, d=today)
        if count_today >= FREE_DAILY_CHALLENGES:
            raise ValueError("daily_limit_exceeded")
        obj = await self.repo.create(user_id=user_id, challenge_id=challenge_id)
        await self.session.commit()
        return obj


