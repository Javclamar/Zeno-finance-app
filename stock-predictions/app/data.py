import os
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from datetime import datetime, timedelta
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.requests import NewsRequest
from alpaca.data.timeframe import TimeFrame
import os
from dotenv import load_dotenv

load_dotenv()


tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'BAC', 'SPY', 'QQQ'] # Tickers that we will predict
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEW_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "new_stock_data.csv")
HISTORICAL_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "historical_stock_data.csv")

SECRET_KEY = os.getenv('SECRET')
API_KEY = os.getenv('KEY')

# Preprocessing of the data, scaling, encoding and sorting by ticker and date to create the time-series for each ticker
def preprocessing(csv_path):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # Create the target value, that  is the Close value of the next day (row in this case)
    df['Target'] = df['Close'].shift(-1)
    df['Days_until_next_close'] = (df['Date'].shift(-1)- df['Date']).dt.days
    df['Day_of_the_week'] = df['Date'].dt.dayofweek
    df.dropna(inplace=True)
    print(df.head())

    df_scaled = []
    scalers = {}
    columns = ['Open', 'Close', 'High', 'Low', 'Volume', 'RSI', 'SMA_20', 'Days_until_next_close', 'Target']

    # Scale the data by ticker, since the values can differ a lot depending on the ticker we cant scale all at once
    for ticker in df['Ticker'].unique():
        scaler = MinMaxScaler()
        df_ticker = df[df['Ticker'] == ticker].copy()
        
        scaled_values = scaler.fit_transform(df_ticker[columns])
        
        df_ticker_scaled = pd.DataFrame(scaled_values, columns=columns, index=df_ticker['Date'])
        df_ticker_scaled['Ticker'] = df_ticker['Ticker'].values
        df_ticker_scaled['Day_of_the_week'] = df_ticker['Day_of_the_week'].values
        
        df_scaled.append(df_ticker_scaled)
        scalers[ticker] = scaler

    df_scaled = pd.concat(df_scaled)

    # Encode the Ticker column
    le = LabelEncoder()
    df_scaled['Ticker'] = le.fit_transform(df_scaled['Ticker'])
    return df_scaled, scalers, le

# Creates a N days sequence of data and returns the X df( Values ), y df( Target ) and tickers_labels
def create_sequences(df, N=60, columns=['Open', 'Close', 'High', 'Low', 'Volume', 'RSI', 'SMA_20', 'Days_until_next_close'], target='Target'):
    X_seq, X_dow, y, ticker_ids = [], [], [], []

    for ticker in df['Ticker'].unique():
        df_ticker = df[df['Ticker'] == ticker].sort_values('Date')
        data = df_ticker[columns].values
        targets = df_ticker[target].values
        dow_values = df_ticker['Day_of_the_week'].values

        for i in range(len(data) - N):
            seq = data[i:i+N]
            dow = dow_values[i+N-1] 

            X_seq.append(seq)
            X_dow.append(dow)
            y.append(targets[i+N])
            ticker_ids.append(ticker)  # already encoded

    return (
        np.array(X_seq),
        np.array(y),
        np.array(ticker_ids).reshape(-1, 1),
        np.array(X_dow).reshape(-1, 1)
    )

def get_stock_data(ticker, days):
    df = pd.read_csv(HISTORICAL_DATA_PATH)
    df.dropna(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Ticker'] == ticker]
    df.sort_values(['Date'], inplace=True)
    df = df[-days:]
    df = df[['Date', 'Close']]
    df['Date'] = df['Date'].astype(str)
    return df.to_dict(orient='records')

def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", interval="1m")
    if not data.empty:
        price = data['Close'].iloc[-1]
        return {"ticker": ticker, "price": round(price, 2)}
    else:
        return {"ticker": ticker, "price": None, "error": "No data found"}

def get_historical_data_alpaca():
    client = StockHistoricalDataClient(
        api_key=API_KEY,
        secret_key=SECRET_KEY
    )

    request_params = StockBarsRequest(
        symbol_or_symbols=tickers,
        timeframe=TimeFrame.Day,
        start=datetime(2020, 1, 1),
        end=datetime.today().date()
    )
    
    bars = client.get_stock_bars(request_params)
    dfs = []
    for ticker in tickers:
        ticker_bars = bars[ticker]

        df = pd.DataFrame([{
        "Open": float(bar.open),
        "High": float(bar.high),
        "Low": float(bar.low),
        "Close": float(bar.close),
        "Volume": float(bar.volume),
        "Ticker": ticker,
        "Date": bar.timestamp.date().isoformat()
    } for bar in ticker_bars])
        
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['SMA_20'] = ta.sma(df['Close'], length=20)
        df.dropna(inplace=True)
        df.sort_values('Date', inplace=True)
        dfs.append(df)
        
    final_df = pd.concat(dfs, ignore_index=True)
    final_df.sort_values(['Ticker', 'Date'], inplace=True)
    final_df.to_csv(HISTORICAL_DATA_PATH, index=False)

def get_recent_data_alpaca():

    start_date = datetime.today().date() - timedelta(days=120)

    client = StockHistoricalDataClient(
        api_key=API_KEY,
        secret_key=SECRET_KEY
    )

    request_params = StockBarsRequest(
        symbol_or_symbols=tickers,
        timeframe=TimeFrame.Day,
        include_extended_hours=True,
        start=start_date,
        end=datetime.today().date()
    )
    bars = client.get_stock_bars(request_params)
    dfs = []
    for ticker in tickers:
        ticker_bars = bars[ticker]
    
        df = pd.DataFrame([{
        "Open": float(bar.open),
        "High": float(bar.high),
        "Low": float(bar.low),
        "Close": float(bar.close),
        "Volume": float(bar.volume),
        "Ticker": ticker,
        "Date": bar.timestamp.date().isoformat()
    } for bar in ticker_bars])
        
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['SMA_20'] = ta.sma(df['Close'], length=20)
        df.dropna(inplace=True)
        df.sort_values('Date', inplace=True)
        dfs.append(df)
        
    final_df = pd.concat(dfs, ignore_index=True)
    final_df.sort_values(['Ticker', 'Date'], inplace=True)
    final_df.to_csv(NEW_DATA_PATH, index=False)
    
def get_stock_news():
    
    client = NewsClient(
        api_key=API_KEY,
        secret_key=SECRET_KEY
    )
    
    request_params = NewsRequest(
        end=datetime.today().date(),
        symbols='AAPL,MSFT,GOOG,AMZN,META,TSLA,NFLX,NVDA,JPM,BAC,SPY,QQQ',
        limit=2
    )
    
    news_data = client.get_news(request_params)
    filtered_news = []
    for article in news_data['news']:
        filtered_news.append({
            "headline": article.headline,
            "summary": article.summary,
            "images": article.images[1],   
            "source": article.source
        })
    
    return {"data": filtered_news, "count": len(filtered_news)}



get_historical_data_alpaca()
get_recent_data_alpaca()