
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.bot.keyboards import main_menu

router = Router()

@router.message(F.text == "/start")
async def start(msg: Message):
    await msg.answer("Привет! Я помогу продать или найти авто от собственника.", reply_markup=main_menu())
