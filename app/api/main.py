
from fastapi import FastAPI
from app.api.routes.cars import router as cars_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.payments import router as payments_router
from app.api.routes.users import router as users_router

app = FastAPI(title="CarBot API")

app.include_router(cars_router)
app.include_router(metrics_router)
app.include_router(payments_router)
app.include_router(users_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
