from datetime import date, datetime, time, timezone
from typing import List

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_activity import UserActivity, UserFavorite


def _day_bounds(d: date) -> tuple[datetime, datetime]:
    start = datetime.combine(d, time.min, tzinfo=timezone.utc)
    end = datetime.combine(d, time.max, tzinfo=timezone.utc)
    return start, end


class UserActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_activity(
        self,
        user_id: int,
        activity_type: str,
        challenge_id: int,
    ) -> UserActivity:
        obj = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            challenge_id=challenge_id
        )
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def count_swipes_today(self, user_id: int, today: date) -> int:
        start, end = _day_bounds(today)
        stmt = select(func.count(UserActivity.id)).where(
            and_(
                UserActivity.user_id == user_id,
                UserActivity.activity_type.in_(['swipe_left', 'swipe_right']),
                UserActivity.created_at >= start,
                UserActivity.created_at <= end,
            )
        )
        res = await self.session.execute(stmt)
        return int(res.scalar_one() or 0)

    async def get_viewed_challenges(self, user_id: int) -> List[int]:
        stmt = select(UserActivity.challenge_id).where(
            and_(
                UserActivity.user_id == user_id,
                UserActivity.activity_type == 'view'
            )
        ).distinct()
        res = await self.session.execute(stmt)
        return [row[0] for row in res.fetchall()]

    async def get_selected_challenges(self, user_id: int) -> List[int]:
        stmt = select(UserActivity.challenge_id).where(
            and_(
                UserActivity.user_id == user_id,
                UserActivity.activity_type == 'select'
            )
        ).distinct()
        res = await self.session.execute(stmt)
        return [row[0] for row in res.fetchall()]

    async def is_challenge_viewed(self, user_id: int, challenge_id: int) -> bool:
        stmt = select(UserActivity.id).where(
            and_(
                UserActivity.user_id == user_id,
                UserActivity.challenge_id == challenge_id,
                UserActivity.activity_type == 'view'
            )
        ).limit(1)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None

    async def is_challenge_selected(self, user_id: int, challenge_id: int) -> bool:
        stmt = select(UserActivity.id).where(
            and_(
                UserActivity.user_id == user_id,
                UserActivity.challenge_id == challenge_id,
                UserActivity.activity_type == 'select'
            )
        ).limit(1)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None


class UserFavoriteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_favorite(self, user_id: int, challenge_id: int) -> UserFavorite:
        # Check if already exists
        existing = await self.get_favorite(user_id, challenge_id)
        if existing:
            return existing
            
        obj = UserFavorite(user_id=user_id, challenge_id=challenge_id)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def remove_favorite(self, user_id: int, challenge_id: int) -> bool:
        stmt = select(UserFavorite).where(
            and_(
                UserFavorite.user_id == user_id,
                UserFavorite.challenge_id == challenge_id
            )
        )
        res = await self.session.execute(stmt)
        favorite = res.scalar_one_or_none()
        
        if favorite:
            await self.session.delete(favorite)
            return True
        return False

    async def get_favorites(self, user_id: int) -> List[UserFavorite]:
        stmt = select(UserFavorite).where(
            UserFavorite.user_id == user_id
        ).order_by(UserFavorite.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_favorite(self, user_id: int, challenge_id: int) -> UserFavorite | None:
        stmt = select(UserFavorite).where(
            and_(
                UserFavorite.user_id == user_id,
                UserFavorite.challenge_id == challenge_id
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def is_favorite(self, user_id: int, challenge_id: int) -> bool:
        favorite = await self.get_favorite(user_id, challenge_id)
        return favorite is not None
