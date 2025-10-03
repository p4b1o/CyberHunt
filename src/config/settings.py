import json
import os
from pydantic import BaseModel


class AppSettings(BaseModel):
    log_level: str = "INFO"
    hunter_api_key: str | None = None
    reconng_api_keys: dict[str, str] = {}


def load_settings() -> AppSettings:
    log_level = os.getenv("LOG_LEVEL", "INFO")
    hunter_api_key = os.getenv("HUNTER_API_KEY")
    reconng_api_keys_raw = os.getenv("RECONNG_API_KEYS", "{}")
    try:
        reconng_api_keys = json.loads(reconng_api_keys_raw) if reconng_api_keys_raw else {}
        if not isinstance(reconng_api_keys, dict):
            reconng_api_keys = {}
    except Exception:
        reconng_api_keys = {}
    return AppSettings(
        log_level=log_level,
        hunter_api_key=hunter_api_key,
        reconng_api_keys=reconng_api_keys,
    )


settings = load_settings()


