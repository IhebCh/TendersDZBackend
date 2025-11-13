from __future__ import annotations

import json
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "TenderFlow API"
    DATABASE_URL: str = "postgresql+psycopg2://postgres:admin@localhost:5432/tenderflow"
    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # Accept string, comma-separated string, JSON array, or "*"
    CORS_ORIGINS: List[str] | str = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "*", # for developement only
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def normalize_cors(cls, v):
        if v is None:
            return ["http://localhost:5173"]

        # Already a list
        if isinstance(v, list):
            return v

        # String input
        if isinstance(v, str):
            s = v.strip()
            # wildcard
            if s == "*":
                return ["*"]

            # JSON array
            if s.startswith("["):
                try:
                    arr = json.loads(s)
                    if isinstance(arr, list):
                        return [str(x).strip() for x in arr]
                except Exception:
                    # fall through to comma split
                    pass

            # Comma-separated or single value
            return [part.strip() for part in s.split(",") if part.strip()]

        # Fallback (unexpected types)
        return ["http://localhost:5173"]


settings = Settings()
