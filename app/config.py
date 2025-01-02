from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    DB_PORT: int
    DB_HOST: str
    MODE: Optional[str] = "DEV"

    @property
    def DATABASE_URL_async(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        validate_default=False, env_file=".env", extra="allow"
    )

    def get_mode(self):
        return True if self.MODE == "DEV" else False


config = Config()
