
import os, time, uuid, httpx
from typing import Optional

class TonGateway:
    """Простой шлюз: создаёт transfer-link для TonConnect/кошельков и проверяет входящие платежи по memo (comment)."""

    def __init__(self, wallet: str | None = None, api_base: str | None = None, api_key: str | None = None):
        self.wallet = wallet or os.getenv("TON_WALLET")
        self.api_base = api_base or os.getenv("TON_API_BASE", "https://toncenter.com/api/v3")
        self.api_key = api_key or os.getenv("TON_API_KEY")

    def create_memo(self, user_id: int, kind: str) -> str:
        return f"{kind}:{user_id}:{uuid.uuid4().hex[:8]}"

    def transfer_link(self, amount_ton: float, memo: str) -> str:
        # Универсальная ссылка для кошельков (TON DeepLink)
        # ton://transfer/<address>?amount=<nanoton>&text=<comment>
        nano = int(amount_ton * 1e9)
        from urllib.parse import quote
        return f"ton://transfer/{self.wallet}?amount={nano}&text={quote(memo)}"

    async def check_paid(self, memo: str, min_amount_ton: float = 0.0) -> bool:
        """Проверка входящих по адресу кошелька и комментарию.
        Реализовано через публичный REST (тонцентр/тон-апи). Требует API_KEY при необходимости."""
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        # На toncenter/tonapi схемы отличаются; здесь упрощённый пример через tonapi v2
        base = self.api_base.rstrip("/")
        async with httpx.AsyncClient(timeout=15) as client:
            # пример эндпоинта: /v2/blockchain/getTransactions?account=<addr>&limit=50
            url = f"{base}/v2/blockchain/getTransactions?account={self.wallet}&limit=50"
            r = await client.get(url, headers=headers)
            if r.status_code != 200:
                return False
            data = r.json()
            txs = data.get("transactions") or data.get("result") or []
            for tx in txs:
                cm = (tx.get("comment") or tx.get("in_msg", {}).get("message") or "") if isinstance(tx, dict) else ""
                if memo in cm:
                    # Проверим сумму (упрощённо)
                    amt = tx.get("amount") or tx.get("in_msg", {}).get("value")
                    try:
                        amt_ton = float(amt) / 1e9 if amt else 0.0
                    except Exception:
                        amt_ton = 0.0
                    if amt_ton >= min_amount_ton:
                        return True
            return False
