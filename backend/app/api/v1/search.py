from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.security import get_current_user
from app.services.search_service import GlobalSearchService

router = APIRouter(prefix="/search", tags=["Global Search Platform"])


@router.get("/")
async def global_search(
    q: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await GlobalSearchService.global_search(db, q)
