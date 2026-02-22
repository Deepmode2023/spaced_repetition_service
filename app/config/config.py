import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler("monitor.logs", maxBytes=5000000, backupCount=3)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.ERROR)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class GlobalConfig(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    DB_PORT: int
    DB_HOST: str
    MODE: Optional[str] = "DEV"
    AUTH_MARKER: str

    @property
    def DATABASE_URL_async(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        validate_default=False,
        env_file=f"{os.getcwd()}/app/config/.env",
        extra="allow",
    )

    def is_dev(self):
        return True if self.MODE == "DEV" else False


global_config = GlobalConfig()
