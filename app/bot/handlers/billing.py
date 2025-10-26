
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.bot.keyboards import billing_kb
from app.core.config import get_settings
from app.services.payments.ton import TonGateway

router = Router()

@router.callback_query(F.data == "billing")
async def show_billing(cb: CallbackQuery):
    s = get_settings()
    gw = TonGateway(s.TON_WALLET, s.TON_API_BASE, s.TON_API_KEY)
    # Тестовый перерасчёт в TON (см. /api/payments/create для серверной логики)
    memo_basic = gw.create_memo(cb.from_user.id, "tier_basic")
    memo_pro = gw.create_memo(cb.from_user.id, "tier_pro")
    memo_boost = gw.create_memo(cb.from_user.id, "boost")

    # Допустим 1 TON = 350 RUB
    link_basic = gw.transfer_link(s.TIER_BASIC_RUB/350.0, memo_basic)
    link_pro = gw.transfer_link(s.TIER_PRO_RUB/350.0, memo_pro)
    link_boost = gw.transfer_link(s.BOOST_RUB/350.0, memo_boost)

    await cb.message.edit_text(
        "Премиум и бусты: выбери пакет и оплати через TON. После оплаты статус подтянется автоматически.",
        reply_markup=billing_kb(link_basic, link_pro, link_boost)
    )
