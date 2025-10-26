
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.db.base import SessionLocal
from app.db.crud import upsert_car_by_fingerprint
from app.services.assessor import assess_car
from json import dumps
import hashlib

router = Router()

class SellForm(StatesGroup):
    title = State()
    price = State()
    region = State()

@router.callback_query(F.data == "seller")
async def seller_enter(cb: CallbackQuery, state: FSMContext):
    await state.set_state(SellForm.title)
    await cb.message.edit_text("Как назовём объявление? Укажи марку/модель/год.")

@router.message(SellForm.title)
async def ask_price(msg: Message, state: FSMContext):
    await state.update_data(title=msg.text)
    await state.set_state(SellForm.price)
    await msg.answer("Цена в ₽?")

@router.message(SellForm.price)
async def ask_region(msg: Message, state: FSMContext):
    price = float(msg.text.replace(" ", "").replace(",", "."))
    await state.update_data(price=price)
    await state.set_state(SellForm.region)
    await msg.answer("Регион?")

@router.message(SellForm.region)
async def save_listing(msg: Message, state: FSMContext):
    data = await state.get_data()
    region = msg.text
    car = {
        "title": data["title"],
        "brand": data["title"].split()[0] if data["title"] else "",
        "model": (data["title"].split()[1] if len(data["title"].split())>1 else ""),
        "year": 0,
        "price": data["price"],
        "mileage": 0,
        "region": region,
        "vin": None,
        "description": "",
        "photos": None,
        "status": "published",
    }
    fp = hashlib.sha1(f"{car['title']}|{car['price']}|{car['region']}".lower().encode()).hexdigest()
    a = assess_car(car)
    car["score"] = a.score
    car["flags"] = dumps(a.flags, ensure_ascii=False)

    async with SessionLocal() as s:
        await upsert_car_by_fingerprint(s, fp, car)
    await state.clear()
    await msg.answer("Готово! Объявление опубликовано.")
