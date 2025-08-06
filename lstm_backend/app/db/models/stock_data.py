from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint
from app.db.base import Base

class StockData(Base):
    __tablename__ = 'stock_data'

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    rsi = Column(Float)
    sma20 = Column(Float)

    def __repr__(self):
        return f"<StockData(ticker={self.ticker}, date={self.date}, close_price={self.close})>"
    
    __table_args__ = (
        UniqueConstraint("ticker", "date", name="uix_ticker_date"),
    )