from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.db.session import get_db_session
from app.schemas.user import UserRead
from app.services.user_service import UserService
from app.api.deps.auth import get_current_user_id


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_me(
    x_user_email: str = Header(..., alias="X-User-Email"),
    session=Depends(get_db_session),
):
    if not x_user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    service = UserService(session=session)
    user = await service.get_or_create_by_email(email=x_user_email)
    return user


@router.get("/me-auth", response_model=UserRead)
async def read_me_auth(
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    service = UserService(session=session)
    user = await service.get_or_create_by_email(email=f"{user_id}@example.com")
    return user


