from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Header, Query, status
from pydantic import BaseModel
from sqlalchemy import and_, delete, or_, select, update

from app.core.settings import get_settings
from app.db.session import get_db_session
from app.models.challenge import Challenge
from app.models.meta import Category, Size, Tag
from app.schemas.challenge import ChallengeCreate, ChallengeRead
from app.tasks.seed_challenges import seed as seed_challenges
from app.tasks.seed_meta import seed as seed_meta


router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(
    x_admin_token: str = Header(None, alias="X-Admin-Token"),
):
    settings = get_settings()
    # В режиме разработки не требуем токен
    if settings.environment == "dev" and settings.debug:
        return
    # В продакшене требуем токен
    if not settings.admin_token or x_admin_token != settings.admin_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/challenges", response_model=ChallengeRead, dependencies=[Depends(require_admin)])
async def create_challenge(
    payload: ChallengeCreate,
    session=Depends(get_db_session),
):
    obj = Challenge(
        title=payload.title,
        short_description=payload.short_description,
        category=payload.category,
        tags=payload.tags,
        size=payload.size,
        estimated_duration_min=payload.estimated_duration_min,
        is_premium_only=payload.is_premium_only,
    )
    session.add(obj)
    await session.flush()
    await session.commit()
    return obj


@router.delete("/challenges/{challenge_id}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_challenge(
    challenge_id: int,
    session=Depends(get_db_session),
):
    await session.execute(delete(Challenge).where(Challenge.id == challenge_id))
    await session.commit()
    return


class ChallengeUpdate(BaseModel):
    title: str | None = None
    short_description: str | None = None
    category: str | None = None
    tags: str | None = None
    size: str | None = None
    estimated_duration_min: int | None = None
    is_premium_only: bool | None = None


@router.get("/challenges", response_model=list[ChallengeRead], dependencies=[Depends(require_admin)])
async def list_challenges_admin(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    q: str | None = Query(default=None),
    category: str | None = Query(default=None),
    size: str | None = Query(default=None),
    premium_only: bool | None = Query(default=None),
    session=Depends(get_db_session),
):
    stmt = select(Challenge)
    conds = []
    if q:
        like = f"%{q}%"
        conds.append(or_(Challenge.title.ilike(like), Challenge.short_description.ilike(like)))
    if category:
        conds.append(Challenge.category == category)
    if size:
        conds.append(Challenge.size == size)
    if premium_only is not None:
        conds.append(Challenge.is_premium_only.is_(premium_only))
    if conds:
        stmt = stmt.where(and_(*conds))
    stmt = stmt.order_by(Challenge.id.desc()).limit(limit).offset(offset)
    rows = await session.execute(stmt)
    return list(rows.scalars().all())


@router.patch("/challenges/{challenge_id}", response_model=ChallengeRead, dependencies=[Depends(require_admin)])
async def update_challenge(
    challenge_id: int,
    payload: ChallengeUpdate,
    session=Depends(get_db_session),
):
    data = {k: v for k, v in payload.dict().items() if v is not None}
    if not data:
        row = await session.execute(select(Challenge).where(Challenge.id == challenge_id))
        obj = row.scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return obj
    await session.execute(update(Challenge).where(Challenge.id == challenge_id).values(**data))
    await session.commit()
    row = await session.execute(select(Challenge).where(Challenge.id == challenge_id))
    obj = row.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return obj


@router.get("/meta", dependencies=[Depends(require_admin)])
async def list_meta(
    session=Depends(get_db_session),
):
    cats = (await session.execute(select(Category))).scalars().all()
    sizes = (await session.execute(select(Size))).scalars().all()
    tags = (await session.execute(select(Tag))).scalars().all()
    return {
        "categories": [{"id": c.id, "name": c.name} for c in cats],
        "sizes": [{"id": s.id, "name": s.name} for s in sizes],
        "tags": [{"id": t.id, "name": t.name} for t in tags],
    }


class MetaCreate(BaseModel):
    name: str


def _meta_model(kind: str):
    mapping = {"categories": Category, "sizes": Size, "tags": Tag}
    if kind not in mapping:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return mapping[kind]


@router.post("/meta/{kind}", dependencies=[Depends(require_admin)])
async def create_meta(
    kind: str,
    payload: MetaCreate,
    session=Depends(get_db_session),
):
    Model = _meta_model(kind)
    obj = Model(name=payload.name)
    session.add(obj)
    await session.flush()
    await session.commit()
    return {"id": obj.id, "name": obj.name}


@router.delete("/meta/{kind}/{item_id}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_meta(
    kind: str,
    item_id: int,
    session=Depends(get_db_session),
):
    Model = _meta_model(kind)
    await session.execute(delete(Model).where(Model.id == item_id))
    await session.commit()
    return


@router.post("/seed/challenges", status_code=202, dependencies=[Depends(require_admin)])
async def admin_seed_challenges():
    await seed_challenges()
    return {"status": "ok"}


@router.post("/seed/meta", status_code=202, dependencies=[Depends(require_admin)])
async def admin_seed_meta():
    await seed_meta()
    return {"status": "ok"}


@router.get("/users", dependencies=[Depends(require_admin)])
async def list_users(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session=Depends(get_db_session),
):
    from app.models.user import User
    stmt = select(User).order_by(User.created_at.desc()).limit(limit).offset(offset)
    rows = await session.execute(stmt)
    users = list(rows.scalars().all())
    
    return [
        {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "premium_until": user.premium_until.isoformat() if user.premium_until else None,
            "replacements_count_today": user.replacements_count_today,
            "challenges_count_today": user.challenges_count_today,
            "last_seen": user.last_seen.isoformat() if user.last_seen else None,
            "created_at": user.created_at.isoformat(),
        }
        for user in users
    ]

