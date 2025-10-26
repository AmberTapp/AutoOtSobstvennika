
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from app.db.base import get_session, AsyncSession
from app.db.models import Car

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/summary")
async def summary(session: AsyncSession = Depends(get_session)):
    total = (await session.execute(select(func.count()).select_from(Car))).scalar() or 0
    avg_price = (await session.execute(select(func.avg(Car.price)).where(Car.price > 0))).scalar()
    return {"total_cars": total, "avg_price": float(avg_price) if avg_price else 0.0}

@router.get("/top-brands")
async def top_brands(limit: int = 10, session: AsyncSession = Depends(get_session)):
    q = select(Car.brand, func.count().label("cnt")).group_by(Car.brand).order_by(func.count().desc()).limit(limit)
    rows = (await session.execute(q)).all()
    return [{"brand": b or "?", "count": int(c)} for b, c in rows]

@router.get("/regions")
async def regions(session: AsyncSession = Depends(get_session)):
    q = select(Car.region, func.count().label("cnt")).group_by(Car.region).order_by(func.count().desc())
    rows = (await session.execute(q)).all()
    return [{"region": r or "?", "count": int(c)} for r, c in rows]
