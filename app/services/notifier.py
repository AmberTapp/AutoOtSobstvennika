
from aiogram import Bot

async def notify_user(bot: Bot, tg_id: int, text: str, **kwargs):
    try:
        await bot.send_message(tg_id, text, **kwargs)
    except Exception as e:
        print("Notify error", e)
