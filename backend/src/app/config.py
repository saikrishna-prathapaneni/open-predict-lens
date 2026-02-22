"""App settings loaded from environment (backend.env or .env)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "trading-backend"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 9000
    log_level: str = "info"
    # SurrealDB
    surreal_url: str = "http://localhost:8000"
    surreal_user: str = "root"
    surreal_pass: str = "root"
    surreal_ns: str = "trading"
    surreal_db: str = "trading"
    api_key: str = "changeme"


settings = Settings()
