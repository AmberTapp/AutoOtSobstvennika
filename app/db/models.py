
from sqlalchemy import String, Integer, BigInteger, ForeignKey, DateTime, Float, Text, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    role: Mapped[str] = mapped_column(String(20), default="user")
    region: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    premium_until: Mapped[datetime | None]

    cars = relationship("Car", back_populates="owner")

class Car(Base):
    __tablename__ = "cars"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(120))
    brand: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    year: Mapped[int]
    price: Mapped[float]
    mileage: Mapped[int]
    region: Mapped[str]
    vin: Mapped[str | None] = mapped_column(String(32))
    description: Mapped[str | None] = mapped_column(Text())
    photos: Mapped[str | None] = mapped_column(Text())
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft|published|sold|blocked
    score: Mapped[float] = mapped_column(Float, default=0)
    flags: Mapped[str | None] = mapped_column(Text())
    fingerprint: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="cars")

class BuyerProfile(Base):
    __tablename__ = "buyer_profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    regions: Mapped[str | None]  # JSON
    brands: Mapped[str | None]
    budget_min: Mapped[float | None]
    budget_max: Mapped[float | None]
    body_types: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class EventLog(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50))
    payload: Mapped[str | None] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[float]
    currency: Mapped[str] = mapped_column(String(10), default="TON")
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending|paid|failed
    memo: Mapped[str | None]  # comment/tag used for TON transfer
    payload: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

Index("ux_car_fingerprint", Car.fingerprint, unique=True)
