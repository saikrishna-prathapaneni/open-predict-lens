import logging
from surrealdb import AsyncSurreal

logger = logging.getLogger(__name__)

async def seed_markets(db: AsyncSurreal):
    """Seed the database with default mock markets if empty."""
    
    try:
        # Check if we already have markets
        result = await db.query("SELECT count() FROM market GROUP ALL;")
        count_result = result[0].get("result", [])
        
        if count_result and len(count_result) > 0 and count_result[0].get("count", 0) > 0:
            logger.info("Database already seeded with markets.")
            return

        logger.info("Seeding initial market data into SurrealDB...")
        markets = [
            {
                "id": "POLY_OPENAI_GPT5",
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
                "id": "POLY_FED_RATE",
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
            },
            {
                "id": "KXCLIMATE2026",
                "ticker": "KXCLIMATE2026",
                "title": "Will global average temperature increase by 0.1°C in 2026?",
                "status": "active",
                "platform": "Kalshi",
                "category": "Climate",
                "score": 85,
                "ai_confidence": 85,
                "ai_outlook": "Bullish Outlook",
                "ai_description": "High probability based on current climate models and historical trends.",
                "last_price_dollars": "0.85",
                "close_time": "2026-12-31T23:59:59Z",
                "volume": 950000
            },
            {
                "id": "KXBTC100K",
                "ticker": "KXBTC100K",
                "title": "Will Bitcoin reach $100,000 by end of Q2 2026?",
                "status": "active",
                "platform": "Kalshi",
                "category": "Cryptocurrency",
                "score": 78,
                "ai_confidence": 78,
                "ai_outlook": "Bullish Outlook",
                "ai_description": "Strong positive sentiment driven by institutional adoption and regulatory clarity in major markets.",
                "last_price_dollars": "0.78",
                "close_time": "2026-06-30T23:59:59Z",
                "volume": 2500000
            }
        ]

        for market in markets:
            try:
                market_id = market.pop("id")
                await db.query("CREATE type::record('market', $id) CONTENT $data", {
                    "id": market_id,
                    "data": market
                })
                logger.info(f"Created market: {market['ticker']}")
            except Exception as e:
                logger.error(f"Failed to create market {market['ticker']}: {e}")

        logger.info("Database seeding complete!")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")

async def init_db(db: AsyncSurreal):
    await seed_markets(db)