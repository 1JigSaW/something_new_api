from datetime import date
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_activity_repo import UserActivityRepository, UserFavoriteRepository


class UserActivityService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.activity_repo = UserActivityRepository(session)
        self.favorite_repo = UserFavoriteRepository(session)

    async def track_swipe(self, user_id: int, challenge_id: int, direction: str) -> None:
        """Track a swipe action (left or right)"""
        activity_type = f"swipe_{direction}"
        await self.activity_repo.create_activity(user_id, activity_type, challenge_id)
        await self.session.commit()

    async def track_view(self, user_id: int, challenge_id: int) -> None:
        """Track when user views a challenge"""
        # Only track if not already viewed
        if not await self.activity_repo.is_challenge_viewed(user_id, challenge_id):
            await self.activity_repo.create_activity(user_id, "view", challenge_id)
            await self.session.commit()

    async def track_selection(self, user_id: int, challenge_id: int) -> None:
        """Track when user selects a challenge"""
        # Only track if not already selected
        if not await self.activity_repo.is_challenge_selected(user_id, challenge_id):
            await self.activity_repo.create_activity(user_id, "select", challenge_id)
            await self.session.commit()

    async def get_swipes_today(self, user_id: int, today: date) -> int:
        """Get number of swipes used today"""
        return await self.activity_repo.count_swipes_today(user_id, today)

    async def get_viewed_challenges(self, user_id: int) -> List[int]:
        """Get list of viewed challenge IDs"""
        return await self.activity_repo.get_viewed_challenges(user_id)

    async def get_selected_challenges(self, user_id: int) -> List[int]:
        """Get list of selected challenge IDs"""
        return await self.activity_repo.get_selected_challenges(user_id)

    async def is_challenge_viewed(self, user_id: int, challenge_id: int) -> bool:
        """Check if challenge was viewed"""
        return await self.activity_repo.is_challenge_viewed(user_id, challenge_id)

    async def is_challenge_selected(self, user_id: int, challenge_id: int) -> bool:
        """Check if challenge was selected"""
        return await self.activity_repo.is_challenge_selected(user_id, challenge_id)

    # Favorites methods
    async def add_favorite(self, user_id: int, challenge_id: int) -> bool:
        """Add challenge to favorites"""
        try:
            await self.favorite_repo.add_favorite(user_id, challenge_id)
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            return False

    async def remove_favorite(self, user_id: int, challenge_id: int) -> bool:
        """Remove challenge from favorites"""
        try:
            result = await self.favorite_repo.remove_favorite(user_id, challenge_id)
            await self.session.commit()
            return result
        except Exception:
            await self.session.rollback()
            return False

    async def get_favorites(self, user_id: int) -> List[int]:
        """Get list of favorite challenge IDs"""
        favorites = await self.favorite_repo.get_favorites(user_id)
        return [fav.challenge_id for fav in favorites]

    async def is_favorite(self, user_id: int, challenge_id: int) -> bool:
        """Check if challenge is in favorites"""
        return await self.favorite_repo.is_favorite(user_id, challenge_id)
