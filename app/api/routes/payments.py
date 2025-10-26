
from fastapi import APIRouter, Depends, Body
from app.core.security import require_api_secret
from app.core.config import get_settings
from app.services.payments.ton import TonGateway
from app.db.base import get_session, AsyncSession
from app.db.crud import create_payment, mark_payment_paid
import math, asyncio

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create", dependencies=[Depends(require_api_secret)])
async def create_payment_link(payload: dict = Body(...), session: AsyncSession = Depends(get_session)):
    s = get_settings()
    gw = TonGateway(s.TON_WALLET, s.TON_API_BASE, s.TON_API_KEY)
    user_id = int(payload["user_id"])
    rub = float(payload["amount_rub"])
    # В реальности нужен курс RUB/TON — здесь используем фикс (пример: 1 TON = 350 RUB)
    ton_rate = 350.0
    amount_ton = round(rub / ton_rate, 3)
    memo = gw.create_memo(user_id, kind=payload.get("kind","tier"))
    p = await create_payment(session, user_id=user_id, amount=amount_ton, memo=memo)
    link = gw.transfer_link(amount_ton, memo)
    return {"payment_id": p.id, "amount_ton": amount_ton, "memo": memo, "link": link}

@router.post("/check", dependencies=[Depends(require_api_secret)])
async def check_payment_status(payload: dict = Body(...), session: AsyncSession = Depends(get_session)):
    s = get_settings()
    gw = TonGateway(s.TON_WALLET, s.TON_API_BASE, s.TON_API_KEY)
    payment_id = int(payload["payment_id"])
    memo = payload["memo"]
    min_amount = float(payload.get("min_amount_ton", 0.0))
    ok = await gw.check_paid(memo, min_amount_ton=min_amount)
    if ok:
        await mark_payment_paid(session, payment_id)
    return {"paid": ok}
