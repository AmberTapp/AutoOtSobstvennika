
from .celery_app import celery
from app.services.parser_telegram import harvest_region
from app.services.assessor import assess_car
from app.db.base import SessionLocal
from app.db.crud import upsert_car_by_fingerprint
from json import dumps

@celery.task
def crawl_region(region: str) -> dict:
    import asyncio
    data = asyncio.run(harvest_region(region))
    return {"region": region, "found": len(data)}

@celery.task
def ingest_region(region: str) -> dict:
    import asyncio
    data = asyncio.run(harvest_region(region))
    saved = 0
    async def _save_all(items):
        nonlocal saved
        async with SessionLocal() as s:
            for car in items:
                a = assess_car(car)
                car["score"] = a.score
                car["flags"] = dumps(a.flags, ensure_ascii=False)
                fp = car.pop("fingerprint")
                await upsert_car_by_fingerprint(s, fp, car)
                saved += 1
    asyncio.run(_save_all(data))
    return {"region": region, "saved": saved}
