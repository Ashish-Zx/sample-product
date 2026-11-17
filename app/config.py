import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    # In a real deployment this would point at Postgres.
    database_url: str = "sqlite:///./orders.db"
    # E-commerce catalog / promo flags.
    promo_engine_enabled: bool = True
    default_currency: str = "USD"


settings = Settings()
