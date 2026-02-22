import httpx


async def fetch_market(ticker: str) -> dict:
    """Fetch market data for a given ticker from Kalshi API."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"https://api.elections.kalshi.com/trade-api/v2/markets/{ticker}"
        )
        resp.raise_for_status()
        return resp.json().get("market", {})
    
async def list_markets(limit: int = 100) -> list:
    """List all available markets from Kalshi API."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"https://api.elections.kalshi.com/trade-api/v2/markets?limit={limit}")
        resp.raise_for_status()
        return resp.json().get("markets", [])


