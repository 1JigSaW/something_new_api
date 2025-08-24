from datetime import date, datetime, time, timezone

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge_completion import ChallengeCompletion


def _day_bounds(d: date) -> tuple[datetime, datetime]:
    start = datetime.combine(d, time.min, tzinfo=timezone.utc)
    end = datetime.combine(d, time.max, tzinfo=timezone.utc)
    return start, end


class ChallengeCompletionRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def count_for_day(
        self,
        user_id: int,
        d: date,
    ) -> int:
        start, end = _day_bounds(d)
        stmt = select(func.count(ChallengeCompletion.id)).where(
            and_(
                ChallengeCompletion.user_id == user_id,
                ChallengeCompletion.created_at >= start,
                ChallengeCompletion.created_at <= end,
            )
        )
        res = await self.session.execute(stmt)
        return int(res.scalar_one() or 0)

    async def create(
        self,
        user_id: int,
        challenge_id: int,
    ) -> ChallengeCompletion:
        obj = ChallengeCompletion(user_id=user_id, challenge_id=challenge_id)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def list_for_period(
        self,
        user_id: int,
        date_from: date,
        date_to: date,
    ) -> list[ChallengeCompletion]:
        start = datetime.combine(date_from, time.min, tzinfo=timezone.utc)
        end = datetime.combine(date_to, time.max, tzinfo=timezone.utc)
        stmt = (
            select(ChallengeCompletion)
            .where(
                and_(
                    ChallengeCompletion.user_id == user_id,
                    ChallengeCompletion.created_at >= start,
                    ChallengeCompletion.created_at <= end,
                )
            )
            .order_by(ChallengeCompletion.created_at.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())


