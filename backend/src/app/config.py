"""App settings loaded from environment (backend.env or .env)."""
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class KalshiSettings(BaseModel):
    """Kalshi API configuration."""
    api_key: str = "changeme"
    base_url: str = "https://api.elections.kalshi.com/trade-api/v2"
    markets_url: str = "https://api.elections.kalshi.com/trade-api/v2/markets"
    series_url: str = "https://api.elections.kalshi.com/trade-api/v2/series"
    timeout: float = 10.0

class PolymarketSettings(BaseModel):
    """Polymarket API configuration."""
    base_url: str = "https://gamma-api.polymarket.com"
    timeout: float = 10.0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
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
    # Kalshi API
    kalshi: KalshiSettings = KalshiSettings()
    # LLM configuration
    llm_provider: str = "ollama"
    # Ollama / LiteLLM
    ollama_model_name: str = "qwen3:0.6b"
    ollama_url: str = "http://localhost:11434/v1"

   

settings = Settings()
