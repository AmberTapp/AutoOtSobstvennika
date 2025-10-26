
import os, re, hashlib, json, asyncio
from typing import List, Dict
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

PRICE_RE = re.compile(r"(\d[\d\s]{3,})\s*(?:₽|руб|руб\.|RUB)?", re.I)
YEAR_RE = re.compile(r"(20\d{2}|19\d{2})")
MILEAGE_RE = re.compile(r"(\d[\d\s]{2,})\s*(?:км|km)", re.I)

def _clean_digits(s: str) -> int:
    return int(re.sub(r"\D", "", s)) if s else 0

def _fingerprint(car: Dict) -> str:
    key = f"{car.get('brand','')}|{car.get('model','')}|{car.get('year','')}|{car.get('price','')}|{car.get('region','')}|{car.get('mileage','')}|{car.get('title','')}".lower()
    return hashlib.sha1(key.encode("utf-8")).hexdigest()

def _normalize_title(text: str) -> Dict:
    text = text or ""
    year = 0
    y = YEAR_RE.search(text)
    if y:
        year = int(y.group(1))
    parts = text.split()
    brand = parts[0] if parts else ""
    model = parts[1] if len(parts) > 1 else ""
    return {"brand": brand, "model": model, "year": year}

def _extract_price(text: str) -> int:
    m = PRICE_RE.search(text or "")
    return _clean_digits(m.group(1)) if m else 0

def _extract_mileage(text: str) -> int:
    m = MILEAGE_RE.search(text or "")
    return _clean_digits(m.group(1)) if m else 0

def normalize_post(msg_text: str, region: str) -> Dict:
    title = msg_text.splitlines()[0][:120] if msg_text else "Объявление"
    base = _normalize_title(title)
    price = _extract_price(msg_text)
    mileage = _extract_mileage(msg_text)
    car = {
        "title": title,
        "brand": base["brand"],
        "model": base["model"],
        "year": base["year"],
        "price": price,
        "mileage": mileage,
        "region": region,
        "vin": None,
        "description": msg_text[:2000] if msg_text else "",
        "photos": None,
        "status": "published",
    }
    car["fingerprint"] = _fingerprint(car)
    return car

def get_region_channels_map() -> Dict[str, List[str]]:
    env = os.environ
    channels = {}
    for k, v in env.items():
        if k.startswith("CHANNELS_") and v:
            region = k.replace("CHANNELS_", "").title()
            channels[region] = [x.strip() for x in v.strip('"').split(";") if x.strip()]
    return channels

async def harvest_region(region: str, limit_per_channel: int = 30) -> List[Dict]:
    api_id = int(os.getenv("TELEGRAM_API_ID", "0"))
    api_hash = os.getenv("TELEGRAM_API_HASH", "")
    session_str = os.getenv("TELEGRAM_SESSION", "")
    if not api_id or not api_hash or not session_str:
        raise RuntimeError("Telethon creds missing: TELEGRAM_API_ID/HASH/SESSION")

    channels_map = get_region_channels_map()
    channels = channels_map.get(region, [])
    if not channels:
        return []

    out: List[Dict] = []
    async with TelegramClient(StringSession(session_str), api_id, api_hash) as client:
        for ch in channels:
            try:
                async for msg in client.iter_messages(ch, limit=limit_per_channel):
                    if not msg or not (msg.message or msg.text):
                        continue
                    car = normalize_post(msg.message or msg.text, region=region)
                    out.append(car)
            except FloodWaitError as e:
                await asyncio.sleep(int(e.seconds) + 1)
            except Exception:
                continue
    return out
