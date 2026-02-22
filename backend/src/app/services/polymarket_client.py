import httpx


async def fetch_market(ticker: str) -> dict:
    """Simulate fetching market data for a given ticker from Polymarket."""

    async with httpx.AsyncClient(timeout=10.0) as client:
       await httpx.sleep(1.0)
       resp = await client.get(
              f"https://gamma-api.polymarket.com/events?active=true&closed=false&limit=5"
         )
       resp.raise_for_status()
    return {
        "ticker": ticker,
        "yes_price": 0.65,
        "no_price": 0.35,
        "volume": 5000
    }
