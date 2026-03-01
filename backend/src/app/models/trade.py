# Trade records are stored in SurrealDB table `trade`.
# Use app.db.get_db() and db.query() / db.select("trade") to read/write.
from pydantic import BaseModel, Field

class Trade(BaseModel):
    id: str
    market_id: str
    price: float
    quantity: int
    timestamp: int

class TradeCreate(BaseModel):
    market_id: str
    price: float
    quantity: int
    timestamp: int

class Series(BaseModel):
    id: str
    name: str
    description: str
    category: str
    
class KalshiSeries(Series):
    ticker: str
 