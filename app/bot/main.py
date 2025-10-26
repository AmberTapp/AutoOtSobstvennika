
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from app.core.config import get_settings
from app.core.logging import logger
from .handlers import start, seller, buyer, billing, admin, common

async def main():
    s = get_settings()
    bot = Bot(token=s.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(seller.router)
    dp.include_router(buyer.router)
    dp.include_router(billing.router)
    dp.include_router(admin.router)
    dp.include_router(common.router)

    logger.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
