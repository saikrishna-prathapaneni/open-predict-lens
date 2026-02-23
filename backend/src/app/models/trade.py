# Trade records are stored in SurrealDB table `trade`.
# Use app.db.get_db() and db.query() / db.select("trade") to read/write.
from pydantic import BaseModel

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

