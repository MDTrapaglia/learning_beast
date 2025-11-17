"""Application configuration for the Learning Beast backend."""
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Simple configuration object."""

    app_name: str = "Learning Beast API"
    version: str = "0.1.0"
    allowed_origins: List[str] = ["http://localhost", "http://localhost:5173"]
    data_dir: Path = Path(__file__).resolve().parent.parent / "data"
    session_ttl_minutes: int = 90

    class Config:
        env_prefix = "LEARNING_BEAST_"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings to avoid reparsing the environment."""

    return Settings()
