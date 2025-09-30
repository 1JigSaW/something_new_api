from datetime import datetime, timezone
import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Header
import httpx
from pydantic import BaseModel, EmailStr

from app.db.session import get_db_session
from app.services.auth_service import AuthService
from app.core.security import create_access_token, create_refresh_token, blacklist_token
from app.core.settings import get_settings
from app.api.deps.auth import get_current_user_id
from app.repositories.user_repo import UserRepository


router = APIRouter(prefix="/auth", tags=["auth"])


class RequestCodeIn(BaseModel):
    email: EmailStr


class VerifyIn(BaseModel):
    email: EmailStr
    code: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None


class RefreshIn(BaseModel):
    refresh_token: str


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
    settings = get_settings()
    sub = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]).get("sub")
    refresh = create_refresh_token(subject=str(sub))
    return TokenOut(access_token=token, refresh_token=refresh)


@router.post("/refresh", response_model=TokenOut)
async def refresh(
    payload: RefreshIn,
):
    settings = get_settings()
    try:
        data = jwt.decode(payload.refresh_token, settings.jwt_refresh_secret, algorithms=[settings.jwt_algorithm])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access = create_access_token(subject=str(data.get("sub")))
    return TokenOut(access_token=access)


@router.post("/logout", status_code=204)
async def logout(
    user_id: int = Depends(get_current_user_id),
    authorization: str = Header(..., alias="Authorization"),
):
    settings = get_settings()
    token = authorization.split(" ", 1)[1]
    data = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    issued_at = int(data.get("iat"))
    exp = int(data.get("exp"))
    ttl = max(0, exp - int(datetime.now(timezone.utc).timestamp()))
    blacklist_token(jti=str(issued_at), ttl_seconds=ttl)
    return


@router.get("/me")
async def me(
    user_id: int = Depends(get_current_user_id),
):
    return {"user": {"id": user_id}}


class LoginIn(BaseModel):
    provider: str
    id_token: str


@router.post("/login")
async def login(
    payload: LoginIn,
    session=Depends(get_db_session),
):
    if payload.provider != "google":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported provider")

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": payload.id_token})
    if resp.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid id_token")

    token_info = resp.json()
    email = token_info.get("email")
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found in token")

    user_repo = UserRepository(session=session)
    user = await user_repo.create_if_not_exists(email=email)
    # Persist the user so that subsequent requests (new DB sessions)
    # can reference the row (avoids FK violations on completions)
    await session.commit()

    access = create_access_token(subject=str(user.id))
    refresh = create_refresh_token(subject=str(user.id))

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "provider": "google",
        },
        "tokens": {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "Bearer",
            "expires_in": 3600,
        },
    }


