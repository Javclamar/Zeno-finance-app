import os
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from datetime import datetime, timedelta
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'BAC', 'SPY', 'QQQ'] # Tickers that we will predict
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEW_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "new_stock_data.csv")
HISTORICAL_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "historical_stock_data.csv")

SECRET = 'msKtm4Mhj2Gu1sSZoNAJuVvp6ZXcXPMlOebaIgJB'
KEY = 'PKBKHWDRUWLU7Z9GJXZI'

# Downloads the data used to train the model, this will be used in training
def download_historical_data():

    data = yf.download(tickers, start='2020-01-01', group_by='ticker')
    dfs = []
    for ticker in tickers:
        df = data[ticker].copy()
        df['Ticker'] = ticker
        df['Date'] = df.index
        dfs.append(df.reset_index(drop=True))
    df_all = pd.concat(dfs)
    df_all.sort_values(['Ticker', 'Date'], inplace=True)
    df_all.to_csv(HISTORICAL_DATA_PATH, index=False)
    print("✅ Data saved to historical_stock_data.csv")

# Downloads the data used to make predictions. This could be swapped with a query to a MongoDB in the feature so we dont have 2 different datasets
def download_recent_data():
    start = datetime.today().date() - timedelta(days=100)
    start_str =  start.strftime('%Y-%m-%d')

    data = yf.download(tickers, start=start_str, group_by='ticker')
    dfs = []
    for ticker in tickers:
        df = data[ticker].copy()
        df['Ticker'] = ticker
        df['Date'] = df.index
        dfs.append(df.reset_index(drop=True))
    df_all = pd.concat(dfs)
    df_all.sort_values(['Ticker', 'Date'], inplace=True)
    df_all.to_csv(NEW_DATA_PATH, index=False)
    print("✅ Data saved to new_stock_data.csv")

# Preprocessing of the data, scaling, encoding and sorting by ticker and date to create the time-series for each ticker
def preprocessing(csv_path):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # Create the target value, that  is the Close value of the next day (row in this case)
    df['Target'] = df['Close'].shift(-1)
    df['Days_until_next_close'] = (df['Date'].shift(-1)- df['Date']).dt.days
    df['Day_of_the_week'] = df['Date'].dt.dayofweek
    df.dropna(inplace=True)

    df_scaled = []
    scalers = {}
    columns = ['Open', 'Close', 'High', 'Low', 'Volume', 'Days_until_next_close', 'Target']

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
def create_sequences(df, N=60, columns=['Open', 'Close', 'High', 'Low', 'Volume', 'Days_until_next_close'], target='Target'):
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
        api_key=KEY,
        secret_key=SECRET
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

        dfs.append(df)
        
    final_df = pd.concat(dfs, ignore_index=True)
    final_df.sort_values(['Ticker', 'Date'], inplace=True)
    final_df.to_csv(HISTORICAL_DATA_PATH, index=False)

def get_recent_data_alpaca():

    start_date = datetime.today().date() - timedelta(days=100)

    client = StockHistoricalDataClient(
        api_key=KEY,
        secret_key=SECRET
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

        dfs.append(df)
        
    final_df = pd.concat(dfs, ignore_index=True)
    final_df.sort_values(['Ticker', 'Date'], inplace=True)
    final_df.to_csv(NEW_DATA_PATH, index=False)



get_historical_data_alpaca()
get_recent_data_alpaca()