from datetime import date
from fastapi import Query

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.auth import get_current_user_id
from app.db.session import get_db_session
from app.schemas.replacement import ReplacementCreate, ReplacementRead
from app.services.replacement_service import ReplacementService
from app.repositories.replacement_repo import ReplacementRepository


router = APIRouter(prefix="/replacements", tags=["replacements"])


@router.post("/", response_model=ReplacementRead, status_code=201)
async def create_replacement(
    payload: ReplacementCreate,
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    service = ReplacementService(session=session)
    try:
        obj = await service.create_with_limit(
            user_id=user_id,
            from_item=payload.from_item,
            to_item=payload.to_item,
            today=date.today(),
        )
        return obj
    except ValueError:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@router.get("/", response_model=list[ReplacementRead])
async def list_replacements(
    date_from: date = Query(...),
    date_to: date = Query(...),
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    repo = ReplacementRepository(session=session)
    items = await repo.list_for_period(user_id=user_id, date_from=date_from, date_to=date_to)
    return items


