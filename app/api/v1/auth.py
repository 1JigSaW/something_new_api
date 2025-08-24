from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.db.session import get_db_session
from app.services.auth_service import AuthService
from app.core.security import create_access_token
from app.api.deps.auth import get_current_user_id


router = APIRouter(prefix="/auth", tags=["auth"])


class RequestCodeIn(BaseModel):
    email: EmailStr


class VerifyIn(BaseModel):
    email: EmailStr
    code: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/request-code", status_code=204)
async def request_code(
    payload: RequestCodeIn,
    session=Depends(get_db_session),
):
    service = AuthService(session=session)
    try:
        await service.request_code(email=payload.email)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@router.post("/verify", response_model=TokenOut)
async def verify(
    payload: VerifyIn,
    session=Depends(get_db_session),
):
    service = AuthService(session=session)
    try:
        token = await service.verify_code(email=payload.email, code=payload.code)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return TokenOut(access_token=token)


@router.post("/refresh", response_model=TokenOut)
async def refresh(
    user_id: int = Depends(get_current_user_id),
):
    token = create_access_token(subject=str(user_id))
    return TokenOut(access_token=token)


@router.post("/logout", status_code=204)
async def logout():
    return


