
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.core.config import get_settings
from app.worker.tasks import ingest_region

router = Router()

@router.callback_query(F.data.startswith("admin:ingest:"))
async def admin_ingest(cb: CallbackQuery):
    user_id = cb.from_user.id
    if user_id not in get_settings().admins_list():
        await cb.answer("Нет доступа", show_alert=True)
        return
    region = cb.data.split(":")[-1]
    ingest_region.delay(region)
    await cb.message.answer(f"Запустил ingest региона: {region}")
