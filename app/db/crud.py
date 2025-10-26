
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, Car, Payment
from typing import Optional

async def get_or_create_user(session: AsyncSession, tg_id: int) -> User:
    res = await session.execute(select(User).where(User.tg_id == tg_id))
    user = res.scalars().first()
    if not user:
        user = User(tg_id=tg_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user

async def get_car_by_fingerprint(session: AsyncSession, fp: str) -> Optional[Car]:
    res = await session.execute(select(Car).where(Car.fingerprint == fp))
    return res.scalars().first()

async def upsert_car_by_fingerprint(session: AsyncSession, fp: str, data: dict) -> Car:
    car = await get_car_by_fingerprint(session, fp)
    if car:
        for k, v in data.items():
            if hasattr(car, k) and v is not None:
                setattr(car, k, v)
        await session.commit()
        await session.refresh(car)
        return car
    car = Car(**data, fingerprint=fp, status=data.get("status", "published"))
    session.add(car)
    await session.commit()
    await session.refresh(car)
    return car

async def list_cars(session: AsyncSession, limit=10):
    res = await session.execute(select(Car).where(Car.status=="published").order_by(Car.created_at.desc()).limit(limit))
    return res.scalars().all()

async def create_payment(session: AsyncSession, user_id: int, amount: float, memo: str) -> Payment:
    p = Payment(user_id=user_id, amount=amount, memo=memo, status="pending")
    session.add(p)
    await session.commit()
    await session.refresh(p)
    return p

async def mark_payment_paid(session: AsyncSession, payment_id: int):
    res = await session.execute(select(Payment).where(Payment.id == payment_id))
    p = res.scalars().first()
    if p:
        p.status = "paid"
        await session.commit()
        await session.refresh(p)
        return p
    return None
