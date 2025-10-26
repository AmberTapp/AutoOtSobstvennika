
from fastapi import Header, HTTPException
from app.core.config import get_settings

async def require_api_secret(x_api_secret: str = Header(default="")):
    if x_api_secret != get_settings().API_SECRET:
        raise HTTPException(401, "Unauthorized")
