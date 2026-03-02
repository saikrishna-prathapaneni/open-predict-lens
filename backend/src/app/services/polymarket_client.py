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

async def list_markets(limit: int = 100) -> list:
    """Simulate fetching active markets from Polymarket."""
    # Returning default mock data as per plan
    return [
        {
            "ticker": "POLY-OPENAI-GPT5",
            "title": "Will OpenAI release GPT-5 by September 2026?",
            "status": "active",
            "platform": "Polymarket",
            "category": "Technology",
            "score": 71,
            "ai_confidence": 71,
            "ai_outlook": "Bullish Outlook",
            "ai_description": "Good probability based on development timeline and competitive pressure.",
            "last_price_dollars": "0.71",
            "close_time": "2026-09-30T23:59:59Z",
            "volume": 2100000
        },
        {
            "ticker": "POLY-FED-RATE",
            "title": "Will the Fed cut rates before July 2026?",
            "status": "active",
            "platform": "Polymarket",
            "category": "Economics",
            "score": 45,
            "ai_confidence": 60,
            "ai_outlook": "Bearish Outlook",
            "ai_description": "Persistent inflation indicators suggest stable rates holding.",
            "last_price_dollars": "0.45",
            "close_time": "2026-06-30T23:59:59Z",
            "volume": 5400000
        }
    ]
