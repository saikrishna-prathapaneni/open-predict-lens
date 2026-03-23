# Trade records are stored in SurrealDB table `trade`.
# Use app.db.get_db() and db.query() / db.select("trade") to read/write.
from datetime import datetime

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
 

class Event(BaseModel):
    """Defines the format for events in the system."""
    series_id : str
    date : datetime = Field(..., description="The date of the event in YYYY-MM-DD format")
    
    @property
    def to_event(self):
        """Converts the series_id and date into a standardized event string format."""
        # "KXHIGHNY-25MAR08"
        return f"{self.series_id}-{self.date.strftime('%y%b%d').upper()}"