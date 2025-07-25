from fastapi import FastAPI
from app.predict import predict_new_data
from app.train import train
from app.data import get_stock_data
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()
scheduler = BackgroundScheduler()

scheduler.add_job(train, 'cron', hour=2)
scheduler.start()

@app.get("/predictions")
def getPredictions():
    predictions = predict_new_data()
    return {"predictions": predictions}

@app.get("/stock-data")
def getStockData(ticker: str, days: int):
    stockData = get_stock_data(ticker, days)
    return {"stockData": stockData}



