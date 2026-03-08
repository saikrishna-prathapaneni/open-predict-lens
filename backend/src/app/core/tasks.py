import asyncio
import logging
from surrealdb import AsyncSurreal

from app.services.kalshi_client import list_markets as kalshi_list_markets
from app.services.kalshi_client import list_series, get_series
from app.services.polymarket_client import list_markets as polymarket_list_markets

logger = logging.getLogger(__name__)

async def process_kalshi_markets(db: AsyncSurreal):
    logger.info("Fetching Kalshi markets...")
    try:
        raw_markets = await kalshi_list_markets(limit=10)
        for rm in raw_markets:
            ticker = rm.get("ticker")
            
            # Simplified mapping
            market_data = {
                "ticker": ticker,
                "title": rm.get("title", ""),
                "status": rm.get("status", "active"),
                "platform": "Kalshi",
                "last_price_dollars": str(rm.get("last_price", 0) / 100.0), # Assuming cents
                "close_time": rm.get("close_time", ""),
                "volume": rm.get("volume", 0)
            }
            # Add dynamic mock context (in real scenario, llm analysis runs here)
            market_data.update({
                 "score": 65,
                 "ai_confidence": 75,
                 "ai_outlook": "Bullish Outlook",
                 "ai_description": "Steady volume and positive trend line.",
                 "category": "General"
            })
            
            await db.query("UPDATE type::record('market', $id) CONTENT $data", {
                "id": ticker,
                "data": market_data
            })
    except Exception as e:
        logger.error(f"Error processing Kalshi markets: {e}")

async def process_kalshi_series(db: AsyncSurreal, limit: int = 10):
    logger.info("Fetching Kalshi series...")
    try:
        raw_series = await list_series(limit=limit)
        for rs in raw_series:
            ticker = rs.get("ticker")
            series_data = {
                "ticker": ticker,
                "title": rs.get("title", ""),
                "category": rs.get("category", "General"),
                "contract_terms_url": rs.get("contract_terms_url", ""),
                "settlement_sources": rs.get("settlement_sources", [])
            }
            await db.query("UPDATE type::record('series', $id) CONTENT $data", {
                "id": ticker,
                "data": series_data
            })
    except Exception as e:
        logger.error(f"Error processing Kalshi series: {e}")

async def process_polymarket_markets(db: AsyncSurreal):
    logger.info("Fetching Polymarket mock markets...")
    try:
        raw_markets = await polymarket_list_markets(limit=5)
        for market in raw_markets:
            ticker = market.get("ticker")
            await db.query("UPDATE type::record('market', $id) CONTENT $data", {
                "id": ticker,
                "data": market
            })
    except Exception as e:
         logger.error(f"Error processing Polymarket markets: {e}")


async def sync_markets_loop(db: AsyncSurreal, interval_seconds: int = 300):
    """Continuously runs in the background to sync markets."""
    logger.info("Background market sync task started.")
    while True:
        try:
            logger.info("Starting market sync cycle.")
            await process_kalshi_markets(db) # Sync Kalshi markets
            await process_kalshi_series(db) # Sync Kalshi series
            #await process_polymarket_markets(db)
            logger.info(f"Market sync complete. Sleeping for {interval_seconds}s.")
        except Exception as e:
            logger.error(f"Top-level error in sync loop: {e}")
        
        await asyncio.sleep(interval_seconds)
