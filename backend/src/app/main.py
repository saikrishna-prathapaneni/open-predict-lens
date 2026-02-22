import asyncio
from httpx import AsyncClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import surreal_lifespan
from app.services.kalshi_client import fetch_market
from app.services.kalshi_client import list_markets

app = FastAPI(title=settings.app_name, lifespan=surreal_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_web_context(query: str, client: AsyncClient):
    await asyncio.sleep(1.5) # Simulate I/O
    return f"Latest news context for {query}: Inflation is cooling..."

@app.get("/analyze/{ticker}")
async def analyze_bet(ticker: str):
    async with AsyncClient() as client:
        try:
            kalshi_task = asyncio.create_task(fetch_market(ticker))
            context_task = asyncio.create_task(get_web_context(ticker, client))
            
            market_data, news_context = await asyncio.gather(kalshi_task, context_task)

            analysis = await asyncio.sleep(1.0, result=f"LLM analysis for {ticker} based on market data and news context")
            
            # Use price_dollars if available for better visualization
            market_price = market_data.get("yes_bid_dollars") or market_data.get("last_price_dollars") or "N/A"
            
            return {
                "ticker": ticker,
                "market_probability": market_price,
                "llm_insight": analysis
            }
        except Exception as e:
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/markets")
async def list_markets_endpoint(limit: int = 100):
    markets = await list_markets(limit)
    return {"markets": markets}

@app.get("/health")
async def health_check():
    from app.db import get_db
    try:
        await get_db().query("RETURN 1")
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail=f"SurrealDB unhealthy: {e}")
    return {"status": "ok"}