from datetime import date, datetime, time, timezone

from sqlalchemy import and_, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.replacement import Replacement


def _day_bounds(d: date) -> tuple[datetime, datetime]:
    start = datetime.combine(d, time.min, tzinfo=timezone.utc)
    end = datetime.combine(d, time.max, tzinfo=timezone.utc)
    return start, end


class ReplacementRepository:
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
        stmt = select(func.count(Replacement.id)).where(
            and_(
                Replacement.user_id == user_id,
                Replacement.created_at >= start,
                Replacement.created_at <= end,
            )
        )
        res = await self.session.execute(stmt)
        return int(res.scalar_one() or 0)

    async def create(
        self,
        user_id: int,
        from_item: str,
        to_item: str,
    ) -> Replacement:
        obj = Replacement(user_id=user_id, from_item=from_item, to_item=to_item)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def list_for_period(
        self,
        user_id: int,
        date_from: date,
        date_to: date,
    ) -> list[Replacement]:
        start = datetime.combine(date_from, time.min, tzinfo=timezone.utc)
        end = datetime.combine(date_to, time.max, tzinfo=timezone.utc)
        stmt = (
            select(Replacement)
            .where(
                and_(
                    Replacement.user_id == user_id,
                    Replacement.created_at >= start,
                    Replacement.created_at <= end,
                )
            )
            .order_by(Replacement.created_at.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())


