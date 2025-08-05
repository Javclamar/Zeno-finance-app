from fastapi import FastAPI
from app.lstm_functions.predict import predict_new_data
from app.lstm_functions.train import train
from app.lstm_functions.data import get_stock_data, get_current_price, get_stock_news
from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import async_session 

app = FastAPI()
scheduler = BackgroundScheduler()
async def scheduled_tasks():
    async with async_session() as db:
        await train(db)
        await train(db)
        await predict_new_data(db)

scheduler.add_job(scheduled_tasks, 'interval', hours=5)

@app.get("/predictions")
async def getPredictions():
    async with async_session() as db:
        predictions = await predict_new_data(db)
    return {"predictions": predictions}

@app.get("/stock-data")
async def getStockData(ticker: str, days: int,):
    async with async_session() as db:
        stockData = await get_stock_data(ticker, days, db)
    return {"stockData": stockData}

@app.get("/current-price")
def getCurrentPrice(ticker:str):
    currentPrice = get_current_price(ticker)
    return {"currentPrice": currentPrice}

@app.get("/stock-news")
def getStockNews():
    news = get_stock_news()
    return {"news": news}



