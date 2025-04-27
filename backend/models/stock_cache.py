from sqlalchemy import Column, String, DateTime, JSON
from datetime import datetime
from utils.db import Base

class StockCache(Base):
    __tablename__ = 'stock_cache'
    symbol = Column(String, primary_key=True, index=True)
    data = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 