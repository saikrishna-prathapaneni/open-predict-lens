import asyncio
from httpx import AsyncClient
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import surreal_lifespan
from app.services.kalshi_client import fetch_market, list_markets
from app.services.kalshi_client import list_series, get_series

from app.core.llm import get_llm_client

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

@app.get("/analyze/series/{series_ticker}")
async def analyze_series(series_ticker: str):
    series = await get_series(series_ticker)
    return {"series": series}

# list set of series with optional filters allow for number of series to be displayed
@app.get("/analyze/series")
async def analyze_series_list(
    limit: int = 10,
    status: Optional[str] = None,
    category: Optional[str] = None
):
    series_list = await list_series(limit=limit, status=status, category=category)
    return {"series": series_list}

@app.get("/analyze/{ticker}")
async def analyze_bet(ticker: str):
    async with AsyncClient() as client:
        try:
            kalshi_task = asyncio.create_task(fetch_market(ticker))
            context_task = asyncio.create_task(get_web_context(ticker, client))
            client = get_llm_client()
            market_data, news_context = await asyncio.gather(kalshi_task, context_task)

            #analysis = f"LLM analysis for {ticker} based on market data and news context"
            llm_task = asyncio.create_task(client.generate(f"What is the current probability of the {ticker} > $150 bet?"))
            llm_result = await llm_task
            
            # Use price_dollars if available for better visualization
            market_price = market_data.get("yes_bid_dollars") or market_data.get("last_price_dollars") or "N/A"
            
            return {
                "ticker": ticker,
                "market_probability": market_price,
                "llm_insight": llm_result["text"]
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

@app.get("/llm-test")
async def llm_test(client: Optional[str] = None):
    client = get_llm_client(client)
    response = await client.generate("What is the current probability of the AAPL > $150 bet?")
    return response