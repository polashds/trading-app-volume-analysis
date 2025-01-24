from celery import Celery
from api_client import fetch_stock_data
from database import SessionLocal, StockData

#configure celery with Redis
celery = Celery(__name__, broker='redis://localhost:6379/0') #, backend='redis://localhost:6379/0')

@celery.task
def get_stock_data():
    session = SessionLocal()
    stocks = ["AAPL", "GOOGL", "MSFT", "AMZN"]
    for symbol in stocks:
        data = fetch_stock_data(symbol)
        stock_entry = StockData(
            symbol=data["symbol"], 
            price=data["price"], 
            volume=data["volume"]
        )
        session.add(stock_entry)
    session.commit()
    session.close()

