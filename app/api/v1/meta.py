from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.db.session import get_db_session
from app.models.meta import Category, Size, Tag


router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/filters")
async def meta_filters(session=Depends(get_db_session)):
    cats = (await session.execute(select(Category.name).order_by(Category.name))).scalars().all()
    sizes = (await session.execute(select(Size.name).order_by(Size.name))).scalars().all()
    tags = (await session.execute(select(Tag.name).order_by(Tag.name))).scalars().all()
    return {"categories": list(cats), "sizes": list(sizes), "tags": list(tags)}


