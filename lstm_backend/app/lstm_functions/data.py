import os
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from datetime import datetime, timedelta
from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
import os
from dotenv import load_dotenv
from app.db.models.stock_data import StockData
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func

load_dotenv()


tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'BAC', 'SPY', 'QQQ'] # Tickers that we will predict
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORICAL_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "historical_stock_data.csv")

SECRET_KEY = os.getenv('SECRET')
API_KEY = os.getenv('KEY')

async def load_stock_data(db: AsyncSession, days):
    result = await db.execute(
        select(StockData).order_by(StockData.date.desc())
        .limit(days * len(tickers))
    )
    stocks = result.scalars().all() 
    
    data = []
    for stock in stocks:
        data.append({
            "Ticker": stock.ticker,
            "Date": stock.date.isoformat(),
            "Open": stock.open, 
            "High": stock.high,
            "Low": stock.low,
            "Close": stock.close,
            "Volume": stock.volume,
        })
        
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Preprocessing of the data, scaling, encoding and sorting by ticker and date to create the time-series for each ticker
async def preprocessing(db: AsyncSession):
    df = await load_stock_data(db, 3650)

    # Create the target value, that  is the Close value of the next day (row in this case)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day_of_the_week'] = df['Date'].dt.dayofweek
    df.sort_values(['Ticker', 'Date'], inplace=True)
    df['Target'] = df['Close'].shift(-1)
    df.dropna(inplace=True)

    df_scaled = []
    scalers = {}
    columns = ['Open', 'Close', 'High', 'Low', 'Volume', 'Target', 'RSI', 'SMA_20']

    # Scale the data by ticker, since the values can differ a lot depending on the ticker we cant scale all at once
    for ticker in df['Ticker'].unique():
        scaler = MinMaxScaler()
        df_ticker = df[df['Ticker'] == ticker].copy()
        
        df_ticker['RSI'] = ta.rsi(df_ticker['Close'], length=14)
        df_ticker['SMA_20'] = ta.sma(df_ticker['Close'], length=20)
        
        scaled_values = scaler.fit_transform(df_ticker[columns])
        
        df_ticker_scaled = pd.DataFrame(scaled_values, columns=columns, index=df_ticker['Date'])
        df_ticker_scaled['Ticker'] = df_ticker['Ticker'].values
        df_ticker_scaled['Day_of_the_week'] = df_ticker['Day_of_the_week'].values
        
        df_ticker_scaled.dropna(inplace=True)
        
        df_scaled.append(df_ticker_scaled)
        scalers[ticker] = scaler

    df_scaled = pd.concat(df_scaled)

    # Encode the Ticker column
    le = LabelEncoder()
    df_scaled['Ticker'] = le.fit_transform(df_scaled['Ticker'])

    return df_scaled, scalers, le

# Creates a N days sequence of data and returns the X df( Values ), y df( Target ) and tickers_labels
def create_sequences(df, sequence_length=60, columns=['Open', 'Close', 'High', 'Low', 'Volume', 'RSI', 'SMA_20'], target='Target'):
    X_seq, X_dow, y, ticker_ids = [], [], [], []

    for ticker in df['Ticker'].unique():
        df_ticker = df[df['Ticker'] == ticker].sort_values('Date')
        data = df_ticker[columns].values
        targets = df_ticker[target].values
        dow_values = df_ticker['Day_of_the_week'].values

        for i in range(len(data) - sequence_length):
            seq = data[i:i+sequence_length]
            dow = dow_values[i+sequence_length-1] 

            X_seq.append(seq)
            X_dow.append(dow)
            y.append(targets[i+sequence_length])
            ticker_ids.append(ticker)  # already encoded

    return (
        np.array(X_seq),
        np.array(y),
        np.array(ticker_ids).reshape(-1, 1),
        np.array(X_dow).reshape(-1, 1)
    )

# Gets the stock data for a specific ticker and number of days
async def get_stock_data(ticker, days, db: AsyncSession):
    result = await db.execute(
        select(StockData).where(
            StockData.ticker == ticker
        ).order_by(StockData.date.desc()).limit(days)
    )
    stocks = result.scalars().all() 
    
    data = []
    for stock in stocks:
        data.append({
            "Date": stock.date.isoformat(),
            "Close": stock.close,
        })
        
    df = pd.DataFrame(data)
    df = df[['Date', 'Close']]
    df['Date'] = df['Date'].astype(str)
    return df.to_dict(orient='records')

# Gets the current price of a stock using yfinance
def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", interval="1m")
    if not data.empty:
        price = data['Close'].iloc[-1]
        return {"ticker": ticker, "price": round(price, 2)}
    else:
        return {"ticker": ticker, "price": None, "error": "No data found"}

# Gets historical data from yfinance
async def get_historical_data(db: AsyncSession):
        
        # Calculate date range
        current_date = datetime.now().date()
        
        result = await db.execute(
            select(func.max(StockData.date))
        )
        
        last_date = result.scalar()
        last_date = last_date.date() if last_date else None
        
        # If we have data, start from the last date + 1 day
        start_date = min(
            (last_date + timedelta(days=1) if last_date else datetime(2010, 1, 1).date()),
            current_date
        ).isoformat()
        
        # End date should be today or the last market day
        end_date = current_date.isoformat()
        
        print(f"Fetching historical data from {start_date} to {end_date}")
        
        # Only make the request if start_date is before end_date
        if start_date >= end_date:
            print("No new data to fetch - database is up to date")
            return
        
        try:
            historical_data = yf.download(tickers, start=start_date, end=end_date, progress=True, group_by='ticker', threads=True)

            dfs = []
            
            for ticker in tickers:
                if ticker not in historical_data.columns.levels[0]:
                    print(f"No data for ticker {ticker}")
                    continue

                df = historical_data[ticker].reset_index()
                df['Ticker'] = ticker
                dfs.append(df)
                print(f"Added {len(df)} rows for {ticker}")
            
            if not dfs:
                print("No data frames to concatenate")
                return
                
            final_df = pd.concat(dfs, ignore_index=True)
            print(f"Created final DataFrame with {len(final_df)} rows")

            # Prepare rows for insertion
            rows = [{
                "ticker": row['Ticker'],
                "date": pd.to_datetime(row['Date']).date(),
                "open": float(row['Open']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "close": float(row['Close']),
                "volume": int(row['Volume']),
            } for _, row in final_df.iterrows()]

            # Insert in batches
            BATCH_SIZE = 500
            for i in range(0, len(rows), BATCH_SIZE):
                batch = rows[i:i + BATCH_SIZE]
                stmt = insert(StockData).values(batch)
                stmt = stmt.on_conflict_do_nothing(index_elements=['ticker', 'date'])
                await db.execute(stmt)

            await db.commit()
            print(f"Committed {len(rows)} rows in total")

        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            raise
    
# Gets recent stock newsfrom Alpaca API
def get_stock_news(ticker: str):
    
    client = NewsClient(
        api_key=API_KEY,
        secret_key=SECRET_KEY
    )
    
    request_params = NewsRequest(
        end=datetime.today().date(),
        symbols=ticker,
        limit=4
    )
    
    news_data = client.get_news(request_params)
    filtered_news = []
    for article in news_data['news']:
        filtered_news.append({
            "headline": article.headline,
            "summary": article.summary,
            "images": article.images,   
            "url": article.url
            
        })
    
    return {"data": filtered_news, "count": len(filtered_news)}

