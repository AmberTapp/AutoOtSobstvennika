
from fastapi import APIRouter, Depends, Body
from app.db.base import get_session, AsyncSession
from sqlalchemy import select
from app.db.models import BuyerProfile, User
from datetime import datetime, timedelta

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/buyer-profile")
async def save_buyer_profile(payload: dict = Body(...), session: AsyncSession = Depends(get_session)):
    uid = int(payload["user_id"])
    res = await session.execute(select(BuyerProfile).where(BuyerProfile.user_id == uid))
    bp = res.scalars().first()
    data = dict(
        regions=payload.get("regions"),
        brands=payload.get("brands"),
        budget_min=payload.get("budget_min"),
        budget_max=payload.get("budget_max"),
        body_types=payload.get("body_types"),
    )
    if not bp:
        bp = BuyerProfile(user_id=uid, **data)
        session.add(bp)
    else:
        for k, v in data.items():
            setattr(bp, k, v)
    await session.commit()
    await session.refresh(bp)
    return {"ok": True}

@router.post("/grant-premium")
async def grant_premium(payload: dict = Body(...), session: AsyncSession = Depends(get_session)):
    uid = int(payload["user_id"])
    days = int(payload.get("days", 30))
    res = await session.execute(select(User).where(User.tg_id == uid))
    u = res.scalars().first()
    if not u:
        return {"ok": False, "error": "user not found"}
    u.premium_until = datetime.utcnow() + timedelta(days=days)
    await session.commit()
    return {"ok": True, "premium_until": u.premium_until.isoformat()}
