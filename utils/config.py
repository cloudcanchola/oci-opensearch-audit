from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class OCISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True
    )

    TENANCY: str
    USER: str
    FINGERPRINT: str
    KEY_FILE: str
    REGION: str
    INGEST_URL: str


@lru_cache
def get_settings() -> OCISettings:
    return OCISettings()

