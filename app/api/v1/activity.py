from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.api.deps.auth import get_current_user_id
from app.db.session import get_db_session
from app.services.user_activity_service import UserActivityService

router = APIRouter(prefix="/activity", tags=["activity"])


class SwipeRequest(BaseModel):
    challenge_id: int
    direction: str  # "left" or "right"


class ViewRequest(BaseModel):
    challenge_id: int


class SelectionRequest(BaseModel):
    challenge_id: int


class FavoriteRequest(BaseModel):
    challenge_id: int


@router.post("/swipe")
async def track_swipe(
    request: SwipeRequest,
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    """Track a swipe action"""
    if request.direction not in ["left", "right"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Direction must be 'left' or 'right'"
        )
    
    service = UserActivityService(session=session)
    await service.track_swipe(user_id, request.challenge_id, request.direction)
    return {"message": "Swipe tracked successfully"}


@router.post("/view")
async def track_view(
    request: ViewRequest,
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    """Track when user views a challenge"""
    service = UserActivityService(session=session)
    await service.track_view(user_id, request.challenge_id)
    return {"message": "View tracked successfully"}


@router.post("/select")
async def track_selection(
    request: SelectionRequest,
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    """Track when user selects a challenge"""
    service = UserActivityService(session=session)
    await service.track_selection(user_id, request.challenge_id)
    return {"message": "Selection tracked successfully"}


@router.post("/favorite")
async def add_favorite(
    request: FavoriteRequest,
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    """Add challenge to favorites"""
    service = UserActivityService(session=session)
    success = await service.add_favorite(user_id, request.challenge_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add to favorites"
        )
    
    return {"message": "Added to favorites successfully"}


@router.delete("/favorite/{challenge_id}")
async def remove_favorite(
    challenge_id: int,
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    """Remove challenge from favorites"""
    service = UserActivityService(session=session)
    success = await service.remove_favorite(user_id, challenge_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    return {"message": "Removed from favorites successfully"}


@router.get("/favorites")
async def get_favorites(
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    """Get user's favorite challenges"""
    service = UserActivityService(session=session)
    favorites = await service.get_favorites(user_id)
    return {"favorites": favorites}


@router.get("/viewed")
async def get_viewed_challenges(
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    """Get list of viewed challenge IDs"""
    service = UserActivityService(session=session)
    viewed = await service.get_viewed_challenges(user_id)
    return {"viewed": viewed}


@router.get("/selected")
async def get_selected_challenges(
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    """Get list of selected challenge IDs"""
    service = UserActivityService(session=session)
    selected = await service.get_selected_challenges(user_id)
    return {"selected": selected}


@router.get("/swipes/today")
async def get_swipes_today(
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    """Get number of swipes used today"""
    from datetime import date
    service = UserActivityService(session=session)
    swipes = await service.get_swipes_today(user_id, date.today())
    return {"swipes_today": swipes}
