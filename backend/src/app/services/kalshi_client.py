import httpx
from typing import Optional, Dict, Any, List

from app.config import settings

_kalshi = settings.kalshi

async def fetch_market(ticker: str) -> dict:
    """Fetch market data for a given ticker from Kalshi API."""
    async with httpx.AsyncClient(timeout=_kalshi.timeout) as client:
        resp = await client.get(
            f"{_kalshi.markets_url}/{ticker}"
        )
        resp.raise_for_status()
        return resp.json().get("market", {})
    
async def list_markets(limit: int = 10) -> list:
    """List all available markets from Kalshi API."""
    async with httpx.AsyncClient(timeout=_kalshi.timeout) as client:
        resp = await client.get(f"{_kalshi.markets_url}?limit={limit}")
        resp.raise_for_status()
        return resp.json().get("markets", [])

async def list_series(
    limit: int = 10,
    status: str | None = None,   # filter by series status
    category: str | None = None, # e.g. "economics", "climate", "technology"
) -> list:
    """Fetch all available series from Kalshi. No auth required."""
    params: Dict[str, Any] = {"limit": limit}
    if status is not None:
        params["status"] = status
    if category is not None:
        params["category"] = category

    async with httpx.AsyncClient(timeout=_kalshi.timeout) as client:
        resp = await client.get(
            _kalshi.series_url,
            params=params
        )
        resp.raise_for_status()
        return resp.json().get("series", [])

    
async def get_series(series_ticker: str) -> dict:
    """Fetch a single series by its ticker (e.g. 'KXHIGHNY')."""
    async with httpx.AsyncClient(timeout=_kalshi.timeout) as client:
        resp = await client.get(
            f"{_kalshi.series_url}/{series_ticker}"
        )
        resp.raise_for_status()
        return resp.json().get("series", {})

