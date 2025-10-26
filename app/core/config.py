
from pydantic import BaseModel
from functools import lru_cache
import os

class Settings(BaseModel):
    BOT_TOKEN: str
    ADMINS: str = ""
    DATABASE_URL: str
    REDIS_URL: str
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_SECRET: str
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    TELEGRAM_API_ID: int | None = None
    TELEGRAM_API_HASH: str | None = None
    TELEGRAM_SESSION: str | None = None

    TON_WALLET: str | None = None
    TON_API_BASE: str | None = None
    TON_API_KEY: str | None = None

    TIER_BASIC_RUB: int = 299
    TIER_PRO_RUB: int = 799
    BOOST_RUB: int = 99

    def admins_list(self) -> list[int]:
        return [int(x) for x in self.ADMINS.split(",") if x]

@lru_cache()
def get_settings() -> Settings:
    return Settings(**{k: v for k, v in os.environ.items()})
