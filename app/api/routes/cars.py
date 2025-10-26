
from fastapi import APIRouter, Depends, Query
from app.db.base import get_session, AsyncSession
from app.db.crud import list_cars
from typing import Optional

router = APIRouter(prefix="/cars", tags=["cars"])

@router.get("")
async def cars(limit: int = Query(10, le=50), session: AsyncSession = Depends(get_session)):
    return await list_cars(session, limit=limit)
