
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from app.db.base import SessionLocal
from app.db.crud import list_cars

router = Router()

@router.callback_query(F.data == "buyer")
async def buyer_enter(cb: CallbackQuery):
    await cb.message.edit_text("Напиши критерии: например `Kia Rio до 1 млн Калининград` — я пришлю подборку.")

@router.callback_query(F.data == "feed")
async def latest_feed(cb: CallbackQuery):
    async with SessionLocal() as s:
        cars = await list_cars(s, 5)
    if not cars:
        await cb.message.edit_text("Пока нет объявлений. Залей своё первым!")
        return
    text = "\n\n".join([f"{c.title} — {int(c.price):,} ₽, {c.region}" for c in cars])
    await cb.message.edit_text(text)
